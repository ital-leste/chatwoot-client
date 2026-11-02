"""Help Center: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class HelpCenterResource:
    """Recurso Help Center."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/portals; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/portals"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/portals; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/portals"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def get(self, account_id: int, portal_id: str | int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/portals/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        caminho = f"api/v1/accounts/{account_id}/portals/{portal_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, portal_id: str | int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/portals/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/portals/{portal_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def create_category(self, account_id: int, portal_id: str | int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/portals/{id}/categories; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/portals/{portal_id}/categories"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def create_article(self, account_id: int, portal_id: str | int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/portals/{id}/articles; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/portals/{portal_id}/articles"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)
