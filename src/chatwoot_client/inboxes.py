"""Consultas de inboxes da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .input_validation import validar_ids_usuarios

from typing import TYPE_CHECKING, Any

from .models.application import InboxSettingsInput

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

    def update_branded_email_layout(
        self, account_id: int, *, branded_email_layout: str | None,
    ) -> Any:
        """None explícito é serializado como JSON null."""
        self._client._validar_id(account_id, "account_id")
        if branded_email_layout is not None and not isinstance(branded_email_layout, str):
            raise ValueError("branded_email_layout deve ser texto ou None.")
        return self._client._patch(
            f"api/v1/accounts/{account_id}/branded_email_layout",
            dados={"branded_email_layout": branded_email_layout},
        )

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inboxes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/inboxes"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id, inbox: InboxSettingsInput) -> Any:
        """POST com contrato de entrada InboxSettingsInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(inbox, InboxSettingsInput):
            raise TypeError("inbox deve ser InboxSettingsInput.")
        dados = inbox.to_payload(required=["name","channel"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/inboxes", dados=dados, parametros=consulta)

    def update(self, account_id, inbox_id, inbox: InboxSettingsInput) -> Any:
        """PATCH com contrato de entrada InboxSettingsInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        if not isinstance(inbox, InboxSettingsInput):
            raise TypeError("inbox deve ser InboxSettingsInput.")
        dados = inbox.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/inboxes/{inbox_id}", dados=dados, parametros=consulta)

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
        if "name" in consulta and (not isinstance(consulta["name"], str) or not consulta["name"].strip()):
            raise ValueError("name deve ser texto não vazio.")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def get_agent_bot(self, account_id: int, inbox_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inboxes/{id}/agent_bot; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}/agent_bot"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def set_agent_bot(
        self, account_id: int, inbox_id: int, *, agent_bot: int | None,
    ) -> Any:
        """Define ou desvincula AgentBot: None explícito gera JSON null."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        if agent_bot is not None:
            self._client._validar_id(agent_bot, "agent_bot")
        caminho = f"api/v1/accounts/{account_id}/inboxes/{inbox_id}/set_agent_bot"
        return self._client._post(caminho, dados={"agent_bot": agent_bot})

    def list_members(self, account_id: int, inbox_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/inbox_members/{inbox_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        caminho = f"api/v1/accounts/{account_id}/inbox_members/{inbox_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def add_member(
        self, account_id: int, *, inbox_id: int, user_ids: Sequence[int],
    ) -> Any:
        """POST de membros, sem depender de payloads não tipados."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        return self._client._solicitar_json(
            "POST", caminho, dados={"inbox_id": inbox_id, "user_ids": ids},
        )


    def update_members(
        self, account_id: int, *, inbox_id: int, user_ids: Sequence[int],
    ) -> Any:
        """PATCH de membros, sem depender de payloads não tipados."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        return self._client._solicitar_json(
            "PATCH", caminho, dados={"inbox_id": inbox_id, "user_ids": ids},
        )


    def remove_members(
        self, account_id: int, *, inbox_id: int, user_ids: Sequence[int],
    ) -> Any:
        """DELETE de membros, sem depender de payloads não tipados."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(inbox_id, "inbox_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/inbox_members"
        return self._client._solicitar_json(
            "DELETE", caminho, dados={"inbox_id": inbox_id, "user_ids": ids},
        )

