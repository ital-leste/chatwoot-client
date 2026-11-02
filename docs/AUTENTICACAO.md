# Autenticação e segurança

A Application API da versão 4.19.0 recomenda Authorization: Bearer TOKEN. O cabeçalho api_access_token permanece legado e pode ser descontinuado.

Existem tokens de usuário, Agent Bot e Platform App com escopos diferentes. A implementação atual cobre a Application API e não substitui a Platform API.

## Exemplo

    from chatwoot_client import CWClient

    with CWClient("https://chatwoot.exemplo", "TOKEN") as cw:
        perfil = cw.profile.get()

    with CWClient("https://chatwoot.exemplo", "TOKEN", auth_mode="api_access_token") as cw:
        perfil = cw.profile.get()

Nunca registrar token ou mensagens sensíveis em logs, nem versionar credenciais em arquivos ou URLs Git. Preferir HTTPS. O sistema consumidor deve autorizar explicitamente ações de escrita, exclusão e publicação.
