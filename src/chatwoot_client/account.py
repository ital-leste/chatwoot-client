"""Consultas de conta da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

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

    def update(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def update_form(self, account_id: int, data: Mapping[str, Any]) -> Any:
        """PATCH /api/v1/accounts/{account_id}, codificado em form-urlencoded."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto de formulário.")
        return self._client._solicitar_json(
            "PATCH", f"api/v1/accounts/{account_id}", formulario=data
        )

