# Matriz da Application API Chatwoot 4.19.0

Referência oficial: https://github.com/chatwoot/chatwoot/blob/v4.19.0/swagger/tag_groups/application_swagger.json

Cada linha corresponde a verbo e caminho HTTP, vinculados ao método Python. A matriz cataloga 124 operações em 75 caminhos. Interfaces redundantes de operações tipadas foram removidas durante a homologação; a matriz descreve verbos e caminhos, não contratos legados. A existência de um método não substitui teste contra instalação real.

| Categoria | Verbo | Caminho oficial | Método do cliente | Origem | Entrada (atual) | Revisão contratual | Homologação real |
|---|---|---|---|---|---|---|---|
| Account | GET | `/api/v1/accounts/{account_id}` | `cw.account.get()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Account | PATCH | `/api/v1/accounts/{account_id}` | `cw.account.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Audit Logs | GET | `/api/v1/accounts/{account_id}/audit_logs` | `cw.audit_logs.list()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Account AgentBots | GET | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Account AgentBots | POST | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Account AgentBots | GET | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Account AgentBots | PATCH | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Account AgentBots | DELETE | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Agents | GET | `/api/v1/accounts/{account_id}/agents` | `cw.agents.list()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Agents | POST | `/api/v1/accounts/{account_id}/agents` | `cw.agents.create()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Agents | PATCH | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.update()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Agents | DELETE | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Canned Responses | GET | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Canned Responses | POST | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.create()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Canned Responses | PATCH | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.update()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Canned Responses | DELETE | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Custom Attributes | GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.list()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Custom Attributes | POST | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Custom Attributes | GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Custom Attributes | PATCH | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Custom Attributes | DELETE | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.create()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.get()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | PUT | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.update()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Contacts | DELETE | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}/conversations` | `cw.contacts.list_conversations()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contact Labels | GET | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contact Labels | POST | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.replace()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/search` | `cw.contacts.search()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts/filter` | `cw.contacts.filter()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes` | `cw.contacts.add_inbox()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes` | `cw.contacts.list_contactable_inboxes()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Contacts | POST | `/api/v1/accounts/{account_id}/actions/contact_merge` | `cw.contacts.merge()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Automation Rule | GET | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Automation Rule | POST | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Automation Rule | GET | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Automation Rule | PATCH | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Automation Rule | DELETE | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | GET | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | GET | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | PATCH | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals/{id}/categories` | `cw.help_center.create_category()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals/{id}/articles` | `cw.help_center.create_article()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/meta` | `cw.conversations.meta()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.list()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.create()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/filter` | `cw.conversations.filter()` | Herdado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.get()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.update()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status` | `cw.conversations.set_status()` | Herdado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority` | `cw.conversations.toggle_priority()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status` | `cw.conversations.set_typing_status()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen` | `cw.conversations.update_last_seen()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes` | `cw.conversations.update_custom_attributes()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes` | `cw.conversations.delete_custom_attributes()` | Novo | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversation Assignments | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments` | `cw.conversation_assignments.assign()` | Herdado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.list()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.replace()` | Herdado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events` | `cw.conversations.reporting_events()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.get_branded_email_layout()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.update_branded_email_layout()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.get()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}/message_templates` | `cw.inboxes.list_message_templates()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}/agent_bot` | `cw.inboxes.get_agent_bot()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inboxes/{id}/set_agent_bot` | `cw.inboxes.set_agent_bot()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inbox_members/{inbox_id}` | `cw.inboxes.list_members()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.add_member()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.update_members()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Inboxes | DELETE | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.remove_members()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Labels | GET | `/api/v1/accounts/{account_id}/labels` | `cw.labels.list()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Labels | POST | `/api/v1/accounts/{account_id}/labels` | `cw.labels.create(LabelDefinition)` | Tipado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Labels | GET | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Labels | PATCH | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Labels | DELETE | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Messages | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.list()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Messages | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.send_text()` / `send_media()` | Tipado | Tipado existente | Interface consolidada; verificar API real | Pendente por rota |
| Messages | PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.update_status()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Messages | DELETE | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Integrations | GET | `/api/v1/accounts/{account_id}/integrations/apps` | `cw.integrations.list_apps()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Integrations | POST | `/api/v1/accounts/{account_id}/integrations/hooks` | `cw.integrations.create_hook()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Integrations | PATCH | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.update_hook()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Integrations | DELETE | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.delete_hook()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Profile | GET | `/api/v1/profile` | `cw.profile.get()` | Herdado | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Profile | PUT | `/api/v1/profile` | `cw.profile.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Teams | GET | `/api/v1/accounts/{account_id}/teams` | `cw.teams.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Teams | POST | `/api/v1/accounts/{account_id}/teams` | `cw.teams.create()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Teams | GET | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Teams | PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.update()` | Novo | Payload da API / parâmetros | Etapa A: validar campos e valores | Pendente por rota |
| Teams | DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Teams | GET | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.list_members()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Teams | POST | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.add_members()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Teams | PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.update_members()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Teams | DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.remove_members()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Custom Filters | GET | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.list()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Custom Filters | POST | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.create()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Custom Filters | GET | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Custom Filters | PATCH | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.update()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Custom Filters | DELETE | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Webhooks | GET | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Webhooks | POST | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.create()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Webhooks | PATCH | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.update()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Webhooks | DELETE | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v1/accounts/{account_id}/reporting_events` | `cw.reports.list_reporting_events()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports` | `cw.reports.list_conversation_statistics()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/summary` | `cw.reports.summary()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/conversations` | `cw.reports.conversation_metrics()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/conversations/` | `cw.reports.agent_conversation_metrics()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/channel` | `cw.reports.channel_summary()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/inbox` | `cw.reports.inbox_summary()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/agent` | `cw.reports.agent_summary()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/team` | `cw.reports.team_summary()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/first_response_time_distribution` | `cw.reports.first_response_time_distribution()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/inbox_label_matrix` | `cw.reports.inbox_label_matrix()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/outgoing_messages_count` | `cw.reports.outgoing_messages_count()` | Novo | Parâmetros tipados | Teste HTTP simulado adicionado | Pendente por rota |
| Campaigns | GET | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.list()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Campaigns | POST | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.create()` | Novo | Payload API com envelope obrigatório | Teste HTTP simulado adicionado | Pendente por rota |
| Campaigns | GET | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.get()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |
| Campaigns | PATCH | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.update()` | Novo | Payload API com envelope obrigatório | Teste HTTP simulado adicionado | Pendente por rota |
| Campaigns | DELETE | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.delete()` | Novo | Parâmetros/IDs | Etapa A: validar campos e valores | Pendente por rota |

Formatos alternativos: `cw.messages.send_media()` (multipart), `cw.profile.update_multipart()` (avatar) e `cw.account.update_form()` (form-urlencoded). Eles não representam novos endpoints além dos já contados.
