"""Validações mínimas de resposta sem alterar o contrato JSON público."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import (
    Attachment,
    CWClient,
    ErroAPIChatwoot,
    MediaMessage,
    MimeType,
    TextMessage,
)


def cliente_simulado(resposta: object, chamadas: list[httpx.Request]) -> CWClient:
    def responder(request: httpx.Request) -> httpx.Response:
        chamadas.append(request)
        return httpx.Response(200, json=resposta)

    cliente = CWClient("https://chatwoot.example", "token-de-teste")
    headers = dict(cliente._http.headers)
    cliente._http.close()
    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/",
        headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cliente


@pytest.mark.parametrize("conteudo", [
    {}, {"error": "erro"}, {"id": None}, {"id": True},
    {"id": "42"}, {"id": 42.0}, {"id": 0}, {"id": -5},
])
@pytest.mark.parametrize("tipo", ["texto", "midia"])
def test_publicacao_sem_id_inteiro_positivo_nao_e_sucesso(conteudo, tipo):
    chamadas: list[httpx.Request] = []
    with cliente_simulado(conteudo, chamadas) as cliente, pytest.raises(ErroAPIChatwoot) as erro:
        if tipo == "texto":
            cliente.messages.send_text(1, 2, TextMessage("Mensagem", private=True))
        else:
            cliente.messages.send_media(
                1, 2,
                MediaMessage((Attachment(b"pdf", MimeType.PDF, "laudo.pdf"),), private=True),
            )
    assert not erro.value.status_http
    assert len(chamadas) == 1  # Nunca há retry de escrita.
    assert "laudo.pdf" not in str(erro.value)
    assert "erro" not in str(erro.value).lower() or conteudo != {"error": "erro"}


@pytest.mark.parametrize("tipo", ["texto", "midia"])
def test_publicacao_valida_preserva_campos_adicionais(tipo):
    resposta = {"id": 42, "extra": {"novo": "preservado"}}
    chamadas: list[httpx.Request] = []
    with cliente_simulado(resposta, chamadas) as cliente:
        if tipo == "texto":
            resultado = cliente.messages.send_text(1, 2, TextMessage("Mensagem", private=False))
        else:
            resultado = cliente.messages.send_media(
                1, 2, MediaMessage((Attachment(b"pdf", MimeType.PDF, "laudo.pdf"),)),
            )
    assert resultado == resposta
    assert len(chamadas) == 1


@pytest.mark.parametrize("conteudo", [
    {}, {"error": "erro"}, {"payload": None}, {"payload": {}},
    {"payload": "oops"}, {"payload": [None]}, {"payload": [5]},
    {"payload": [{}]}, {"payload": [{"id": "42"}]},
    {"payload": [{"id": False}]}, {"payload": [{"id": 0}]},
])
def test_listagem_rejeita_payload_ou_identidade_invalidos(conteudo):
    chamadas: list[httpx.Request] = []
    with cliente_simulado(conteudo, chamadas) as cliente, pytest.raises(ErroAPIChatwoot):
        cliente.messages.list(1, 2)
    assert len(chamadas) == 1


@pytest.mark.parametrize("payload", [
    [], [{"id": 42}], [{"id": 42, "new_field": {"x": 1}}, {"id": 43}],
])
def test_listagem_preserva_json_nativo_com_payload_valido(payload):
    resposta = {"meta": {"novo": True}, "payload": payload, "extra": "valor"}
    chamadas: list[httpx.Request] = []
    with cliente_simulado(resposta, chamadas) as cliente:
        assert cliente.messages.list(1, 2) == resposta
    assert len(chamadas) == 1
