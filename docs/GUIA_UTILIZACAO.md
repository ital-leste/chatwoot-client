# Guia de utilização

Instalação: `python -m pip install -e ".[test]"`. Validação: `python -m pytest -q`.

## Importações públicas

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment,
    MimeType, MessageType, ConversationStatus,
    LabelDefinition, CannedResponse, ErroAPIChatwoot, ErroAnexoChatwoot,
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

## Respostas rápidas — contrato único de entrada

```python
from chatwoot_client import CannedResponse

with CWClient(URL, TOKEN) as cw:
    # GET sem filtro: todas as respostas rápidas da conta.
    todas: list[dict] = cw.canned_responses.list(1)

    # GET com search: filtros por short_code e content no servidor.
    filtradas: list[dict] = cw.canned_responses.list(1, search="gnv")

    # POST e PATCH exigem o mesmo contrato imutável.
    criada: dict = cw.canned_responses.create(
        1, CannedResponse(short_code="gnv_periodica", content="Texto padrão.")
    )
    atualizada: dict = cw.canned_responses.update(
        1, criada["id"], CannedResponse(content="Texto revisado.")
    )

    # DELETE por ID. Não existe restauração automática pela API.
    cw.canned_responses.delete(1, criada["id"])
```

`CannedResponse` contém apenas `short_code` e `content` opcionais; sua dataclass é `frozen=True`. `create()` exige os dois campos e `update()` exige ao menos um. O serializador omite campos `None` e nunca envia metadados de saída. `list()` devolve o array de objetos JSON do Chatwoot (sem envelope `payload`). Não há `list_typed()`, `CannedResponseCreate` nem `CannedResponseUpdate`.

O dashboard aplica `picoSearch` no frontend; o cliente Python faz uma única chamada GET com `search` e respeita a ordenação do servidor. Variáveis Liquid nos conteúdos não são resolvidas por este cliente.

## Restrições de segurança

Contratos tipados são exigidos nas operações modeladas. O consumidor não deve fornecer `dict` onde existe `TextMessage`, `MediaMessage`, `LabelDefinition` ou `CannedResponse`. Os métodos de recursos ainda não modelados continuam espelhando a API com `Mapping`.

Erros de conexão, HTTP ou JSON inválido geram `ErroAPIChatwoot`, sem vazar dados de resposta. A confirmação da API não representa confirmação de entrega WhatsApp. Não há retry implícito de POST/PATCH/DELETE.
