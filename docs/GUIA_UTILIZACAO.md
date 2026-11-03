# Guia de utilização

Instalação: `python -m pip install -e ".[test]"`. Validação: `python -m pytest -q`.

## Importações públicas

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment,
    MimeType, MessageType, ConversationStatus, ConversationPriority,
    Contact, ConversationCreate, FilterCondition,
    LabelDefinition, ErroAPIChatwoot, ErroAnexoChatwoot,
)
```

## Consultas e filtros

Consultas que não possuem contrato específico continuam retornando o JSON da API com seus envelopes, cursores e metadados:

```python
with CWClient(URL, TOKEN, timeout=30) as cw:
    perfil = cw.profile.get()
    conversas = cw.conversations.list(1, status="open", page=1)
    mensagens = cw.messages.list(1, 2)
    contatos = cw.contacts.list(1)
```

## Enviar mensagens e notas internas

```python
with CWClient(URL, TOKEN) as cw:
    publica = cw.messages.send_text(1, 2, TextMessage("Bom dia!"))
    nota = cw.messages.send_text(
        1, 2, TextMessage("Verificar documentos.", private=True)
    )
    identificador = publica["id"]  # JSON nativo; não há modelo de saída
```

`MessageType.INCOMING` e `MessageType.OUTGOING` são os valores aceitos para o tipo de mensagem. A visibilidade é somente `private: bool`.

## Mídia: PDF, imagem, áudio, vídeo e anexos múltiplos

Todas as mídias usam o mesmo método público `send_media()` e o único endpoint oficial de mensagens (multipart), sem aliases especializados.

```python
with CWClient(URL, TOKEN) as cw:
    cw.messages.send_media(
        1, 2,
        MediaMessage(
            attachments=[Attachment.from_path("laudo.pdf", mime_type=MimeType.PDF)],
            caption="Segue o laudo solicitado.",
        ),
    )
    cw.messages.send_media(
        1, 2,
        MediaMessage(
            attachments=[
                Attachment(b"%PDF-1.4...", MimeType.PDF, "primeiro.pdf"),
                Attachment.from_path("segundo.pdf"),
            ],
            private=True,
        ),
    )
```

Para fontes HTTPS:

```python
arquivo = Attachment.from_url(
    "https://arquivos.exemplo.com/laudo.pdf", mime_type=MimeType.PDF,
)
cw.messages.send_media(
    1, 2, MediaMessage(attachments=[arquivo], caption="Laudo"),
    allowed_hosts={"arquivos.exemplo.com"},
    max_bytes=25 * 1024 * 1024,
    url_timeout=30.0,
)
```

A obtenção do anexo usa cliente HTTP separado, HTTPS público, porta 443, sem credenciais nem redirecionamentos automáticos. Nunca envia o token do Chatwoot ao host externo. Arquivos locais devem existir na máquina que executa a biblioteca; streams binários fornecidos pelo consumidor não são fechados por ela.

## Áudio de voz

```python
cw.messages.send_media(
    1, 2,
    MediaMessage(
        attachments=[Attachment.from_path("gravacao.ogg", mime_type=MimeType.OGG)],
        is_voice_message=True,
    ),
)
```

O Chatwoot reconhece `is_voice_message` para áudio OGG no código-fonte 4.19.0; a entrega real depende da integração do canal. O marcador não é enviado para áudio comum.

## Conversas e etiquetas

```python
cw.conversations.set_status(1, 2, ConversationStatus.PENDING)
cw.conversations.set_status(1, 2, ConversationStatus.RESOLVED)

cw.labels.create(
    1, LabelDefinition(
        title="aguardando-laudo", color="#224466",
        description="Documentação solicitada",
    )
)
cw.conversation_labels.add(1, 2, "aguardando-laudo")
cw.conversation_labels.add(1, 2, ["hermes-ativo", "aguardando-laudo"])
cw.conversation_labels.remove(1, 2, "hermes-ativo")
cw.conversation_labels.replace(1, 2, ["aguardando-laudo"])
```

`replace()` substitui toda a lista. `add()` e `remove()` leem a lista atual e escrevem o conjunto consolidado, preservando as demais etiquetas, mas **não são operações atômicas**. O executor deve serializar operações concorrentes por conversa. A criação de uma etiqueta no catálogo não a associa automaticamente à conversa. Outros métodos de etiqueta que ainda não possuem contrato (como atualização parcial) permanecem com os parâmetros da API.

## Conversas — padronização da Application API

```python
from chatwoot_client import (
    ConversationCreate, ConversationStatus, ConversationPriority, FilterCondition,
)

# Criação com contrato tipado (source_id identifica a origem no canal).
nova = cw.conversations.create(
    1,
    ConversationCreate(
        source_id="origem-canal", inbox_id=1, contact_id=42,
        status=ConversationStatus.OPEN,
    ),
)

# Prioridade: enum obrigatório; None explícito limpa o valor anterior.
cw.conversations.update(1, 9, priority=ConversationPriority.HIGH)
cw.conversations.update(1, 9, priority=None)

# Estado explicitamente definido; snoozed_until em Unix segundos.
cw.conversations.set_status(1, 9, ConversationStatus.PENDING)

# Digitação: entrada simples, sem dataclass.
cw.conversations.set_typing_status(1, 9, typing_status="on", is_private=False)

# Filtros avançados compartilhados com Contacts.
condicao = FilterCondition(
    attribute_key="status", filter_operator="equal_to", values=["pending"]
)
conversas = cw.conversations.filter(1, [condicao], page=1)
contatos = cw.contacts.filter(1, [
    FilterCondition(attribute_key="name", filter_operator="contains", values=["Maria"])
])

# Por padrão, preserva os demais atributos existentes da conversa.
cw.conversations.update_custom_attributes(
    1, 9, custom_attributes={"interesse": "gnv"}
)
# Substituir todos os atributos exige intenção explícita.
cw.conversations.update_custom_attributes(
    1, 9, custom_attributes={"interesse": "gnv"}, merge=False
)
cw.conversations.delete_custom_attributes(1, 9, keys=["interesse"])
```

`create()` exige `ConversationCreate`. Os métodos simples não possuem dataclasses redundantes. `update()` opera sobre prioridade; `priority=None` é uma solicitação **explícita** de limpeza (não é ausência). O contrato `FilterCondition` usa os mesmos campos de filtro no Chatwoot para contatos e conversas. Sua validação é estrutural; a validade de cada operador para cada atributo cabe ao backend.

**Retornos diferentes permanecem diferentes:** `conversations.list()` usa envelope `data.meta/data.payload`; `conversations.filter()` usa `meta/payload`; `conversations.get/create/update()` devolvem objetos, não DTOs. `toggle_priority()` e `set_typing_status()` normalmente retornam `None` (HTTP sem corpo).

`update_custom_attributes()` envia `merge=True` por padrão, diferentemente do padrão do servidor (`merge=false`). O contrato protege contra substituição acidental dos demais atributos. A atualização de status `pending` → `open` pode disparar handoff no Chatwoot ao usar uma credencial AgentBot; a aplicação consumidora deve determinar sua política de autorização.

## Contatos — dataclass de entrada e preservação de campos

`Contact` representa os campos a escrever, não um objeto de retorno. A mesma dataclass é utilizada na criação e na atualização.

```python
from chatwoot_client import Contact

# Criação: inbox_id é opcional no controlador do Chatwoot 4.19.0
criado = cw.contacts.create(
    1,
    Contact(name="Maria", phone_number="+5511999999999", email="maria@exemplo.com"),
    inbox_id=1,
)
novo_id = criado["payload"]["contact"]["id"]

# Atualização pontual: o e-mail e o telefone cadastrados NÃO são enviados.
atualizado = cw.contacts.update(1, novo_id, Contact(name="Maria Souza"))

# Limpeza intencional: somente email será enviado como JSON null;
# o Chatwoot decide se a operação é permitida para esse campo.
cw.contacts.update(1, novo_id, Contact(email=None))

# False é um valor explícito, não deve ser omitido.
cw.contacts.update(1, novo_id, Contact(blocked=False))

# Atributos extras: a API mescla as chaves fornecidas às existentes.
cw.contacts.update(1, novo_id, Contact(
    custom_attributes={"tipo_veiculo": "automovel"}
))
```

**Garantia do cliente:** um campo não informado no `Contact(...)` não entra no JSON de atualização. Os atributos existentes são preservados pelo comportamento de atualização parcial do Chatwoot, sem precisar realizar GET anterior. Não confundir campo omitido com `None` explicitamente informado; este último será serializado como `null`, e o resultado depende das regras do servidor. Para não reenviar campos antigos, crie um `Contact` com apenas os campos que deseja alterar.

Os validadores locais verificam formatos simples de e-mail, E.164 para telefone, tipos básicos e objetos JSON válidos, mas a conta Chatwoot continua validando unicidade e atributos configurados. O contrato não contempla `avatar` binário nesta fase; `avatar_url` é suportada.

## Respostas rápidas — parâmetros nomeados

```python
with CWClient(URL, TOKEN) as cw:
    # GET: sem filtro retorna todas; com filtro busca no servidor.
    todas: list[dict] = cw.canned_responses.list(1)
    filtradas: list[dict] = cw.canned_responses.list(1, search="gnv")

    # POST: short_code e content obrigatórios.
    criada: dict = cw.canned_responses.create(
        1, short_code="gnv_periodica", content="Texto padrão."
    )

    # PATCH: pelo menos um campo obrigatório, sem alterar o outro.
    atualizada: dict = cw.canned_responses.update(
        1, criada["id"], content="Texto revisado."
    )
    cw.canned_responses.update(1, criada["id"], short_code="gnv_periodica_2")

    # DELETE por ID; não há restauração automática pela API.
    cw.canned_responses.delete(1, criada["id"])
```

`create()` exige `short_code: str` e `content: str` não vazios. `update()` aceita os mesmos campos opcionalmente e exige ao menos um presente. A validação mínima ocorre antes de qualquer chamada HTTP; regras como a unicidade do atalho pertencem ao Chatwoot. Não há dataclass `CannedResponse` nem entrada alternativa por `Mapping`.

`list()` devolve um array JSON com os campos originais do Chatwoot (sem envelope `payload`). O parâmetro `search` é enviado em um único GET e filtra por `short_code` ou `content` no servidor, sem reproduzir a busca dinâmica `picoSearch` do dashboard. Variáveis Liquid não são resolvidas por este cliente.

## Restrições de segurança

A interface de entrada usa parâmetros nomeados tipados em operações simples e contratos de domínio quando há estrutura ou validações que os justificam. Não forneça dicionários onde a operação exige `TextMessage`, `MediaMessage` ou `LabelDefinition`. Recursos ainda não modelados continuam espelhando a API com `Mapping`.

Erros de conexão, HTTP ou JSON inválido geram `ErroAPIChatwoot`, sem vazar dados de resposta. A confirmação da API não representa confirmação de entrega WhatsApp. Não há retry implícito de POST/PATCH/DELETE.
