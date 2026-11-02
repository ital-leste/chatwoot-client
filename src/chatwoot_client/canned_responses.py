"""Canned Responses: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class CannedResponsesResource:
    """Recurso Canned Responses."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/canned_responses; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/canned_responses; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update(self, account_id: int, canned_response_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/canned_responses/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, canned_response_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/canned_responses/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(canned_response_id, "canned_response_id")
        caminho = f"api/v1/accounts/{account_id}/canned_responses/{canned_response_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
