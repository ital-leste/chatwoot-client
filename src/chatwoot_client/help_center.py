"""Help Center: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .models.application import HelpCenterPortalInput, HelpCenterCategoryInput, HelpCenterArticleInput

if TYPE_CHECKING:
    from .client import CWClient


class HelpCenterResource:
    """Recurso Help Center."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def create(self, account_id, portal: HelpCenterPortalInput) -> Any:
        """POST com contrato de entrada HelpCenterPortalInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(portal, HelpCenterPortalInput):
            raise TypeError("portal deve ser HelpCenterPortalInput.")
        dados = portal.to_payload(required=["name","slug"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/portals", dados=dados, parametros=consulta)

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/portals; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/portals"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def get(self, account_id: int, portal_id: str | int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/portals/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        caminho = f"api/v1/accounts/{account_id}/portals/{portal_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id, portal_id: str | int, portal: HelpCenterPortalInput) -> Any:
        """PATCH com contrato de entrada HelpCenterPortalInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(portal, HelpCenterPortalInput):
            raise TypeError("portal deve ser HelpCenterPortalInput.")
        dados = portal.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/portals/{portal_id}", dados=dados, parametros=consulta)

    def create_category(self, account_id, portal_id: str | int, category: HelpCenterCategoryInput) -> Any:
        """POST com contrato de entrada HelpCenterCategoryInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(category, HelpCenterCategoryInput):
            raise TypeError("category deve ser HelpCenterCategoryInput.")
        dados = category.to_payload(required=["name"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/portals/{portal_id}/categories", dados=dados, parametros=consulta)

    def create_article(self, account_id, portal_id: str | int, article: HelpCenterArticleInput) -> Any:
        """POST com contrato de entrada HelpCenterArticleInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        portal_id = self._client._segmento(portal_id, "portal_id")
        if not isinstance(article, HelpCenterArticleInput):
            raise TypeError("article deve ser HelpCenterArticleInput.")
        dados = article.to_payload(required=["title","content"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/portals/{portal_id}/articles", dados=dados, parametros=consulta)

