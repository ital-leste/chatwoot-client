"""Contratos tipados e transporte para mensagens e anexos Chatwoot, sem envios reais."""
from __future__ import annotations

import io
import json
import socket
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from chatwoot_client import (
    Attachment, CWClient, ErroAPIChatwoot, ErroAnexoChatwoot,
    MediaMessage, MessageType, MimeType, TextMessage,
)
from chatwoot_client import attachment_resolver as resolver


def mock_client(seen, *, response=None):
    def handler(request):
        seen.append(request)
        return response(request) if callable(response) else httpx.Response(200, json={"id": 44})
    cw = CWClient("https://cw.example/proxy", "test-key")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://cw.example/", headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return cw


def test_tipos_exportados_pela_raiz():
    assert MimeType.PDF.value == "application/pdf"
    assert MimeType.OGG.value == "audio/ogg"
    assert MessageType.OUTGOING.value == "outgoing"
    assert MessageType.INCOMING.value == "incoming"


@pytest.mark.parametrize(
    "factory",
    [
        lambda: TextMessage(""),
        lambda: TextMessage("   "),
        lambda: TextMessage(12),
        lambda: TextMessage("oi", private="false"),
        lambda: TextMessage("oi", message_type="outgoing"),
        lambda: MediaMessage(attachments=[]),
        lambda: MediaMessage(attachments=["arquivo.pdf"]),
        lambda: MediaMessage(attachments=(Attachment(b"x", MimeType.PDF, "a.pdf"),), caption=123),
        lambda: Attachment(source=b"arquivo-sem-nome", mime_type=MimeType.PDF),
        lambda: Attachment(source=b"", filename="a.pdf"),
        lambda: Attachment(source="http://cdn.example.com/a.pdf"),
        lambda: Attachment(source="https://usuario:senha@cdn.example.com/a.pdf"),
        lambda: Attachment(source=b"abc", filename="../outro.pdf", mime_type=MimeType.PDF),
        lambda: Attachment(source=b"abc", filename="laudo.pdf", mime_type="application"),
        lambda: Attachment(source=object(), filename="x.pdf", mime_type=MimeType.PDF),
    ],
)
def test_models_invalidos_rejeitados(factory):
    with pytest.raises((TypeError, ValueError)):
        factory()


def test_texto_publico_serializado_em_json_sem_repetir():
    seen = []
    with mock_client(seen) as cw:
        ret = cw.messages.send_text(
            1, 2, TextMessage("Olá!", private=False)
        )
    assert ret == {"id": 44}
    assert len(seen) == 1
    assert seen[0].url.path == "/proxy/api/v1/accounts/1/conversations/2/messages"
    assert seen[0].method == "POST"
    assert json.loads(seen[0].content) == {
        "content": "Olá!", "message_type": "outgoing", "private": False,
    }


def test_nota_privada_nao_altera_endpoint():
    seen = []
    with mock_client(seen) as cw:
        cw.messages.send_text(1, 2, TextMessage("Nota", private=True))
    assert json.loads(seen[0].content)["private"] is True


def test_texto_tipo_entrada_explicito():
    seen = []
    with mock_client(seen) as cw:
        cw.messages.send_text(1, 2, TextMessage("Histórico", message_type=MessageType.INCOMING))
    assert json.loads(seen[0].content)["message_type"] == "incoming"


def test_pdf_local_com_legenda_multipart_e_nome_inferido(tmp_path: Path):
    arquivo = tmp_path / "laudo.pdf"
    arquivo.write_bytes(b"%PDF-1.4 conteudo")
    seen = []
    with mock_client(seen) as cw:
        retorno = cw.messages.send_media(
            1, 2, MediaMessage(
                attachments=(Attachment.from_path(arquivo),),
                caption="Segue o laudo", private=True,
            )
        )
    assert retorno == {"id": 44}
    assert len(seen) == 1
    req = seen[0]
    assert req.headers["content-type"].startswith("multipart/form-data")
    assert req.content.count(b'name="attachments[]"') == 1
    assert b"laudo.pdf" in req.content
    assert b"application/pdf" in req.content
    assert b"Segue o laudo" in req.content
    assert b'name="private"' in req.content
    assert b"true" in req.content
    assert b"%PDF-1.4 conteudo" in req.content


def test_multiplos_anexos_e_legenda_opcional():
    seen = []
    msg = MediaMessage(
        attachments=[
            Attachment(b"a", MimeType.PDF, "a.pdf"),
            Attachment(b"b", MimeType.PDF, "b.pdf"),
        ],
        caption=None,
    )
    with mock_client(seen) as cw:
        cw.messages.send_media(1, 2, msg)
    req = seen[0]
    assert req.content.count(b'name="attachments[]"') == 2
    assert b'name="content"' not in req.content
    assert b'a.pdf' in req.content and b'b.pdf' in req.content


@pytest.mark.parametrize("mime", [MimeType.PNG, MimeType.OGG, MimeType.MP4, MimeType.PDF])
def test_send_media_unifica_todas_as_familias_mime(mime):
    seen = []
    attachment = Attachment(b"conteudo", mime, "a.bin")
    with mock_client(seen) as cw:
        cw.messages.send_media(1, 2, MediaMessage((attachment,)))
    assert len(seen) == 1
    assert seen[0].method == "POST"
    assert b"conteudo" in seen[0].content


def test_fluxo_binario_externo_permanece_aberto():
    seen = []
    user_stream = io.BytesIO(b"arq")
    with mock_client(seen) as cw:
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment(user_stream, MimeType.PDF, "teste.pdf"),))
        )
    assert not user_stream.closed
    assert b"arq" in seen[0].content


def test_arquivo_local_inexistente_nao_requisita(tmp_path: Path):
    seen = []
    with mock_client(seen) as cw, pytest.raises(ErroAnexoChatwoot):
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_path(tmp_path / "nao.pdf"),))
        )
    assert not seen


def test_limite_de_tamanho_impede_envio(tmp_path: Path):
    path = tmp_path / "arquivo.pdf"
    path.write_bytes(b"x" * 15)
    seen = []
    with mock_client(seen) as cw, pytest.raises(ErroAnexoChatwoot):
        cw.messages.send_media(1, 2, MediaMessage((Attachment.from_path(path),)), max_bytes=10)
    assert not seen


def test_ip_local_bloqueado_sem_requisicao():
    seen = []
    with mock_client(seen) as cw, pytest.raises(ErroAnexoChatwoot):
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_url("https://127.0.0.1/a.pdf"),))
        )
    assert not seen


def test_host_fora_da_allowlist_impede_download():
    seen = []
    with mock_client(seen) as cw, pytest.raises(ErroAnexoChatwoot):
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_url("https://files.example.org/laudo.pdf"),)),
            allowed_hosts={"outro.example.org"},
        )
    assert not seen


def test_url_remota_baixa_sem_repassar_token_e_envia_pdf(monkeypatch):
    seen_upload, seen_download = [], []
    original_httpx_client = httpx.Client

    def download_factory(*args, **kwargs):
        assert kwargs["trust_env"] is False
        assert kwargs["follow_redirects"] is False
        return original_httpx_client(
            transport=httpx.MockTransport(
                lambda req: (seen_download.append(req) or httpx.Response(
                    200, content=b"%PDF-1.4 remoto",
                    headers={"content-length": "15"},
                ))
            ),
        )

    monkeypatch.setattr(
        resolver, "httpx",
        SimpleNamespace(Client=download_factory, HTTPError=httpx.HTTPError),
    )
    monkeypatch.setattr(
        resolver.socket, "getaddrinfo",
        lambda *args, **kwargs: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ],
    )
    with mock_client(seen_upload) as cw:
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_url("https://files.example.org/laudo.pdf"),)),
            allowed_hosts={"files.example.org"},
        )
    assert len(seen_download) == 1
    assert "Authorization" not in seen_download[0].headers
    assert len(seen_upload) == 1
    assert b"%PDF-1.4 remoto" in seen_upload[0].content


def test_erro_envio_tipado_sem_retry():
    seen = []
    def handler(req):
        raise httpx.ReadTimeout("timeout", request=req)
    with mock_client(seen, response=handler) as cw, pytest.raises(ErroAPIChatwoot):
        cw.messages.send_text(1, 2, TextMessage("ok"))
    assert len(seen) == 1


def test_metodos_http_privados_usam_unica_rotina():
    seen = []
    with mock_client(seen) as cw:
        for method in ("_get", "_post", "_put", "_patch", "_delete"):
            getattr(cw, method)("api/v1/accounts/1")
    assert [r.method for r in seen] == ["GET", "POST", "PUT", "PATCH", "DELETE"]


def test_validacao_id_anterior_ao_envio():
    seen = []
    with mock_client(seen) as cw, pytest.raises(ValueError):
        cw.messages.send_text(0, 2, TextMessage("ok"))
    assert not seen


@pytest.mark.parametrize("status", [301, 302, 307, 308])
def test_redirect_midia_rejeitado_antes_de_post(monkeypatch, status):
    """URLs Active Storage /blobs/redirect nao podem gerar escrita ambigua."""
    from chatwoot_client import ErroRedirecionamentoAnexoChatwoot
    enviados, downloads = [], []
    httpx_client = httpx.Client

    def fabricar_download(*args, **kwargs):
        assert kwargs["follow_redirects"] is False
        assert kwargs["trust_env"] is False
        return httpx_client(transport=httpx.MockTransport(
            lambda request: (downloads.append(request) or httpx.Response(
                status, headers={"location": "https://outro.example.org/arquivo.pdf"}
            ))
        ))

    monkeypatch.setattr(resolver, "httpx", SimpleNamespace(
        Client=fabricar_download, HTTPError=httpx.HTTPError,
    ))
    monkeypatch.setattr(resolver.socket, "getaddrinfo", lambda *a, **k: [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
    ])
    with mock_client(enviados) as cw, pytest.raises(
        ErroRedirecionamentoAnexoChatwoot
    ):
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_url(
                "https://files.example.org/rails/active_storage/blobs/redirect/teste"
            , mime_type="application/pdf", filename="teste.pdf"),)),
            allowed_hosts={"files.example.org"},
        )
    assert len(downloads) == 1
    assert "Authorization" not in downloads[0].headers
    assert not enviados  # nenhum POST


def test_erro_download_midia_antes_de_post(monkeypatch):
    enviados = []
    httpx_client = httpx.Client

    def fabricar_download(*args, **kwargs):
        def timeout(req):
            raise httpx.ReadTimeout("sintetico", request=req)
        return httpx_client(transport=httpx.MockTransport(timeout))

    monkeypatch.setattr(resolver, "httpx", SimpleNamespace(
        Client=fabricar_download, HTTPError=httpx.HTTPError,
    ))
    monkeypatch.setattr(resolver.socket, "getaddrinfo", lambda *a, **k: [
        (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
    ])
    with mock_client(enviados) as cw, pytest.raises(ErroAnexoChatwoot):
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment.from_url(
                "https://files.example.org/a.pdf", mime_type="application/pdf",
                filename="a.pdf",
            ),)), allowed_hosts={"files.example.org"},
        )
    assert not enviados
