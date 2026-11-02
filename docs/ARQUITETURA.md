# Arquitetura

## Propósito

Biblioteca Python independente para a Application API Chatwoot. O consumidor fornece base_url e api_token. A biblioteca não depende de Hermes, Evolution, banco de dados, webhook, .env ou infraestrutura de atendimento.

## Camadas

- client.py: objeto CWClient, registro de recursos, validação e interpretação de erros.
- transport.py: execução HTTP com sessão compartilhada, JSON e multipart. Sem retries automáticos.
- Módulos por recurso: classes para Account, Contacts, Conversations, Messages, Agents, Inboxes, Teams, Webhooks, Reports e demais categorias oficiais.
- tests/: contratos simulados usando httpx.MockTransport e regressão dos métodos originais.

## Contratos públicos

Os 16 métodos extraídos do gateway preservam assinatura, caminho e comportamento JSON. Métodos expandidos que precisam de corpo aceitam data: Mapping[str, Any]; consultas apresentam argumentos extraídos da especificação e parametros adicional quando necessário. Sucessos sem corpo retornam None.

## Limites

Cabe à aplicação consumidora: autorizar escritas, persistir e reprocessar eventos, decidir handoff, correlacionar mensagens, tratar idempotência e executar políticas de negócio. O pacote não decide o fluxo de um atendimento.

## Publicação

O desenvolvimento acontece em homolog. Main não deve receber mudanças antes de testes, homologação autorizada e revisão de compatibilidade.
