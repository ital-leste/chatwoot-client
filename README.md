# Chatwoot Client — Ital Leste

Cliente Python independente para a **Application API do Chatwoot 4.19.0**. A biblioteca foi extraída da integração Chatwoot–Hermes e concentra autenticação, recursos HTTP, contratos de entrada, serialização, tratamento de erros e downloads controlados de anexos. Não importa .env, não persiste lotes nem executa decisões do Hermes.

## Regra de arquitetura

**Entradas tipadas conforme a complexidade e saída JSON nativa da API.** Operações simples recebem argumentos nomeados com tipos Python; estruturas com regras próprias utilizam dataclasses. Recursos ainda não modelados podem receber `Mapping[str, Any]`. O pacote verifica erros HTTP/JSON e formatos estruturais conhecidos, sem criar dataclasses para retornos.

```python
from chatwoot_client import (
    CWClient, TextMessage, MediaMessage, Contact,
    Attachment, MimeType, LabelDefinition, ConversationStatus,
)

with CWClient("https://chatwoot.exemplo", "TOKEN") as cw:
    # Texto público ou nota interna
    enviado = cw.messages.send_text(1, 2, TextMessage("Bom dia!"))
    cw.messages.send_text(1, 2, TextMessage("Conferir documento", private=True))

    # Um único método para imagem, áudio, vídeo ou documento
    cw.messages.send_media(1, 2, MediaMessage(
        attachments=[Attachment.from_path("laudo.pdf", mime_type=MimeType.PDF)],
        caption="Segue o laudo",
    ))

    # Atualização de status por enumeração
    cw.conversations.set_status(1, 2, ConversationStatus.PENDING)

    # Etiqueta por contrato; adicionar à conversa sem apagar as antigas
    cw.labels.create(1, LabelDefinition("aguardando-laudo", "#224466"))
    cw.conversation_labels.add(1, 2, "aguardando-laudo")

    # Atualização de contato: não altera campos omitidos
    contato = cw.contacts.update(1, 42, Contact(name="Maria Souza"))

    # Canned Responses: parâmetros nomeados e JSON nativo de saída
    criada = cw.canned_responses.create(
        1, short_code="gnv", content="Informações sobre inspeção GNV."
    )
    todas = cw.canned_responses.list(1)
    filtradas = cw.canned_responses.list(1, search="gnv")
    atualizada = cw.canned_responses.update(
        1, criada["id"], content="Texto revisado."
    )
```

## Instalação e testes

```sh
python -m pip install -e ".[test]"
python -m pytest -q
```

O pacote de distribuição chama-se `ital-leste-chatwoot-client` e é importado como `chatwoot_client`. O repositório é privado: outros projetos devem fixar uma revisão Git e configurar a autenticação fora dos arquivos versionados.

## Integração e segurança

O transporte não repete automaticamente escritas após timeout. Resposta HTTP bem-sucedida não garante entrega no WhatsApp. A aplicação consumidora decide autorização, idempotência, serialização de alterações concorrentes e handoff. Anexos por URL exigem HTTPS e podem ser restritos por `allowed_hosts`; ver o [guia](docs/GUIA_UTILIZACAO.md).

## Documentação

- [Arquitetura](docs/ARQUITETURA.md)
- [Guia de utilização](docs/GUIA_UTILIZACAO.md)
- [Matriz da Application API](docs/MATRIZ_API.md)
- [Contratos HTTP](docs/CONTRATOS_HTTP.md)
- [Autenticação](docs/AUTENTICACAO.md)
- [Compatibilidade](docs/COMPATIBILIDADE.md)
- [Homologação](docs/HOMOLOGACAO.md)

A matriz mantém cobertura dos 124 pares verbo/rota mapeados, não o compromisso de preservar todas as antigas assinaturas Python. Alterações de interfaces anteriores foram feitas ainda em homologação.
