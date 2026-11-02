# Guia de utilização

Instalação: `python -m pip install -e ".[test]"`. Testes: `python -m pytest -q`.

## Importações públicas

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment,
    MimeType, ConversationStatus, LabelDefinition, MessageType,
    ErroAPIChatwoot, ErroAnexoChatwoot,
)
```

## Consultas

```python
with CWClient("https://chatwoot.exemplo", "TOKEN", timeout=30) as cw:
    perfil = cw.profile.get()
    conversas = cw.conversations.list(1, status="open", page=1)
    mensagens = cw.messages.list(1, 2)
    contatos = cw.contacts.list(1)
```

## Enviar texto público ou nota interna

```python
with CWClient("https://chatwoot.exemplo", "TOKEN") as cw:
    cw.messages.send_text(1, 2, TextMessage("Bom dia!"))
    cw.messages.send_text(
        1, 2,
        TextMessage("Verificar documentos.", private=True),
    )
```

## PDF local com legenda

```python
with CWClient("https://chatwoot.exemplo", "TOKEN") as cw:
    arquivo = Attachment.from_path("laudo.pdf", mime_type=MimeType.PDF)
    cw.messages.send_document(1, 2, arquivo, caption="Segue o laudo solicitado.")
```

A abertura do arquivo ocorre no envio, não no construtor de `Attachment`. O `Path` deve existir onde o processo Python está executando; caminho local de um computador não é automaticamente acessível em outra VPS.

## PDF por URL HTTPS

```python
with CWClient("https://chatwoot.exemplo", "TOKEN") as cw:
    arquivo = Attachment.from_url(
        "https://arquivos.exemplo.com/laudo.pdf",
        mime_type=MimeType.PDF,
    )
    cw.messages.send_document(
        1, 2, arquivo, caption="Laudo",
        allowed_hosts={"arquivos.exemplo.com"},
        max_bytes=25 * 1024 * 1024,
        url_timeout=30.0,
    )
```

URLs não são encaminhadas ao endpoint de mensagens: o resolvedor baixa o conteúdo em chunks, sem token Chatwoot, em cliente HTTP isolado. Somente HTTPS público, porta 443, sem redirecionamentos automáticos. Para entradas externas/IA, `allowed_hosts` é fortemente recomendado, além de restrições de rede (egress).

## Bytes, fluxos e envio de vários anexos

```python
arquivo = Attachment(source=b"%PDF-1.4...", filename="laudo.pdf", mime_type=MimeType.PDF)
mensagem = MediaMessage(
    caption="Dois documentos",
    attachments=[
        arquivo,
        Attachment.from_path("segundo.pdf"),
    ],
)
cw.messages.send_media(1, 2, mensagem)
```

Para um fluxo aberto em modo `rb`, informe `filename` e `mime_type`. A biblioteca copia esse fluxo para armazenamento temporário limitado e não fecha o fluxo fornecido pelo consumidor.

## Atalhos por tipo

`send_image`, `send_audio`, `send_video` e `send_document` aceitam um `Attachment`, legenda opcional e parâmetros de visibilidade. Verificam a família do MIME antes de publicar. `send_media` aceita um `MediaMessage` com vários anexos. O resultado é sempre uma requisição multipart por chamada.

## Compatibilidade

Continuam disponíveis `messages.create(1, 2, content="...", private=True)`, `messages.create_with_attachments(...)`, e os outros métodos que aceitam `Mapping[str, Any]`. Todos os recursos usam o transporte centralizado; nenhuma publicação é repetida automaticamente após timeout. A confirmação HTTP não constitui comprovante de entrega ao WhatsApp.

## Mensagem de voz (áudio OGG)

```python
cw.messages.send_media(
    1, 2,
    MediaMessage(
        attachments=[Attachment.from_path("gravacao.ogg", mime_type=MimeType.OGG)],
        is_voice_message=True,
        private=False,
    ),
)
```

O Chatwoot aceita `is_voice_message` e marca o anexo como voz. A biblioteca exige um único arquivo `audio/ogg` para esse modo; o formato final da entrega depende da integração do canal. O flag é omitido para áudio comum. `send_image/audio/video/document` continuam disponíveis por compatibilidade, mas a interface preferencial para mídia é `send_media()`.

## Status de conversa com enumeração

```python
cw.conversations.set_status(1, 2, ConversationStatus.PENDING)
cw.conversations.set_status(1, 2, ConversationStatus.RESOLVED)
```

Valores: `OPEN`, `PENDING`, `RESOLVED` e `SNOOZED`. A forma legada `set_status(1, 2, "pending")` continua suportada. Para `SNOOZED` pode-se definir `snoozed_until` em segundos Unix. A semântica de handoff ao mudar de pending para open depende das regras do Chatwoot e do ator autenticado.

## Etiquetas do catálogo e associação na conversa

Criar uma etiqueta no catálogo da conta é diferente de associá-la à conversa:

```python
etiqueta = LabelDefinition(
    title="aguardando-laudo",
    color="#224466",
    description="Documentação solicitada",
)
cw.labels.create_label(1, etiqueta)

# Preserva as etiquetas atuais e acrescenta uma nova.
cw.conversation_labels.add(1, 2, "aguardando-laudo")

# Acrescenta várias, sem duplicar:
cw.conversation_labels.add(1, 2, ["hermes-ativo", "aguardando-laudo"])

# Remove uma etiqueta preservando as demais:
cw.conversation_labels.remove(1, 2, "hermes-ativo")

# API legada: substituição completa e deliberada da lista
cw.conversation_labels.replace(1, 2, ["aguardando-laudo"])
```

`add` e `remove` executam GET das etiquetas existentes e POST da lista consolidada apenas quando necessário. A resposta GET deve conter `{"payload": ["etiqueta", ...]}`; se estiver inválida, a biblioteca falha sem executar substituição potencialmente destrutiva. Essas operações não são atômicas: para várias automações alterando a mesma conversa, serializar no executor/worker por `account_id` e `conversation_id` é necessário para evitar lost updates. `cw.labels.create_label` não cria associações por conta própria; não existe criação automática de etiquetas desconhecidas ao chamar `add`.

## Respostas rápidas — catálogo e filtros

O recurso `canned_responses` oferece GET de todas as respostas ou de respostas filtradas, usando o mesmo endpoint. O filtro `search` é aplicado no banco do Chatwoot 4.19.0 sobre `short_code` e `content`; a ordenação é determinada pelo servidor.

```python
from chatwoot_client import CannedResponse, CannedResponseCreate, CannedResponseUpdate

# Retorno legado: lista JSON sem envelope payload.
todas_raw = cw.canned_responses.list(1)
filtradas_raw = cw.canned_responses.list(1, search="gnv")
legado = cw.canned_responses.list(1, parametros={"search": "gnv"})

# Contrato tipado: mesma consulta GET, sem filtros locais.
todas = cw.canned_responses.list_typed(1)
filtradas = cw.canned_responses.list_typed(1, search="gnv")
for resposta in filtradas:
    assert isinstance(resposta, CannedResponse)
    print(resposta.short_code, resposta.content)

# Escrita tipada, mantendo métodos e respostas JSON atuais.
criada = cw.canned_responses.create(
    1, CannedResponseCreate(
        short_code="inspecao_gnv", content="Consulte os documentos exigidos."
    )
)
atualizada = cw.canned_responses.update(
    1, criada["id"], CannedResponseUpdate(content="Texto corrigido.")
)
# A exclusão não tem desfazimento na API:
# cw.canned_responses.delete(1, criada["id"])
```

`CannedResponseCreate` exige `short_code` e `content` não vazios; `CannedResponseUpdate` exige ao menos um deles. Os dois contratos não executam HTTP ao serem instanciados. `list_typed` verifica o array e cada objeto retornado; as datas do servidor permanecem como strings ISO. `create/update` preservam também entrada `Mapping[str, Any]`.

O dashboard usa pesquisa dinâmica local; o cliente envia um único GET com ou sem `search`. A busca do servidor não é obrigada a replicar exatamente a ordenação do frontend. Nenhum conteúdo é automaticamente enviado ao contato, nem variáveis Liquid são substituídas pelo cliente HTTP.

