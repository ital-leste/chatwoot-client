# Arquitetura — contrato de entrada, saída nativa

## Objetivo e fronteiras

Biblioteca Python independente para a Application API Chatwoot 4.19.0, sem acoplamento ao Hermes, Evolution, VPS, banco, webhook ou .env. A aplicação fornece URL/token e controla autorização, idempotência, concorrência e regras de atendimento.

**Regra oficial:** entradas simples são expressas por parâmetros nomeados e tipados; contratos imutáveis são usados somente para estruturas que justifiquem uma classe própria. Quando houver contrato de entrada, o método exige exclusivamente esse tipo. Recursos ainda não modelados podem usar `Mapping[str, Any]`. As respostas permanecem JSON nativo (`dict`, `list` ou `None`), sem modelos de saída de domínio obrigatórios.

Tipos primitivos como IDs, parâmetros de busca, booleanos e paginação não justificam dataclass isolada. Enumerações representam domínios fechados como `ConversationStatus`.

## Componentes

- `client.py`: composição dos recursos; transporte HTTP compartilhado em `_request`; cabeçalhos; exceções; os métodos privados `_get/_post/_put/_patch/_delete`; `_solicitar_json` como adaptador interno dos recursos não refatorados.
- `transport.py`: execução HTTP, serialização JSON, multipart e formulário.
- `models/`: contratos imutáveis de **entrada** quando agregam estrutura ou regras (`TextMessage`, `MediaMessage`, `Attachment`, `LabelDefinition`); Canned Responses usam parâmetros simples.
- `enums/`: tipos de mensagens, MIME, conteúdo e estados de conversa.
- `message_payload.py`: serialização de texto/mídia para os campos oficiais.
- `attachment_resolver.py`: caminhos, bytes, streams e downloads HTTPS com limites.
- `messages.py`: `send_text(TextMessage)` e `send_media(MediaMessage)`; um endpoint, JSON ou multipart conforme os anexos. Não há `messages.create`, `create_with_attachments` ou atalhos por tipo de mídia.
- `labels.py`: `create(LabelDefinition)`; métodos sem contrato de entrada específico ainda seguem a API.
- `conversation_labels.py`: `add/remove` consolidam listas por GET + POST, `replace` substitui integralmente.
- `conversations.py`: `set_status(ConversationStatus)` exige enum; consultas de conversas preservam JSON nativo.
- `canned_responses.py`: `list(search=None)` faz GET completo/filtrado; `create(short_code=..., content=...)` e `update(short_code=None, content=None)` validam entradas simples; `delete(id)` remove.

## Respostas rápidas

Não há dataclass `CannedResponse`: o recurso precisa apenas de `short_code: str` e `content: str`, sem estrutura aninhada ou regras complexas de serialização. A criação exige os dois campos e a atualização parcial exige ao menos um; os campos fornecidos devem ser textos não vazios. A validação fica no recurso, antes do HTTP. O Chatwoot continua responsável pela unicidade de `short_code` na conta.

A API devolve arrays JSON em listagens e objetos JSON nas escritas. O cliente confere a forma esperada, mas não transforma respostas em dataclasses; assim, campos novos fornecidos pelo Chatwoot não são descartados. O parâmetro `search`, observado no controlador 4.19.0, pesquisa no servidor sobre `short_code` e `content`, sem busca fuzzy local ou cache.

## Segurança, erros e concorrência

`_request` é a única fronteira de execução HTTP, sem retry automático de escrita. Erros HTTP/JSON são convertidos em `ErroAPIChatwoot` sem expor tokens ou corpos sensíveis. HTTP 204 e sucesso sem corpo retornam `None`. Não são retornados objetos `httpx.Response` brutos.

Anexos por URL exigem HTTPS, DNS público e porta 443, sem credenciais nem redirecionamentos automáticos; `allowed_hosts` limita destinos. Downloads são feitos em cliente separado com `trust_env=False`, nunca com o token Chatwoot. O filtro DNS não substitui egress/allowlist de rede. Tamanho máximo padrão de 25 MiB por anexo.

Alterações de etiquetas por `add/remove` não são atômicas; o executor deve ordenar requisições concorrentes por conversa e conferir o estado final quando necessário. Regras para ferramentas do Hermes, permissões de edição de respostas rápidas e publicação pública/privada pertencem à aplicação consumidora.

## Abrangência e versionamento

A matriz registra 124 pares verbo/rota da Application API, independentemente do número de métodos Python públicos. A refatoração tipada removeu aliases e assinaturas redundantes durante a homologação, antes do uso em produção. Uma versão publicada com consumidores externos exigiria migração ou versionamento incompatível adequado.
