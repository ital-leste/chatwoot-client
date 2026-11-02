# Matriz da Application API Chatwoot 4.19.0

Referência oficial: https://github.com/chatwoot/chatwoot/blob/v4.19.0/swagger/tag_groups/application_swagger.json

Cada linha corresponde a verbo e caminho HTTP, vinculados ao método Python. A matriz cataloga 124 operações em 75 caminhos. Os 16 métodos herdados permanecem compatíveis. A existência de um método não substitui teste contra instalação real.

| Categoria | Verbo | Caminho oficial | Método do cliente | Origem |
|---|---|---|---|---|
| Account | GET | `/api/v1/accounts/{account_id}` | `cw.account.get()` | Herdado |
| Account | PATCH | `/api/v1/accounts/{account_id}` | `cw.account.update()` | Novo |
| Audit Logs | GET | `/api/v1/accounts/{account_id}/audit_logs` | `cw.audit_logs.list()` | Novo |
| Account AgentBots | GET | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.list()` | Novo |
| Account AgentBots | POST | `/api/v1/accounts/{account_id}/agent_bots` | `cw.account_agentbots.create()` | Novo |
| Account AgentBots | GET | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.get()` | Novo |
| Account AgentBots | PATCH | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.update()` | Novo |
| Account AgentBots | DELETE | `/api/v1/accounts/{account_id}/agent_bots/{id}` | `cw.account_agentbots.delete()` | Novo |
| Agents | GET | `/api/v1/accounts/{account_id}/agents` | `cw.agents.list()` | Herdado |
| Agents | POST | `/api/v1/accounts/{account_id}/agents` | `cw.agents.create()` | Novo |
| Agents | PATCH | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.update()` | Novo |
| Agents | DELETE | `/api/v1/accounts/{account_id}/agents/{id}` | `cw.agents.delete()` | Novo |
| Canned Responses | GET | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.list()` | Novo |
| Canned Responses | POST | `/api/v1/accounts/{account_id}/canned_responses` | `cw.canned_responses.create()` | Novo |
| Canned Responses | PATCH | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.update()` | Novo |
| Canned Responses | DELETE | `/api/v1/accounts/{account_id}/canned_responses/{id}` | `cw.canned_responses.delete()` | Novo |
| Custom Attributes | GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.list()` | Novo |
| Custom Attributes | POST | `/api/v1/accounts/{account_id}/custom_attribute_definitions` | `cw.custom_attributes.create()` | Novo |
| Custom Attributes | GET | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.get()` | Novo |
| Custom Attributes | PATCH | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.update()` | Novo |
| Custom Attributes | DELETE | `/api/v1/accounts/{account_id}/custom_attribute_definitions/{id}` | `cw.custom_attributes.delete()` | Novo |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.list()` | Novo |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts` | `cw.contacts.create()` | Novo |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.get()` | Herdado |
| Contacts | PUT | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.update()` | Novo |
| Contacts | DELETE | `/api/v1/accounts/{account_id}/contacts/{id}` | `cw.contacts.delete()` | Novo |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}/conversations` | `cw.contacts.list_conversations()` | Novo |
| Contact Labels | GET | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.list()` | Novo |
| Contact Labels | POST | `/api/v1/accounts/{account_id}/contacts/{id}/labels` | `cw.contact_labels.replace()` | Novo |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/search` | `cw.contacts.search()` | Novo |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts/filter` | `cw.contacts.filter()` | Novo |
| Contacts | POST | `/api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes` | `cw.contacts.add_inbox()` | Novo |
| Contacts | GET | `/api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes` | `cw.contacts.list_contactable_inboxes()` | Novo |
| Contacts | POST | `/api/v1/accounts/{account_id}/actions/contact_merge` | `cw.contacts.merge()` | Novo |
| Automation Rule | GET | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.list()` | Novo |
| Automation Rule | POST | `/api/v1/accounts/{account_id}/automation_rules` | `cw.automation_rules.create()` | Novo |
| Automation Rule | GET | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.get()` | Novo |
| Automation Rule | PATCH | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.update()` | Novo |
| Automation Rule | DELETE | `/api/v1/accounts/{account_id}/automation_rules/{id}` | `cw.automation_rules.delete()` | Novo |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.create()` | Novo |
| Help Center | GET | `/api/v1/accounts/{account_id}/portals` | `cw.help_center.list()` | Novo |
| Help Center | GET | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.get()` | Novo |
| Help Center | PATCH | `/api/v1/accounts/{account_id}/portals/{id}` | `cw.help_center.update()` | Novo |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals/{id}/categories` | `cw.help_center.create_category()` | Novo |
| Help Center | POST | `/api/v1/accounts/{account_id}/portals/{id}/articles` | `cw.help_center.create_article()` | Novo |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/meta` | `cw.conversations.meta()` | Novo |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.list()` | Herdado |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations` | `cw.conversations.create()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/filter` | `cw.conversations.filter()` | Herdado |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.get()` | Herdado |
| Conversations | PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}` | `cw.conversations.update()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status` | `cw.conversations.set_status()` | Herdado |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority` | `cw.conversations.toggle_priority()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status` | `cw.conversations.set_typing_status()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen` | `cw.conversations.update_last_seen()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes` | `cw.conversations.update_custom_attributes()` | Novo |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes` | `cw.conversations.delete_custom_attributes()` | Novo |
| Conversation Assignments | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments` | `cw.conversation_assignments.assign()` | Herdado |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.list()` | Herdado |
| Conversations | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels` | `cw.conversation_labels.replace()` | Herdado |
| Conversations | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events` | `cw.conversations.reporting_events()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.get_branded_email_layout()` | Novo |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/branded_email_layout` | `cw.inboxes.update_branded_email_layout()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.list()` | Novo |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inboxes` | `cw.inboxes.create()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.get()` | Herdado |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/inboxes/{id}` | `cw.inboxes.update()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}/message_templates` | `cw.inboxes.list_message_templates()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inboxes/{id}/agent_bot` | `cw.inboxes.get_agent_bot()` | Novo |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inboxes/{id}/set_agent_bot` | `cw.inboxes.set_agent_bot()` | Novo |
| Inboxes | GET | `/api/v1/accounts/{account_id}/inbox_members/{inbox_id}` | `cw.inboxes.list_members()` | Novo |
| Inboxes | POST | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.add_member()` | Novo |
| Inboxes | PATCH | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.update_members()` | Novo |
| Inboxes | DELETE | `/api/v1/accounts/{account_id}/inbox_members` | `cw.inboxes.remove_members()` | Novo |
| Labels | GET | `/api/v1/accounts/{account_id}/labels` | `cw.labels.list()` | Herdado |
| Labels | POST | `/api/v1/accounts/{account_id}/labels` | `cw.labels.create()` | Herdado |
| Labels | GET | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.get()` | Novo |
| Labels | PATCH | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.update()` | Novo |
| Labels | DELETE | `/api/v1/accounts/{account_id}/labels/{id}` | `cw.labels.delete()` | Novo |
| Messages | GET | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.list()` | Herdado |
| Messages | POST | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages` | `cw.messages.create()` | Herdado |
| Messages | PATCH | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.update_status()` | Novo |
| Messages | DELETE | `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}` | `cw.messages.delete()` | Novo |
| Integrations | GET | `/api/v1/accounts/{account_id}/integrations/apps` | `cw.integrations.list_apps()` | Novo |
| Integrations | POST | `/api/v1/accounts/{account_id}/integrations/hooks` | `cw.integrations.create_hook()` | Novo |
| Integrations | PATCH | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.update_hook()` | Novo |
| Integrations | DELETE | `/api/v1/accounts/{account_id}/integrations/hooks/{hook_id}` | `cw.integrations.delete_hook()` | Novo |
| Profile | GET | `/api/v1/profile` | `cw.profile.get()` | Herdado |
| Profile | PUT | `/api/v1/profile` | `cw.profile.update()` | Novo |
| Teams | GET | `/api/v1/accounts/{account_id}/teams` | `cw.teams.list()` | Novo |
| Teams | POST | `/api/v1/accounts/{account_id}/teams` | `cw.teams.create()` | Novo |
| Teams | GET | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.get()` | Novo |
| Teams | PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.update()` | Novo |
| Teams | DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}` | `cw.teams.delete()` | Novo |
| Teams | GET | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.list_members()` | Novo |
| Teams | POST | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.add_members()` | Novo |
| Teams | PATCH | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.update_members()` | Novo |
| Teams | DELETE | `/api/v1/accounts/{account_id}/teams/{team_id}/team_members` | `cw.teams.remove_members()` | Novo |
| Custom Filters | GET | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.list()` | Novo |
| Custom Filters | POST | `/api/v1/accounts/{account_id}/custom_filters` | `cw.custom_filters.create()` | Novo |
| Custom Filters | GET | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.get()` | Novo |
| Custom Filters | PATCH | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.update()` | Novo |
| Custom Filters | DELETE | `/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}` | `cw.custom_filters.delete()` | Novo |
| Webhooks | GET | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.list()` | Novo |
| Webhooks | POST | `/api/v1/accounts/{account_id}/webhooks` | `cw.webhooks.create()` | Novo |
| Webhooks | PATCH | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.update()` | Novo |
| Webhooks | DELETE | `/api/v1/accounts/{account_id}/webhooks/{webhook_id}` | `cw.webhooks.delete()` | Novo |
| Reports | GET | `/api/v1/accounts/{account_id}/reporting_events` | `cw.reports.list_reporting_events()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports` | `cw.reports.list_conversation_statistics()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/summary` | `cw.reports.summary()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/conversations` | `cw.reports.conversation_metrics()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/conversations/` | `cw.reports.agent_conversation_metrics()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/channel` | `cw.reports.channel_summary()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/inbox` | `cw.reports.inbox_summary()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/agent` | `cw.reports.agent_summary()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/summary_reports/team` | `cw.reports.team_summary()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/first_response_time_distribution` | `cw.reports.first_response_time_distribution()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/inbox_label_matrix` | `cw.reports.inbox_label_matrix()` | Novo |
| Reports | GET | `/api/v2/accounts/{account_id}/reports/outgoing_messages_count` | `cw.reports.outgoing_messages_count()` | Novo |
| Campaigns | GET | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.list()` | Novo |
| Campaigns | POST | `/api/v1/accounts/{account_id}/campaigns` | `cw.campaigns.create()` | Novo |
| Campaigns | GET | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.get()` | Novo |
| Campaigns | PATCH | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.update()` | Novo |
| Campaigns | DELETE | `/api/v1/accounts/{account_id}/campaigns/{id}` | `cw.campaigns.delete()` | Novo |

Métodos complementares para formatos alternativos: cw.messages.create_with_attachments() (multipart), cw.profile.update_multipart() (avatar) e cw.account.update_form() (form-urlencoded). Eles representam variações de transporte de operações já contadas, não endpoints novos.
