# Changelog

## Unreleased — homolog

- Regra oficial: **contratos tipados para entradas de operações modeladas; retorno JSON nativo da API**.
- `CannedResponse` é a única dataclass de entrada para criação e atualização; `create` exige `short_code` e `content`, `update` exige ao menos um. `list(search=None)` mantém GET integral/filtrado e devolve `list[dict]`.
- Removidas as interfaces `list_typed`, `CannedResponseCreate`, `CannedResponseUpdate` e as entradas alternativas `Mapping` em operações de respostas rápidas.
- Mensagens expõem somente `send_text(TextMessage)` e `send_media(MediaMessage)`, com `private: bool`; retirados `MessageVisibility`, `visibility`, `messages.create`, `create_with_attachments` e atalhos redundantes por MIME.
- Etiquetas da conta são criadas por `labels.create(LabelDefinition)`; `create_label` foi retirado. `conversations.set_status` exige `ConversationStatus`, não aceita strings soltas.
- Consultas e operações ainda sem contratos específicos permanecem como interfaces da Application API, com JSON nativo, erros HTTP controlados e sem retry automático.
- A cobertura da matriz API v4.19.0 permanece em 124 pares verbo/rota; os testes simulados não substituem homologação real.

## 0.1.0

- Primeira extração independente do gateway Chatwoot do projeto Hermes, com operações iniciais e transporte HTTP centralizado.
