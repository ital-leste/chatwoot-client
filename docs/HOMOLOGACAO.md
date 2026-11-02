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
4. Verificar mensagens públicas e notas privadas, multipart, erros de autorização e timeouts sem reenvio automático.
5. Usar apenas dados de teste para operações de exclusão, mesclagem e alterações administrativas.
6. Validar o consumidor chawoot-hermes-agent com dependência fixada em SHA ou tag, sem alterar as regras homologadas de webhook/worker.
7. Documentar cenário, resultado, ambiente, evidência e pendências, sem dados pessoais ou credenciais.

## Barreiras

Testes simulados não comprovam compatibilidade operacional em servidor real. A promoção à main exige aprovação da regressão, da revisão e dos cenários integrados pertinentes.
