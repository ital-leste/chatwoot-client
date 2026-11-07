"""Contratos restantes: equipes, etiquetas, perfil e layout do e-mail."""
from __future__ import annotations
import json
import httpx
import pytest
from chatwoot_client import CWClient, ProfileInput


def cliente_mock(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"ok": True})
    c = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(c._http.headers)
    c._http.close()
    c._http = httpx.Client(base_url="https://chatwoot.example/", headers=headers,
                          transport=httpx.MockTransport(responder))
    return c


@pytest.mark.parametrize("chamada,verbo,caminho,dados", [
    (lambda c: c.teams.create(1, name="Equipe", allow_auto_assign=False),
     "POST", "/api/v1/accounts/1/teams", {"name":"Equipe","allow_auto_assign":False}),
    (lambda c: c.teams.update(1, 2, name="Renomeada"),
     "PATCH", "/api/v1/accounts/1/teams/2", {"name":"Renomeada"}),
    (lambda c: c.labels.update(1, 3, color="#ff0000", show_on_sidebar=False),
     "PATCH", "/api/v1/accounts/1/labels/3", {"color":"#ff0000","show_on_sidebar":False}),
    (lambda c: c.inboxes.update_branded_email_layout(1, branded_email_layout=None),
     "PATCH", "/api/v1/accounts/1/branded_email_layout", {"branded_email_layout":None}),
    (lambda c: c.profile.update(ProfileInput(name="Maria", ui_settings={})),
     "PUT", "/api/v1/profile", {"profile":{"name":"Maria","ui_settings":{}}}),
])
def test_payload_estrito(chamada, verbo, caminho, dados):
    chamadas=[]
    with cliente_mock(chamadas) as cw:
        assert chamada(cw)=={"ok":True}
    assert len(chamadas)==1
    assert chamadas[0].method==verbo
    assert chamadas[0].url.path==caminho
    assert json.loads(chamadas[0].content)==dados


@pytest.mark.parametrize("chamada", [
    lambda c: c.teams.create(1, name=""),
    lambda c: c.teams.update(1, 2),
    lambda c: c.teams.update(1, 2, allow_auto_assign=1),
    lambda c: c.labels.update(1, 3, color="red"),
    lambda c: c.labels.update(1, 3),
    lambda c: c.inboxes.update_branded_email_layout(1, branded_email_layout=123),
    lambda c: c.messages.update_status(1, 2, 3, status="draft"),
    lambda c: c.profile.update({"name":"sem contrato"}),
    lambda c: c.profile.update(ProfileInput()),
])
def test_rejeicao_pre_http(chamada):
    chamadas=[]
    with cliente_mock(chamadas) as cw, pytest.raises((ValueError, TypeError)):
        chamada(cw)
    assert chamadas==[]
