"""Garantias dos contratos Application API: argumentos tipados, omissão e defesa de JSON."""
from __future__ import annotations

import pytest
from chatwoot_client import (
    AccountSettingsInput, AgentBotInput, AutomationRuleInput,
    InboxSettingsInput, CustomAttributeInput, CustomFilterInput,
    HelpCenterPortalInput, HelpCenterCategoryInput, HelpCenterArticleInput,
    IntegrationHookInput,
)


@pytest.mark.parametrize("entrada,payload", [
    (AccountSettingsInput(name="Conta", auto_resolve_ignore_waiting=False),
     {"name": "Conta", "auto_resolve_ignore_waiting": False}),
    (AccountSettingsInput(auto_resolve_after=None),
     {"auto_resolve_after": None}),
    (AgentBotInput(name="Bot", bot_config={"x": 1}),
     {"name": "Bot", "bot_config": {"x": 1}}),
    (AutomationRuleInput(name="Regra", event_name="message_created",
                         actions=[{"action_name": "add_label"}], active=False),
     {"name": "Regra", "event_name": "message_created",
      "actions": [{"action_name": "add_label"}], "active": False}),
    (InboxSettingsInput(name="Inbox", channel={"type": "Channel::Api"},
                        branded_email_layout=None),
     {"name": "Inbox", "channel": {"type": "Channel::Api"},
      "branded_email_layout": None}),
    (CustomAttributeInput(attribute_key="placa", attribute_values=["A","B"]),
     {"attribute_key": "placa", "attribute_values": ["A","B"]}),
    (CustomFilterInput(name="Pendentes", type="conversation", query={"payload": []}),
     {"name": "Pendentes", "type": "conversation", "query": {"payload": []}}),
    (HelpCenterPortalInput(name="Central", slug="central", archived=False),
     {"name": "Central", "slug": "central", "archived": False}),
    (HelpCenterCategoryInput(name="GNV", position=0),
     {"name": "GNV", "position": 0}),
    (HelpCenterArticleInput(title="Guia", content="Texto", meta={}),
     {"title": "Guia", "content": "Texto", "meta": {}}),
    (IntegrationHookInput(app_id=2, inbox_id=5, settings={"enabled": False}),
     {"app_id": 2, "inbox_id": 5, "settings": {"enabled": False}}),
])
def test_campos_omitidos_e_json_nativo(entrada, payload):
    assert entrada.to_payload() == payload
    assert entrada.to_payload() == payload


@pytest.mark.parametrize("fabrica", [
    lambda: AccountSettingsInput(auto_resolve_after=True),
    lambda: AccountSettingsInput(name=None),
    lambda: AgentBotInput(bot_type="local"),
    lambda: AgentBotInput(name=" "),
    lambda: AutomationRuleInput(event_name="evento_inexistente"),
    lambda: AutomationRuleInput(actions={"not": "a-list"}),
    lambda: InboxSettingsInput(greeting_enabled=1),
    lambda: InboxSettingsInput(sender_name_type="invalido"),
    lambda: InboxSettingsInput(channel={"x": object()}),
    lambda: CustomAttributeInput(attribute_model=False),
    lambda: CustomAttributeInput(attribute_values=["a", 2]),
    lambda: CustomFilterInput(type="inbox"),
    lambda: HelpCenterPortalInput(config={"x": float("nan")}),
    lambda: HelpCenterCategoryInput(position="um"),
    lambda: HelpCenterArticleInput(meta={4: "num"}),
    lambda: IntegrationHookInput(settings={"a": object()}),
])
def test_falhas_de_tipo_e_json_antes_do_http(fabrica):
    with pytest.raises(ValueError):
        fabrica()


def test_obrigatoriedade_por_operacao_nao_por_dataclass():
    with pytest.raises(ValueError, match="obrigatórios"):
        AgentBotInput(description="parcial").to_payload(required=["name"])
    assert AgentBotInput(description="parcial").to_payload() == {"description": "parcial"}
    with pytest.raises(ValueError, match="ao menos um campo"):
        InboxSettingsInput().to_payload()


def test_copia_e_revalidacao_de_objetos_aninhados():
    entrada = {"param": {"v": 1}}
    config = AgentBotInput(name="Bot", bot_config=entrada)
    entrada["param"]["v"] = 10
    assert config.to_payload()["bot_config"]["param"]["v"] == 1
    saida = config.to_payload()
    saida["bot_config"]["param"]["v"] = 100
    assert config.to_payload()["bot_config"]["param"]["v"] == 1
    config.bot_config["erro"] = object()
    with pytest.raises(ValueError):
        config.to_payload()
