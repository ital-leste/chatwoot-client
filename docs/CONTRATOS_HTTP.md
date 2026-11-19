# Contratos HTTP

Documentação-fonte: https://github.com/chatwoot/chatwoot/blob/v4.19.0/swagger/tag_groups/application_swagger.json

- URL: raiz da instalação, podendo incluir prefixo de proxy. Não aceita credenciais, query ou fragmentos.
- Autenticação: Authorization: Bearer TOKEN por padrão, ou auth_mode="api_access_token" para cabeçalho legado. A URL-base aceita HTTP(S), prefixo e portas válidas; rejeita host ausente, porta inválida, credenciais, query e fragmento.
- Sessão: httpx.Client síncrono e context manager, com timeout numérico positivo (padrão 30 s) ou `httpx.Timeout` granular nativo. Não há configuração de retry implícito.
- Requisições: JSON quando há data, multipart/form-data no envio de anexos. Qualquer `dados` enviado como objeto JSON é verificado quanto a chaves de texto **em todos os níveis** e serialização JSON válida **antes do HTTP**, inclusive em recursos que seguem payloads da API sem contrato próprio.
- Respostas: o transporte devolve `None` para HTTP 204 ou sucesso sem corpo. Os recursos que exigem corpo validam a estrutura antes de devolver o JSON nativo. `messages.list()` exige um `payload` em lista com IDs inteiros positivos. `messages.send_text()` e `messages.send_media()` exigem um objeto com o ID inteiro positivo da mensagem criada.
- Erros: `ErroAPIChatwoot` informa `caminho` e, quando disponível, `status_http`. Falhas de transporte usam `ErroConexaoChatwoot` e respostas inválidas usam `ErroFormatoChatwoot`, ambas subclasses de `ErroAPIChatwoot`. Erros HTTP podem expor `retry_after` em segundos quando o cabeçalho é numérico e `request_id` sanitizado. Uma validação estrutural após a decodificação pode gerar erro sem acesso ao status original. A exceção omite o corpo, o token e os cabeçalhos brutos.
- Paginação: sem agregação automática; envelopes, contadores e cursores permanecem intactos. Em `messages.list()`, `before` e `after` são IDs não negativos; juntos representam `[after, before)` e exigem `after < before`. Isoladamente, `before` usa IDs menores e `after` usa IDs maiores (veja o guia).
- Retry: ausente em escritas. Um timeout após POST pode significar resultado indeterminado.
- Entradas: parâmetros Python nomeados e tipados para casos simples, contratos imutáveis para estruturas mais complexas. **Sem contrato próprio, enviar os campos e a estrutura previstos pela Application API**, normalmente via `Mapping[str, Any]`, sem remodelar arbitrariamente o payload.
- Atualizações parciais: campos omitidos não são serializados nem substituídos por `None`; quando a API permite `null` explícito, a entrada distingue os dois estados (em Contacts, via marcador privado). Não é feita leitura automática anterior à escrita.
- Conversations: prioridade em enum; `priority=None` significa limpar explicitamente. Custom attributes usam `merge=True` por padrão para preservar as demais chaves; `merge=False` faz substituição total intencional.
- Filtros avançados: `FilterCondition` reutilizado por Contacts e Conversations; cada recurso serializa em `payload` sem DTO de saída.
- Saídas: JSON nativo do Chatwoot, com verificação de formato quando o endpoint o define. Nenhum DTO de saída obrigatório.
- Mensagens: `TextMessage.content` e `MediaMessage.caption` respeitam o máximo de 150.000 caracteres validado em `Message` no Chatwoot 4.19.0. Fluxos de anexo com `read() is None` falham antes do POST, sem anexos truncados.

A biblioteca não traduz respostas da API para DTOs obrigatórios. O servidor continua responsável por verificar permissões e validade de parâmetros específicos.

## Contratos administrativos após homologação simulada

- Escritas complexas: dataclasses imutáveis de entrada, com `to_payload()`, cópia defensiva de campos mutáveis e omissão de valores não informados. `None` só é emitido quando explicitamente admitido no contrato.
- Escritas simples: campos nomeados, validação local de IDs, enums, listas, textos e corpo obrigatório antes do HTTP.
- Estruturas variáveis de canais, configurações, condições/ações e campanhas preservam o formato nativo da API dentro de contratos, em vez de criar DTOs restritivos.
- `profile.update(ProfileInput)` adiciona o envelope requerido `profile`; `campaigns.create/update` adicionam `campaign`.
- Alternativos `account.update_form()` e `profile.update_multipart()` mantêm seus próprios formatos de formulário/arquivo.
- Alterações são de interface Python em `homolog`; não mudam as 124 combinações verbo/rota e não configuram homologação real.
