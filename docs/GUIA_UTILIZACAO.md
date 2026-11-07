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

## Como escolher a entrada

Métodos simples recebem argumentos nomeados; métodos modelados exigem seus contratos de entrada. **Nos demais métodos, utilize diretamente os campos documentados na Application API**, normalmente por `Mapping[str, Any]`:

```python
# Campanhas usam payload variável da API, encapsulado sob "campaign".
cw.campaigns.update(1, 7, {"enabled": False})
```

Os modelos são apenas de entrada. Os retornos permanecem em `dict`, `list` ou `None` conforme cada endpoint, sem objetos de saída próprios.

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
cw.conversations.toggle_priority(1, 9, priority=ConversationPriority.LOW)

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

`create()` exige `ConversationCreate`. Os métodos simples não possuem dataclasses redundantes. `toggle_priority()` exige `priority` explícito; `update()` aceita `priority`, `sla_policy_id` ou ambos, exigindo ao menos um campo. `priority=None` é uma solicitação **explícita** de limpeza (não é ausência). O contrato `FilterCondition` usa os mesmos campos de filtro no Chatwoot para contatos e conversas. Sua validação é estrutural; a validade de cada operador para cada atributo cabe ao backend.

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

Os validadores locais verificam formatos simples de e-mail, E.164 para telefone, tipos básicos e objetos JSON válidos, mas a conta Chatwoot continua validando unicidade e atributos configurados. Dicionários JSON são copiados defensivamente e revalidados ao serializar: a imutabilidade da dataclass não deve ser confundida com imutabilidade profunda dos valores aninhados. O contrato suporta `avatar` como campo textual do payload JSON oficial e `avatar_url`; upload binário direto de avatar do contato não é implementado por este método.

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

A interface de entrada usa parâmetros nomeados tipados em operações simples e contratos de domínio quando há estrutura ou validações que os justificam. Não forneça dicionários onde a operação exige `TextMessage`, `MediaMessage`, `LabelDefinition`, `Contact`, `ConversationCreate` ou `FilterCondition`. Recursos ainda não modelados continuam espelhando a API com `Mapping`.

Erros de conexão, HTTP ou JSON inválido geram `ErroAPIChatwoot`, sem vazar dados de resposta. A confirmação da API não representa confirmação de entrega WhatsApp. Não há retry implícito de POST/PATCH/DELETE.

## Revisão contratual 07/11/2026 — operações administrativas

As entradas simples abaixo deixam de receber `data: Mapping`, passando a aceitar
parâmetros nomeados. Não existe duplicação do método com payload legado.

```python
# Associar contato, mesclar contatos e substituir etiquetas de contato.
cw.contacts.add_inbox(1, 42, inbox_id=3, source_id="canal-whatsapp")
cw.contacts.merge(1, base_contact_id=42, mergee_contact_id=43)
cw.contact_labels.replace(1, 42, ["aguardando-laudo"])

# Associar/desassociar AgentBot e gerir membros da inbox.
cw.inboxes.set_agent_bot(1, 3, agent_bot=5)
cw.inboxes.set_agent_bot(1, 3, agent_bot=None)
cw.inboxes.add_member(1, inbox_id=3, user_ids=[10, 11])
cw.inboxes.update_members(1, inbox_id=3, user_ids=[10])
cw.inboxes.remove_members(1, inbox_id=3, user_ids=[11])

# Gerenciamento de equipes, atualização de status de mensagem.
cw.teams.add_members(1, 2, [10])
cw.teams.remove_members(1, 2, [11])
cw.messages.update_status(1, 9, 100, status="failed", external_error="motivo")

# Agentes e webhooks com opções tipadas.
cw.agents.create(1, name="João", email="joao@example.com", role="agent")
cw.agents.update(1, 10, role="administrator", availability="busy")
cw.webhooks.create(
    1, url="https://hooks.example.com/receiver",
    subscriptions=["message_created"],
)
cw.webhooks.update(1, 5, name="Receptor principal")

# Campanhas preservam o envelope obrigatório da API.
cw.campaigns.create(1, {"title": "Teste", "enabled": False})
cw.campaigns.update(1, 5, {"enabled": False})

# Enums de consulta devem coincidir com as opções do Swagger.
cw.reports.list_conversation_statistics(
    1, metric="conversations_count", type_="account"
)
cw.reports.outgoing_messages_count(1, group_by="inbox")
cw.custom_attributes.list(1, attribute_model="0")
cw.custom_filters.list(1, filter_type="conversation")
cw.audit_logs.list(1, sort="desc")
```

Os exemplos de mutação acima são ilustrativos e exigem permissões e autorização
para qualquer uso contra Chatwoot real. `merge()` é potencialmente irreversível;
`replace()` substitui todas as etiquetas. O envio de `agent_bot=None` requer
homologação real da regra de desvinculação do servidor 4.19.0.

As operações de inbox, AgentBots, automações, atributos, filtros, Help Center e integrações
recebem **contratos dataclass de entrada**. Campos de estrutura dinâmica dentro desses
contratos (como `channel`, `bot_config`, `actions`, `conditions` e `settings`)
continuam aceitando objetos/arrays JSON da API, sem inventar subclasses de canais ou
mapeamentos específicos de outros consumidores. Veja [catálogo dos contratos](CATALOGO_CONTRATOS.md).

## Novos contratos administrativos de entrada

```python
from chatwoot_client import (
    CWClient, AgentBotInput, InboxSettingsInput, AutomationRuleInput,
    CustomAttributeInput, CustomFilterInput, HelpCenterPortalInput,
    HelpCenterCategoryInput, HelpCenterArticleInput, IntegrationHookInput,
    AccountSettingsInput, ProfileInput,
)

# Campos ausentes não são enviados no PATCH.
cw.account.update(1, AccountSettingsInput(auto_resolve_ignore_waiting=False))
cw.account_agentbots.create(1, AgentBotInput(name="Atendimento", outgoing_url="https://bot.example/hook"))
cw.account_agentbots.update(1, 2, AgentBotInput(bot_config={"modo": "teste"}))
cw.inboxes.create(1, InboxSettingsInput(name="API", channel={"type": "Channel::Api"}))
cw.inboxes.update(1, 3, InboxSettingsInput(name="Nova identificação"))
cw.automation_rules.create(1, AutomationRuleInput(
    name="Etiquetar", event_name="message_created",
    actions=[{"action_name": "add_label", "action_params": ["triagem"]}],
    conditions=[], active=False,
))
cw.custom_attributes.create(1, CustomAttributeInput(
    attribute_key="placa", attribute_display_name="Placa", attribute_model=0,
))
cw.custom_filters.create(1, CustomFilterInput(
    name="Pendentes", type="conversation", query={"payload": []},
))
cw.help_center.create(1, HelpCenterPortalInput(name="Central", slug="central"))
cw.help_center.create_category(1, "central", HelpCenterCategoryInput(name="Dúvidas"))
cw.help_center.create_article(1, "central", HelpCenterArticleInput(
    title="Guia", content="Conteúdo", category_id=1,
))
cw.integrations.create_hook(1, IntegrationHookInput(app_id=2, inbox_id=3, settings={}))
cw.profile.update(ProfileInput(display_name="Atendimento"))

# Operações simples sem dataclasses redundantes.
cw.labels.update(1, 3, color="#123456", show_on_sidebar=False)
cw.teams.create(1, name="Suporte", allow_auto_assign=False)
cw.inboxes.update_branded_email_layout(1, branded_email_layout=None)
cw.conversations.update(1, 3, sla_policy_id=10)
```

Os exemplos são demonstrativos: não executá-los sem dados de teste, permissão e aprovação
para escrita na instalação real. `profile.update()` serializa `{"profile": {...}}`.
`campaigns.create/update()` mantém `{"campaign": {...}}` com campos variáveis.
`account.update_form()` e `profile.update_multipart()` são caminhos alternativos de
transporte para endpoints já existentes, não novas rotas.
