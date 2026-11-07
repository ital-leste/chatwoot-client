"""Campaigns: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class CampaignsResource:
    """Recurso Campaigns."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/campaigns; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/campaigns"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def create(self, account_id: int, campaign: Mapping[str, Any]) -> Any:
        """Envia o envelope obrigatório {"campaign": {...}} da Application API."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(campaign, Mapping) or not campaign:
            raise ValueError("campaign deve ser objeto JSON não vazio.")
        return self._client._post(
            f"api/v1/accounts/{account_id}/campaigns",
            dados={"campaign": dict(campaign)},
        )

    def get(self, account_id: int, campaign_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/campaigns/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(campaign_id, "campaign_id")
        caminho = f"api/v1/accounts/{account_id}/campaigns/{campaign_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def update(self, account_id: int, campaign_id: int, campaign: Mapping[str, Any]) -> Any:
        """PATCH preserva envelope campaign; conteúdo segue a API."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(campaign_id, "campaign_id")
        if not isinstance(campaign, Mapping) or not campaign:
            raise ValueError("campaign deve ser objeto JSON não vazio.")
        return self._client._patch(
            f"api/v1/accounts/{account_id}/campaigns/{campaign_id}",
            dados={"campaign": dict(campaign)},
        )

    def delete(self, account_id: int, campaign_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/campaigns/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(campaign_id, "campaign_id")
        caminho = f"api/v1/accounts/{account_id}/campaigns/{campaign_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
