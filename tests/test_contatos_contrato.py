"""Validação de contratos Contact sem acesso externo."""
import json
import httpx
import pytest

from chatwoot_client import CWClient, Contact


def cliente(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"payload": {"id": 42, "name": "Maria"}})
    cw = CWClient("https://chatwoot.example", "test-token")
    headers = dict(cw._http.headers)
    cw._http.close()
    cw._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return cw


def test_update_nome_poupa_email_telefone_e_demais_campos():
    chamadas = []
    with cliente(chamadas) as cw:
        result = cw.contacts.update(1, 42, Contact(name="Novo nome"))
    assert result == {"payload": {"id": 42, "name": "Maria"}}
    assert len(chamadas) == 1
    assert chamadas[0].method == "PUT"
    assert json.loads(chamadas[0].content) == {"name": "Novo nome"}


def test_none_explicitamente_informado_nao_e_omitido():
    chamadas = []
    with cliente(chamadas) as cw:
        cw.contacts.update(1, 42, Contact(email=None, blocked=False))
    assert json.loads(chamadas[0].content) == {"email": None, "blocked": False}


def test_create_com_inbox_e_atributos_json():
    chamadas = []
    with cliente(chamadas) as cw:
        cw.contacts.create(1, Contact(
            name="Novo contato", phone_number="+5511999999999",
            custom_attributes={"interesse": "gnv"},
        ), inbox_id=2, source_id="origem")
    assert json.loads(chamadas[0].content) == {
        "name": "Novo contato", "phone_number": "+5511999999999",
        "custom_attributes": {"interesse": "gnv"}, "inbox_id": 2, "source_id": "origem",
    }


@pytest.mark.parametrize("valores", [
    {"email": "email_invalido"},
    {"phone_number": "11999999999"},
    {"name": "x" * 256},
    {"blocked": None},
    {"custom_attributes": ["nao_e_objeto"]},
])
def test_rejeita_campos_invalidos(valores):
    with pytest.raises(ValueError):
        Contact(**valores)


def test_update_vazio_e_dicionarios_antigos_bloqueados_sem_http():
    chamadas = []
    with cliente(chamadas) as cw:
        with pytest.raises(ValueError):
            cw.contacts.update(1, 42, Contact())
        with pytest.raises(TypeError):
            cw.contacts.update(1, 42, {"name": "Maria"})
        with pytest.raises(TypeError):
            cw.contacts.create(1, {"name": "Maria"})
    assert chamadas == []


def test_update_somente_custom_attributes_nao_envia_campos_omissos():
    chamadas = []
    with cliente(chamadas) as cw:
        cw.contacts.update(1, 42, Contact(custom_attributes={"cidade": "SP"}))
    assert json.loads(chamadas[0].content) == {"custom_attributes": {"cidade": "SP"}}
