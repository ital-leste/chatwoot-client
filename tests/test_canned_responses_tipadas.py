"""Canned Responses: parâmetros tipados, GET filtrado e JSON bruto preservado."""
from __future__ import annotations

import json

import httpx
import pytest

import chatwoot_client
from chatwoot_client import CWClient, ErroAPIChatwoot
from chatwoot_client import models


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


def test_listagem_sem_filtro_usa_get_e_preserva_todos_os_campos():
    chamadas = []
    with _client(chamadas) as cw:
        resultado = cw.canned_responses.list(1)
    assert resultado == [_registro()]
    assert type(resultado[0]) is dict
    assert resultado[0]["extra_provedor"] == {"valor": 42}
    assert len(chamadas) == 1
    assert chamadas[0].method == "GET"
    assert chamadas[0].url.path == "/api/v1/accounts/1/canned_responses"
    assert chamadas[0].url.query == b""


def test_listagem_filtrada_usa_mesmo_get_com_search():
    chamadas = []
    with _client(chamadas) as cw:
        resultado = cw.canned_responses.list(1, search=" gnv ")
    assert resultado == [_registro()]
    assert len(chamadas) == 1
    assert chamadas[0].method == "GET"
    assert chamadas[0].url.params["search"] == "gnv"


def test_listagem_vazia_retorna_lista_vazia():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, json=[])) as cw:
        assert cw.canned_responses.list(1, search="sem_resultado") == []


@pytest.mark.parametrize("search", ["", "   ", "\x00unsafe", 12, False, ["gnv"]])
def test_search_invalido_nao_envia_requisicao(search):
    chamadas = []
    with _client(chamadas) as cw, pytest.raises(ValueError):
        cw.canned_responses.list(1, search=search)
    assert not chamadas


@pytest.mark.parametrize("payload", [None, {}, {"payload": []}, "texto", [1], ["texto"], [None]])
def test_lista_com_formato_invalido_rejeitada(payload):
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, json=payload)) as cw:
        with pytest.raises(ErroAPIChatwoot):
            cw.canned_responses.list(1)
    assert len(chamadas) == 1


def test_criacao_recebe_somente_parametros_nomeados_e_retorna_json():
    chamadas = []
    with _client(chamadas) as cw:
        resultado = cw.canned_responses.create(
            1, short_code="gnv_periodica", content="Mensagem padrão"
        )
    assert resultado == _registro()
    assert type(resultado) is dict
    assert chamadas[0].method == "POST"
    assert chamadas[0].url.path == "/api/v1/accounts/1/canned_responses"
    assert json.loads(chamadas[0].content) == {
        "short_code": "gnv_periodica",
        "content": "Mensagem padrão",
    }


def test_atualizacao_parcial_apenas_conteudo():
    chamadas = []
    with _client(chamadas) as cw:
        resultado = cw.canned_responses.update(1, 7, content="Texto revisado")
    assert resultado == _registro()
    assert chamadas[0].method == "PATCH"
    assert chamadas[0].url.path.endswith("/canned_responses/7")
    assert json.loads(chamadas[0].content) == {"content": "Texto revisado"}


def test_atualizacao_parcial_apenas_atalho():
    chamadas = []
    with _client(chamadas) as cw:
        cw.canned_responses.update(1, 7, short_code="outro")
    assert json.loads(chamadas[0].content) == {"short_code": "outro"}


def test_atualizacao_de_ambos_os_campos():
    chamadas = []
    with _client(chamadas) as cw:
        cw.canned_responses.update(1, 7, short_code="outro", content="Novo conteúdo")
    assert json.loads(chamadas[0].content) == {
        "short_code": "outro", "content": "Novo conteúdo"
    }


@pytest.mark.parametrize(("operacao", "argumentos"), [
    ("create", {"short_code": "", "content": "válido"}),
    ("create", {"short_code": "  ", "content": "válido"}),
    ("create", {"short_code": "válido", "content": ""}),
    ("create", {"short_code": "válido", "content": "  "}),
    ("create", {"short_code": 12, "content": "válido"}),
    ("create", {"short_code": False, "content": "válido"}),
    ("create", {"short_code": "válido", "content": 123}),
    ("update", {}),
    ("update", {"content": ""}),
    ("update", {"short_code": "  "}),
    ("update", {"short_code": 1}),
    ("update", {"content": False}),
    ("update", {"short_code": "válido", "content": ""}),
])
def test_escrita_invalida_nao_efetua_http(operacao, argumentos):
    chamadas = []
    with _client(chamadas) as cw, pytest.raises(ValueError):
        if operacao == "create":
            cw.canned_responses.create(1, **argumentos)
        else:
            cw.canned_responses.update(1, 7, **argumentos)
    assert not chamadas


def test_ausencia_de_campo_obrigatorio_ou_entrada_estruturada():
    chamadas = []
    with _client(chamadas) as cw:
        with pytest.raises(TypeError):
            cw.canned_responses.create(1, short_code="gnv")
        with pytest.raises(TypeError):
            cw.canned_responses.create(1, {"short_code": "gnv", "content": "x"})
        with pytest.raises(TypeError):
            cw.canned_responses.update(1, 7, {"content": "x"})
        with pytest.raises(TypeError):
            cw.canned_responses.update(1, 7, data={"content": "x"})
        with pytest.raises(TypeError):
            cw.canned_responses.list(1, parametros={"search": "gnv"})
    assert not chamadas


def test_modelo_desnecessario_nao_e_exportado():
    assert not hasattr(chatwoot_client, "CannedResponse")
    assert not hasattr(models, "CannedResponse")


def test_ids_invalidos_nao_efetuam_http():
    chamadas = []
    with _client(chamadas) as cw:
        with pytest.raises(ValueError):
            cw.canned_responses.list(0)
        with pytest.raises(ValueError):
            cw.canned_responses.create(0, short_code="x", content="y")
        with pytest.raises(ValueError):
            cw.canned_responses.update(1, 0, content="y")
        with pytest.raises(ValueError):
            cw.canned_responses.delete(1, 0)
    assert not chamadas


def test_erro_http_repassa_status_sem_vazar_corpo():
    chamadas = []
    with _client(
        chamadas, handler=lambda req: httpx.Response(403, json={"token": "sigilo"})
    ) as cw:
        with pytest.raises(ErroAPIChatwoot) as exc:
            cw.canned_responses.create(1, short_code="gnv", content="texto")
    assert exc.value.status_http == 403
    assert "sigilo" not in str(exc.value)
    assert len(chamadas) == 1


def test_criacao_retorno_nao_objeto_rejeitado():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, json=[])) as cw:
        with pytest.raises(ErroAPIChatwoot):
            cw.canned_responses.create(1, short_code="gnv", content="texto")
    assert len(chamadas) == 1


def test_exclusao_200_sem_corpo_retorna_none():
    chamadas = []
    with _client(chamadas) as cw:
        assert cw.canned_responses.delete(1, 7) is None
    assert chamadas[0].method == "DELETE"
