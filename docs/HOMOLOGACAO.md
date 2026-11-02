# Plano de homologação

## Validação local e CI

    python -m pip install -e ".[test]"
    python -m pip check
    python -m pytest -q

Os testes unitários e de contrato usam httpx.MockTransport; não devem disparar mensagens nem acessar VPS.

## Homologação integrada

1. Registrar versão/edição da instalação Chatwoot, base URL e escopo de permissões (sem armazenar token).
2. Executar leituras em conta de testes, incluindo filtros, paginação e consulta por ID.
3. Autorizar separadamente escritas por categoria, verificando estado final, não apenas HTTP 200.
4. Verificar `send_text` público/privado, `send_media` e atalhos de imagem, áudio, vídeo e PDF, multipart com legenda, erros de autorização e timeouts sem reenvio automático.
5. Exercitar caminhos locais na máquina do processo, URLs HTTPS de hosts permitidos, arquivos binários e fluxo aberto; confirmar MIME, nome, limites, fechamento e ausência de Base64.
6. Para mídia recebida de fontes externas/IA, configurar `allowed_hosts` e controles de saída de rede, e verificar bloqueio de URL local, redirecionamentos e tamanhos excedidos.
7. Usar apenas dados de teste para operações de exclusão, mesclagem e alterações administrativas.
8. Validar o consumidor chawoot-hermes-agent com dependência fixada em SHA ou tag, sem alterar as regras homologadas de webhook/worker.
9. Documentar cenário, resultado, ambiente, evidência e pendências, sem dados pessoais ou credenciais.

## Barreiras

Testes simulados não comprovam compatibilidade operacional em servidor real. A promoção à main exige aprovação da regressão, da revisão e dos cenários integrados pertinentes.

## Regressão das operações para Hermes

- `ConversationStatus`: testar cada estado e a compatibilidade de strings legadas.
- Catálogo: criar `LabelDefinition` em conta de teste; conferir cor, campos opcionais e retorno.
- Associação: partir de duas etiquetas existentes, adicionar uma terceira e confirmar que as primeiras persistem; não duplicar na segunda chamada.
- Remoção: remover uma etiqueta e confirmar que as demais permanecem.
- Substituição intencional: confirmar que `replace` continua sobrescrevendo todas.
- Resposta GET inválida/HTTP 5xx: confirmar que `add` não envia POST.
- Concorrência: simular duas alterações em uma conversa e confirmar a necessidade de ordenação por conversa no executor Hermes.
- Mensagem de voz: testar o flag `is_voice_message` com `audio/ogg`, sem pressupor paridade dos adaptadores Evolution e WhatsApp Cloud.

## Canned Responses — cenários de homologação

1. Executar `list(1)` e `list_typed(1)`, conferindo o retorno da lista completa de uma conta de teste.
2. Consultar `search="termo"` por parte do atalho e por parte do conteúdo; conferir que ambas as consultas utilizam GET e que a ordenação acompanha o servidor.
3. Exercitar `CannedResponseCreate` e atualização parcial com `CannedResponseUpdate`, confirmando visualização no dashboard humano.
4. Verificar compatibilidade de `list(1, parametros={"search": "..."})` e dos payloads `Mapping` antigos.
5. Testar entrada inválida, lista vazia, formato JSON inesperado, status 403 e atalho duplicado.
6. Excluir somente uma resposta criada para homologação, com autorização explícita, pois não há restauração pela API.
7. Confirmar que a biblioteca não envia mensagens nem permite que um agente edite o catálogo sem autorização do consumidor.

