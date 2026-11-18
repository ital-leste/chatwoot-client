"""Limite de conteúdo Chatwoot 4.19.0 e cópia íntegra de streams."""
from __future__ import annotations

import httpx
import pytest

from chatwoot_client import Attachment, CWClient, ErroAnexoChatwoot, MediaMessage, MimeType, TextMessage


@pytest.mark.parametrize("fabrica", [
    lambda texto: TextMessage(texto),
    lambda texto: MediaMessage(
        attachments=[Attachment(b"pdf", MimeType.PDF, "arquivo.pdf")], caption=texto,
    ),
])
def test_limite_de_conteudo_por_caracteres(fabrica):
    valido = fabrica("á" * 150_000)
    assert valido is not None
    with pytest.raises(ValueError, match="150000"):
        fabrica("á" * 150_001)


class FluxoParcial:
    def __init__(self, partes):
        self.partes = iter(partes)
        self.closed = False

    def read(self, tamanho=-1):
        return next(self.partes)

    def close(self):
        self.closed = True


def _cliente_mock(chamadas):
    cliente = CWClient("https://chatwoot.example", "token-de-teste")
    headers = dict(cliente._http.headers)
    cliente._http.close()

    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"id": 7})

    cliente._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cliente


@pytest.mark.parametrize("partes", [
    [None],
    [b"conteudo-parcial", None],
    [b"conteudo-parcial", "texto"],
])
def test_read_invalido_rejeita_envio_sem_truncar(partes):
    chamadas = []
    fluxo = FluxoParcial(partes)
    with _cliente_mock(chamadas) as cliente:
        with pytest.raises(ErroAnexoChatwoot):
            cliente.messages.send_media(
                1, 2, MediaMessage([Attachment(fluxo, MimeType.PDF, "arquivo.pdf")])
            )
    assert chamadas == []
    assert fluxo.closed is False


def test_read_com_eof_em_bytes_preserva_envio():
    chamadas = []
    fluxo = FluxoParcial([b"parte-um", b"-parte-dois", b""])
    with _cliente_mock(chamadas) as cliente:
        retorno = cliente.messages.send_media(
            1, 2, MediaMessage([Attachment(fluxo, MimeType.PDF, "arquivo.pdf")])
        )
    assert retorno == {"id": 7}
    assert len(chamadas) == 1
    assert b"parte-um-parte-dois" in chamadas[0].content
    assert fluxo.closed is False
