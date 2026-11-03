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
11. Para Contacts, criar/atualizar com `Contact`, garantindo que `Contact(name="Novo")` envie somente `name`, não leia o contato previamente e não produza chaves `email`, `phone_number` ou outras ausentes.
12. Diferenciar `Contact(email=None)` (JSON `null`) de e-mail omitido; manter `blocked=False`, dicionários vazios e mesclagem dos atributos sob a regra do backend.
13. Rejeitar antes do HTTP e-mail inválido, telefone fora de E.164, payload vazio, objetos com campos inválidos e dados não JSON; verificar create com inbox e retorno `payload.contact`.
14. Criar conversa somente com `ConversationCreate`, exigindo `source_id` e preservando retornos JSON com campos adicionais; rejeitar status/IDs/mensagens inválidos antes do HTTP.
15. Usar `FilterCondition` em `contacts.filter()` e `conversations.filter()`, verificando envelopes diferentes de `conversations.list()` e `conversations.filter()` e rejeitando listas livres de dicionários.
16. Confirmar prioridade tipada para `update()`/`toggle_priority()`, `priority=None` explícito, digitação `on/off` e `is_private: bool` sem entrada Mapping.
17. Verificar que `update_custom_attributes()` envia `merge=True` como padrão, que `merge=False` substitui deliberadamente e que `delete_custom_attributes(keys=...)` remove apenas chaves solicitadas; nenhuma leitura/atualização adicional.
18. Testar saída `None` para `head :ok`, status/handoff por `set_status()` e que os recursos de conversas preservam as 13 rotas HTTP oficiais.

19. Confirmar que URL de configuração com tipo inválido gera `ErroConfiguracaoChatwoot`, não `AttributeError`.
20. Confirmar que objetos JSON recebidos por `Contact` e `ConversationCreate` são copiados e revalidados na serialização, sem permitir dados não JSON nem uma mensagem sem `content` válido após a construção.
21. Rejeitar cursores de mensagens com tipos incorretos e valores negativos antes de HTTP, preservando o cursor zero usado em integrações existentes.

## Homologação integrada posterior

Registrar versão/edição da instalação Chatwoot, URL e permissões, sem tokens em relatórios. Executar leituras reais primeiro. Qualquer POST, PATCH ou DELETE real deve ser autorizado por categoria e usar somente dados de teste, com verificação posterior do estado no dashboard.

Validar separadamente o comportamento de quaisquer canais e aplicações que consumirem a biblioteca, inclusive mídia e mensagens privadas. HTTP 2xx do Chatwoot não comprova entrega final em outro canal. Os consumidores devem fixar SHA/tag da biblioteca e homologar suas operações antes de promover versões a produção.

A aprovação do CI verifica contratos simulados, não homologação operacional na instalação real.
