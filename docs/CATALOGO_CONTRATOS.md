# Catálogo oficial de contratos — Application API 4.19.0

Este documento descreve as **entradas públicas** do cliente Python na branch `homolog`.
O conjunto de rotas é o do Swagger oficial v4.19.0: **124 pares verbo/rota em
75 caminhos**. O cliente não implementa Platform API, Client API ou endpoints internos.

## Regras de interface

- Entradas simples: IDs e argumentos nomeados, com validação de tipos, obrigatoriedade e opções fechadas.
- Entradas estruturadas: dataclasses imutáveis somente de **entrada**; omissão é diferente de `None` explícito. `to_payload()` revalida objetos mutáveis aninhados e rejeita JSON inválido.
- Saída: JSON nativo da API (`dict`, `list` ou `None`), sem DTO obrigatório.
- Operações sem requestBody: IDs e parâmetros de consulta. `parametros` em alguns métodos de consulta é um escape hatch de API, não uma representação de corpo JSON.
- Sem retry implícito em escritas. A autorização do destino cabe ao consumidor; o cliente não transporta regras do ItalBot.
- `tests/test_api_cobertura.py`, testes por recurso e testes de contratos conferem envio HTTP simulado. **Não** equivale a homologação real.

## Modelos administrativos de entrada

| Modelo público | Campos e finalidade | Métodos que o consomem |
|---|---|---|
| `AccountSettingsInput` | Configurações de conta e auto-resolução | `cw.account.update` |
| `AgentBotInput` | Dados, URL e configuração de AgentBot | `cw.account_agentbots.create/update` |
| `AutomationRuleInput` | Evento, condições, ações e ativação de automação | `cw.automation_rules.create/update` |
| `InboxSettingsInput` | Inbox e configuração de canal variável | `cw.inboxes.create/update` |
| `CustomAttributeInput` | Definição e valores de atributo personalizado | `cw.custom_attributes.create/update` |
| `CustomFilterInput` | Nome, tipo e consulta estruturada | `cw.custom_filters.create/update` |
| `HelpCenterPortalInput` | Configuração de portal | `cw.help_center.create/update` |
| `HelpCenterCategoryInput` | Nome e metadados de categoria | `cw.help_center.create_category` |
| `HelpCenterArticleInput` | Título, conteúdo e metadados de artigo | `cw.help_center.create_article` |
| `IntegrationHookInput` | Identificadores e settings de integração | `cw.integrations.create_hook/update_hook` |
| `ProfileInput` | Nome, perfil, configurações e credenciais (sem registrar valores) | `cw.profile.update` |

Os contratos já existentes `Contact`, `ConversationCreate`, `FilterCondition`,
`TextMessage`, `MediaMessage`, `Attachment` e `LabelDefinition` permanecem válidos.

## Parametrização de operações simples

| Recurso | Interface |
|---|---|
| Equipes | `cw.teams.create(..., name=..., allow_auto_assign=...)`; `update(..., name=...)` |
| Etiquetas | `cw.labels.update(..., color=..., show_on_sidebar=...)` |
| Layout de e-mail | `cw.inboxes.update_branded_email_layout(..., branded_email_layout=None)` |
| Associação de bot | `cw.inboxes.set_agent_bot(..., agent_bot=...)` |
| Membros de inbox/equipe | `inbox_id`, `team_id` e `user_ids: Sequence[int]` |
| Contatos | `add_inbox(..., inbox_id=...)`, `merge(..., base_contact_id=..., mergee_contact_id=...)` |
| Conversas | `update(..., priority=..., sla_policy_id=...)`; prioridade `None` explícita é limpeza |
| Mensagens | `update_status(..., status="sent"|"delivered"|"read"|"failed")` |
| Consultas | Ordenação, filtros, páginas e IDs por argumentos tipados |

## Variabilidade intencional da API

Certos campos oficiais dependem do canal, de uma configuração de conta ou da
estrutura interna do Chatwoot e não têm esquema fechado suficiente para submodelos
universais. Os contratos preservam:

- `InboxSettingsInput.channel` como objeto JSON de canal;
- `AgentBotInput.bot_config` como objeto JSON;
- `AutomationRuleInput.actions/conditions` como sequências de objetos JSON;
- `CustomFilterInput.query` e `IntegrationHookInput.settings` como objetos JSON;
- `campaigns.create/update` como objeto da API dentro de `{"campaign": {...}}`;
- `account.update_form` e `profile.update_multipart` como transportes alternativos, com validações próprias.

Isso evita forçar enums ou dataclasses de cada integração de terceiros sem
especificação oficial. Não há endpoint faltando na matriz devido a esses campos
dinâmicos.

## Critérios de aceite para promoção

1. Cobertura estática `124/124` e rastreabilidade de `CWClient` para todos os métodos da matriz.
2. CI Python 3.11 e 3.13 em Linux e Windows aprovado.
3. Comportamentos de corpo, query e falhas cobertos por `httpx.MockTransport`.
4. Impacto das alterações incompatíveis sobre consumidores externos revisado.
5. Homologação real das operações necessárias, controlada e documentada, antes de declarálas integradas.
6. A promoção para `main` é uma decisão separada: esta entrega não a executa.

Fonte de caminhos: [Matriz](MATRIZ_API.md) e
[Especificação de entradas](ESPECIFICACAO_ENTRADAS.md).
