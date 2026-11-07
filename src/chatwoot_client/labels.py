"""Catálogo de etiquetas da conta na Application API."""

from __future__ import annotations

from collections.abc import Mapping
import re

from .models import LabelDefinition

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

    def create(self, account_id: int, label: LabelDefinition) -> dict[str, Any]:
        """Criação de etiqueta com o contrato de entrada oficial."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(label, LabelDefinition):
            raise TypeError("label deve ser LabelDefinition.")
        caminho = f"api/v1/accounts/{account_id}/labels"
        resposta = self._client._post(caminho, dados=label.to_payload())
        return self._client._exigir_objeto(
            resposta, operacao="criar etiqueta na conta", caminho=caminho
        )

    def get(self, account_id: int, label_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/labels/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(label_id, "label_id")
        caminho = f"api/v1/accounts/{account_id}/labels/{label_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, label_id: int, *,
               title: str | None = None, description: str | None = None,
               color: str | None = None, show_on_sidebar: bool | None = None) -> Any:
        """PATCH parcial sem exigir LabelDefinition de criação."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(label_id, "label_id")
        dados = {k: v for k, v in (
            ("title", title), ("description", description),
            ("color", color), ("show_on_sidebar", show_on_sidebar),
        ) if v is not None}
        if not dados:
            raise ValueError("Atualização requer ao menos um campo.")
        for nome in ("title", "description"):
            if nome in dados and (not isinstance(dados[nome], str) or
                                  (nome == "title" and not dados[nome].strip())):
                raise ValueError(f"{nome} deve ser texto válido.")
        if "color" in dados and (not isinstance(color, str) or
                                 not re.fullmatch(r"#[0-9A-Fa-f]{6}", color)):
            raise ValueError("color deve seguir #RRGGBB.")
        if "show_on_sidebar" in dados and type(show_on_sidebar) is not bool:
            raise ValueError("show_on_sidebar deve ser bool.")
        return self._client._patch(f"api/v1/accounts/{account_id}/labels/{label_id}", dados=dados)

    def delete(self, account_id: int, label_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/labels/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(label_id, "label_id")
        caminho = f"api/v1/accounts/{account_id}/labels/{label_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
