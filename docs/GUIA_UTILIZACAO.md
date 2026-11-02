# Guia de utilização

Instalação: `python -m pip install -e ".[test]"`. Validação: `python -m pytest -q`.

## Importações públicas

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment,
    MimeType, MessageType, ConversationStatus,
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
