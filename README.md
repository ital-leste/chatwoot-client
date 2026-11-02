# Chatwoot Client — Ital Leste

Biblioteca Python independente para a **Application API do Chatwoot**, extraída sem alterações funcionais de `ital-leste/chawoot-hermes-agent`, revisão consolidada `122ab821`.

## Uso

```python
from chatwoot_client import CWClient, ErroAPIChatwoot

with CWClient(base_url="https://chatwoot.example", api_token="seu-token") as cw:
    conversa = cw.conversations.get(1, 2)
    mensagens = cw.messages.list(1, 2)
    # Uma escrita requer autorizacao e controle do sistema consumidor:
    # cw.messages.create(1, 2, content="Teste", private=True)
```

O construtor recebe URL, token e timeout explicitamente. O pacote não carrega `.env`, não gerencia sessões Hermes, não recebe webhooks e não persiste lotes. O aplicativo consumidor decide quando uma ação Chatwoot é autorizada.

Os recursos foram ampliados para as 22 categorias documentadas da Application API v4.19.0. Os 16 métodos originalmente extraídos permanecem com suas assinaturas; consulte a matriz completa na documentação para conhecer os 108 métodos adicionais.

## Instalação e testes

```sh
python -m pip install -e ".[test]"
python -m pytest -q
```

A distribuição Python se chama `ital-leste-chatwoot-client`, importada como `chatwoot_client`.

Este repositório é privado. Aplicações externas devem utilizá-lo como dependência Git em uma referência imutável e autenticar o Git pela configuração do ambiente, **nunca com tokens escritos em arquivos versionados**.

## Compatibilidade

- Preservados: `CWClient`, `ErroAPIChatwoot`, `ErroConfiguracaoChatwoot`, recursos, assinaturas, endpoints e retornos JSON existentes.
- `messages.create()` preserva a publicação de texto JSON. `messages.create_with_attachments()` adiciona multipart, e `profile.update_multipart()` suporta atualização de avatar.
- `conversation_labels.replace()` substitui todas as etiquetas.
- `conversation_assignments.assign()` exige exatamente um `assignee_id` ou `team_id`.
- Não existe retry automático para POST; um timeout pode deixar resultado indeterminado.
- O pacote não é automaticamente um plugin do Hermes; futuras ferramentas devem registrar handlers com escopo e autorização própria.

## Governança

Toda evolução do transporte Chatwoot acontece neste repositório. O projeto `chawoot-hermes-agent` importa esta biblioteca, e mantém apenas as decisões de webhook, admissibilidade, persistência, debounce, worker e integração Hermes. Esta extração não autoriza publicação real ou handoff.

Origem: `src/chatwoot_hermes_agent/gateway/chatwoot/` do commit `122ab821`.

## Contratos tipados de mensagens (homolog)

A fronteira pública do pacote exporta `TextMessage`, `MediaMessage`, `Attachment`, `MimeType`, `MessageType` e `MessageVisibility`. O consumo recomendado de mensagens usa `cw.messages.send_text()` ou `send_media()`, com atalhos `send_image()`, `send_audio()`, `send_video()` e `send_document()`. Todos usam o mesmo endpoint oficial sem expor essa característica ao consumidor.

```python
from chatwoot_client import CWClient, TextMessage, MediaMessage, Attachment, MimeType, MessageVisibility

with CWClient("https://chatwoot.example", "TOKEN") as cw:
    cw.messages.send_text(1, 2, TextMessage("Bom dia!"))
    cw.messages.send_text(1, 2, TextMessage("Nota interna", visibility=MessageVisibility.PRIVATE))
    cw.messages.send_document(1, 2, Attachment.from_path("laudo.pdf", mime_type=MimeType.PDF), caption="Segue o laudo")
```

Anexos aceitam caminhos locais, bytes, fluxos binários e URL HTTPS. Para URLs de agentes ou outros sistemas externos, configure `allowed_hosts` no envio e limite tamanho/timeout. A busca remota nunca recebe o token do Chatwoot. Nenhum envio aplica retry implícito. Veja [Guia de utilização](docs/GUIA_UTILIZACAO.md).

## Expansão da Application API (homolog)

Cobertura de código de 124 operações da Application API do Chatwoot v4.19.0. Os contratos anteriores continuam presentes; os novos recursos aceitam payloads data e parâmetros de consulta. Os testes simulados não substituem homologação real da instalação.

- [Arquitetura](docs/ARQUITETURA.md)
- [Matriz dos endpoints](docs/MATRIZ_API.md)
- [Contratos HTTP](docs/CONTRATOS_HTTP.md)
- [Autenticação](docs/AUTENTICACAO.md)
- [Guia de utilização](docs/GUIA_UTILIZACAO.md)
- [Compatibilidade](docs/COMPATIBILIDADE.md)
- [Homologação](docs/HOMOLOGACAO.md)

A autenticação padrão é Bearer; auth_mode="api_access_token" ativa o cabeçalho legado. Anexos podem ser enviados por messages.create_with_attachments(). Nenhuma escrita é repetida automaticamente após timeout.
