"""URL-base, URLs de anexos e timeout granular sem chamadas externas."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import (
    Attachment, CWClient, ErroAnexoChatwoot, ErroConfiguracaoChatwoot,
    MediaMessage, MimeType,
)


@pytest.mark.parametrize("url", [
    "https://:443",
    "https://chatwoot.example:invalida",
    "https://chatwoot.example:65536",
    "https://chatwoot.example:0",
    "https://chatwoot.example:",
    "http://[::1",
    "https://chatwoot.example?x=1",
    "https://chatwoot.example?",
    "https://chatwoot.example#",
    "https://usuario@chatwoot.example",
    "https://ho st.example",
    "https://chatwoot.example\\outro",
])
def test_url_base_invalida_erro_de_configuracao(url):
    with pytest.raises(ErroConfiguracaoChatwoot):
        CWClient(url, "token-teste")


@pytest.mark.parametrize("url,host,caminho", [
    ("http://localhost:5000/proxy", "localhost", "proxy"),
    ("https://chatwoot.example:8443/api-base", "chatwoot.example", "api-base"),
    ("http://127.0.0.1:3000", "127.0.0.1", ""),
    ("http://[::1]:8080", "::1", ""),
])
def test_url_base_legitima_preservada(url, host, caminho):
    with CWClient(url, "token-teste") as cliente:
        assert cliente._http.base_url.host == host
        assert cliente._base_path == caminho


def test_timeout_numerico_continua_compativel():
    with CWClient("https://chatwoot.example", "token", timeout=12.5) as cliente:
        assert cliente._http.timeout.connect == 12.5
        assert cliente._http.timeout.read == 12.5


def test_timeout_granular_nativo_preservado():
    configuracao = httpx.Timeout(
        30.0, connect=5.0, read=60.0, write=15.0, pool=2.0,
    )
    with CWClient("https://chatwoot.example", "token", timeout=configuracao) as cliente:
        assert cliente._http.timeout.connect == 5.0
        assert cliente._http.timeout.read == 60.0
        assert cliente._http.timeout.write == 15.0
        assert cliente._http.timeout.pool == 2.0


@pytest.mark.parametrize("timeout", [True, None, "30", 0, -1, float("inf"), float("nan")])
def test_timeout_escalar_invalido_rejeitado(timeout):
    with pytest.raises(ErroConfiguracaoChatwoot):
        CWClient("https://chatwoot.example", "token", timeout=timeout)


def test_attachment_url_ipv6_malformado_nao_vaza_erro_parser():
    with pytest.raises(ValueError, match="URL de anexo"):
        Attachment.from_url("https://[::1/arquivo.pdf")


@pytest.mark.parametrize("url", [
    "https://files.example.org:abc/arquivo.pdf",
    "https://files.example.org:65536/arquivo.pdf",
    "https://files.example.org:/arquivo.pdf",
])
def test_url_remota_porta_invalida_impede_envio(url):
    # A validação da porta final ocorre na resolução, antes de qualquer download.
    chamadas = []
    cliente = CWClient("https://chatwoot.example", "token")
    headers = dict(cliente._http.headers)
    cliente._http.close()

    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"id": 9})

    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(responder),
    )
    with cliente:
        with pytest.raises(ErroAnexoChatwoot):
            cliente.messages.send_media(
                1, 2, MediaMessage([Attachment.from_url(
                    url, filename="arquivo.pdf", mime_type=MimeType.PDF,
                )])
            )
    assert chamadas == []
