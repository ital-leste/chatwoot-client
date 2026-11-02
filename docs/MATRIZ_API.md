# Matriz oficial de operações — Chatwoot 4.19.0

Referência congelada: https://github.com/chatwoot/chatwoot/blob/v4.19.0/swagger/tag_groups/application_swagger.json

O documento registra 124 operações de 75 caminhos HTTP, distribuídas por 22 categorias da Application API. A implementação preserva 16 operações originais e adiciona 108. Implementação de método não equivale a homologação real do endpoint no servidor.

| Categoria | Verbo HTTP | Caminho | Operation ID |
|---|---|---|---|
| Account | GET | /api/v1/accounts/{account_id} | get-account-details |
| Account | PATCH | /api/v1/accounts/{account_id} | update-account |
| Audit Logs | GET | /api/v1/accounts/{account_id}/audit_logs | get-account-audit-logs |
| Account AgentBots | GET | /api/v1/accounts/{account_id}/agent_bots | list-all-account-agent-bots |
| Account AgentBots | POST | /api/v1/accounts/{account_id}/agent_bots | create-an-account-agent-bot |
| Account AgentBots | GET | /api/v1/accounts/{account_id}/agent_bots/{id} | get-details-of-a-single-account-agent-bot |
| Account AgentBots | PATCH | /api/v1/accounts/{account_id}/agent_bots/{id} | update-an-account-agent-bot |
| Account AgentBots | DELETE | /api/v1/accounts/{account_id}/agent_bots/{id} | delete-an-account-agent-bot |
| Agents | GET | /api/v1/accounts/{account_id}/agents | get-account-agents |
| Agents | POST | /api/v1/accounts/{account_id}/agents | add-new-agent-to-account |
| Agents | PATCH | /api/v1/accounts/{account_id}/agents/{id} | update-agent-in-account |
| Agents | DELETE | /api/v1/accounts/{account_id}/agents/{id} | delete-agent-from-account |
| Canned Responses | GET | /api/v1/accounts/{account_id}/canned_responses | get-account-canned-response |
| Canned Responses | POST | /api/v1/accounts/{account_id}/canned_responses | add-new-canned-response-to-account |
| Canned Responses | PATCH | /api/v1/accounts/{account_id}/canned_responses/{id} | update-canned-response-in-account |
| Canned Responses | DELETE | /api/v1/accounts/{account_id}/canned_responses/{id} | delete-canned-response-from-account |
| Custom Attributes | GET | /api/v1/accounts/{account_id}/custom_attribute_definitions | get-account-custom-attribute |
| Custom Attributes | POST | /api/v1/accounts/{account_id}/custom_attribute_definitions | add-new-custom-attribute-to-account |
| Custom Attributes | GET | /api/v1/accounts/{account_id}/custom_attribute_definitions/{id} | get-details-of-a-single-custom-attribute |
| Custom Attributes | PATCH | /api/v1/accounts/{account_id}/custom_attribute_definitions/{id} | update-custom-attribute-in-account |
| Custom Attributes | DELETE | /api/v1/accounts/{account_id}/custom_attribute_definitions/{id} | delete-custom-attribute-from-account |
| Contacts | GET | /api/v1/accounts/{account_id}/contacts | contactList |
| Contacts | POST | /api/v1/accounts/{account_id}/contacts | contactCreate |
| Contacts | GET | /api/v1/accounts/{account_id}/contacts/{id} | contactDetails |
| Contacts | PUT | /api/v1/accounts/{account_id}/contacts/{id} | contactUpdate |
| Contacts | DELETE | /api/v1/accounts/{account_id}/contacts/{id} | contactDelete |
| Contacts | GET | /api/v1/accounts/{account_id}/contacts/{id}/conversations | contactConversations |
| Contact Labels | GET | /api/v1/accounts/{account_id}/contacts/{id}/labels | list-all-labels-of-a-contact |
| Contact Labels | POST | /api/v1/accounts/{account_id}/contacts/{id}/labels | contact-add-labels |
| Contacts | GET | /api/v1/accounts/{account_id}/contacts/search | contactSearch |
| Contacts | POST | /api/v1/accounts/{account_id}/contacts/filter | contactFilter |
| Contacts | POST | /api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes | contactInboxCreation |
| Contacts | GET | /api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes | contactableInboxesGet |
| Contacts | POST | /api/v1/accounts/{account_id}/actions/contact_merge | contactMerge |
| Automation Rule | GET | /api/v1/accounts/{account_id}/automation_rules | get-account-automation-rule |
| Automation Rule | POST | /api/v1/accounts/{account_id}/automation_rules | add-new-automation-rule-to-account |
| Automation Rule | GET | /api/v1/accounts/{account_id}/automation_rules/{id} | get-details-of-a-single-automation-rule |
| Automation Rule | PATCH | /api/v1/accounts/{account_id}/automation_rules/{id} | update-automation-rule-in-account |
| Automation Rule | DELETE | /api/v1/accounts/{account_id}/automation_rules/{id} | delete-automation-rule-from-account |
| Help Center | POST | /api/v1/accounts/{account_id}/portals | add-new-portal-to-account |
| Help Center | GET | /api/v1/accounts/{account_id}/portals | get-portal |
| Help Center | GET | /api/v1/accounts/{account_id}/portals/{id} | get-details-of-a-single-portal |
| Help Center | PATCH | /api/v1/accounts/{account_id}/portals/{id} | update-portal-to-account |
| Help Center | POST | /api/v1/accounts/{account_id}/portals/{id}/categories | add-new-category-to-account |
| Help Center | POST | /api/v1/accounts/{account_id}/portals/{id}/articles | add-new-article-to-account |
| Conversations | GET | /api/v1/accounts/{account_id}/conversations/meta | conversationListMeta |
| Conversations | GET | /api/v1/accounts/{account_id}/conversations | conversationList |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations | newConversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/filter | conversationFilter |
| Conversations | GET | /api/v1/accounts/{account_id}/conversations/{conversation_id} | get-details-of-a-conversation |
| Conversations | PATCH | /api/v1/accounts/{account_id}/conversations/{conversation_id} | update-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status | toggle-status-of-a-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority | toggle-priority-of-a-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status | toggle-typing-status-of-a-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen | conversationUpdateLastSeen |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes | update-custom-attributes-of-a-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes | destroy-custom-attributes-of-a-conversation |
| Conversation Assignments | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments | assign-a-conversation |
| Conversations | GET | /api/v1/accounts/{account_id}/conversations/{conversation_id}/labels | list-all-labels-of-a-conversation |
| Conversations | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/labels | conversation-add-labels |
| Conversations | GET | /api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events | get-conversation-reporting-events |
| Inboxes | GET | /api/v1/accounts/{account_id}/branded_email_layout | getAccountBrandedEmailLayout |
| Inboxes | PATCH | /api/v1/accounts/{account_id}/branded_email_layout | updateAccountBrandedEmailLayout |
| Inboxes | GET | /api/v1/accounts/{account_id}/inboxes | listAllInboxes |
| Inboxes | POST | /api/v1/accounts/{account_id}/inboxes | inboxCreation |
| Inboxes | GET | /api/v1/accounts/{account_id}/inboxes/{id} | GetInbox |
| Inboxes | PATCH | /api/v1/accounts/{account_id}/inboxes/{id} | updateInbox |
| Inboxes | GET | /api/v1/accounts/{account_id}/inboxes/{id}/message_templates | listWhatsappMessageTemplates |
| Inboxes | GET | /api/v1/accounts/{account_id}/inboxes/{id}/agent_bot | getInboxAgentBot |
| Inboxes | POST | /api/v1/accounts/{account_id}/inboxes/{id}/set_agent_bot | updateAgentBot |
| Inboxes | GET | /api/v1/accounts/{account_id}/inbox_members/{inbox_id} | get-inbox-members |
| Inboxes | POST | /api/v1/accounts/{account_id}/inbox_members | add-new-agent-to-inbox |
| Inboxes | PATCH | /api/v1/accounts/{account_id}/inbox_members | update-agents-in-inbox |
| Inboxes | DELETE | /api/v1/accounts/{account_id}/inbox_members | delete-agent-in-inbox |
| Labels | GET | /api/v1/accounts/{account_id}/labels | list-all-labels |
| Labels | POST | /api/v1/accounts/{account_id}/labels | create-a-label |
| Labels | GET | /api/v1/accounts/{account_id}/labels/{id} | get-details-of-a-single-label |
| Labels | PATCH | /api/v1/accounts/{account_id}/labels/{id} | update-a-label |
| Labels | DELETE | /api/v1/accounts/{account_id}/labels/{id} | delete-a-label |
| Messages | GET | /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages | list-all-messages |
| Messages | POST | /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages | create-a-new-message-in-a-conversation |
| Messages | PATCH | /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id} | update-message-status |
| Messages | DELETE | /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id} | delete-a-message |
| Integrations | GET | /api/v1/accounts/{account_id}/integrations/apps | get-details-of-all-integrations |
| Integrations | POST | /api/v1/accounts/{account_id}/integrations/hooks | create-an-integration-hook |
| Integrations | PATCH | /api/v1/accounts/{account_id}/integrations/hooks/{hook_id} | update-an-integrations-hook |
| Integrations | DELETE | /api/v1/accounts/{account_id}/integrations/hooks/{hook_id} | delete-an-integration-hook |
| Profile | GET | /api/v1/profile | fetchProfile |
| Profile | PUT | /api/v1/profile | updateProfile |
| Teams | GET | /api/v1/accounts/{account_id}/teams | list-all-teams |
| Teams | POST | /api/v1/accounts/{account_id}/teams | create-a-team |
| Teams | GET | /api/v1/accounts/{account_id}/teams/{team_id} | get-details-of-a-single-team |
| Teams | PATCH | /api/v1/accounts/{account_id}/teams/{team_id} | update-a-team |
| Teams | DELETE | /api/v1/accounts/{account_id}/teams/{team_id} | delete-a-team |
| Teams | GET | /api/v1/accounts/{account_id}/teams/{team_id}/team_members | get-team-members |
| Teams | POST | /api/v1/accounts/{account_id}/teams/{team_id}/team_members | add-new-agent-to-team |
| Teams | PATCH | /api/v1/accounts/{account_id}/teams/{team_id}/team_members | update-agents-in-team |
| Teams | DELETE | /api/v1/accounts/{account_id}/teams/{team_id}/team_members | delete-agent-in-team |
| Custom Filters | GET | /api/v1/accounts/{account_id}/custom_filters | list-all-filters |
| Custom Filters | POST | /api/v1/accounts/{account_id}/custom_filters | create-a-custom-filter |
| Custom Filters | GET | /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id} | get-details-of-a-single-custom-filter |
| Custom Filters | PATCH | /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id} | update-a-custom-filter |
| Custom Filters | DELETE | /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id} | delete-a-custom-filter |
| Webhooks | GET | /api/v1/accounts/{account_id}/webhooks | list-all-webhooks |
| Webhooks | POST | /api/v1/accounts/{account_id}/webhooks | create-a-webhook |
| Webhooks | PATCH | /api/v1/accounts/{account_id}/webhooks/{webhook_id} | update-a-webhook |
| Webhooks | DELETE | /api/v1/accounts/{account_id}/webhooks/{webhook_id} | delete-a-webhook |
| Reports | GET | /api/v1/accounts/{account_id}/reporting_events | get-account-reporting-events |
| Reports | GET | /api/v2/accounts/{account_id}/reports | list-all-conversation-statistics |
| Reports | GET | /api/v2/accounts/{account_id}/reports/summary | list-all-conversation-statistics-summary |
| Reports | GET | /api/v2/accounts/{account_id}/reports/conversations | get-account-conversation-metrics |
| Reports | GET | /api/v2/accounts/{account_id}/reports/conversations/ | get-agent-conversation-metrics |
| Reports | GET | /api/v2/accounts/{account_id}/summary_reports/channel | get-channel-summary-report |
| Reports | GET | /api/v2/accounts/{account_id}/summary_reports/inbox | get-inbox-summary-report |
| Reports | GET | /api/v2/accounts/{account_id}/summary_reports/agent | get-agent-summary-report |
| Reports | GET | /api/v2/accounts/{account_id}/summary_reports/team | get-team-summary-report |
| Reports | GET | /api/v2/accounts/{account_id}/reports/first_response_time_distribution | get-first-response-time-distribution |
| Reports | GET | /api/v2/accounts/{account_id}/reports/inbox_label_matrix | get-inbox-label-matrix |
| Reports | GET | /api/v2/accounts/{account_id}/reports/outgoing_messages_count | get-outgoing-messages-count |
| Campaigns | GET | /api/v1/accounts/{account_id}/campaigns | list-campaigns |
| Campaigns | POST | /api/v1/accounts/{account_id}/campaigns | create-campaign |
| Campaigns | GET | /api/v1/accounts/{account_id}/campaigns/{id} | get-campaign |
| Campaigns | PATCH | /api/v1/accounts/{account_id}/campaigns/{id} | update-campaign |
| Campaigns | DELETE | /api/v1/accounts/{account_id}/campaigns/{id} | delete-campaign |
