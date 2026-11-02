# Guia de utilização

Instalação: `python -m pip install -e ".[test]"`. Testes: `python -m pytest -q`.

## Importações públicas

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Attachment,
    MimeType, MessageVisibility, MessageType,
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
        TextMessage("Verificar documentos.", visibility=MessageVisibility.PRIVATE),
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
