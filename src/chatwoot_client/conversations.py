"""Consultas de conversas na API Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from .enums import ConversationStatus

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ConversationsResource:
    """Operações de leitura de conversas."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(
        self,
        account_id: int,
        *,
        assignee_type: str | None = None,
        status: str | None = None,
        q: str | None = None,
        inbox_id: int | None = None,
        team_id: int | None = None,
        labels: list[str] | None = None,
        page: int | None = None,
    ) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/conversations.

        Aceita os filtros e a página documentados pela Application API e
        retorna o envelope JSON completo sem acumular páginas automaticamente.
        """
        self._client._validar_id(account_id, "account_id")
        for value, name in ((inbox_id, "inbox_id"), (team_id, "team_id"), (page, "page")):
            if value is not None:
                self._client._validar_id(value, name)
        filters = {
            name: value
            for name, value in (
                ("assignee_type", assignee_type),
                ("status", status),
                ("q", q),
                ("inbox_id", inbox_id),
                ("team_id", team_id),
                ("page", page),
            )
            if value is not None
        }
        if labels is not None:
            # A Application API recebe a lista como parâmetro de array do Rails.
            filters["labels[]"] = labels
        path = f"api/v1/accounts/{account_id}/conversations"
        response = self._client._solicitar_json("GET", path, parametros=filters)
        return self._client._exigir_objeto(
            response, operacao="listar as conversas", caminho=path
        )

    def get(self, account_id: int, conversation_id: int) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/conversations/{conversation_id}."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        path = f"api/v1/accounts/{account_id}/conversations/{conversation_id}"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response,
            operacao="consultar a conversa",
            caminho=path,
        )

    def set_status(
        self,
        account_id: int,
        conversation_id: int,
        status: ConversationStatus,
        *,
        snoozed_until: int | None = None,
    ) -> dict[str, Any]:
        """POST toggle_status com estado explícito (não alternância implícita)."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(status, ConversationStatus):
            raise TypeError("status deve ser ConversationStatus.")
        if snoozed_until is not None:
            if status is not ConversationStatus.SNOOZED:
                raise ValueError("snoozed_until só é válido quando status='snoozed'.")
            self._client._validar_id(snoozed_until, "snoozed_until")
        dados: dict[str, Any] = {"status": str(status)}
        if snoozed_until is not None:
            dados["snoozed_until"] = snoozed_until
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status"
        resposta = self._client._solicitar_json("POST", caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="alterar status da conversa", caminho=caminho
        )

    def filter(
        self,
        account_id: int,
        payload: list[dict[str, Any]],
        *,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        """POST de consulta filtrada; preserva o envelope JSON integral."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(payload, list) or not payload or any(
            not isinstance(filtro, dict) for filtro in payload
        ):
            raise ValueError("payload deve ser lista não vazia de objetos.")
        if page is not None:
            self._client._validar_id(page, "page")
        if sort_by is not None and (
            not isinstance(sort_by, str) or not sort_by.strip()
        ):
            raise ValueError("sort_by deve ser string não vazia.")
        parametros: dict[str, Any] = {}
        if page is not None:
            parametros["page"] = page
        if sort_by is not None:
            parametros["sort_by"] = sort_by
        caminho = f"api/v1/accounts/{account_id}/conversations/filter"
        resposta = self._client._solicitar_json(
            "POST", caminho, dados={"payload": payload}, parametros=parametros
        )
        return self._client._exigir_objeto(
            resposta, operacao="filtrar conversas", caminho=caminho
        )

    def meta(self, account_id: int, *, status: str | None = None, q: str | None = None, inbox_id: int | None = None, team_id: int | None = None, labels: list[Any] | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/conversations/meta; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/meta"
        consulta: dict[str, Any] = {
            "status": status,
            "q": q,
            "inbox_id": inbox_id,
            "team_id": team_id,
            "labels": labels,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update(self, account_id: int, conversation_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/conversations/{conversation_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def toggle_priority(self, account_id: int, conversation_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def set_typing_status(self, account_id: int, conversation_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_typing_status"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def update_last_seen(self, account_id: int, conversation_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/update_last_seen"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, parametros=consulta)

    def update_custom_attributes(self, account_id: int, conversation_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/custom_attributes"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def delete_custom_attributes(self, account_id: int, conversation_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/destroy_custom_attributes"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def reporting_events(self, account_id: int, conversation_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/reporting_events"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)
