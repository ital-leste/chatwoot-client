"""Audit Logs: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

from .input_validation import validar_opcao

if TYPE_CHECKING:
    from .client import CWClient


class AuditLogsResource:
    """Recurso Audit Logs."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, page: int | None = None, q: str | None = None, types: list[Any] | None = None, since: int | None = None, until: int | None = None, sort: Literal["asc", "desc"] | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/audit_logs; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/audit_logs"
        consulta: dict[str, Any] = {
            "page": page,
            "q": q,
            "types": types,
            "since": since,
            "until": until,
            "sort": sort,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        if "sort" in consulta:
            validar_opcao(consulta["sort"], ("asc", "desc"), "sort")
        return self._client._solicitar_json("GET", caminho, parametros=consulta)
