"""Contratos de payload multipart e application/x-www-form-urlencoded."""
import httpx
from chatwoot_client import CWClient


def _client(reqs):
    def handle(request):
        reqs.append(request)
        return httpx.Response(200, json={"ok": True})
    cw = CWClient("https://chatwoot.exemplo", "token")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.exemplo/", headers=headers,
        transport=httpx.MockTransport(handle),
    )
    return cw


def test_conta_update_form_urlencoded():
    reqs = []
    with _client(reqs) as cw:
        assert cw.account.update_form(1, {"name": "Nova Conta"}) == {"ok": True}
    req = reqs[0]
    assert req.method == "PATCH"
    assert req.url.path == "/api/v1/accounts/1"
    assert req.headers["content-type"].startswith("application/x-www-form-urlencoded")
    assert b"name=Nova+Conta" in req.content


def test_profile_update_multipart_avatar():
    reqs = []
    with _client(reqs) as cw:
        assert cw.profile.update_multipart(
            avatar=("avatar.png", b"conteudo-imagem", "image/png"),
            fields={"display_name": "Teste"},
        ) == {"ok": True}
    req = reqs[0]
    assert req.method == "PUT"
    assert req.url.path == "/api/v1/profile"
    assert req.headers["content-type"].startswith("multipart/form-data; boundary=")
    assert b'name="profile[avatar]"' in req.content
    assert b'name="profile[display_name]"' in req.content
    assert b"conteudo-imagem" in req.content


def test_delete_sucesso_sem_corpo():
    reqs = []
    with _client(reqs) as cw:
        assert cw.teams.delete(1, 2) == {"ok": True}
