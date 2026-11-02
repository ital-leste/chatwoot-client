"""Contratos HTTP do client Chatwoot, sem acessar uma instalação real."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx
import pytest

from chatwoot_client import CWClient, ErroAPIChatwoot


def _cliente_simulado(handler: Callable[[httpx.Request], httpx.Response]) -> CWClient:
    client = CWClient(base_url="https://chatwoot.example", api_token="token-de-teste")
    headers = dict(client._http.headers)
    client._http.close()
    client._http = httpx.Client(
        base_url="https://chatwoot.example/",
        headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return client


@pytest.mark.parametrize(
    ("call", "path", "body"),
    [
        (lambda c: c.profile.get(), "/api/v1/profile", {"id": 5, "new_field": "ok"}),
        (lambda c: c.account.get(1), "/api/v1/accounts/1", {"id": 1, "extra": {"a": 1}}),
        (lambda c: c.agents.list(1), "/api/v1/accounts/1/agents", [{"id": 5, "extra": 2}]),
        (lambda c: c.contacts.get(1, 2), "/api/v1/accounts/1/contacts/2", {"id": 2}),
        (lambda c: c.inboxes.get(1, 3), "/api/v1/accounts/1/inboxes/3", {"id": 3}),
        (
            lambda c: c.conversations.get(1, 4),
            "/api/v1/accounts/1/conversations/4",
            {"id": 4, "status": "open", "new_field": [1, 2]},
        ),
    ],
)
def test_consultas_usam_rotas_oficiais_e_preservam_json(call, path, body):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=body)

    with _cliente_simulado(handler) as client:
        result = call(client)

    assert result == body
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == path
    assert requests[0].headers["Authorization"] == "Bearer token-de-teste"
    assert not requests[0].url.params


def test_construtor_usa_apenas_parametros_fornecidos(monkeypatch):
    monkeypatch.setenv("CHATWOOT_BASE_URL", "https://outro-servidor.invalid")
    monkeypatch.setenv("CHATWOOT_API_TOKEN", "token-do-ambiente")

    with CWClient("https://chatwoot.example", "token-do-consumidor") as client:
        assert client._http.base_url.host == "chatwoot.example"
        assert client._http.headers["Authorization"] == "Bearer token-do-consumidor"
        assert not hasattr(client, "from_env")


def test_listagem_de_conversas_encaminha_filtros_sem_alterar_envelope():
    requests: list[httpx.Request] = []
    body = {"data": {"meta": {"all_count": 1}, "payload": [{"id": 4, "new": 2}]}}

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=body)

    with _cliente_simulado(handler) as client:
        result = client.conversations.list(
            1,
            assignee_type="all",
            status="pending",
            inbox_id=3,
            labels=["nova", "prioridade"],
            page=2,
        )

    assert result == body
    assert requests[0].url.path == "/api/v1/accounts/1/conversations"
    params = requests[0].url.params
    assert params["assignee_type"] == "all"
    assert params["status"] == "pending"
    assert params["inbox_id"] == "3"
    assert params["page"] == "2"
    assert params.get_list("labels[]") == ["nova", "prioridade"]
    assert "team_id" not in params
    assert "q" not in params


def test_listagem_de_mensagens_encaminha_cursores_e_preserva_metadados():
    requests: list[httpx.Request] = []
    body = {
        "meta": {"labels": ["teste"], "new_field": {"value": 7}},
        "payload": [{"id": 43, "attachments": [{"content_type": "image/jpeg", "width": 600}]}],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=body)

    with _cliente_simulado(handler) as client:
        result = client.messages.list(1, 2, before=43, after=0)

    assert result == body
    assert requests[0].url.path == "/api/v1/accounts/1/conversations/2/messages"
    assert requests[0].url.params["before"] == "43"
    assert requests[0].url.params["after"] == "0"


def test_erro_http_e_reportado_sem_expor_dados_de_resposta():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": "informacao-sensivel"})

    with _cliente_simulado(handler) as client, pytest.raises(ErroAPIChatwoot) as caught:
        client.contacts.get(1, 2)

    assert caught.value.status_http == 403
    assert "informacao-sensivel" not in str(caught.value)
