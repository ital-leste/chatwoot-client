"""Validação de query parameters oficiais antes do transporte HTTP."""
from __future__ import annotations

import httpx
import pytest
from chatwoot_client import CWClient


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


@pytest.mark.parametrize("chamada,caminho,campos", [
    (lambda c: c.contacts.list(1, sort="-email", page=3),
     "/api/v1/accounts/1/contacts", {"sort": "-email", "page": "3"}),
    (lambda c: c.contacts.search(1, q="Maria", sort="last_activity_at"),
     "/api/v1/accounts/1/contacts/search", {"q": "Maria", "sort": "last_activity_at"}),
    (lambda c: c.audit_logs.list(1, types=["User"], since=0, sort="desc"),
     "/api/v1/accounts/1/audit_logs", {"types": "User", "since": "0", "sort": "desc"}),
    (lambda c: c.reports.inbox_label_matrix(1, inbox_ids=[1], label_ids=[2]),
     "/api/v2/accounts/1/reports/inbox_label_matrix", {"inbox_ids": "1", "label_ids": "2"}),
    (lambda c: c.reports.inbox_summary(1, business_hours=False),
     "/api/v2/accounts/1/summary_reports/inbox", {"business_hours": "false"}),
    (lambda c: c.automation_rules.list(1, page=2),
     "/api/v1/accounts/1/automation_rules", {"page": "2"}),
    (lambda c: c.inboxes.list_message_templates(1, 2, name="hello"),
     "/api/v1/accounts/1/inboxes/2/message_templates", {"name": "hello"}),
])
def test_queries_certas(chamada, caminho, campos):
    chamadas=[]
    with cliente_mock(chamadas) as c:
        assert chamada(c)=={"ok": True}
    assert len(chamadas)==1
    assert chamadas[0].url.path==caminho
    assert dict(chamadas[0].url.params)==campos


@pytest.mark.parametrize("chamada", [
    lambda c: c.contacts.list(1, sort="random"),
    lambda c: c.contacts.list(1, page=False),
    lambda c: c.contacts.search(1, sort="invalido"),
    lambda c: c.audit_logs.list(1, types=[1]),
    lambda c: c.audit_logs.list(1, since=-2),
    lambda c: c.audit_logs.list(1, page=0),
    lambda c: c.reports.inbox_label_matrix(1, inbox_ids=[True]),
    lambda c: c.reports.inbox_label_matrix(1, label_ids=["a"]),
    lambda c: c.reports.inbox_summary(1, business_hours=1),
    lambda c: c.reports.list_reporting_events(1, inbox_id="1"),
    lambda c: c.automation_rules.list(1, page=-1),
    lambda c: c.inboxes.list_message_templates(1, 2, name=""),
])
def test_queries_invalidas_sem_http(chamada):
    chamadas=[]
    with cliente_mock(chamadas) as c, pytest.raises(ValueError):
        chamada(c)
    assert chamadas==[]
