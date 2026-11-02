# Arquitetura

## Propósito

Biblioteca Python independente para a Application API Chatwoot 4.19.0. O consumidor fornece base_url e api_token. O pacote não depende de Hermes, Evolution, banco de dados, webhook, .env ou infraestrutura de atendimento.

## Fronteiras e responsabilidades

- `chatwoot_client/__init__.py`: exporta CWClient, models, enums e exceções oficialmente suportados.
- `client.py`: composição dos recursos, autenticação, execução HTTP centralizada em `_request` e verbos privados `_get/_post/_put/_patch/_delete`, retorno e erros. `_solicitar_json` permanece como adaptador retrocompatível.
- `transport.py`: envio HTTP efetivo, JSON, multipart e formulário. Os recursos não acessam httpx diretamente.
- `models/`: contratos imutáveis e validação estrutural, sem leitura de arquivos nem operações de rede no construtor.
- `enums/`: valores oficiais de mensagem, visibilidade, conteúdo e MIME comuns; MIME não é lista exaustiva.
- `attachment_resolver.py`: preparação de caminhos, fluxos, bytes e downloads HTTPS; controla limites e fechamento de arquivos.
- `message_payload.py`: mapeamento de contratos tipados para campos da Application API.
- `messages.py`: operações semânticas send_text/send_media/send_image/send_audio/send_video/send_document, delegando ao mesmo endpoint.
- Demais recursos: operações específicas sem responsabilidade por execução HTTP, autorização de negócio ou runtime Hermes.

## Contratos públicos e compatibilidade

O cliente continua oferecendo os 16 métodos originais e os 108 métodos adicionados. Os métodos existentes mantêm suas assinaturas e continuam compatíveis com payloads livres. A interface preferencial para publicação de mensagens é tipada. A migração dos demais recursos será gradual, conforme importância e capacidade de validação.

O tipo de conteúdo da mensagem (ex.: text) não deve ser confundido com MIME de anexo (ex.: application/pdf). Os modelos validam invariantes; condições externas como arquivo existente ou resposta de URL são avaliadas na execução.

## Segurança e limites

O envio pode produzir efeitos externos: não há retry automático de POST após timeout. O sistema consumidor gerencia idempotência, permissões, handoff e autorização de envio.

URLs de anexos exigem HTTPS, destino DNS global, porta 443, sem credenciais e sem redirecionamentos automáticos; tamanho máximo padrão de 25 MiB por anexo, configurável em cada chamada. O resolvedor aplica `trust_env=False` ao download e jamais envia o token Chatwoot ao host remoto. `allowed_hosts` restringe os domínios; deve ser definido para URLs originadas de entradas não confiáveis (como respostas de agentes). O filtro DNS reduz riscos de SSRF, mas, por limitações da resolução DNS/TOCTOU, não substitui controles de egress/allowlist do ambiente. Arquivos obtidos de URLs são copiados em chunks para arquivo temporário; caminhos locais são abertos por streaming. Fluxos do consumidor não são fechados pela biblioteca.

## Publicação

Desenvolvimento em homolog. Main preservada até homologação real, regressão e aprovação da mudança.
