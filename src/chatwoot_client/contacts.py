"""Consultas de contatos da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ContactsResource:
    """Operações da categoria Contacts."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int, contact_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/contacts/{id}: contato por ID."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        path = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar o contato", caminho=path
        )

    def list(self, account_id: int, *, sort: str | None = None, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/contacts"
        consulta: dict[str, Any] = {
            "sort": sort,
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update(self, account_id: int, contact_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PUT /api/v1/accounts/{account_id}/contacts/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        consulta = parametros
        return self._client._solicitar_json("PUT", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/contacts/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)

    def list_conversations(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/conversations; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/conversations"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def search(self, account_id: int, *, q: str | None = None, sort: str | None = None, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/search; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/search"
        consulta: dict[str, Any] = {
            "q": q,
            "sort": sort,
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def filter(self, account_id: int, data: Mapping[str, Any], *, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts/filter; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/filter"
        consulta: dict[str, Any] = {
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def add_inbox(self, account_id: int, contact_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/contacts/{id}/contact_inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contact_inboxes"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def list_contactable_inboxes(self, account_id: int, contact_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/contacts/{id}/contactable_inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(contact_id, "contact_id")
        caminho = f"api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def merge(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/actions/contact_merge; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/actions/contact_merge"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)
