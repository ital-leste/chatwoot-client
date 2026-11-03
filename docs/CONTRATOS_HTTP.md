# Contratos HTTP

Documentação-fonte: https://github.com/chatwoot/chatwoot/blob/v4.19.0/swagger/tag_groups/application_swagger.json

- URL: raiz da instalação, podendo incluir prefixo de proxy. Não aceita credenciais, query ou fragmentos.
- Autenticação: Authorization: Bearer TOKEN por padrão, ou auth_mode="api_access_token" para cabeçalho legado.
- Sessão: httpx.Client síncrono e context manager, com timeout configurável.
- Requisições: JSON quando há data, multipart/form-data no envio de anexos. Qualquer `dados` enviado como objeto JSON é verificado quanto a chaves de texto e serialização JSON válida **antes do HTTP**, inclusive em recursos que seguem payloads da API sem contrato próprio.
- Respostas: preservação do JSON original. HTTP 204 e sucesso sem corpo retornam None.
- Erros: ErroAPIChatwoot informa caminho e status_http, mas nunca o corpo completo nem o token.
- Paginação: sem agregação automática; envelopes, contadores e cursores permanecem intactos.
- Retry: ausente em escritas. Um timeout após POST pode significar resultado indeterminado.
- Entradas: parâmetros Python nomeados e tipados para casos simples, contratos imutáveis para estruturas mais complexas. **Sem contrato próprio, enviar os campos e a estrutura previstos pela Application API**, normalmente via `Mapping[str, Any]`, sem remodelar arbitrariamente o payload.
- Atualizações parciais: campos omitidos não são serializados nem substituídos por `None`; quando a API permite `null` explícito, a entrada distingue os dois estados (em Contacts, via marcador privado). Não é feita leitura automática anterior à escrita.
- Conversations: prioridade em enum; `priority=None` significa limpar explicitamente. Custom attributes usam `merge=True` por padrão para preservar as demais chaves; `merge=False` faz substituição total intencional.
- Filtros avançados: `FilterCondition` reutilizado por Contacts e Conversations; cada recurso serializa em `payload` sem DTO de saída.
- Saídas: JSON nativo do Chatwoot, com verificação de formato quando o endpoint o define. Nenhum DTO de saída obrigatório.

A biblioteca não traduz respostas da API para DTOs obrigatórios. O servidor continua responsável por verificar permissões e validade de parâmetros específicos.
