"""Automation Rule: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .models.application import AutomationRuleInput

if TYPE_CHECKING:
    from .client import CWClient


class AutomationRulesResource:
    """Recurso Automation Rule."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, page: int | None = None, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/automation_rules; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/automation_rules"
        consulta: dict[str, Any] = {
            "page": page,
        }
        consulta = {k: v for k, v in consulta.items() if v is not None}
        if parametros:
            consulta.update(parametros)
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id, rule: AutomationRuleInput) -> Any:
        """POST com contrato de entrada AutomationRuleInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(rule, AutomationRuleInput):
            raise TypeError("rule deve ser AutomationRuleInput.")
        dados = rule.to_payload(required=["name","event_name"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/automation_rules", dados=dados, parametros=consulta)

    def get(self, account_id: int, rule_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/automation_rules/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(rule_id, "rule_id")
        caminho = f"api/v1/accounts/{account_id}/automation_rules/{rule_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id, rule_id, rule: AutomationRuleInput) -> Any:
        """PATCH com contrato de entrada AutomationRuleInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(rule_id, "rule_id")
        if not isinstance(rule, AutomationRuleInput):
            raise TypeError("rule deve ser AutomationRuleInput.")
        dados = rule.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/automation_rules/{rule_id}", dados=dados, parametros=consulta)

    def delete(self, account_id: int, rule_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/automation_rules/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(rule_id, "rule_id")
        caminho = f"api/v1/accounts/{account_id}/automation_rules/{rule_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
