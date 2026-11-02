"""Regressão: listagem integral/filtrada e contratos tipados de Canned Responses."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import (
    CWClient, CannedResponse, CannedResponseCreate, CannedResponseUpdate,
    ErroAPIChatwoot,
)


def _registro(*, id=7, account_id=1, short_code="gnv", content="Inspeção GNV"):
    return {
        "id": id,
        "account_id": account_id,
        "short_code": short_code,
        "content": content,
        "created_at": "2026-11-02T10:00:00Z",
        "updated_at": "2026-11-02T10:30:00Z",
    }


def _client(requests, handler=None):
    def responder(request):
        requests.append(request)
        if handler:
            return handler(request)
        if request.method == "GET":
            return httpx.Response(200, json=[_registro()])
        if request.method == "DELETE":
            return httpx.Response(200, content=b"")
        return httpx.Response(200, json=_registro())

    client = CWClient("https://chatwoot.exemplo", "token")
    headers = dict(client._http.headers)
    client._http.close()
    client._http = httpx.Client(
        base_url="https://chatwoot.exemplo/",
        headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return client


def test_list_sem_filtro_usa_get_unico_e_preserva_json():
    requests = []
    with _client(requests) as cw:
        result = cw.canned_responses.list(1)
    assert result == [_registro()]
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/api/v1/accounts/1/canned_responses"
    assert requests[0].url.query == b""


def test_list_com_search_usa_mesmo_get_sem_post():
    requests = []
    with _client(requests) as cw:
        result = cw.canned_responses.list(1, search="gnv")
    assert result == [_registro()]
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.params["search"] == "gnv"


def test_search_antigo_via_parametros_continua_funcionando():
    requests = []
    with _client(requests) as cw:
        cw.canned_responses.list(1, parametros={"search": "periodica"})
    assert requests[0].url.params["search"] == "periodica"


def test_lista_tipadas_inteira_e_filtrada():
    requests = []
    with _client(requests) as cw:
        all_items = cw.canned_responses.list_typed(1)
        filtered = cw.canned_responses.list_typed(1, search="GNv")
    assert len(requests) == 2
    assert all(isinstance(item, CannedResponse) for item in all_items + filtered)
    assert all_items[0].short_code == "gnv"
    assert all_items[0].updated_at == "2026-11-02T10:30:00Z"
    assert requests[1].url.params["search"] == "GNv"
    assert requests[0].method == requests[1].method == "GET"


def test_lista_vazia_tipadas():
    requests = []
    with _client(requests, lambda req: httpx.Response(200, json=[])) as cw:
        assert cw.canned_responses.list_typed(1, search="sem_match") == []


@pytest.mark.parametrize("invalid", [
    "", " ", "\x00texto", 33, False,
])
def test_search_invalido_nao_dispara_http(invalid):
    requests = []
    with _client(requests) as cw, pytest.raises(ValueError):
        cw.canned_responses.list(1, search=invalid)
    assert not requests


def test_search_nao_pode_conflitar_com_parametros():
    requests = []
    with _client(requests) as cw, pytest.raises(ValueError):
        cw.canned_responses.list(1, search="abc", parametros={"search": "def"})
    assert not requests


@pytest.mark.parametrize("payload", [
    {"payload": [_registro()]},
    {},
    None,
    [_registro(id=True)],
    [_registro(account_id=0)],
    [_registro(content="")],
    [{"id": 3, "short_code": "x", "content": "a"}],
    ["texto inesperado"],
])
def test_resposta_invalida_levanta_erro_chatwoot(payload):
    requests = []
    with _client(requests, lambda req: httpx.Response(200, json=payload)) as cw:
        with pytest.raises(ErroAPIChatwoot):
            cw.canned_responses.list_typed(1)


def test_criacao_tipadas_json_campos_oficiais():
    requests = []
    with _client(requests) as cw:
        result = cw.canned_responses.create(
            1, CannedResponseCreate(short_code="gnv", content="Faça inspeção.")
        )
    assert result["id"] == 7
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/api/v1/accounts/1/canned_responses"
    assert requests[0].read().decode().find("canned_response") == -1
    assert requests[0].headers["content-type"].startswith("application/json")
    assert requests[0].content == b'{"short_code":"gnv","content":"Fa\\u00e7a inspe\\u00e7\\u00e3o."}' or __import__("json").loads(requests[0].content) == {"short_code": "gnv", "content": "Faça inspeção."}


def test_update_tipado_parcial_e_patch():
    requests = []
    with _client(requests) as cw:
        cw.canned_responses.update(
            1, 7, CannedResponseUpdate(content="Novo texto")
        )
    assert len(requests) == 1
    assert requests[0].method == "PATCH"
    assert requests[0].url.path == "/api/v1/accounts/1/canned_responses/7"
    import json
    assert json.loads(requests[0].content) == {"content": "Novo texto"}


def test_delete_retorna_none_para_200_sem_corpo():
    requests = []
    with _client(requests) as cw:
        assert cw.canned_responses.delete(1, 7) is None
    assert requests[0].method == "DELETE"


def test_compatibilidade_mapping_create_update():
    import json
    requests = []
    with _client(requests) as cw:
        cw.canned_responses.create(1, {"short_code": "old", "content": "Original"})
        cw.canned_responses.update(1, 7, {"content": "Corrigido"})
    assert len(requests) == 2
    assert json.loads(requests[0].content)["short_code"] == "old"
    assert json.loads(requests[1].content) == {"content": "Corrigido"}


@pytest.mark.parametrize("factory", [
    lambda: CannedResponseCreate("", "texto"),
    lambda: CannedResponseCreate("atalho", "  "),
    lambda: CannedResponseCreate(123, "texto"),
    lambda: CannedResponseUpdate(),
    lambda: CannedResponseUpdate(content=""),
    lambda: CannedResponseUpdate(short_code=123),
    lambda: CannedResponseUpdate(content="x", short_code=" "),
    lambda: CannedResponse.from_api({"id": 1, "account_id": 2, "short_code": "x"}),
])
def test_modelos_invalidos_antes_de_http(factory):
    with pytest.raises(ValueError):
        factory()


def test_erro_http_propagado_sem_retry():
    requests = []
    with _client(requests, lambda req: httpx.Response(403, json={"error": "denied"})) as cw:
        with pytest.raises(ErroAPIChatwoot) as exc:
            cw.canned_responses.list_typed(1)
    assert exc.value.status_http == 403
    assert len(requests) == 1
