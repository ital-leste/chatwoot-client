"""Teams: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping, Sequence

from .input_validation import validar_ids_usuarios
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class TeamsResource:
    """Recurso Teams."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/teams; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/teams"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """POST /api/v1/accounts/{account_id}/teams; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/teams"
        consulta = parametros
        return self._client._solicitar_json("POST", caminho, dados=data, parametros=consulta)

    def get(self, account_id: int, team_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/teams/{team_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, team_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/teams/{team_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, team_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/teams/{team_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)

    def list_members(self, account_id: int, team_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/teams/{team_id}/team_members; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)


    def add_members(
        self, account_id: int, team_id: int, user_ids: Sequence[int],
    ) -> Any:
        """POST de membros da equipe com IDs explícitos."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        return self._client._solicitar_json("POST", caminho, dados={"user_ids": ids})


    def update_members(
        self, account_id: int, team_id: int, user_ids: Sequence[int],
    ) -> Any:
        """PATCH de membros da equipe com IDs explícitos."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        return self._client._solicitar_json("PATCH", caminho, dados={"user_ids": ids})


    def remove_members(
        self, account_id: int, team_id: int, user_ids: Sequence[int],
    ) -> Any:
        """DELETE de membros da equipe com IDs explícitos."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        ids = validar_ids_usuarios(user_ids)
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        return self._client._solicitar_json("DELETE", caminho, dados={"user_ids": ids})

