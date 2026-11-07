"""Campos de conteúdo e template no envio de mensagens (Swagger 4.19.0)."""
from __future__ import annotations
import json

import httpx
import pytest
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment, MimeType, MessageContentType,
)


def cliente_mock(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"id": 5})
    c = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(c._http.headers)
    c._http.close()
    c._http = httpx.Client(base_url="https://chatwoot.example/",
                          headers=headers, transport=httpx.MockTransport(responder))
    return c


def test_json_com_content_type_attributes_campaign_e_template():
    chamadas=[]
    entrada={"items":[{"title":"Documento"}]}
    msg=TextMessage(
        "Documentos", content_type=MessageContentType.CARDS,
        content_attributes=entrada, campaign_id=4, template_params={"name":"Maria"},
    )
    entrada["items"][0]["title"]="Alterado externamente"
    with cliente_mock(chamadas) as c:
        assert c.messages.send_text(1, 2, msg)=={"id":5}
    assert json.loads(chamadas[0].content)=={
        "content":"Documentos","message_type":"outgoing","private":False,
        "content_type":"cards",
        "content_attributes":{"items":[{"title":"Documento"}]},
        "campaign_id":4,"template_params":{"name":"Maria"},
    }


def test_multipart_com_content_type_e_attributes_escalares():
    chamadas=[]
    media=MediaMessage(
        attachments=[Attachment(b"%PDF-1.4", MimeType.PDF, "arquivo.pdf")],
        caption="Arquivo", content_type=MessageContentType.TEXT,
        content_attributes={"idioma":"pt-BR","ativo":True},
    )
    with cliente_mock(chamadas) as c:
        assert c.messages.send_media(1, 2, media)=={"id":5}
    corpo=chamadas[0].content.decode("utf-8",errors="replace")
    assert 'name="content_type"' in corpo
    assert 'name="content_attributes[idioma]"' in corpo
    assert 'name="content_attributes[ativo]"' in corpo


@pytest.mark.parametrize("fabrica", [
    lambda: TextMessage("ok", content_type="cards"),
    lambda: TextMessage("ok", campaign_id=True),
    lambda: TextMessage("ok", campaign_id=0),
    lambda: TextMessage("ok", content_attributes={1:"valor"}),
    lambda: TextMessage("ok", template_params={"x":object()}),
    lambda: MediaMessage(attachments=[Attachment(b"x",MimeType.PDF,"x.pdf")],
                         content_type="text"),
])
def test_invalidos_impedidos_no_contrato(fabrica):
    with pytest.raises((TypeError,ValueError)):
        fabrica()


def test_mutacao_aninhada_rejeitada_pre_http():
    msg=TextMessage("ok", content_attributes={"x":"ok"})
    msg.content_attributes["x"]=object()
    chamadas=[]
    with cliente_mock(chamadas) as c, pytest.raises(ValueError):
        c.messages.send_text(1,2,msg)
    assert chamadas==[]


def test_multipart_nao_converte_subobjeto_em_string_indefinida():
    media=MediaMessage(
        attachments=[Attachment(b"x",MimeType.PDF,"x.pdf")],
        content_attributes={"nested":{"key":"value"}},
    )
    chamadas=[]
    with cliente_mock(chamadas) as c, pytest.raises(ValueError):
        c.messages.send_media(1,2,media)
    assert chamadas==[]
