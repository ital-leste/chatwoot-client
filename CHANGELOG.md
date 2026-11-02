# Changelog

## Unreleased — homolog

- Mensagens tipadas simplificadas com `private: bool` e `send_media` como interface preferencial; `MessageVisibility` continua como alias de compatibilidade.
- `MediaMessage.is_voice_message` habilita marcador oficial do builder Chatwoot para arquivo OGG.
- `ConversationStatus` exportado na raiz e aceito por `conversations.set_status` sem quebrar strings originais.
- `LabelDefinition` e `labels.create_label()` para criação tipada no catálogo.
- `conversation_labels.add/remove` implementam união/subtração conservadora da lista existente; `replace` mantém substituição total.


- Contratos tipados imutáveis `TextMessage`, `MediaMessage`, `Attachment` e enumerações exportadas pela raiz do pacote.
- Operações `send_text`, `send_media`, `send_image`, `send_audio`, `send_video`, `send_document`, mantendo o endpoint de mensagens existente.
- Resolução de caminho local, bytes, fluxo e HTTPS para anexos com limite de tamanho, allowlist opcional e sem exposição de token Chatwoot a outros hosts.
- Centralização dos verbos HTTP privados no CWClient e preservação de `_solicitar_json` para retrocompatibilidade.


- 108 operações da Application API v4.19.0 acrescentadas a 16 contratos existentes.
- Transporte extraído para transport.py, com HTTP 204, cabeçalho legado opcional e multipart.
- messages.create_with_attachments e profile.update_multipart para arquivos, sem reenvio implícito.
- account.update_form para payload form-urlencoded.
- Testes HTTP simulados de cobertura por rota e documentação dos contratos de arquitetura e homologação.

## 0.1.0

- Primeira extração independente do gateway do projeto Hermes.
