"""Regressão: entradas de Conversations e filtros compartilhados sem HTTP real."""
from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from typing import Any

import httpx
import pytest

from chatwoot_client import (
    CWClient, ConversationCreate, ConversationPriority, ConversationStatus,
    FilterCondition, ErroAPIChatwoot,
)


def _client(chamadas: list[httpx.Request], handler=None) -> CWClient:
    def responder(req: httpx.Request) -> httpx.Response:
        chamadas.append(req)
        if handler is not None:
            return handler(req)
        return httpx.Response(200, json={"ok": True, "extra": {"campo": [1]}})

    cw = CWClient("https://chatwoot.example", "token-teste")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cw


def test_criar_conversa_com_contrato_tipado_e_json_bruto():
    chamadas = []
    objeto = ConversationCreate(
        source_id="origem123", inbox_id=2, contact_id=42,
        status=ConversationStatus.PENDING,
        additional_attributes={"browser": "Firefox"},
        custom_attributes={"interesse": "GNV"},
        message={"content": "Bem-vindo!"},
    )
    with pytest.raises(FrozenInstanceError):
        objeto.source_id = "alterado"
    with _client(chamadas) as cw:
        resposta = cw.conversations.create(1, objeto)
    assert resposta == {"ok": True, "extra": {"campo": [1]}}
    assert chamadas[0].method == "POST"
    assert chamadas[0].url.path == "/api/v1/accounts/1/conversations"
    assert json.loads(chamadas[0].content) == {
        "source_id": "origem123", "inbox_id": 2, "contact_id": 42,
        "status": "pending", "additional_attributes": {"browser": "Firefox"},
        "custom_attributes": {"interesse": "GNV"},
        "message": {"content": "Bem-vindo!"},
    }


def test_criar_conversa_minima_nao_materializa_campos_ausentes():
    assert ConversationCreate(source_id="cid").to_payload() == {"source_id": "cid"}


@pytest.mark.parametrize("parametros", [
    {"source_id": ""},
    {"source_id": 4},
    {"source_id": "origem", "inbox_id": 0},
    {"source_id": "origem", "contact_id": True},
    {"source_id": "origem", "status": "open"},
    {"source_id": "origem", "status": ConversationStatus.SNOOZED},
    {"source_id": "origem", "message": {"conteudo": "incorreto"}},
    {"source_id": "origem", "additional_attributes": {"n": object()}},
    {"source_id": "origem", "custom_attributes": ["x"]},
    {"source_id": "origem", "snoozed_until": "nao-e-iso"},
])
def test_criacao_rejeita_entrada_invalida(parametros):
    with pytest.raises((ValueError, TypeError)):
        ConversationCreate(**parametros)


def test_prioridade_tipadas_e_none_explicitamente_indicado():
    chamadas = []
    with _client(chamadas) as cw:
        cw.conversations.update(1, 9, priority=ConversationPriority.HIGH)
        cw.conversations.update(1, 9, priority=None)
        cw.conversations.toggle_priority(1, 9, priority=ConversationPriority.LOW)
        cw.conversations.toggle_priority(1, 9)
    assert [r.method for r in chamadas] == ["PATCH", "PATCH", "POST", "POST"]
    assert [json.loads(r.content) for r in chamadas] == [
        {"priority": "high"}, {"priority": None},
        {"priority": "low"}, {"priority": None},
    ]


def test_typing_status_e_corpo_bool():
    chamadas = []
    with _client(chamadas) as cw:
        cw.conversations.set_typing_status(1, 9, typing_status="on", is_private=True)
        cw.conversations.set_typing_status(1, 9, typing_status="off")
    assert [json.loads(r.content) for r in chamadas] == [
        {"typing_status": "on", "is_private": True},
        {"typing_status": "off", "is_private": False},
    ]


def test_atributos_personalizados_preservam_demais_por_padrao():
    chamadas = []
    with _client(chamadas) as cw:
        cw.conversations.update_custom_attributes(
            1, 9, custom_attributes={"interesse": "gnv"}
        )
        cw.conversations.update_custom_attributes(
            1, 9, custom_attributes={"novo": True}, merge=False
        )
        cw.conversations.delete_custom_attributes(1, 9, keys=["interesse", "novo"])
    assert [json.loads(r.content) for r in chamadas] == [
        {"custom_attributes": {"interesse": "gnv"}, "merge": True},
        {"custom_attributes": {"novo": True}, "merge": False},
        {"custom_attributes": ["interesse", "novo"]},
    ]


def test_filtro_compartilhado_mesmo_json_para_contacts_e_conversations():
    filtro = FilterCondition(
        attribute_key="name", filter_operator="contains",
        values=["Maria"], query_operator="AND", timezone="America/Sao_Paulo",
    )
    assert filtro.values == ("Maria",)
    with pytest.raises(FrozenInstanceError):
        filtro.attribute_key = "email"
    chamadas = []
    with _client(chamadas) as cw:
        contato = cw.contacts.filter(1, [filtro], page=2)
        conversa = cw.conversations.filter(1, [filtro], page=2, sort_by="created_at_desc")
    assert contato == conversa == {"ok": True, "extra": {"campo": [1]}}
    assert [r.method for r in chamadas] == ["POST", "POST"]
    assert [dict(r.url.params) for r in chamadas] == [
        {"page": "2"},
        {"page": "2", "sort_by": "created_at_desc"},
    ]
    esperado = {"payload": [{
        "attribute_key": "name", "filter_operator": "contains",
        "values": ["Maria"], "query_operator": "AND", "timezone": "America/Sao_Paulo",
    }]}
    assert [json.loads(r.content) for r in chamadas] == [esperado, esperado]


@pytest.mark.parametrize("parametros", [
    {"attribute_key": "", "filter_operator": "equal_to", "values": ["x"]},
    {"attribute_key": "name", "filter_operator": "", "values": ["x"]},
    {"attribute_key": "name", "filter_operator": "contains", "values": "x"},
    {"attribute_key": "name", "filter_operator": "contains", "values": [42]},
    {"attribute_key": "name", "filter_operator": "contains", "values": ["x"], "query_operator": "XOR"},
])
def test_filtro_structuralmente_invalido(parametros):
    with pytest.raises((ValueError, TypeError)):
        FilterCondition(**parametros)


@pytest.mark.parametrize("acao", [
    lambda cw: cw.conversations.create(1, {"source_id": "x"}),
    lambda cw: cw.conversations.update(1, 9, priority="high"),
    lambda cw: cw.conversations.toggle_priority(1, 9, priority="low"),
    lambda cw: cw.conversations.set_typing_status(1, 9, typing_status="writing"),
    lambda cw: cw.conversations.set_typing_status(1, 9, typing_status="on", is_private=1),
    lambda cw: cw.conversations.filter(1, [{"attribute_key": "name"}]),
    lambda cw: cw.conversations.filter(1, []),
    lambda cw: cw.contacts.filter(1, [{"attribute_key": "name"}]),
    lambda cw: cw.conversations.update_custom_attributes(1, 9, custom_attributes={"i": object()}),
    lambda cw: cw.conversations.update_custom_attributes(1, 9, custom_attributes={}, merge="true"),
    lambda cw: cw.conversations.delete_custom_attributes(1, 9, keys=[]),
    lambda cw: cw.conversations.list(1, status="desconhecido"),
    lambda cw: cw.conversations.meta(1, labels=[""]),
    lambda cw: cw.conversations.list(1, assignee_type="desconhecido"),
    lambda cw: cw.conversations.filter(1, [FilterCondition(
        attribute_key="name", filter_operator="contains", values=["m"]
    )], sort_by="incorreto"),
])
def test_entrada_invalida_impede_http(acao):
    chamadas = []
    with _client(chamadas) as cw, pytest.raises((ValueError, TypeError)):
        acao(cw)
    assert not chamadas


def test_get_list_meta_filter_preservam_envelopes_diferentes():
    chamadas = []
    def responder(req: httpx.Request) -> httpx.Response:
        sufixo = req.url.path
        if sufixo.endswith("/meta"):
            return httpx.Response(200, json={"meta": {"all_count": 8}})
        if sufixo.endswith("/filter"):
            return httpx.Response(200, json={"meta": {"all_count": 8}, "payload": []})
        if sufixo.endswith("/conversations"):
            return httpx.Response(200, json={"data": {"meta": {"all_count": 8}, "payload": []}})
        return httpx.Response(200, json={"id": 9, "status": "open", "extra": 123})

    filtro = FilterCondition(attribute_key="status", filter_operator="equal_to", values=["pending"])
    with _client(chamadas, handler=responder) as cw:
        assert cw.conversations.list(1) == {"data": {"meta": {"all_count": 8}, "payload": []}}
        assert cw.conversations.meta(1) == {"meta": {"all_count": 8}}
        assert cw.conversations.filter(1, [filtro]) == {"meta": {"all_count": 8}, "payload": []}
        assert cw.conversations.get(1, 9) == {"id": 9, "status": "open", "extra": 123}


def test_operacoes_head_sem_corpo_retorna_none():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(200, content=b"")) as cw:
        assert cw.conversations.toggle_priority(1, 2) is None
        assert cw.conversations.set_typing_status(1, 2, typing_status="on") is None


def test_erro_http_nao_expõe_corpo_e_nao_reenvia():
    chamadas = []
    with _client(chamadas, handler=lambda req: httpx.Response(422, json={"secret": "sigilo"})) as cw:
        with pytest.raises(ErroAPIChatwoot) as e:
            cw.conversations.update(1, 9, priority=ConversationPriority.HIGH)
    assert e.value.status_http == 422
    assert "sigilo" not in str(e.value)
    assert len(chamadas) == 1
