"""Enums de consultas: opções fechadas e preservação de query HTTP."""
from __future__ import annotations

import httpx
import pytest
from chatwoot_client import CWClient, CustomFilterInput


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


@pytest.mark.parametrize("chamada,path,consulta", [
    (lambda c: c.reports.list_conversation_statistics(
        1, metric="avg_first_response_time", type_="inbox", id="12"),
     "/api/v2/accounts/1/reports", {"metric": "avg_first_response_time", "type": "inbox", "id": "12"}),
    (lambda c: c.reports.summary(1, type_="team"),
     "/api/v2/accounts/1/reports/summary", {"type": "team"}),
    (lambda c: c.reports.conversation_metrics(1, type_="account"),
     "/api/v2/accounts/1/reports/conversations", {"type": "account"}),
    (lambda c: c.reports.agent_conversation_metrics(1, type_="agent", user_id="2"),
     "/api/v2/accounts/1/reports/conversations/", {"type": "agent", "user_id": "2"}),
    (lambda c: c.reports.outgoing_messages_count(1, group_by="label"),
     "/api/v2/accounts/1/reports/outgoing_messages_count", {"group_by": "label"}),
    (lambda c: c.custom_attributes.list(1, attribute_model="0"),
     "/api/v1/accounts/1/custom_attribute_definitions", {"attribute_model": "0"}),
    (lambda c: c.custom_filters.list(1, filter_type="contact"),
     "/api/v1/accounts/1/custom_filters", {"filter_type": "contact"}),
    (lambda c: c.audit_logs.list(1, sort="desc"),
     "/api/v1/accounts/1/audit_logs", {"sort": "desc"}),
])
def test_query_tipado(chamada, path, consulta):
    chamadas = []
    with mock_cw(chamadas) as cw:
        assert chamada(cw) == {"ok": True}
    assert len(chamadas) == 1
    assert chamadas[0].method == "GET"
    assert chamadas[0].url.path == path
    assert dict(chamadas[0].url.params) == consulta


@pytest.mark.parametrize("chamada", [
    lambda c: c.reports.list_conversation_statistics(1, metric="foo", type_="account"),
    lambda c: c.reports.list_conversation_statistics(1, metric="conversations_count", type_="foo"),
    lambda c: c.reports.summary(1, type_="administrator"),
    lambda c: c.reports.conversation_metrics(1, type_="agent"),
    lambda c: c.reports.agent_conversation_metrics(1, type_="account"),
    lambda c: c.reports.outgoing_messages_count(1, group_by="date"),
    lambda c: c.custom_attributes.list(1, attribute_model="user"),
    lambda c: c.custom_filters.list(1, filter_type="inbox"),
    lambda c: c.custom_filters.create(1, CustomFilterInput(type="inbox")),
    lambda c: c.custom_filters.update(1, 3, CustomFilterInput(type="inbox")),
    lambda c: c.audit_logs.list(1, sort="oldest"),
    lambda c: c.reports.summary(1, type_="account", parametros={"type": "wrong"}),
])
def test_opcoes_invalidas_nao_enviam_requisicao(chamada):
    chamadas = []
    with mock_cw(chamadas) as cw, pytest.raises(ValueError):
        chamada(cw)
    assert chamadas == []
