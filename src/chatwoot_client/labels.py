"""Catálogo de etiquetas da conta na Application API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class LabelsResource:
    """Consultar ou criar etiquetas disponíveis na conta."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/labels"
        resposta = self._client._solicitar_json("GET", caminho)
        return self._client._exigir_objeto(
            resposta, operacao="listar etiquetas da conta", caminho=caminho
        )

    def create(
        self,
        account_id: int,
        *,
        title: str,
        color: str,
        description: str | None = None,
        show_on_sidebar: bool | None = None,
    ) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title deve ser string não vazia.")
        if not isinstance(color, str) or not color.strip():
            raise ValueError("color deve ser string não vazia.")
        if description is not None and not isinstance(description, str):
            raise ValueError("description deve ser string ou None.")
        if show_on_sidebar is not None and not isinstance(show_on_sidebar, bool):
            raise ValueError("show_on_sidebar deve ser booleano ou None.")
        dados: dict[str, Any] = {"title": title, "color": color}
        if description is not None:
            dados["description"] = description
        if show_on_sidebar is not None:
            dados["show_on_sidebar"] = show_on_sidebar
        caminho = f"api/v1/accounts/{account_id}/labels"
        resposta = self._client._solicitar_json("POST", caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="criar etiqueta na conta", caminho=caminho
        )
