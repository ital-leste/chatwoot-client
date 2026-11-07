"""Webhooks: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
from urllib.parse import urlsplit
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


def _dados_webhook(
    *, url: str | None, name: str | None, subscriptions: Sequence[str] | None,
) -> dict[str, Any]:
    """Validação de tipos; unicidade e subscrições válidas cabem ao servidor."""
    dados: dict[str, Any] = {}
    if url is not None:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url deve ser string não vazia.")
        partes = urlsplit(url)
        if partes.scheme not in {"http", "https"} or not partes.hostname or partes.username or partes.password:
            raise ValueError("url deve ser HTTP(S) sem credenciais.")
        dados["url"] = url
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name deve ser string não vazia.")
        dados["name"] = name
    if subscriptions is not None:
        if not isinstance(subscriptions, (list, tuple)) or any(
            not isinstance(item, str) or not item.strip() for item in subscriptions
        ):
            raise ValueError("subscriptions deve ser lista de strings.")
        dados["subscriptions"] = list(subscriptions)
    return dados


class WebhooksResource:
    """Recurso Webhooks."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/webhooks; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/webhooks"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def create(
        self, account_id: int, *, url: str, name: str | None = None,
        subscriptions: Sequence[str] | None = None,
    ) -> Any:
        self._client._validar_id(account_id, "account_id")
        dados = _dados_webhook(url=url, name=name, subscriptions=subscriptions)
        return self._client._post(f"api/v1/accounts/{account_id}/webhooks", dados=dados)


    def update(
        self, account_id: int, webhook_id: int, *,
        url: str | None = None, name: str | None = None,
        subscriptions: Sequence[str] | None = None,
    ) -> Any:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(webhook_id, "webhook_id")
        dados = _dados_webhook(url=url, name=name, subscriptions=subscriptions)
        if not dados:
            raise ValueError("update exige ao menos um campo.")
        return self._client._patch(f"api/v1/accounts/{account_id}/webhooks/{webhook_id}", dados=dados)

    def delete(self, account_id: int, webhook_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/webhooks/{webhook_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(webhook_id, "webhook_id")
        caminho = f"api/v1/accounts/{account_id}/webhooks/{webhook_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
