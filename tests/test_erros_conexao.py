"""Classificação de transporte versus contrato de resposta no SDK público."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import CWClient, ErroAPIChatwoot, ErroConexaoChatwoot, ErroFormatoChatwoot


def cliente_falso(handler):
    cliente = CWClient("https://cw.invalid", "token-sintetico")
    cabecalhos = dict(cliente._http.headers)
    cliente._http.close()
    cliente._http = httpx.Client(
        base_url="https://cw.invalid/",
        headers=cabecalhos,
        transport=httpx.MockTransport(handler),
    )
    return cliente


@pytest.mark.parametrize("tipo", [httpx.ConnectError, httpx.ReadTimeout])
def test_transporte_tem_subclasse_publica_sem_repetir_requisicao(tipo):
    chamadas = []

    def handler(request):
        chamadas.append(request)
        raise tipo("indisponivel", request=request)

    with cliente_falso(handler) as cw, pytest.raises(ErroConexaoChatwoot) as capturado:
        cw.conversations.get(1, 2)

    erro = capturado.value
    assert isinstance(erro, ErroAPIChatwoot)
    assert erro.status_http is None
    assert erro.caminho == "api/v1/accounts/1/conversations/2"
    assert len(chamadas) == 1


@pytest.mark.parametrize("operacao,retorno", [
    ("objeto", [1, 2]),
    ("lista", {"id": 10}),
])
def test_estrutura_inesperada_sem_status_nao_e_transporte(operacao, retorno):
    def handler(request):
        return httpx.Response(200, json=retorno)

    with cliente_falso(handler) as cw, pytest.raises(ErroAPIChatwoot) as capturado:
        if operacao == "objeto":
            cw.conversations.get(1, 2)
        else:
            cw.agents.list(1)

    erro = capturado.value
    assert type(erro) is ErroFormatoChatwoot
    assert isinstance(erro, ErroAPIChatwoot)
    assert not isinstance(erro, ErroConexaoChatwoot)
    assert erro.status_http is None


def test_json_invalido_nao_e_transporte():
    def handler(request):
        return httpx.Response(200, content=b"{json-malformado")

    with cliente_falso(handler) as cw, pytest.raises(ErroAPIChatwoot) as capturado:
        cw.conversations.get(1, 2)

    assert type(capturado.value) is ErroFormatoChatwoot
    assert isinstance(capturado.value, ErroAPIChatwoot)
    assert not isinstance(capturado.value, ErroConexaoChatwoot)
    assert capturado.value.status_http == 200


@pytest.mark.parametrize("status", [401, 404, 408, 429, 503])
def test_erro_http_permanece_na_classe_original(status):
    def handler(request):
        return httpx.Response(status, json={"error": "sintetico"})

    with cliente_falso(handler) as cw, pytest.raises(ErroAPIChatwoot) as capturado:
        cw.conversations.get(1, 2)

    erro = capturado.value
    assert type(erro) is ErroAPIChatwoot
    assert not isinstance(erro, ErroConexaoChatwoot)
    assert erro.status_http == status


@pytest.mark.parametrize("status,conteudo", [
    (204, b""), (200, b""), (200, b"null"),
])
def test_resposta_sem_objeto_e_classificada_como_formato(status, conteudo):
    def handler(request):
        return httpx.Response(status, content=conteudo)

    with cliente_falso(handler) as cw, pytest.raises(ErroFormatoChatwoot) as capturado:
        cw.conversations.get(1, 2)

    assert isinstance(capturado.value, ErroAPIChatwoot)
    assert not isinstance(capturado.value, ErroConexaoChatwoot)
