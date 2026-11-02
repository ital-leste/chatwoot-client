# Arquitetura

## Propósito

Biblioteca Python independente para a Application API Chatwoot 4.19.0. O consumidor fornece base_url e api_token. O pacote não depende de Hermes, Evolution, banco de dados, webhook, .env ou infraestrutura de atendimento.

## Fronteiras e responsabilidades

- `chatwoot_client/__init__.py`: exporta CWClient, models, enums e exceções oficialmente suportados.
- `client.py`: composição dos recursos, autenticação, execução HTTP centralizada em `_request` e verbos privados `_get/_post/_put/_patch/_delete`, retorno e erros. `_solicitar_json` permanece como adaptador retrocompatível.
- `transport.py`: envio HTTP efetivo, JSON, multipart e formulário. Os recursos não acessam httpx diretamente.
- `models/`: contratos imutáveis de mensagens, anexos e definição de etiqueta da conta, com validação estrutural; sem arquivo/rede no construtor.
- `enums/`: valores oficiais de tipo de mensagem, status de conversa, conteúdo e MIME comuns; `private: bool` é preferido. `MessageVisibility` permanece por compatibilidade.
- `attachment_resolver.py`: preparação de caminhos, fluxos, bytes e downloads HTTPS; controla limites e fechamento de arquivos.
- `message_payload.py`: mapeamento de contratos tipados para campos da Application API.
- `messages.py`: operações principais `send_text` e `send_media` pelo mesmo endpoint; atalhos específicos de mídia preservados por compatibilidade. `is_voice_message` diferencia voz de áudio comum.
- `conversations.py`: `set_status` aceita `ConversationStatus` e strings antigas.
- `labels.py`: `create_label` aceita `LabelDefinition`; `create` anterior preservado.
- `conversation_labels.py`: `add/remove` fazem GET + consolidação + POST, `replace` preserva semântica integral.
- Demais recursos: operações específicas sem responsabilidade por execução HTTP, autorização de negócio ou runtime Hermes.

## Contratos públicos e compatibilidade

O cliente continua oferecendo os 16 métodos originais e os 108 métodos adicionados. Os métodos existentes mantêm suas assinaturas e continuam compatíveis com payloads livres. A interface preferencial para publicação de mensagens é tipada. A migração dos demais recursos será gradual, conforme importância e capacidade de validação.

O tipo de conteúdo da mensagem (ex.: text) não deve ser confundido com MIME de anexo (ex.: application/pdf). Os modelos validam invariantes; condições externas como arquivo existente ou resposta de URL são avaliadas na execução.

## Segurança e limites

O envio pode produzir efeitos externos: não há retry automático de POST após timeout. O sistema consumidor gerencia idempotência, permissões, handoff e autorização de envio.

URLs de anexos exigem HTTPS, destino DNS global, porta 443, sem credenciais e sem redirecionamentos automáticos; tamanho máximo padrão de 25 MiB por anexo, configurável em cada chamada. O resolvedor aplica `trust_env=False` ao download e jamais envia o token Chatwoot ao host remoto. `allowed_hosts` restringe os domínios; deve ser definido para URLs originadas de entradas não confiáveis (como respostas de agentes). O filtro DNS reduz riscos de SSRF, mas, por limitações da resolução DNS/TOCTOU, não substitui controles de egress/allowlist do ambiente. Arquivos obtidos de URLs são copiados em chunks para arquivo temporário; caminhos locais são abertos por streaming. Fluxos do consumidor não são fechados pela biblioteca.

## Publicação

Desenvolvimento em homolog. Main preservada até homologação real, regressão e aprovação da mudança.

## Concorrência na associação de etiquetas

O endpoint de etiquetas da conversa é uma substituição completa, não um append atômico. `add/remove` são operações de conveniência read-modify-write e podem sofrer lost update se agentes e usuários alterarem etiquetas simultaneamente. O pacote não introduz bloqueios distribuídos nem garante transação entre GET e POST. O executor que já controla lotes por conversa deve serializar atualizações de etiquetas e, quando crítico, conferir o estado final. Etiquetas criadas no catálogo e etiquetas associadas à conversa têm recursos separados.

## Compatibilidade de mensagens

`private` é o campo booleano da API. `visibility=MessageVisibility.PRIVATE` segue aceito nas dataclasses para preservar código criado na primeira evolução; interfaces novas devem preferir `private=True`. Mensagens de voz utilizam `is_voice_message` no multipart, parâmetro observado no código-fonte 4.19.0 e não presente na especificação OpenAPI consultada. Validar entrega final por canal.

## Canned Responses

`models/canned_responses.py` contém os contratos imutáveis `CannedResponse`, `CannedResponseCreate` e `CannedResponseUpdate`. `canned_responses.py` orquestra GET, POST, PATCH e DELETE, utilizando os verbos privados de `CWClient`. Esses modelos são expostos em `chatwoot_client/__init__.py`.

`list()` preserva o JSON original e aceita opcionalmente `search` (ou o parâmetro legado `parametros`); `list_typed()` usa a mesma consulta e converte a lista em contratos validados. Sem `search`, a API lista tudo; com `search`, filtra por `short_code` ou `content` no próprio servidor. A resposta é array JSON, não `{"payload": ...}`. Não há cache nem busca dinâmica no cliente Python.

O catálogo é compartilhado com agentes humanos. O cliente não valida autorização de negócio, não interpreta variáveis Liquid, não cria versões e não implementa restauração após exclusão. O consumidor (por exemplo, Hermes) deve controlar permissões para operações de escrita.

