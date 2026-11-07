"""Contratos de agentes, webhooks e campanhas; sem rede ou escrita real."""
from __future__ import annotations

import json
import httpx
import pytest
from chatwoot_client import CWClient


def mock_cw(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"ok": True})
    cw = CWClient("https://chatwoot.example", "chave-ficticia")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(base_url="https://chatwoot.example/",
                           headers=headers, transport=httpx.MockTransport(responder))
    return cw


@pytest.mark.parametrize("chamada,metodo,caminho,payload", [
    (lambda c: c.agents.create(1, name="Joao", email="joao@example.com", role="agent",
                             availability="busy", auto_offline=False),
     "POST", "/api/v1/accounts/1/agents",
     {"name": "Joao", "email": "joao@example.com", "role": "agent",
      "availability": "busy", "auto_offline": False}),
    (lambda c: c.agents.update(1, 7, role="administrator"),
     "PATCH", "/api/v1/accounts/1/agents/7", {"role": "administrator"}),
    (lambda c: c.webhooks.create(1, url="https://hooks.example.com/a",
                                name="App", subscriptions=["message_created"]),
     "POST", "/api/v1/accounts/1/webhooks",
     {"url": "https://hooks.example.com/a", "name": "App",
      "subscriptions": ["message_created"]}),
    (lambda c: c.webhooks.update(1, 8, subscriptions=[]),
     "PATCH", "/api/v1/accounts/1/webhooks/8", {"subscriptions": []}),
    (lambda c: c.campaigns.create(1, {"title": "Teste", "enabled": False}),
     "POST", "/api/v1/accounts/1/campaigns",
     {"campaign": {"title": "Teste", "enabled": False}}),
    (lambda c: c.campaigns.update(1, 5, {"enabled": False}),
     "PATCH", "/api/v1/accounts/1/campaigns/5",
     {"campaign": {"enabled": False}}),
])
def test_http_payload_exato(chamada, metodo, caminho, payload):
    chamadas = []
    with mock_cw(chamadas) as cw:
        assert chamada(cw) == {"ok": True}
    assert len(chamadas) == 1
    assert chamadas[0].method == metodo
    assert chamadas[0].url.path == caminho
    assert json.loads(chamadas[0].content) == payload


@pytest.mark.parametrize("chamada", [
    lambda c: c.agents.create(1, name="", email="joao@example.com", role="agent"),
    lambda c: c.agents.create(1, name="A", email="sem-email", role="agent"),
    lambda c: c.agents.create(1, name="A", email="a@example.com", role="admin"),
    lambda c: c.agents.update(1, 3, role="root"),
    lambda c: c.agents.update(1, 3, role="agent", availability="away"),
    lambda c: c.agents.update(1, 3, role="agent", auto_offline=1),
    lambda c: c.webhooks.create(1, url="ftp://example.com/hook"),
    lambda c: c.webhooks.create(1, url="https://usuario:senha@host.example/hook"),
    lambda c: c.webhooks.update(1, 5),
    lambda c: c.webhooks.update(1, 5, subscriptions="message_created"),
    lambda c: c.campaigns.create(1, {}),
    lambda c: c.campaigns.update(1, 2, {}),
    lambda c: c.campaigns.update(1, 2, {"title": object()}),
])
def test_bloqueia_antes_de_http(chamada):
    chamadas = []
    with mock_cw(chamadas) as cw, pytest.raises((ValueError, TypeError)):
        chamada(cw)
    assert chamadas == []
