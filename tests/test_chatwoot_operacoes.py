"""Teste das oito operações adicionadas, sem chamadas à VPS."""

from __future__ import annotations

import json
from collections.abc import Callable

import httpx
import pytest

from chatwoot_client import CWClient, ErroAPIChatwoot


def cliente_mock(handler: Callable[[httpx.Request], httpx.Response]) -> CWClient:
    cliente = CWClient("https://chatwoot.example", "token-testes")
    headers = dict(cliente._http.headers)
    cliente._http.close()
    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return cliente


@pytest.mark.parametrize(
    ("call", "method", "path", "body", "query"),
    [
        (lambda c: c.conversations.set_status(1, 2, "pending"), "POST",
         "/api/v1/accounts/1/conversations/2/toggle_status", {"status": "pending"}, {}),
        (lambda c: c.conversations.set_status(1, 2, "snoozed", snoozed_until=1770000000), "POST",
         "/api/v1/accounts/1/conversations/2/toggle_status",
         {"status": "snoozed", "snoozed_until": 1770000000}, {}),
        (lambda c: c.conversation_labels.list(1, 2), "GET",
         "/api/v1/accounts/1/conversations/2/labels", None, {}),
        (lambda c: c.conversation_labels.replace(1, 2, ["hermes-ativo", "teste"]), "POST",
         "/api/v1/accounts/1/conversations/2/labels",
         {"labels": ["hermes-ativo", "teste"]}, {}),
        (lambda c: c.conversation_labels.replace(1, 2, []), "POST",
         "/api/v1/accounts/1/conversations/2/labels", {"labels": []}, {}),
        (lambda c: c.labels.list(1), "GET", "/api/v1/accounts/1/labels", None, {}),
        (lambda c: c.labels.create(1, title="hermes-ativo", color="#123456"), "POST",
         "/api/v1/accounts/1/labels",
         {"title": "hermes-ativo", "color": "#123456"}, {}),
        (lambda c: c.labels.create(
            1, title="teste", color="#fedcba",
            description="Laboratório", show_on_sidebar=False,
         ), "POST", "/api/v1/accounts/1/labels",
         {"title": "teste", "color": "#fedcba",
          "description": "Laboratório", "show_on_sidebar": False}, {}),
        (lambda c: c.conversation_assignments.assign(1, 2, assignee_id=3), "POST",
         "/api/v1/accounts/1/conversations/2/assignments", {"assignee_id": 3}, {}),
        (lambda c: c.conversation_assignments.assign(1, 2, team_id=4), "POST",
         "/api/v1/accounts/1/conversations/2/assignments", {"team_id": 4}, {}),
        (lambda c: c.messages.create(1, 2, content="Bom dia!"), "POST",
         "/api/v1/accounts/1/conversations/2/messages",
         {"content": "Bom dia!", "message_type": "outgoing", "private": False}, {}),
        (lambda c: c.messages.create(1, 2, content="Nota", private=True), "POST",
         "/api/v1/accounts/1/conversations/2/messages",
         {"content": "Nota", "message_type": "outgoing", "private": True}, {}),
        (lambda c: c.conversations.filter(
            1, [{"attribute_key": "status", "filter_operator": "equal_to",
                 "values": ["pending"], "query_operator": None}],
            page=2, sort_by="created_at_desc",
        ), "POST", "/api/v1/accounts/1/conversations/filter",
         {"payload": [{"attribute_key": "status", "filter_operator": "equal_to",
                       "values": ["pending"], "query_operator": None}]},
         {"page": "2", "sort_by": "created_at_desc"}),
    ],
)
def test_novos_endpoints_preservam_http_e_json(call, method, path, body, query):
    chamadas = []
    response = {"meta": {"extra": "preservado"}, "payload": {"novo": 5}}

    def handler(request):
        chamadas.append(request)
        return httpx.Response(200, json=response)

    with cliente_mock(handler) as client:
        retorno = call(client)

    assert retorno == response
    assert len(chamadas) == 1
    enviada = chamadas[0]
    assert enviada.method == method
    assert enviada.url.path == path
    assert enviada.headers["authorization"] == "Bearer token-testes"
    assert dict(enviada.url.params) == query
    if body is None:
        assert not enviada.content
    else:
        assert json.loads(enviada.content) == body


@pytest.mark.parametrize(
    "call",
    [
        lambda c: c.conversations.set_status(1, 2, "all"),
        lambda c: c.conversations.set_status(1, 2, "open", snoozed_until=123),
        lambda c: c.conversations.set_status(1, 2, "snoozed", snoozed_until=0),
        lambda c: c.conversation_labels.replace(1, 2, "etiqueta"),
        lambda c: c.conversation_labels.replace(1, 2, ["ok", ""]),
        lambda c: c.labels.create(1, title="", color="#111111"),
        lambda c: c.labels.create(1, title="teste", color=""),
        lambda c: c.labels.create(1, title="teste", color="#abcdef", show_on_sidebar="sim"),
        lambda c: c.conversation_assignments.assign(1, 2),
        lambda c: c.conversation_assignments.assign(1, 2, assignee_id=1, team_id=2),
        lambda c: c.messages.create(1, 2, content=""),
        lambda c: c.messages.create(1, 2, content="ok", message_type="activity"),
        lambda c: c.messages.create(1, 2, content="ok", private=1),
        lambda c: c.conversations.filter(1, []),
        lambda c: c.conversations.filter(1, [{}], page=0),
    ],
)
def test_validacao_impede_chamada(call):
    chamadas = []

    def handler(request):
        chamadas.append(request)
        return httpx.Response(200, json={})

    with cliente_mock(handler) as client, pytest.raises((ValueError, TypeError)):
        call(client)

    assert not chamadas


def test_erro_post_preserva_status_sem_expor_resposta_ou_reenviar():
    chamadas = []

    def handler(request):
        chamadas.append(request)
        return httpx.Response(422, json={"private": "segredo"})

    with cliente_mock(handler) as client, pytest.raises(ErroAPIChatwoot) as erro:
        client.messages.create(1, 2, content="teste")

    assert len(chamadas) == 1
    assert erro.value.status_http == 422
    assert "segredo" not in str(erro.value)


def test_timeout_nao_reenvia_mensagem():
    chamadas = []

    def handler(request):
        chamadas.append(request)
        raise httpx.ReadTimeout("timeout", request=request)

    with cliente_mock(handler) as client, pytest.raises(ErroAPIChatwoot):
        client.messages.create(1, 2, content="teste")

    assert len(chamadas) == 1
