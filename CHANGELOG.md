# Changelog

## Unreleased — homolog

- 108 operações da Application API v4.19.0 acrescentadas a 16 contratos existentes.
- Transporte extraído para transport.py, com HTTP 204, cabeçalho legado opcional e multipart.
- messages.create_with_attachments e profile.update_multipart para arquivos, sem reenvio implícito.
- account.update_form para payload form-urlencoded.
- Testes HTTP simulados de cobertura por rota e documentação dos contratos de arquitetura e homologação.

## 0.1.0

- Primeira extração independente do gateway do projeto Hermes.
