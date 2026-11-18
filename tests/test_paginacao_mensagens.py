"""Paginação por cursor do MessageFinder do Chatwoot 4.19.0."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import CWClient


def _cliente(chamadas: list[httpx.Request], resposta: dict) -> CWClient:
    cliente = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(cliente._http.headers)
    cliente._http.close()

    def responder(request: httpx.Request) -> httpx.Response:
        chamadas.append(request)
        return httpx.Response(200, json=resposta)

    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/",
        headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cliente


@pytest.mark.parametrize(("cursores", "esperados"), [
    ({}, {}),
    ({"before": 123}, {"before": "123"}),
    ({"after": 123}, {"after": "123"}),
    ({"after": 0, "before": 123}, {"after": "0", "before": "123"}),
    ({"after": 100, "before": 200}, {"after": "100", "before": "200"}),
])
def test_cursores_validos_preservam_json_original(cursores, esperados):
    chamadas: list[httpx.Request] = []
    resposta = {
        "meta": {"all_count": 77, "extra": {"cursor": "nativo"}},
        "payload": [{"id": 123, "content": "teste", "extra": [1, 2]}],
    }
    with _cliente(chamadas, resposta) as cliente:
        resultado = cliente.messages.list(1, 2, **cursores)

    assert resultado == resposta
    assert len(chamadas) == 1
    assert chamadas[0].url.path == "/api/v1/accounts/1/conversations/2/messages"
    assert dict(chamadas[0].url.params) == esperados


@pytest.mark.parametrize("cursores", [
    {"before": -1},
    {"after": -1},
    {"before": True},
    {"after": False},
    {"before": "123"},
    {"after": 1.0},
    {"before": 10, "after": 10},
    {"before": 10, "after": 11},
    {"before": 0, "after": 0},
])
def test_cursores_invalidos_nao_disparam_http(cursores):
    chamadas: list[httpx.Request] = []
    with _cliente(chamadas, {"meta": {}, "payload": []}) as cliente:
        with pytest.raises(ValueError):
            cliente.messages.list(1, 2, **cursores)

    assert chamadas == []
