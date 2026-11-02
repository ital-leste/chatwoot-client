"""Contact Labels: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ContactLabelsResource:
    """Recurso Contact Labels."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/labels; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/labels"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def replace(self, account_id: int, contact_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts/{id}/labels; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/labels"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)
