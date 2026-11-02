"""Consultas de conta da Application API do Chatwoot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class AccountResource:
    """Operações da categoria Account."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}: detalhes da conta."""
        self._client._validar_id(account_id, "account_id")
        path = f"api/v1/accounts/{account_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar a conta", caminho=path
        )
