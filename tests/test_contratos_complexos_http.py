"""HTTP exato dos contratos estruturados (17 POST/PATCH); sem Chatwoot real."""
from __future__ import annotations

import json
import httpx
import pytest
from chatwoot_client import (
    CWClient, AccountSettingsInput, AgentBotInput, AutomationRuleInput,
    InboxSettingsInput, CustomAttributeInput, CustomFilterInput,
    HelpCenterPortalInput, HelpCenterCategoryInput, HelpCenterArticleInput,
    IntegrationHookInput,
)


def cliente_mock(chamadas):
    def responder(req):
        chamadas.append(req)
        return httpx.Response(200, json={"ok": True})
    c = CWClient("https://chatwoot.example", "token-ficticio")
    headers = dict(c._http.headers)
    c._http.close()
    c._http = httpx.Client(
        base_url="https://chatwoot.example/", headers=headers,
        transport=httpx.MockTransport(responder),
    )
    return c


@pytest.mark.parametrize("chamada,verbo,caminho,corpo", [
    (lambda c: c.account.update(1, AccountSettingsInput(name="Conta", auto_resolve_after=None)),
     "PATCH", "/api/v1/accounts/1", {"name":"Conta","auto_resolve_after":None}),
    (lambda c: c.account_agentbots.create(1, AgentBotInput(name="Bot", outgoing_url="https://example.org/bot")),
     "POST", "/api/v1/accounts/1/agent_bots", {"name":"Bot","outgoing_url":"https://example.org/bot"}),
    (lambda c: c.account_agentbots.update(1, 2, AgentBotInput(bot_config={"x":1})),
     "PATCH", "/api/v1/accounts/1/agent_bots/2", {"bot_config":{"x":1}}),
    (lambda c: c.automation_rules.create(1, AutomationRuleInput(name="Regra", event_name="message_created",
                                actions=[{"action_name":"add_label"}], conditions=[], active=False)),
     "POST", "/api/v1/accounts/1/automation_rules",
     {"name":"Regra","event_name":"message_created","actions":[{"action_name":"add_label"}],"conditions":[],"active":False}),
    (lambda c: c.automation_rules.update(1, 3, AutomationRuleInput(active=False)),
     "PATCH", "/api/v1/accounts/1/automation_rules/3", {"active":False}),
    (lambda c: c.inboxes.create(1, InboxSettingsInput(name="API", channel={"type":"Channel::Api"}, enable_auto_assignment=False)),
     "POST", "/api/v1/accounts/1/inboxes", {"name":"API","channel":{"type":"Channel::Api"},"enable_auto_assignment":False}),
    (lambda c: c.inboxes.update(1, 4, InboxSettingsInput(name="Renomeada", branded_email_layout=None)),
     "PATCH", "/api/v1/accounts/1/inboxes/4", {"name":"Renomeada","branded_email_layout":None}),
    (lambda c: c.custom_attributes.create(1, CustomAttributeInput(attribute_key="placa", attribute_model=0)),
     "POST", "/api/v1/accounts/1/custom_attribute_definitions", {"attribute_key":"placa","attribute_model":0}),
    (lambda c: c.custom_attributes.update(1, 5, CustomAttributeInput(attribute_display_name="Placa")),
     "PATCH", "/api/v1/accounts/1/custom_attribute_definitions/5", {"attribute_display_name":"Placa"}),
    (lambda c: c.custom_filters.create(1, CustomFilterInput(name="Filtro", type="conversation", query={"payload":[]}), filter_type="conversation"),
     "POST", "/api/v1/accounts/1/custom_filters", {"name":"Filtro","type":"conversation","query":{"payload":[]}}),
    (lambda c: c.custom_filters.update(1, 6, CustomFilterInput(query={"payload":[]})),
     "PATCH", "/api/v1/accounts/1/custom_filters/6", {"query":{"payload":[]}}),
    (lambda c: c.help_center.create(1, HelpCenterPortalInput(name="Central", slug="central", archived=False)),
     "POST", "/api/v1/accounts/1/portals", {"name":"Central","slug":"central","archived":False}),
    (lambda c: c.help_center.update(1, "portal", HelpCenterPortalInput(page_title="Principal")),
     "PATCH", "/api/v1/accounts/1/portals/portal", {"page_title":"Principal"}),
    (lambda c: c.help_center.create_category(1, "portal", HelpCenterCategoryInput(name="GNV")),
     "POST", "/api/v1/accounts/1/portals/portal/categories", {"name":"GNV"}),
    (lambda c: c.help_center.create_article(1, "portal", HelpCenterArticleInput(title="Guia", content="Texto", category_id=2)),
     "POST", "/api/v1/accounts/1/portals/portal/articles", {"title":"Guia","content":"Texto","category_id":2}),
    (lambda c: c.integrations.create_hook(1, IntegrationHookInput(app_id=2, inbox_id=3, settings={"k":"v"})),
     "POST", "/api/v1/accounts/1/integrations/hooks", {"app_id":2,"inbox_id":3,"settings":{"k":"v"}}),
    (lambda c: c.integrations.update_hook(1, 7, IntegrationHookInput(status=1)),
     "PATCH", "/api/v1/accounts/1/integrations/hooks/7", {"status":1}),
])
def test_contrato_com_verbo_caminho_e_json(chamada, verbo, caminho, corpo):
    chamadas=[]
    with cliente_mock(chamadas) as c:
        assert chamada(c)=={"ok":True}
    assert len(chamadas)==1
    request=chamadas[0]
    assert request.method==verbo
    assert request.url.path==caminho
    assert request.headers["content-type"].startswith("application/json")
    assert json.loads(request.content)==corpo


@pytest.mark.parametrize("chamada", [
    lambda c: c.account.update(1, AccountSettingsInput()),
    lambda c: c.account_agentbots.create(1, AgentBotInput(description="sem nome")),
    lambda c: c.automation_rules.create(1, AutomationRuleInput(name="sem event_name")),
    lambda c: c.inboxes.create(1, InboxSettingsInput(name="sem channel")),
    lambda c: c.custom_attributes.create(1, CustomAttributeInput(attribute_display_name="sem key")),
    lambda c: c.custom_filters.create(1, CustomFilterInput(name="sem tipo")),
    lambda c: c.help_center.create(1, HelpCenterPortalInput(name="sem slug")),
    lambda c: c.help_center.create_article(1, "portal", HelpCenterArticleInput(title="sem content")),
    lambda c: c.integrations.create_hook(1, IntegrationHookInput(app_id=2)),
    lambda c: c.automation_rules.update(1, 2, AutomationRuleInput()),
    lambda c: c.help_center.update(1, "portal", HelpCenterPortalInput()),
])
def test_validacao_invalida_antes_de_http(chamada):
    chamadas=[]
    with cliente_mock(chamadas) as c, pytest.raises((ValueError,TypeError)):
        chamada(c)
    assert chamadas==[]
