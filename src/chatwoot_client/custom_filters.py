"""Custom Filters: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

from .input_validation import validar_opcao

if TYPE_CHECKING:
    from .client import CWClient


class CustomFiltersResource:
    """Recurso Custom Filters."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, filter_type: Literal["conversation", "contact", "report"] | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/custom_filters; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/custom_filters"
        consulta: dict[str, Any] = {
            "filter_type": filter_type,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        if "filter_type" in consulta:
            validar_opcao(consulta["filter_type"], ("conversation", "contact", "report"), "filter_type")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, filter_type: Literal["conversation", "contact", "report"] | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/custom_filters; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        if "type" in data:
            validar_opcao(data["type"], ("conversation", "contact", "report"), "type")
        caminho = f"api/v1/accounts/{account_id}/custom_filters"
        consulta: dict[str, Any] = {
            "filter_type": filter_type,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        if "filter_type" in consulta:
            validar_opcao(consulta["filter_type"], ("conversation", "contact", "report"), "filter_type")
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def get(self, account_id: int, custom_filter_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        caminho = f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, custom_filter_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        if "type" in data:
            validar_opcao(data["type"], ("conversation", "contact", "report"), "type")
        caminho = f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, custom_filter_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        caminho = f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
