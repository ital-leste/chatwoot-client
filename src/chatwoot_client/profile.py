"""Consultas do perfil autenticado na API Chatwoot."""

from __future__ import annotations

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
