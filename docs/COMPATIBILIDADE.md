# Compatibilidade

- Referência de cobertura: Chatwoot 4.19.0, Application API.
- Python mínimo: 3.11. Distribuição: ital-leste-chatwoot-client.
- Dependência de execução: httpx >=0.27,<1.
- Matriz: 124 pares verbo/rota mapeados; a quantidade de métodos públicos Python não é necessariamente 124.
- Operações com contratos implementados exigem modelos de entrada tipados. Métodos antigos redundantes foram retirados na homologação, antes de existirem consumidores em produção.
- Autenticação: Bearer por padrão; api_access_token como opção explícita legada.
- Instalações mais antigas podem não oferecer todos os endpoints ou autenticação Bearer.
- A remoção de interfaces redundantes ocorre nesta etapa de homologação, antes de uma versão estável com consumidores externos. Para consumidores futuros, mudanças incompatíveis exigirão versão apropriada e testes de regressão.

Não estão incluídas a Platform API, a Client API, APIs internas nem regras de atendimento de um consumidor específico.
