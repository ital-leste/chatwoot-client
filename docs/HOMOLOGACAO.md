# Plano de homologação

## Regressão sem acesso à VPS

```sh
python -m pip install -e ".[test]"
python -m pip check
python -m pytest -q
```

Os testes usam `httpx.MockTransport` e não podem enviar mensagens reais, excluir dados reais nem consumir credenciais do ambiente.

## Cenários mínimos

1. Testar `messages.send_text(TextMessage)` público e privado, JSON gerado, retorno nativo e erro sem reenvio.
2. Testar `messages.send_media(MediaMessage)` com PDF, imagem, áudio, vídeo, bytes, arquivo local, stream e HTTPS permitido; validar nome/MIME, múltiplos anexos, `is_voice_message`, tamanho e bloqueios SSRF.
3. Conferir `conversations.set_status(ConversationStatus)`, incluindo `SNOOZED` e `snoozed_until`, rejeitando strings.
4. Criar `LabelDefinition` via `labels.create()`; verificar campos, retorno JSON e falhas antes do envio.
5. Incluir e remover etiquetas de conversas, sem duplicar nem apagar outras; em erro no GET, não disparar POST. Testar concorrência de alterações no executor.
6. Listar Canned Responses com e sem `search`, sempre por GET, conferindo o array JSON original e a filtragem por atalho/conteúdo.
7. Criar e atualizar parcialmente respostas rápidas com parâmetros nomeados `short_code`/`content`, exigindo os campos necessários por operação; rejeitar entrada por `Mapping` e campos vazios antes do HTTP.
8. Confirmar que `CannedResponse`, `list_typed`, `CannedResponseCreate`, `CannedResponseUpdate`, `messages.create`, `messages.create_with_attachments`, `send_document`, `labels.create_label` e `MessageVisibility` não são interfaces públicas oficiais.
9. Testar HTTP 403/422/503, JSON inválido e corpo vazio, sem retry automático de escrita; confirmar que campos extras de retorno não são descartados.
10. Confirmar que os recursos sem contratos específicos continuam podendo utilizar payloads da API, mantendo cobertura dos verbos/rotas da matriz.

## Homologação integrada posterior

Registrar versão/edição da instalação Chatwoot, URL e permissões, sem tokens em relatórios. Executar leituras reais primeiro. Qualquer POST, PATCH ou DELETE real deve ser autorizado por categoria e usar somente dados de teste, com verificação posterior do estado no dashboard.

Validar as saídas via Evolution/WhatsApp, inclusive mídia e notas privadas; HTTP 2xx não comprova entrega final. Atualizar o consumidor Chatwoot–Hermes na sua própria branch de homologação, fixando dependência em SHA/tag, antes de promover a integração a produção.

A aprovação do CI verifica contratos simulados, não homologação operacional na instalação real.
