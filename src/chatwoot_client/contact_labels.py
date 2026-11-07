"""Contact Labels: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
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


    def replace(self, account_id: int, contact_id: int, labels: Sequence[str]) -> Any:
        """Substitui todas as etiquetas; [] remove todas."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(labels, (list, tuple)):
            raise ValueError("labels deve ser lista ou tupla de etiquetas.")
        if any(not isinstance(label, str) or not label.strip() for label in labels):
            raise ValueError("Cada etiqueta deve ser texto não vazio.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/labels"
        return self._client._post(caminho, dados={"labels": list(labels)})

