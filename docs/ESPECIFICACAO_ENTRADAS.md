# Especificação de entrada por rota — Chatwoot Application API v4.19.0

Derivado do Swagger oficial da tag `v4.19.0` e vinculado à matriz do cliente Python. Documenta os campos **declarados obrigatórios no Swagger**, sem inferir restrições de validação específicas dos controladores ou permissões. Operações com `Mapping` continuam seguindo o payload nativo da API. Não constitui homologação real.

Resumo: **124 operações**, 6 operações com ao menos um query param obrigatório e 55 operações com requestBody declarado obrigatório no Swagger. A lista é uma checagem estática; campos de regras de negócio adicionais podem ser exigidos pelo servidor.

| Método HTTP | Caminho | Cliente Python | Query obrigatória | Corpo declarado obrigatório | MIME do corpo |
|---|---|---|---|---|---|
| GET | `/api/v1/accounts/{account_id}` | `cw.account.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}` | `cw.account.update()` | — | Sim: verificar esquema/variante | application/json, application/x-www-form-urlencoded |
| GET | `/api/v1/accounts/{account_id}/audit_logs` | `cw.audit_logs.list()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/agents` | `cw.agents.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/agents` | `cw.agents.create()` | — | Sim: name, email, role | application/json |
| PATCH | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.update()` | — | Sim: role | application/json |
| DELETE | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.create()` | — | Sim: verificar esquema/variante | application/json |
| PATCH | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.list()` | attribute_model (0, 1) | — | — |
| POST | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.create()` | — | Sim: inbox_id | application/json |
| GET | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.get()` | — | — | — |
| PUT | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/contacts/{id}/conversations` | `cw.contacts.list_conversations()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.replace()` | — | Sim: labels | application/json |
| GET | `/api/v1/accounts/{account_id}/contacts/search` | `cw.contacts.search()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/contacts/filter` | `cw.contacts.filter()` | — | Sim: verificar esquema/variante | application/json |
| POST | `/api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes` | `cw.contacts.add_inbox()` | — | Sim: inbox_id | application/json |
| GET | `/api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes` | `cw.contacts.list_contactable_inboxes()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/actions/contact_merge` | `cw.contacts.merge()` | — | Sim: base_contact_id, mergee_contact_id | application/json |
| GET | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.delete()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.list()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.update()` | — | Sim: verificar esquema/variante | application/json |
| POST | `/api/v1/accounts/{account_id}/portals/{id}/categories` | `cw.help_center.create_category()` | — | Sim: verificar esquema/variante | application/json |
| POST | `/api/v1/accounts/{account_id}/portals/{id}/articles` | `cw.help_center.create_article()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/conversations/meta` | `cw.conversations.meta()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.create()` | — | Sim: source_id | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/filter` | `cw.conversations.filter()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.update()` | — | Sim: verificar esquema/variante | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status` | `cw.conversations.set_status()` | — | Sim: status | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority` | `cw.conversations.toggle_priority()` | — | — | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status` | `cw.conversations.set_typing_status()` | — | Sim: typing_status | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen` | `cw.conversations.update_last_seen()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes` | `cw.conversations.update_custom_attributes()` | — | Sim: custom_attributes | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes` | `cw.conversations.delete_custom_attributes()` | — | Sim: custom_attributes | application/json |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments` | `cw.conversation_assignments.assign()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.replace()` | — | Sim: labels | application/json |
| GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events` | `cw.conversations.reporting_events()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.get_branded_email_layout()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.update_branded_email_layout()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.update()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/inboxes/{id}/message_templates` | `cw.inboxes.list_message_templates()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/inboxes/{id}/agent_bot` | `cw.inboxes.get_agent_bot()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/inboxes/{id}/set_agent_bot` | `cw.inboxes.set_agent_bot()` | — | Sim: agent_bot | application/json |
| GET | `/api/v1/accounts/{account_id}/inbox_members/{inbox_id}` | `cw.inboxes.list_members()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.add_member()` | — | Sim: inbox_id, user_ids | application/json |
| PATCH | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.update_members()` | — | Sim: inbox_id, user_ids | application/json |
| DELETE | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.remove_members()` | — | Sim: inbox_id, user_ids | application/json |
| GET | `/api/v1/accounts/{account_id}/labels` | `cw.labels.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/labels` | `cw.labels.create(LabelDefinition)` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.send_text()` / `send_media()` | — | Sim: content | application/json, multipart/form-data |
| PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.update_status()` | — | Sim: status | application/json |
| DELETE | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/integrations/apps` | `cw.integrations.list_apps()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/integrations/hooks` | `cw.integrations.create_hook()` | — | Sim: verificar esquema/variante | application/json |
| PATCH | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.update_hook()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.delete_hook()` | — | — | — |
| GET | `/api/v1/profile` | `cw.profile.get()` | — | — | — |
| PUT | `/api/v1/profile` | `cw.profile.update()` | — | Sim: profile | application/json, multipart/form-data |
| GET | `/api/v1/accounts/{account_id}/teams` | `cw.teams.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/teams` | `cw.teams.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.list_members()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.add_members()` | — | Sim: user_ids | application/json |
| PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.update_members()` | — | Sim: user_ids | application/json |
| DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.remove_members()` | — | Sim: user_ids | application/json |
| GET | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.create()` | — | Sim: verificar esquema/variante | application/json |
| GET | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.create()` | — | Sim: verificar esquema/variante | application/json |
| PATCH | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.update()` | — | Sim: verificar esquema/variante | application/json |
| DELETE | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.delete()` | — | — | — |
| GET | `/api/v1/accounts/{account_id}/reporting_events` | `cw.reports.list_reporting_events()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/reports` | `cw.reports.list_conversation_statistics()` | metric (conversations_count, incoming_messages_count, outgoing_messages_count, avg_first_response_time, avg_resolution_time, resolutions_count), type (account, agent, inbox, label, team) | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/summary` | `cw.reports.summary()` | type (account, agent, inbox, label, team) | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/conversations` | `cw.reports.conversation_metrics()` | type (account) | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/conversations/` | `cw.reports.agent_conversation_metrics()` | type (agent) | — | — |
| GET | `/api/v2/accounts/{account_id}/summary_reports/channel` | `cw.reports.channel_summary()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/summary_reports/inbox` | `cw.reports.inbox_summary()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/summary_reports/agent` | `cw.reports.agent_summary()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/summary_reports/team` | `cw.reports.team_summary()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/first_response_time_distribution` | `cw.reports.first_response_time_distribution()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/inbox_label_matrix` | `cw.reports.inbox_label_matrix()` | — | — | — |
| GET | `/api/v2/accounts/{account_id}/reports/outgoing_messages_count` | `cw.reports.outgoing_messages_count()` | group_by (agent, team, inbox, label) | — | — |
| GET | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.list()` | — | — | — |
| POST | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.create()` | — | Sim: campaign | application/json |
| GET | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.get()` | — | — | — |
| PATCH | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.update()` | — | Sim: campaign | application/json |
| DELETE | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.delete()` | — | — | — |
