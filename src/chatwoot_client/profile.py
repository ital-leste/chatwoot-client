"""Consultas do perfil autenticado na API Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ProfileResource:
    """Operações de consulta do perfil associado ao token de API."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def get(self) -> dict[str, Any]:
        """Retorna o JSON do perfil associado ao token, sem alterar dados."""
        path = "api/v1/profile"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_objeto(
            response,
            operacao="consultar o perfil",
            caminho=path,
        )

    def update(self, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PUT /api/v1/profile; retorna JSON ou None."""
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/profile"
        consulta = parametros
        return self._client._solicitar_json("PUT", caminho, dados=data, parametros=consulta)
