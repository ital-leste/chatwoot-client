"""Consultas de contatos da Application API do Chatwoot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ContactsResource:
    """Operações da categoria Contacts."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int, contact_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/contacts/{id}: contato por ID."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        path = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar o contato", caminho=path
        )
