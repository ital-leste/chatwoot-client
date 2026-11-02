"""Testes HTTP simulados de status, associação de etiquetas e API tipada simples."""
from __future__ import annotations

import json
import httpx
import pytest

from chatwoot_client import (
    CWClient, ConversationStatus, LabelDefinition, MediaMessage, Attachment,
    MimeType, TextMessage, ErroAPIChatwoot,
)


def client(requests, *, current_labels=None, status=200, on_request=None):
    if current_labels is None:
        current_labels = []
    def handler(req):
        requests.append(req)
        if on_request is not None:
            return on_request(req)
        if req.method == "GET" and req.url.path.endswith("/labels"):
            return httpx.Response(200, json={"payload": list(current_labels)})
        if req.method == "POST" and "/conversations/" in req.url.path and req.url.path.endswith("/labels"):
            return httpx.Response(200, json={"payload": json.loads(req.content)["labels"]})
        return httpx.Response(status, json={"id": 77})
    cw = CWClient("https://cw.example", "token")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://cw.example/", headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return cw


def test_private_bool_texto_e_interface_pública():
    requests = []
    with client(requests) as cw:
        cw.messages.send_text(1, 2, TextMessage("interno", private=True))
        cw.messages.send_text(1, 2, TextMessage("público"))
    assert [json.loads(r.content)["private"] for r in requests] == [True, False]
    assert all(r.url.path.endswith("/messages") for r in requests)


@pytest.mark.parametrize(
    "message",
    [
        lambda: TextMessage("text", private=1),
        lambda: TextMessage("text", private="false"),
        lambda: MediaMessage((Attachment(b"a", MimeType.PDF, "a.pdf"),), private="false"),
        lambda: MediaMessage((Attachment(b"a", MimeType.OGG, "a.ogg"),), is_voice_message=1),
        lambda: MediaMessage((Attachment(b"a", MimeType.PDF, "a.pdf"),), is_voice_message=True),
        lambda: MediaMessage(
            (Attachment(b"a", MimeType.OGG, "a.ogg"), Attachment(b"b", MimeType.OGG, "b.ogg")),
            is_voice_message=True,
        ),
    ],
)
def test_flags_invalidos_rejeitados_antes_da_requisicao(message):
    with pytest.raises((ValueError, TypeError)):
        message()


def test_voice_message_multipart_com_marcador():
    requests = []
    with client(requests) as cw:
        cw.messages.send_media(
            1, 2,
            MediaMessage(
                (Attachment(b"ogg-bin", MimeType.OGG, "audio.ogg"),),
                is_voice_message=True, private=True,
            ),
        )
    body = requests[0].content
    assert body.count(b'name="attachments[]"') == 1
    assert b'name="is_voice_message"' in body
    assert b"true" in body
    assert b"ogg-bin" in body
    assert requests[0].headers["content-type"].startswith("multipart/form-data")


def test_nao_envia_voice_flag_para_audio_normal():
    requests = []
    with client(requests) as cw:
        cw.messages.send_media(
            1, 2,
            MediaMessage((Attachment(b"ogg-bin", MimeType.OGG, "audio.ogg"),)),
        )
    assert b'name="is_voice_message"' not in requests[0].content


def test_private_bool_uso_canonico():
    requests = []
    with client(requests) as cw:
        cw.messages.send_text(
            1, 2, TextMessage("nota", private=True)
        )
    assert json.loads(requests[0].content)["private"] is True


def test_abaixo_do_pano_um_mesmo_endpoint_com_mime_pdf_e_imagem():
    requests = []
    with client(requests) as cw:
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment(b"PDF", MimeType.PDF, "x.pdf"),))
        )
        cw.messages.send_media(
            1, 2, MediaMessage((Attachment(b"PNG", MimeType.PNG, "x.png"),))
        )
    assert len(requests) == 2
    assert requests[0].url.path == requests[1].url.path
    assert b"application/pdf" in requests[0].content
    assert b"image/png" in requests[1].content


@pytest.mark.parametrize("state", [
    ConversationStatus.OPEN,
    ConversationStatus.PENDING,
    ConversationStatus.RESOLVED,
    ConversationStatus.SNOOZED,
])
def test_status_tipado_mantem_rota_oficial(state):
    requests = []
    with client(requests) as cw:
        cw.conversations.set_status(1, 2, state)
    assert requests[0].method == "POST"
    assert requests[0].url.path.endswith("/conversations/2/toggle_status")
    assert json.loads(requests[0].content)["status"] == state.value


def test_status_string_antiga_rejeitada_sem_http():
    requests = []
    with client(requests) as cw, pytest.raises(TypeError):
        cw.conversations.set_status(1, 2, "pending")
    assert not requests


def test_add_lê_as_antigas_e_gera_lista_completa_sem_duplicar():
    requests = []
    with client(requests, current_labels=["prioridade", "humano"]) as cw:
        result = cw.conversation_labels.add(
            1, 2, ["hermes", "prioridade", "novo", "hermes"]
        )
    assert result["payload"] == ["prioridade", "humano", "hermes", "novo"]
    assert [r.method for r in requests] == ["GET", "POST"]
    assert json.loads(requests[1].content) == {
        "labels": ["prioridade", "humano", "hermes", "novo"]
    }


def test_add_duplicada_não_executa_post():
    requests = []
    with client(requests, current_labels=["prioridade", "hermes"]) as cw:
        response = cw.conversation_labels.add(1, 2, "hermes")
    assert response["payload"] == ["prioridade", "hermes"]
    assert [r.method for r in requests] == ["GET"]


def test_add_sem_etiquetas_anteriores():
    requests = []
    with client(requests, current_labels=[]) as cw:
        result = cw.conversation_labels.add(1, 2, "primeira")
    assert result["payload"] == ["primeira"]
    assert [r.method for r in requests] == ["GET", "POST"]


def test_remove_preserva_restantes():
    requests = []
    with client(requests, current_labels=["a", "b", "c"]) as cw:
        result = cw.conversation_labels.remove(1, 2, ("b", "x"))
    assert result["payload"] == ["a", "c"]
    assert [r.method for r in requests] == ["GET", "POST"]


def test_replace_continua_sendo_substituicao_integral():
    requests = []
    with client(requests, current_labels=["a", "b"]) as cw:
        response = cw.conversation_labels.replace(1, 2, ["nova"])
    assert response["payload"] == ["nova"]
    assert [r.method for r in requests] == ["POST"]


@pytest.mark.parametrize("labels", [[], (), "", ["ok", ""], ["ok", 1], 123])
def test_add_rejeita_entrada_invalida_sem_http(labels):
    requests = []
    with client(requests) as cw, pytest.raises((ValueError, TypeError)):
        cw.conversation_labels.add(1, 2, labels)
    assert requests == []


@pytest.mark.parametrize("response", [
    {"payload": {}}, {"payload": "a"}, {"payload": [1]}, {"payload": ["x", ""]}, {}
])
def test_add_falha_fechada_se_resposta_de_lista_invalida(response):
    requests = []
    def handler(req):
        return httpx.Response(200, json=response)
    with client(requests, on_request=handler) as cw, pytest.raises(ValueError):
        cw.conversation_labels.add(1, 2, "nova")
    assert len(requests) == 1
    assert requests[0].method == "GET"


def test_add_falha_no_get_nao_post():
    requests = []
    def handler(req):
        return httpx.Response(503, json={"error": "outage"})
    with client(requests, on_request=handler) as cw, pytest.raises(ErroAPIChatwoot):
        cw.conversation_labels.add(1, 2, "nova")
    assert len(requests) == 1


def test_catalogo_de_etiquetas_tipado():
    requests = []
    definition = LabelDefinition("hermes", "#aabbcc", description="Atendimento", show_on_sidebar=True)
    with client(requests) as cw:
        cw.labels.create(1, definition)
    assert requests[0].url.path.endswith("/accounts/1/labels")
    assert json.loads(requests[0].content) == {
        "title": "hermes", "color": "#aabbcc",
        "description": "Atendimento", "show_on_sidebar": True,
    }


@pytest.mark.parametrize("factory", [
    lambda: LabelDefinition("", "#abcdef"),
    lambda: LabelDefinition("a", "red"),
    lambda: LabelDefinition("a", "#GGGGGG"),
    lambda: LabelDefinition("a", "#112233", show_on_sidebar=1),
])
def test_etiqueta_invalida(factory):
    with pytest.raises((ValueError, TypeError)):
        factory()


def test_catalogo_nao_e_associacao_de_conversa():
    requests = []
    with client(requests) as cw:
        cw.labels.create(1, LabelDefinition("novo", "#112233"))
    assert len(requests) == 1
    assert "/conversations/" not in requests[0].url.path
