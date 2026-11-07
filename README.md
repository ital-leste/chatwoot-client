# Chatwoot Python Client

Cliente Python para a **Application API do Chatwoot**, com recursos HTTP organizados por domínio, entradas tipadas quando necessário e **retorno JSON nativo da API**. Pode ser utilizado por scripts, aplicações web, serviços e integrações, sem dependência de uma aplicação consumidora específica.

> **Estado:** homologação baseada no Chatwoot **4.19.0**. A suíte automatizada valida entradas, contratos e requisições HTTP simuladas. O comportamento com uma instalação real deve ser homologado separadamente.

## Instalação

Requer Python **3.11+** e utiliza `httpx` para o transporte HTTP. Na raiz do repositório:

```bash
python -m pip install -e .
```

Para instalar as dependências de teste e executar a regressão:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

Distribuição: `ital-leste-chatwoot-client`. Importação: `chatwoot_client`.

## Primeiro uso

```python
from chatwoot_client import CWClient

with CWClient("https://chatwoot.exemplo", "SEU_TOKEN") as cw:
    perfil = cw.profile.get()
    contatos = cw.contacts.list(1, page=1)
    conversas = cw.conversations.list(1, status="open", page=1)

    print(perfil)
    print(contatos["payload"])
    print(conversas["data"]["payload"])
```

`CWClient` recebe a URL da instalação e o token diretamente. A biblioteca não lê arquivos `.env` ou variáveis de ambiente automaticamente. O gerenciador `with` fecha a sessão HTTP. A autenticação padrão usa `Authorization: Bearer TOKEN`; instalações com cabeçalho legado podem usar `auth_mode="api_access_token"`. Veja [Autenticação](docs/AUTENTICACAO.md).

## Como fornecer os dados

Há três estilos de entrada, escolhidos pela complexidade do recurso:

| Entrada | Uso | Exemplo |
|---|---|---|
| **Argumentos tipados** | Campos simples e parâmetros de consulta | `cw.canned_responses.create(1, short_code="prazo", content="Retornaremos em breve.")` |
| **Contrato tipado** | Entrada estruturada com validações | `cw.contacts.update(1, 42, Contact(name="Maria"))` |
| **Payload da API** | Método sem contrato específico | `cw.labels.update(1, 7, {"description": "Atendimento"})` |

**Quando não houver um contrato de entrada próprio, utilize diretamente os campos e a estrutura documentados pela Application API**, geralmente passando `dict` ou `Mapping[str, Any]`. Não é necessário criar uma dataclass para toda operação.

Modelos de entrada disponíveis: `Contact`, `ConversationCreate`, `FilterCondition`, `TextMessage`, `MediaMessage`, `Attachment` e `LabelDefinition`. Enumerações incluem `ConversationStatus`, `ConversationPriority`, `MessageType` e `MimeType`.

### Exemplo de atualização parcial de contato

```python
from chatwoot_client import CWClient, Contact

with CWClient("https://chatwoot.exemplo", "SEU_TOKEN") as cw:
    criado = cw.contacts.create(
        1, Contact(name="Maria", phone_number="+5511999999999"), inbox_id=1
    )
    contato_id = criado["payload"]["contact"]["id"]
    cw.contacts.update(1, contato_id, Contact(name="Maria Silva"))
```

O `update` acima envia somente `{"name": "Maria Silva"}`. Campos **omitidos** não entram no JSON e não substituem valores cadastrados. Um `None` **explicitamente informado** é enviado como JSON `null`, sujeito às regras do Chatwoot. As validações locais verificam tipos e formatos básicos; unicidade e permissões permanecem sob responsabilidade do servidor.

### Exemplo de conversas e mensagens

```python
from chatwoot_client import (
    CWClient, ConversationCreate, ConversationStatus,
    ConversationPriority, FilterCondition, TextMessage,
)

with CWClient("https://chatwoot.exemplo", "SEU_TOKEN") as cw:
    criada = cw.conversations.create(
        1, ConversationCreate(source_id="origem-do-canal", inbox_id=1, contact_id=42)
    )
    cw.conversations.set_status(1, 9, ConversationStatus.PENDING)
    cw.conversations.update(1, 9, priority=ConversationPriority.HIGH)

    # Preserva as outras chaves: merge=True é o padrão do cliente.
    cw.conversations.update_custom_attributes(
        1, 9, custom_attributes={"interesse": "gnv"}
    )

    filtro = FilterCondition(
        attribute_key="status", filter_operator="equal_to", values=["pending"]
    )
    filtradas = cw.conversations.filter(1, [filtro])
    enviada = cw.messages.send_text(1, 9, TextMessage("Olá!"))
```

`FilterCondition` é usado por `contacts.filter()` e `conversations.filter()`. Para enviar anexos, utilize `MediaMessage` e `Attachment`, com suporte a caminhos, bytes, streams e URLs HTTPS sujeitas às verificações do cliente. Veja o [guia de utilização](docs/GUIA_UTILIZACAO.md).

## Saídas e erros

Cada método retorna **o JSON nativo da API** (`dict`, `list` ou `None` quando não existe corpo). Os envelopes variam conforme o recurso e não são normalizados:

- `contacts.list()` → `{"meta": {...}, "payload": [...]}`
- `conversations.list()` → `{"data": {"meta": {...}, "payload": [...]}}`
- `canned_responses.list()` → `[...]`

Paginação, cursores e metadados são preservados; não há agregação automática de páginas. Falhas HTTP, de conexão ou de JSON geram `ErroAPIChatwoot`, que informa o caminho e, quando disponível, o status HTTP, sem incluir o corpo completo nem o token na mensagem de erro. **Escritas não são repetidas automaticamente após timeout.**

## Organização e documentação

`client.py` compõe os recursos; `transport.py` executa requisições; `models/` abriga somente os contratos de **entrada** necessários; `enums/` reúne valores tipados; e os demais módulos de `src/chatwoot_client/` implementam as operações por recurso.

A matriz documenta **124 pares verbo/rota mapeados** da Application API 4.19.0. Mapeamento e testes simulados não demonstram, por si só, a execução bem-sucedida de todos esses endpoints em uma instalação real.

**Evolução em `homolog` (07/11/2026):** auditoria por rota, com 124 pares
verbo/rota preservados, e padronização de operações administrativas, parâmetros
de relatórios e envelope de campanhas. Veja
[Auditoria contratual](docs/AUDITORIA_CONTRATUAL.md) e
[Matriz da API](docs/MATRIZ_API.md). A homologação integrada por endpoint
continua distinta da execução de testes simulados.


| Documento | Finalidade |
|---|---|
| [Guia de utilização](docs/GUIA_UTILIZACAO.md) | Exemplos e assinaturas modeladas |
| [Matriz da API](docs/MATRIZ_API.md) | Verbos, rotas e recursos |
| [Entradas por rota](docs/ESPECIFICACAO_ENTRADAS.md) | Query obrigatória, requestBody e MIME declarados no Swagger 4.19.0 |
| [Arquitetura](docs/ARQUITETURA.md) | Responsabilidades e limites |
| [Contratos HTTP](docs/CONTRATOS_HTTP.md) | Requisições, respostas e falhas |
| [Autenticação](docs/AUTENTICACAO.md) | Credenciais e modos de autenticação |
| [Compatibilidade](docs/COMPATIBILIDADE.md) | Versões e restrições |
| [Homologação](docs/HOMOLOGACAO.md) | Testes e validação integrada |
| [Changelog](CHANGELOG.md) | Histórico de alterações |
