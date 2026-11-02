# Changelog

## Unreleased — homolog

- Regra oficial: **parâmetros nomeados e tipados para entradas simples, contratos de domínio quando necessários; retorno JSON nativo da API**.
- Canned Responses deixam de ter dataclass: `create(short_code=..., content=...)` exige ambos, `update(..., short_code=None, content=None)` exige pelo menos um e `list(search=None)` mantém GET integral/filtrado com retorno `list[dict]`.
- Removidas as interfaces `CannedResponse`, `list_typed`, `CannedResponseCreate` e `CannedResponseUpdate`; não há entrada alternativa `Mapping` nas respostas rápidas.
- Mensagens expõem somente `send_text(TextMessage)` e `send_media(MediaMessage)`, com `private: bool`; retirados `MessageVisibility`, `visibility`, `messages.create`, `create_with_attachments` e atalhos redundantes por MIME.
- Etiquetas da conta são criadas por `labels.create(LabelDefinition)`; `create_label` foi retirado. `conversations.set_status` exige `ConversationStatus`, não aceita strings soltas.
- Consultas e operações ainda sem contratos específicos permanecem como interfaces da Application API, com JSON nativo, erros HTTP controlados e sem retry automático.
- A cobertura da matriz API v4.19.0 permanece em 124 pares verbo/rota; os testes simulados não substituem homologação real.

## 0.1.0

- Primeira extração independente do gateway Chatwoot do projeto Hermes, com operações iniciais e transporte HTTP centralizado.
