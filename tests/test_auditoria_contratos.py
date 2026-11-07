"""Regressão de validação dos contratos públicos e da fronteira HTTP.

Testes locais; não chamam uma instalação Chatwoot.
"""
from __future__ import annotations

import json

import httpx
import pytest

from chatwoot_client import (
    CWClient, Contact, ConversationCreate, ErroConfiguracaoChatwoot,
)


def _cliente(chamadas: list[httpx.Request]) -> CWClient:
    def handler(req: httpx.Request) -> httpx.Response:
        chamadas.append(req)
        return httpx.Response(200, json={"payload": {"id": 42}})
    cw = CWClient("https://chatwoot.example", "token-teste")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(handler),
    )
    return cw


@pytest.mark.parametrize("valor", [None, False, 123, b"https://chatwoot.example", ""])
def test_url_com_tipo_ou_valor_invalido_rejeitada_sem_attribute_error(valor):
    with pytest.raises(ErroConfiguracaoChatwoot):
        CWClient(valor, "token")


def test_contato_nao_retem_referencia_para_mapping_de_entrada_e_saida():
    origem = {"servico": {"tipo": "gnv"}}
    contato = Contact(name="Maria", custom_attributes=origem)
    origem["servico"]["tipo"] = "outro"
    assert contato.to_payload()["custom_attributes"] == {"servico": {"tipo": "gnv"}}
    gerado = contato.to_payload()
    gerado["custom_attributes"]["servico"]["tipo"] = "alterado"
    assert contato.to_payload()["custom_attributes"]["servico"]["tipo"] == "gnv"


def test_criacao_conversa_copia_atributos_e_mensagem_aninhados():
    origem = {"pessoa": {"nome": "Maria"}}
    mensagem = {"content": "Olá", "template_params": {"a": [1, 2]}}
    conversa = ConversationCreate(
        source_id="origem", additional_attributes=origem, message=mensagem
    )
    origem["pessoa"]["nome"] = "Outra"
    mensagem["template_params"]["a"][0] = 99
    assert conversa.to_payload()["additional_attributes"]["pessoa"]["nome"] == "Maria"
    assert conversa.to_payload()["message"]["template_params"]["a"] == [1, 2]
    payload = conversa.to_payload()
    payload["message"]["template_params"]["a"].append(3)
    assert conversa.to_payload()["message"]["template_params"]["a"] == [1, 2]


def test_contato_mutado_para_nao_json_falha_antes_do_http():
    contato = Contact(custom_attributes={"status": "novo"})
    contato.custom_attributes["status"] = object()
    chamadas = []
    with _cliente(chamadas) as cw, pytest.raises(ValueError):
        cw.contacts.update(1, 42, contato)
    assert chamadas == []


def test_criacao_conversa_mutada_para_nao_json_falha_antes_do_http():
    conv = ConversationCreate(source_id="x", message={"content": "Oi"})
    conv.message["objeto"] = object()
    chamadas = []
    with _cliente(chamadas) as cw, pytest.raises(ValueError):
        cw.conversations.create(1, conv)
    assert chamadas == []


@pytest.mark.parametrize("cursores", [
    {"before": True},
    {"before": "10"},
    {"before": -1},
    {"after": -9},
    {"after": False},
    {"after": "0"},
])
def test_mensagem_cursores_invalidos_rejeitados_antes_do_http(cursores):
    chamadas = []
    with _cliente(chamadas) as cw, pytest.raises(ValueError):
        cw.messages.list(1, 42, **cursores)
    assert chamadas == []


def test_cursor_zero_mantem_comportamento_existente():
    chamadas = []
    with _cliente(chamadas) as cw:
        cw.messages.list(1, 42, before=20, after=0)
    assert len(chamadas) == 1
    assert chamadas[0].url.params["before"] == "20"
    assert chamadas[0].url.params["after"] == "0"


def test_update_parametrizado_envia_apenas_campos_informados():
    chamadas = []
    with _cliente(chamadas) as cw:
        cw.labels.update(1, 7, description="Atendimento", show_on_sidebar=False)
    assert len(chamadas) == 1
    assert chamadas[0].method == "PATCH"
    assert json.loads(chamadas[0].content) == {
        "description": "Atendimento", "show_on_sidebar": False,
    }


def test_campos_ausentes_em_contact_nao_viram_null():
    chamadas = []
    with _cliente(chamadas) as cw:
        cw.contacts.update(1, 42, Contact(name="Maria"))
    assert json.loads(chamadas[0].content) == {"name": "Maria"}


@pytest.mark.parametrize("dados", [
    {"extra": object()},
    {"extra": float("nan")},
    {1: "chave_nao_textual"},
])
def test_json_generico_invalido_falha_antes_de_http(dados):
    chamadas = []
    with _cliente(chamadas) as cw, pytest.raises(ValueError):
        cw.campaigns.update(1, 7, dados)
    assert chamadas == []


def test_mensagem_mutada_sem_content_valido_falha_antes_de_http():
    conversa = ConversationCreate(source_id="origem", message={"content": "Oi"})
    conversa.message["content"] = ""
    chamadas = []
    with _cliente(chamadas) as cw, pytest.raises(ValueError):
        cw.conversations.create(1, conversa)
    assert chamadas == []
