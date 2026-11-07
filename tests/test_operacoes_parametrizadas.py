"""Regressão de entradas parametrizadas após auditoria da Application API 4.19.0."""
from __future__ import annotations

import json
import httpx
import pytest
from chatwoot_client import CWClient


def cliente_mock(chamadas):
    def handler(request):
        chamadas.append(request)
        return httpx.Response(200, json={"ok": True})
    cliente = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(cliente._http.headers)
    cliente._http.close()
    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return cliente


@pytest.mark.parametrize("chamada,verbo,caminho,payload", [
    (lambda c: c.contacts.add_inbox(1, 3, inbox_id=9, source_id="whatsapp"),
     "POST", "/api/v1/accounts/1/contacts/3/contact_inboxes", {"inbox_id": 9, "source_id": "whatsapp"}),
    (lambda c: c.contacts.add_inbox(1, 3, inbox_id=9),
     "POST", "/api/v1/accounts/1/contacts/3/contact_inboxes", {"inbox_id": 9}),
    (lambda c: c.contacts.merge(1, base_contact_id=3, mergee_contact_id=4),
     "POST", "/api/v1/accounts/1/actions/contact_merge", {"base_contact_id": 3, "mergee_contact_id": 4}),
    (lambda c: c.contact_labels.replace(1, 3, ("gnv", "laudo")),
     "POST", "/api/v1/accounts/1/contacts/3/labels", {"labels": ["gnv", "laudo"]}),
    (lambda c: c.contact_labels.replace(1, 3, []),
     "POST", "/api/v1/accounts/1/contacts/3/labels", {"labels": []}),
    (lambda c: c.inboxes.set_agent_bot(1, 9, agent_bot=7),
     "POST", "/api/v1/accounts/1/inboxes/9/set_agent_bot", {"agent_bot": 7}),
    (lambda c: c.inboxes.set_agent_bot(1, 9, agent_bot=None),
     "POST", "/api/v1/accounts/1/inboxes/9/set_agent_bot", {"agent_bot": None}),
    (lambda c: c.inboxes.add_member(1, inbox_id=9, user_ids=(3, 4)),
     "POST", "/api/v1/accounts/1/inbox_members", {"inbox_id": 9, "user_ids": [3, 4]}),
    (lambda c: c.inboxes.update_members(1, inbox_id=9, user_ids=[3]),
     "PATCH", "/api/v1/accounts/1/inbox_members", {"inbox_id": 9, "user_ids": [3]}),
    (lambda c: c.inboxes.remove_members(1, inbox_id=9, user_ids=[3]),
     "DELETE", "/api/v1/accounts/1/inbox_members", {"inbox_id": 9, "user_ids": [3]}),
    (lambda c: c.teams.add_members(1, 6, [3, 4]),
     "POST", "/api/v1/accounts/1/teams/6/team_members", {"user_ids": [3, 4]}),
    (lambda c: c.teams.update_members(1, 6, (3,)),
     "PATCH", "/api/v1/accounts/1/teams/6/team_members", {"user_ids": [3]}),
    (lambda c: c.teams.remove_members(1, 6, [4]),
     "DELETE", "/api/v1/accounts/1/teams/6/team_members", {"user_ids": [4]}),
    (lambda c: c.messages.update_status(1, 2, 3, status="failed", external_error="outcome_unknown"),
     "PATCH", "/api/v1/accounts/1/conversations/2/messages/3",
     {"status": "failed", "external_error": "outcome_unknown"}),
    (lambda c: c.messages.update_status(1, 2, 3, status="sent"),
     "PATCH", "/api/v1/accounts/1/conversations/2/messages/3", {"status": "sent"}),
])
def test_http_e_payload_exatos(chamada, verbo, caminho, payload):
    chamadas = []
    with cliente_mock(chamadas) as cliente:
        assert chamada(cliente) == {"ok": True}
    assert len(chamadas) == 1
    assert chamadas[0].method == verbo
    assert chamadas[0].url.path == caminho
    assert json.loads(chamadas[0].content) == payload


@pytest.mark.parametrize("chamada", [
    lambda c: c.contacts.add_inbox(1, 3, inbox_id=0),
    lambda c: c.contacts.add_inbox(1, 3, inbox_id=4, source_id=" "),
    lambda c: c.contacts.merge(1, base_contact_id=3, mergee_contact_id=3),
    lambda c: c.contacts.merge(1, base_contact_id=True, mergee_contact_id=3),
    lambda c: c.contact_labels.replace(1, 3, "string-nao-aceita"),
    lambda c: c.contact_labels.replace(1, 3, ["ok", ""]),
    lambda c: c.inboxes.set_agent_bot(1, 4, agent_bot="bot"),
    lambda c: c.inboxes.add_member(1, inbox_id=4, user_ids=[]),
    lambda c: c.inboxes.add_member(1, inbox_id=4, user_ids=[1, True]),
    lambda c: c.inboxes.update_members(1, inbox_id=4, user_ids=[1, 1]),
    lambda c: c.inboxes.remove_members(1, inbox_id=4, user_ids=[-1]),
    lambda c: c.teams.add_members(1, 3, [0]),
    lambda c: c.teams.update_members(1, 3, "3"),
    lambda c: c.teams.remove_members(1, 3, []),
    lambda c: c.messages.update_status(1, 2, 3, status=""),
    lambda c: c.messages.update_status(1, 2, 3, status="sent", external_error=123),
])
def test_entrada_invalida_impede_http(chamada):
    chamadas = []
    with cliente_mock(chamadas) as cliente, pytest.raises((ValueError, TypeError)):
        chamada(cliente)
    assert chamadas == []
