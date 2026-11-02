# Compatibilidade

- Referência de cobertura: Chatwoot 4.19.0, Application API.
- Python mínimo: 3.11. Distribuição: ital-leste-chatwoot-client.
- Dependência de execução: httpx >=0.27,<1.
- Contratos originais: 16 operações preservadas, incluindo assinaturas e caminhos.
- Expansão: 108 operações adicionais, totalizando 124 endpoints e verbos mapeados.
- Autenticação: Bearer por padrão; api_access_token como opção explícita legada.
- Instalações mais antigas podem não oferecer todos os endpoints ou autenticação Bearer.
- Alterações incompatíveis exigem versão major e testes de regressão.

Não estão incluídas a Platform API, a Client API, APIs internas nem regras de atendimento de um consumidor específico.
