"""Integrations: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .models.application import IntegrationHookInput

if TYPE_CHECKING:
    from .client import CWClient


class IntegrationsResource:
    """Recurso Integrations."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list_apps(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/integrations/apps; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/integrations/apps"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create_hook(self, account_id: int, hook: IntegrationHookInput) -> Any:
        """POST com contrato de entrada IntegrationHookInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(hook, IntegrationHookInput):
            raise TypeError("hook deve ser IntegrationHookInput.")
        dados = hook.to_payload(required=["app_id","inbox_id"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/integrations/hooks", dados=dados, parametros=consulta)

    def update_hook(self, account_id: int, hook_id: int, hook: IntegrationHookInput) -> Any:
        """PATCH com contrato de entrada IntegrationHookInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(hook_id, "hook_id")
        if not isinstance(hook, IntegrationHookInput):
            raise TypeError("hook deve ser IntegrationHookInput.")
        dados = hook.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/integrations/hooks/{hook_id}", dados=dados, parametros=consulta)

    def delete_hook(self, account_id: int, hook_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/integrations/hooks/{hook_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(hook_id, "hook_id")
        caminho = f"api/v1/accounts/{account_id}/integrations/hooks/{hook_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
