"""Metadados seguros de erros HTTP sem repetir requisições."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import CWClient, ErroAPIChatwoot, ErroFormatoChatwoot


def _cliente(resposta, chamadas):
    def handler(req):
        chamadas.append(req)
        return resposta
    c = CWClient("https://cw.example", "token-de-teste")
    cabecalhos = dict(c._http.headers)
    c._http.close()
    c._http = httpx.Client(
        base_url="https://cw.example/", headers=cabecalhos,
        transport=httpx.MockTransport(handler),
    )
    return c


def test_erro_429_expoe_retry_after_e_request_id_sem_corpo():
    chamadas = []
    resposta = httpx.Response(
        429, json={"erro": "SEGREDO-QUE-NAO-PODE-VAZAR"},
        headers={"Retry-After": "7", "X-Request-Id": "req_123-abc"},
    )
    with _cliente(resposta, chamadas) as cw, pytest.raises(ErroAPIChatwoot) as recebido:
        cw.contacts.get(1, 2)
    erro = recebido.value
    assert type(erro) is ErroAPIChatwoot
    assert erro.status_http == 429
    assert erro.retry_after == 7
    assert erro.request_id == "req_123-abc"
    assert "SEGREDO" not in str(erro)
    assert len(chamadas) == 1


@pytest.mark.parametrize("header", ["Wed, 21 Oct 2026 07:28:00 GMT", "-1", "abc", "9" * 20])
def test_retry_after_nao_numerico_nao_e_inferido(header):
    chamadas = []
    resposta = httpx.Response(503, headers={"Retry-After": header})
    with _cliente(resposta, chamadas) as cw, pytest.raises(ErroAPIChatwoot) as recebido:
        cw.contacts.get(1, 2)
    assert recebido.value.retry_after is None
    assert recebido.value.status_http == 503


def test_id_de_requisicao_nao_confiavel_nao_e_repassado():
    chamadas = []
    resposta = httpx.Response(
        403, headers={"X-Request-Id": "TOKEN\tSECRETO"}, json={"error": "senha"},
    )
    with _cliente(resposta, chamadas) as cw, pytest.raises(ErroAPIChatwoot) as recebido:
        cw.contacts.get(1, 2)
    assert recebido.value.request_id is None
    assert recebido.value.retry_after is None
    assert "senha" not in str(recebido.value)


def test_json_malformado_preserva_status_e_classe_formato():
    chamadas = []
    resposta = httpx.Response(200, content=b"{nao-e-json")
    with _cliente(resposta, chamadas) as cw, pytest.raises(ErroFormatoChatwoot) as recebido:
        cw.contacts.get(1, 2)
    assert recebido.value.status_http == 200
    assert recebido.value.retry_after is None
    assert recebido.value.request_id is None
