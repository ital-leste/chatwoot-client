# Auditoria contratual — Application API Chatwoot 4.19.0

Data-base: 2026-11-07. Branch de trabalho: `homolog`.

## Etapa A — inventário e rastreabilidade

- Fonte de verdade: `chatwoot/chatwoot@v4.19.0/swagger/tag_groups/application_swagger.json`.
- Matriz Python comparada por pares `(método HTTP, caminho)`.
- Resultado: **124/124 pares**, **75 caminhos**, nenhuma rota ausente nem excedente.
- Este teste comprova apenas cobertura de mapeamento, não todos os campos da requisição ou comportamento do servidor.
- `tests/test_api_cobertura.py` contém 108 casos de transporte HTTP simulados; vários casos originais usam payloads mínimos artificiais. O restante da suíte cobre interfaces tipadas. Portanto **não** classificar 124 operações como homologadas.
- A matriz agora registra modalidade de entrada, necessidade de revisão e homologação real por rota.

## Etapa B — regra para evolução de contratos

1. Métodos sem corpo: IDs e filtros por argumentos nomeados, sem dataclasses artificiais.
2. Escritas com campos simples e obrigatórios: parâmetros nomeados, valores explícitos, validação antes do HTTP.
3. Escritas complexas (inboxes/channel, bots/bot_config, automações/conditions+actions): manter payload nativo inicialmente e criar contratos somente após verificar variantes oficiais, sem estreitar funcionalidades de outros canais.
4. Saídas: preservar `dict | list | None` nativos, metadados, paginação e eventuais campos futuros.
5. Operações com efeitos irreversíveis ou acesso administrativo não terão retry implícito; autorização pertence ao consumidor e à instalação.
6. Preservar a cobertura 124/124 e revisar os testes que hoje passam payloads não representativos.

### Primeiro grupo de entradas simples

- `inboxes.set_agent_bot`: `agent_bot` explícito, incluindo remoção se admitida pelo servidor.
- `inboxes.{add_member,update_members,remove_members}`: `inbox_id` e `user_ids` obrigatórios.
- `teams.{add_members,update_members,remove_members}`: `user_ids` obrigatório.
- `contacts.add_inbox`: `inbox_id` e `source_id` opcional.
- `contacts.merge`: `base_contact_id` e `mergee_contact_id`.
- `contact_labels.replace`: `labels` estruturado, com lista vazia para remover todas.
- `messages.update_status`: `status` e `external_error` opcional.

### Revisões subsequentes

| Área | Diagnóstico | Abordagem |
|---|---|---|
| Agents | Campos obrigatórios em criação/atualização; opções de role/availability | Parâmetros nomeados, `Literal`/enum se úteis |
| Account AgentBots | Configuração de bot varia por tipo | Contrato de entrada após verificar variantes |
| Inboxes create/update | Campo `channel` polimórfico | Payload nativo, sem DTO universal prematuro |
| Webhooks/Integrations | URL, inscrições e hooks | Parâmetros simples ou contrato se configuração crescer |
| Automation Rules | `actions` e `conditions` aninhados | Contrato estruturado após validação de variantes |
| Custom Attributes/Filters | Tipos e filtros parcialmente fechados | Enum/validações locais proporcionais |
| Campaigns | RequestBody envolto em `campaign` | Manter envelope e testar contra a API |
| Reports/Audit Logs | Query enums, datas e paginação | Parâmetros tipados; nenhum DTO de resposta |
| Help Center | Variações de portais, categorias e artigos | Payload da API, revisar campos requeridos |

## Etapa C — critérios de aceite

- `pytest` com `httpx.MockTransport`: método, rota, corpo JSON, campos omitidos, casos inválidos bloqueados, erros HTTP e ausência de retry em escrita.
- CI Linux/Windows, Python 3.11/3.13: todas as matrizes aprovadas.
- Integração real **separada**: registrar versão/edição, conta de teste, permissões e resultado por rota; leituras antes de escritas; autorização explícita para POST/PATCH/DELETE e comprovação posterior no dashboard.
- Nenhum token/segredo no código, testes, logs ou documentação.
- `main` não deve ser promovida antes da regressão verde e avaliação das mudanças de interface.

## Limites

Cobertura restrita à Application API documentada do Chatwoot v4.19.0. Platform API, Client API e endpoints internos não fazem parte deste gate.

## Estado da execução em `homolog` — 07/11/2026

As duas branches iniciaram no mesmo commit `deff53336e09`; a implementação partiu de `homolog` sem alteração em `main`.

Entregas de B/C registradas nos testes:

- **11 operações** de contatos, inboxes, etiquetas, equipes e mensagens com parâmetros explícitos e validação negativa.
- **4 operações** de agentes e webhooks com argumentos tipados e validações de campos.
- **2 operações** de campanhas com envelope `{"campaign": {...}}` exigido pelo Swagger.
- **10 operações** de consultas/filtros com validações de enums permitidos (relatórios, atributos, filtros, auditoria). A contagem engloba métodos que continuam aceitando payloads da API onde a estrutura é dinâmica.
- **Total de 27 pares método/rota** com revisão adicional de assinatura/envelope/validação e testes MockTransport específicos. Os demais métodos permanecem mapeados; não foram reescritos sem justificativa.

### Gate de homologação real

**Não executado nesta iteração**: ambiente e credenciais reais de Chatwoot não são necessários para CI. Não registrar operações como aprovadas em integração real apenas pelo sucesso dos mocks. Para cada endpoint, confirmar permissão, estado pré/pós operação e compatibilidade da instalação, usando somente dados de teste e autorização explícita para escritas. 

### Mudanças de interface

Os métodos simples citados acima substituem o antigo argumento `data` por parâmetros nomeados, quando pertinente. Alterações estão restritas à branch `homolog`; consumidores que importem esta versão deverão atualizar assinaturas antes de qualquer promoção a `main`.
