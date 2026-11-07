"""Complemento de campos oficiais da API sem perda de semântica parcial."""
from __future__ import annotations
import json
import httpx
import pytest
from chatwoot_client import CWClient, Contact, ConversationPriority


def cliente_mock(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"ok": True})
    c = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(c._http.headers)
    c._http.close()
    c._http = httpx.Client(base_url="https://chatwoot.example/",
                          headers=headers, transport=httpx.MockTransport(responder))
    return c


@pytest.mark.parametrize("chamada,caminho,corpo", [
    (lambda c: c.conversations.update(1, 2, sla_policy_id=9),
     "/api/v1/accounts/1/conversations/2", {"sla_policy_id":9}),
    (lambda c: c.conversations.update(1, 2, priority=ConversationPriority.HIGH, sla_policy_id=8),
     "/api/v1/accounts/1/conversations/2", {"priority":"high","sla_policy_id":8}),
    (lambda c: c.conversations.update(1, 2, priority=None),
     "/api/v1/accounts/1/conversations/2", {"priority":None}),
    (lambda c: c.contacts.update(1, 3, Contact(avatar="data:image/png;base64,YQ==")),
     "/api/v1/accounts/1/contacts/3", {"avatar":"data:image/png;base64,YQ=="}),
])
def test_atualizacoes_cobrem_campos_oficiais(chamada, caminho, corpo):
    chamadas=[]
    with cliente_mock(chamadas) as c:
        c_result=chamada(c)
        assert c_result=={"ok":True}
    assert len(chamadas)==1
    assert chamadas[0].url.path==caminho
    assert json.loads(chamadas[0].content)==corpo


@pytest.mark.parametrize("chamada", [
    lambda c: c.conversations.update(1, 2),
    lambda c: c.conversations.update(1, 2, sla_policy_id=0),
    lambda c: c.conversations.update(1, 2, sla_policy_id=True),
    lambda c: c.conversations.update(1, 2, priority="high"),
    lambda c: c.contacts.update(1, 3, Contact(avatar=999)),
])
def test_entrada_invalida_nao_dispara_http(chamada):
    chamadas=[]
    with cliente_mock(chamadas) as c, pytest.raises((ValueError, TypeError)):
        chamada(c)
    assert chamadas==[]
