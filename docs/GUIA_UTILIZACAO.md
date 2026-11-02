# Guia de utilização

Instalação de desenvolvimento: python -m pip install -e ".[test]".
Testes: python -m pytest -q.

## Consultas

    from chatwoot_client import CWClient

    with CWClient("https://chatwoot.exemplo", "TOKEN", timeout=30) as cw:
        perfil = cw.profile.get()
        conversas = cw.conversations.list(1, status="open", page=1)
        mensagens = cw.messages.list(1, 2)
        contatos = cw.contacts.list(1)
        equipes = cw.teams.list(1)
        bots = cw.account_agentbots.list(1)

## Escritas (somente quando autorizadas)

    cw.messages.create(1, 2, content="Nota privada", private=True)
    cw.conversations.set_status(1, 2, "pending")
    cw.teams.create(1, {"name": "Atendimento"})
    cw.messages.create_with_attachments(
        1, 2, content="Arquivo de teste", private=True,
        attachments=[("teste.txt", b"conteudo", "text/plain")],
    )

Os métodos novos com corpo aceitam um Mapping com os campos oficiais documentados no OpenAPI. Os métodos não aplicam retry automático nem fazem alterações por conta própria.
