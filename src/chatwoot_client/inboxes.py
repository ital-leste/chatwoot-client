"""Consultas de inboxes da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class InboxesResource:
    """Operações da categoria Inboxes."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self, account_id: int, inbox_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/inboxes/{id}: inbox por ID."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        path = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response, operacao="consultar a inbox", caminho=path
        )

    def get_branded_email_layout(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/branded_email_layout; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/branded_email_layout"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update_branded_email_layout(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/branded_email_layout; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/branded_email_layout"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/inboxes"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inboxes"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update(self, account_id: int, inbox_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/inboxes/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def list_message_templates(self, account_id: int, inbox_id: int, *, name: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inboxes/{id}/message_templates; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}/message_templates"
        consulta: dict[str, Any] = {
            "name": name,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def get_agent_bot(self, account_id: int, inbox_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inboxes/{id}/agent_bot; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}/agent_bot"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def set_agent_bot(self, account_id: int, inbox_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/inboxes/{id}/set_agent_bot; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}/set_agent_bot"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def list_members(self, account_id: int, inbox_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inbox_members/{inbox_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        caminho = f"api/v1/accounts/{account_id}/inbox_members/{inbox_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def add_member(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/inbox_members; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update_members(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/inbox_members; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def remove_members(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/inbox_members; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, dados=data, parametros=consulta)
