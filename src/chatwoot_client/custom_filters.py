"""Custom Filters: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

from .input_validation import validar_opcao

from .models.application import CustomFilterInput

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

    def create(self, account_id: int, custom_filter: CustomFilterInput, *, filter_type: Literal["conversation", "contact", "report"] | None = None) -> Any:
        """POST com contrato de entrada CustomFilterInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(custom_filter, CustomFilterInput):
            raise TypeError("custom_filter deve ser CustomFilterInput.")
        dados = custom_filter.to_payload(required=["name","type"])

        if filter_type is not None:
            from .input_validation import validar_opcao
            validar_opcao(filter_type, ("conversation", "contact", "report"), "filter_type")
        consulta = {"filter_type": filter_type} if filter_type is not None else None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/custom_filters", dados=dados, parametros=consulta)

    def get(self, account_id: int, custom_filter_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        caminho = f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, custom_filter_id: int, custom_filter: CustomFilterInput) -> Any:
        """PATCH com contrato de entrada CustomFilterInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        if not isinstance(custom_filter, CustomFilterInput):
            raise TypeError("custom_filter deve ser CustomFilterInput.")
        dados = custom_filter.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}", dados=dados, parametros=consulta)

    def delete(self, account_id: int, custom_filter_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(custom_filter_id, "custom_filter_id")
        caminho = f"api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
