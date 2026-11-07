"""Reports: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

from .input_validation import validar_opcao

if TYPE_CHECKING:
    from .client import CWClient


class ReportsResource:
    """Recurso Reports."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list_reporting_events(self, account_id: int, *, page: int | None = None, since: str | None = None, until: str | None = None, inbox_id: int | None = None, user_id: int | None = None, name: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/reporting_events; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/reporting_events"
        consulta: dict[str, Any] = {
            "page": page,
            "since": since,
            "until": until,
            "inbox_id": inbox_id,
            "user_id": user_id,
            "name": name,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def list_conversation_statistics(self, account_id: int, *, metric: Literal["conversations_count", "incoming_messages_count", "outgoing_messages_count", "avg_first_response_time", "avg_resolution_time", "resolutions_count"], type_: Literal["account", "agent", "inbox", "label", "team"], id: str | None = None, since: str | None = None, until: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports"
        consulta: dict[str, Any] = {
            "metric": metric,
            "type": type_,
            "id": id,
            "since": since,
            "until": until,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        validar_opcao(consulta["metric"], ("conversations_count", "incoming_messages_count", "outgoing_messages_count", "avg_first_response_time", "avg_resolution_time", "resolutions_count"), "metric")
        validar_opcao(consulta["type"], ("account", "agent", "inbox", "label", "team"), "type")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def summary(self, account_id: int, *, type_: Literal["account", "agent", "inbox", "label", "team"], id: str | None = None, since: str | None = None, until: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/summary; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/summary"
        consulta: dict[str, Any] = {
            "type": type_,
            "id": id,
            "since": since,
            "until": until,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        validar_opcao(consulta["type"], ("account", "agent", "inbox", "label", "team"), "type")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def conversation_metrics(self, account_id: int, *, type_: Literal["account"], parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/conversations; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/conversations"
        consulta: dict[str, Any] = {
            "type": type_,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        validar_opcao(consulta["type"], ("account",), "type")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def agent_conversation_metrics(self, account_id: int, *, type_: Literal["agent"], user_id: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/conversations/; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/conversations/"
        consulta: dict[str, Any] = {
            "type": type_,
            "user_id": user_id,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        validar_opcao(consulta["type"], ("agent",), "type")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def channel_summary(self, account_id: int, *, since: str | None = None, until: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/summary_reports/channel; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/summary_reports/channel"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def inbox_summary(self, account_id: int, *, since: str | None = None, until: str | None = None, business_hours: bool | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/summary_reports/inbox; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/summary_reports/inbox"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
            "business_hours": business_hours,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def agent_summary(self, account_id: int, *, since: str | None = None, until: str | None = None, business_hours: bool | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/summary_reports/agent; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/summary_reports/agent"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
            "business_hours": business_hours,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def team_summary(self, account_id: int, *, since: str | None = None, until: str | None = None, business_hours: bool | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/summary_reports/team; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/summary_reports/team"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
            "business_hours": business_hours,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def first_response_time_distribution(self, account_id: int, *, since: str | None = None, until: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/first_response_time_distribution; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/first_response_time_distribution"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def inbox_label_matrix(self, account_id: int, *, since: str | None = None, until: str | None = None, inbox_ids: list[Any] | None = None, label_ids: list[Any] | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/inbox_label_matrix; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/inbox_label_matrix"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
            "inbox_ids": inbox_ids,
            "label_ids": label_ids,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def outgoing_messages_count(self, account_id: int, *, group_by: Literal["agent", "team", "inbox", "label"], since: str | None = None, until: str | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v2/accounts/{account_id}/reports/outgoing_messages_count; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v2/accounts/{account_id}/reports/outgoing_messages_count"
        consulta: dict[str, Any] = {
            "since": since,
            "until": until,
            "group_by": group_by,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        validar_opcao(consulta["group_by"], ("agent", "team", "inbox", "label"), "group_by")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)
