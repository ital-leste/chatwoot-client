"""Contratos de entrada tipados e retornos nativos para respostas rápidas Chatwoot."""
from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import httpx
import pytest

from chatwoot_client import CWClient, CannedResponse, ErroAPIChatwoot


def _registro(**alteracoes):
    dados = {
        "id": 7,
        "account_id": 1,
        "short_code": "gnv",
        "content": "Inspeção GNV",
        "created_at": "2026-11-02T10:00:00Z",
        "updated_at": "2026-11-02T10:30:00Z",
        "extra_provedor": {"valor": 42},
    }
    dados.update(alteracoes)
    return dados


def _client(chamadas, *, handler=None):
    def responder(req):
        chamadas.append(req)
        if handler is not None:
            return handler(req)
        if req.method == "GET":
            return httpx.Response(200, json=[_registro()])
        if req.method == "DELETE":
            return httpx.Response(200, content=b"")
        return httpx.Response(200, json=_registro())

    cw = CWClient("https://chatwoot.exemplo", "token")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.exemplo/",
        headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cw


def test_listagem_completa_get_sem_query_e_json_original():
    chamadas = []
    with _client(chamadas) as cw:
        resposta = cw.canned_responses.list(1)
    assert resposta == [_registro()]
    assert type(resposta[0]) is dict
    assert resposta[0]["extra_provedor"] == {"valor": 42}
    assert len(chamadas) == 1
    assert chamadas[0].method == "GET"
    assert chamadas[0].url.path == "/api/v1/accounts/1/canned_responses"
    assert chamadas[0].url.query == b""


def test_listagem_com_filtro_mantem_get_e_servidor_define_resultados():
    chamadas = []
    with _client(chamadas) as cw:
        resposta = cw.canned_responses.list(1, search=" gnv ")
    assert resposta == [_registro()]
    assert len(chamadas) == 1
    assert chamadas[0].method == "GET"
    assert chamadas[0].url.params["search"] == "gnv"


def test_listagem_vazia_retorna_lista_vazia():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, json=[])) as cw:
        assert cw.canned_responses.list(1, search="sem_resultado") == []


@pytest.mark.parametrize("search", ["", "   ", "\0unsafe", 12, False, ["gnv"]])
def test_filtro_invalido_bloqueia_http(search):
    chamadas = []
    with _client(chamadas) as cw, pytest.raises(ValueError):
        cw.canned_responses.list(1, search=search)
    assert not chamadas


@pytest.mark.parametrize("json_response", [None, {}, {"payload": []}, "resposta", [1], ["texto"], [None]])
def test_formato_de_lista_invalido_falha_fechada(json_response):
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, json=json_response)) as cw:
        with pytest.raises(ErroAPIChatwoot):
            cw.canned_responses.list(1)
    assert len(chamadas) == 1


def test_criar_contrato_e_retorno_json_sem_remodelagem():
    chamadas = []
    response = CannedResponse(short_code="gnv_periodica", content="Mensagem padrão")
    with _client(chamadas) as cw:
        resultado = cw.canned_responses.create(1, response)
    assert resultado == _registro()
    assert isinstance(resultado, dict)
    assert json.loads(chamadas[0].content) == {
        "short_code": "gnv_periodica", "content": "Mensagem padrão"
    }
    assert chamadas[0].method == "POST"


def test_atualizacao_parcial_usa_o_mesmo_contrato():
    chamadas = []
    with _client(chamadas) as cw:
        result = cw.canned_responses.update(
            1, 7, CannedResponse(content="Texto revisado")
        )
    assert result == _registro()
    assert chamadas[0].method == "PATCH"
    assert chamadas[0].url.path.endswith("/canned_responses/7")
    assert json.loads(chamadas[0].content) == {"content": "Texto revisado"}


def test_atualizar_apenas_atalho():
    chamadas = []
    with _client(chamadas) as cw:
        cw.canned_responses.update(1, 7, CannedResponse(short_code="novo"))
    assert json.loads(chamadas[0].content) == {"short_code": "novo"}


@pytest.mark.parametrize("op,argumento", [
    ("create", CannedResponse(content="sem atalho")),
    ("create", CannedResponse(short_code="sem_conteudo")),
    ("create", CannedResponse()),
    ("update", CannedResponse()),
    ("create", {"short_code": "livre", "content": "sem validação"}),
    ("update", {"content": "sem contrato"}),
])
def test_entrada_incompleta_ou_nao_tipado_nao_envia(op, argumento):
    chamadas = []
    with _client(chamadas) as cw, pytest.raises((ValueError, TypeError)):
        if op == "create":
            cw.canned_responses.create(1, argumento)
        else:
            cw.canned_responses.update(1, 7, argumento)
    assert not chamadas


@pytest.mark.parametrize("argumento", [
    {"short_code": 123},
    {"content": ""},
    {"short_code": " "},
    {"content": False},
])
def test_contrato_valida_tipos_e_vazio(argumento):
    with pytest.raises(ValueError):
        CannedResponse(**argumento)


def test_dataclass_congelada_e_nao_modela_saida():
    obj = CannedResponse("atalho", "texto")
    with pytest.raises(FrozenInstanceError):
        obj.content = "alterado"
    assert not hasattr(obj, "id")
    assert not hasattr(CannedResponse, "from_api")


def test_create_update_rejeitam_id_invalido_antes_http():
    chamadas = []
    with _client(chamadas) as cw:
        with pytest.raises(ValueError):
            cw.canned_responses.create(0, CannedResponse("x", "texto"))
        with pytest.raises(ValueError):
            cw.canned_responses.update(1, 0, CannedResponse(content="texto"))
    assert not chamadas


def test_erro_http_e_timeout_sem_retry():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(403, json={"secret": "sigilo"})) as cw:
        with pytest.raises(ErroAPIChatwoot) as exc:
            cw.canned_responses.create(1, CannedResponse("atalho", "conteudo"))
    assert exc.value.status_http == 403
    assert "sigilo" not in str(exc.value)
    assert len(chamadas) == 1


def test_delete_sem_corpo_retorna_none():
    chamadas = []
    with _client(chamadas) as cw:
        assert cw.canned_responses.delete(1, 7) is None
    assert chamadas[0].method == "DELETE"


def test_sem_variantes_publicas_antigas():
    chamadas = []
    with _client(chamadas) as cw:
        assert not hasattr(cw.canned_responses, "list_typed")
        assert not hasattr(cw.canned_responses, "get")
        with pytest.raises(TypeError):
            cw.canned_responses.list(1, parametros={"search": "gnv"})
    assert not chamadas
