# Arquitetura — contrato de entrada, saída nativa

## Objetivo e fronteiras

Biblioteca Python independente para a Application API Chatwoot 4.19.0, sem acoplamento a um sistema consumidor específico, arquivos de ambiente ou persistência. A aplicação fornece URL/token e controla autorização, idempotência, concorrência e regras próprias do negócio.

**Regra oficial:** entradas simples são expressas por parâmetros nomeados e tipados; contratos imutáveis são usados somente para estruturas que justifiquem uma classe própria. Quando houver contrato de entrada, o método exige exclusivamente esse tipo. Recursos ainda não modelados podem usar `Mapping[str, Any]`. As respostas permanecem JSON nativo (`dict`, `list` ou `None`), sem modelos de saída de domínio obrigatórios.

Tipos primitivos como IDs, parâmetros de busca, booleanos e paginação não justificam dataclass isolada. Enumerações representam domínios fechados como `ConversationStatus`. Na ausência de contrato de entrada específico, cada método segue o corpo e os parâmetros da Application API, normalmente aceitando `Mapping[str, Any]`.

## Componentes

- `client.py`: composição dos recursos; transporte HTTP compartilhado em `_request`; cabeçalhos; exceções; os métodos privados `_get/_post/_put/_patch/_delete`; `_solicitar_json` como adaptador interno dos recursos não refatorados.
- `transport.py`: execução HTTP, serialização JSON, multipart e formulário.
- `models/`: contratos imutáveis de **entrada** quando agregam estrutura ou regras (`TextMessage`, `MediaMessage`, `Attachment`, `LabelDefinition`, `Contact`, `ConversationCreate` e `FilterCondition`); Canned Responses usam parâmetros simples.
- `enums/`: tipos de mensagens, MIME, conteúdo, estados de conversa e prioridades (`ConversationPriority`).
- `message_payload.py`: serialização de texto/mídia para os campos oficiais.
- `attachment_resolver.py`: caminhos, bytes, streams e downloads HTTPS com limites.
- `messages.py`: `send_text(TextMessage)` e `send_media(MediaMessage)`; um endpoint, JSON ou multipart conforme os anexos. Não há `messages.create`, `create_with_attachments` ou atalhos por tipo de mídia.
- `labels.py`: `create(LabelDefinition)`; métodos sem contrato de entrada específico ainda seguem a API.
- `conversation_labels.py`: `add/remove` consolidam listas por GET + POST, `replace` substitui integralmente.
- `conversations.py`: `create(ConversationCreate)` e `filter(FilterCondition)`; prioridade via `ConversationPriority`, status por `ConversationStatus`, operações simples por parâmetros tipados. Consultas preservam JSON nativo.
- `canned_responses.py`: `list(search=None)` faz GET completo/filtrado; `create(short_code=..., content=...)` e `update(short_code=None, content=None)` validam entradas simples; `delete(id)` remove.

## Contatos: contrato único e atualização não destrutiva

`Contact` é uma dataclass imutável de **entrada** para `contacts.create(account_id, contact, inbox_id=None, source_id=None)` e `contacts.update(account_id, contact_id, contact)`. As respostas continuam como JSON bruto da API. Criação aceita `inbox_id` opcional como no controlador Chatwoot 4.19.0; `source_id` só faz sentido junto à inbox.

**Regra oficial para atualizações parciais:** um campo *omitido* no objeto Python não pode ser serializado, não pode ser substituído por `None` e não exige uma leitura prévia do contato. O modelo distingue ausência de `None` explícito por marcador privado. Assim, `Contact(name="Maria")` gera exatamente `{"name": "Maria"}`; `Contact(email=None)` gera `{"email": null}` e delega a limpeza às regras do Chatwoot. `False` e dicionários vazios explicitamente informados não são filtrados por verdade/falsidade.

`Contact` contém somente os campos de cadastro suportados pelo payload JSON nesta etapa. E-mail possui checagem simples, telefone segue E.164, `blocked` exige bool e dicionários de atributos precisam ser JSON válidos. Validações de unicidade, disponibilidade de campos, permissões e comportamento de `null` são responsabilidade do backend. Nenhum campo de saída (`id`, timestamps, inboxes, etc.) entra na dataclass. A dataclass é imutável na raiz; objetos JSON recebidos são copiados defensivamente na construção e no `to_payload()`. Valores internos continuam mutáveis em Python, por isso a serialização repete a validação JSON antes de enviá-los.

A API utiliza `PUT` na especificação, e o controlador também permite `PATCH`. O cliente preserva `PUT`, enviando **somente** os campos do objeto informados. O Rails realiza atualização parcial e mescla chaves de `additional_attributes`/`custom_attributes` em vez de substituir o objeto inteiro. A criação/atualização de avatar binário por multipart será tratada separadamente; `avatar_url` é aceita como string pelo contrato.

## Conversas: entradas tipadas, atributos preservados e filtros compartilhados

A criação usa a dataclass imutável `ConversationCreate`, que representa identidade do canal (`source_id`), `inbox_id`, `contact_id`, estado opcional e relações de atribuição; aceita atributos JSON e `message` opcional, exigindo `message.content` quando há mensagem. Não há dataclass de saída. A API exige `source_id`; campos opcionais `None` não entram no payload de criação. Os mapeamentos de atributos e mensagem são copiados na entrada e na saída e revalidados durante a serialização para que mudanças posteriores não contornem os validadores.

O contrato `FilterCondition` é compartilhado por `contacts.filter()` e `conversations.filter()`. Cada recurso só serializa os objetos `FilterCondition` dentro de `{"payload": [...]}`, sem aceitar listas de dicionários alternativas nas operações modeladas. Filtros de leitura simples de `conversations.list()` e `conversations.meta()` recebem parâmetros nomeados (`status`, `q`, IDs, `labels`), sem dataclasses. `list()` retorna `data.meta/data.payload`; `filter()` e `meta()` preservam seus envelopes distintos.

`conversations.update(priority=ConversationPriority.HIGH)` envia `{"priority": "high"}`; `priority=None` envia explicitamente JSON `null` para remover prioridade. `toggle_priority()` possui a mesma entrada simples e o mesmo JSON; sucesso sem corpo retorna `None`. `set_typing_status(typing_status="on"|"off", is_private=bool)` não precisa de contrato. `set_status(ConversationStatus)` continua tipado e conserva a semântica de handoff do Chatwoot ao mudar `pending` para `open` sob um AgentBot.

**Atenção à semântica do servidor:** `conversations.update_custom_attributes(custom_attributes=..., merge=True)` envia `merge=true` expressamente, preservando por padrão chaves de atributos não informadas. `merge=False` substitui o conjunto inteiro de atributos e só deve ser usado intencionalmente. A exclusão de atributos usa `delete_custom_attributes(keys=[...])`. Não há GET prévio nem alteração de outros campos no cliente. O Chatwoot continua responsável por validar definições, permissões e as alterações definitivas.

Consultas e escritas retornam a resposta JSON nativa: `list()` possui `{"data": {"meta": ..., "payload": [...]}}`, `filter()` possui `{"meta": ..., "payload": [...]}`, `get/create/update()` retornam objetos da conversa, e operações com `head :ok` devolvem `None`. Validar a forma da resposta quando conhecida, sem normalizar envelopes nem impor DTOs.

## Respostas rápidas

Não há dataclass `CannedResponse`: o recurso precisa apenas de `short_code: str` e `content: str`, sem estrutura aninhada ou regras complexas de serialização. A criação exige os dois campos e a atualização parcial exige ao menos um; os campos fornecidos devem ser textos não vazios. A validação fica no recurso, antes do HTTP. O Chatwoot continua responsável pela unicidade de `short_code` na conta.

A API devolve arrays JSON em listagens e objetos JSON nas escritas. O cliente confere a forma esperada, mas não transforma respostas em dataclasses; assim, campos novos fornecidos pelo Chatwoot não são descartados. O parâmetro `search`, observado no controlador 4.19.0, pesquisa no servidor sobre `short_code` e `content`, sem busca fuzzy local ou cache.

## Segurança, erros e concorrência

`_request` é a única fronteira de execução HTTP, sem retry automático de escrita. Erros HTTP/JSON são convertidos em `ErroAPIChatwoot` sem expor tokens ou corpos sensíveis. HTTP 204 e sucesso sem corpo retornam `None`. Não são retornados objetos `httpx.Response` brutos.

Anexos por URL exigem HTTPS, DNS público e porta 443, sem credenciais nem redirecionamentos automáticos; `allowed_hosts` limita destinos. Downloads são feitos em cliente separado com `trust_env=False`, nunca com o token Chatwoot. O filtro DNS não substitui egress/allowlist de rede. Tamanho máximo padrão de 25 MiB por anexo.

Alterações de etiquetas por `add/remove` não são atômicas; o executor deve ordenar requisições concorrentes por conversa e conferir o estado final quando necessário. Políticas de autorização para edição, exclusão e publicação pública/privada pertencem à aplicação consumidora.

## Abrangência e versionamento

A matriz registra 124 pares verbo/rota da Application API, independentemente do número de métodos Python públicos. A refatoração tipada removeu aliases e assinaturas redundantes durante a homologação, antes do uso em produção. Uma versão publicada com consumidores externos exigiria migração ou versionamento incompatível adequado.
