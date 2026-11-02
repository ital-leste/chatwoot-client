"""Consultas de atendentes da Application API do Chatwoot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class AgentsResource:
    """Operações da categoria Agents."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int) -> list[Any]:
        """GET /api/v1/accounts/{account_id}/agents: atendentes da conta."""
        self._client._validar_id(account_id, "account_id")
        path = f"api/v1/accounts/{account_id}/agents"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_lista(
            response, operacao="listar os atendentes", caminho=path
        )
