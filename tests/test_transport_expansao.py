"""Testes de autenticação e transporte sem chamadas externas."""
import httpx
import pytest
from chatwoot_client import CWClient, ErroAPIChatwoot, ErroConfiguracaoChatwoot


def cliente(handler, modo="bearer"):
    cw = CWClient(
        "https://chatwoot.exemplo/prefixo",
        "token",
        auth_mode=modo,
    )
    cabecalhos = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.exemplo/",
        headers=cabecalhos,
        transport=httpx.MockTransport(handler),
    )
    return cw


def test_sem_conteudo_204():
    with cliente(lambda req: httpx.Response(204)) as cw:
        assert cw._solicitar_json("DELETE", "api/v1/accounts/1/teams/2") is None


def test_autenticacao_legada():
    requests = []
    def handler(req):
        requests.append(req)
        return httpx.Response(200, json={})
    with cliente(handler, modo="api_access_token") as cw:
        cw.profile.get()
    assert requests[0].headers["api_access_token"] == "token"
    assert "Authorization" not in requests[0].headers


def test_prefixo_reverso_e_multipart():
    requests = []
    def handler(req):
        requests.append(req)
        return httpx.Response(200, json={"id": 99})
    with cliente(handler) as cw:
        resposta = cw.messages.create_with_attachments(
            1, 2, content="Nota", private=True,
            attachments=[
                ("a.txt", b"primeiro", "text/plain"),
                ("b.pdf", b"%PDF", "application/pdf"),
            ],
        )
    assert resposta == {"id": 99}
    req = requests[0]
    assert req.url.path == "/prefixo/api/v1/accounts/1/conversations/2/messages"
    assert req.headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert req.content.count(b'name="attachments[]"') == 2
    assert b"primeiro" in req.content and b"%PDF" in req.content
    assert b'name="private"' in req.content and b"true" in req.content


@pytest.mark.parametrize("mode", ["invalid", "", "Bearer"])
def test_modo_invalido(mode):
    with pytest.raises(ErroConfiguracaoChatwoot):
        CWClient("https://chatwoot.exemplo", "token", auth_mode=mode)


def test_timeout_nao_repete_envio():
    chamadas = []
    def handler(req):
        chamadas.append(req)
        raise httpx.ReadTimeout("timeout", request=req)
    with cliente(handler) as cw, pytest.raises(ErroAPIChatwoot):
        cw.messages.create_with_attachments(
            1, 2, attachments=[("a.txt", b"ok", "text/plain")]
        )
    assert len(chamadas) == 1
