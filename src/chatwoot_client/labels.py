"""Catálogo de etiquetas da conta na Application API."""

from __future__ import annotations

from collections.abc import Mapping

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

    def update(self, account_id: int, label_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/labels/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(label_id, "label_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/labels/{label_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, label_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/labels/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(label_id, "label_id")
        caminho = f"api/v1/accounts/{account_id}/labels/{label_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
