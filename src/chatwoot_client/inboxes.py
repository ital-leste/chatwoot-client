"""Consultas de inboxes da Application API do Chatwoot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class InboxesResource:
    """Operações da categoria Inboxes."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int, inbox_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/inboxes/{id}: inbox por ID."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        path = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar a inbox", caminho=path
        )
