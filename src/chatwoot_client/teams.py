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

    @staticmethod
    def _dados_equipe(*, name: str | None, description: str | None,
                      allow_auto_assign: bool | None, icon: str | None,
                      icon_color: str | None) -> dict[str, Any]:
        dados = {k: v for k, v in (
            ("name", name), ("description", description),
            ("allow_auto_assign", allow_auto_assign),
            ("icon", icon), ("icon_color", icon_color),
        ) if v is not None}
        if not dados:
            raise ValueError("Informe ao menos um campo da equipe.")
        for nome in ("name", "description", "icon", "icon_color"):
            if nome in dados and (not isinstance(dados[nome], str) or
                                  (nome == "name" and not dados[nome].strip())):
                raise ValueError(f"{nome} deve ser string válida.")
        if "allow_auto_assign" in dados and type(dados["allow_auto_assign"]) is not bool:
            raise ValueError("allow_auto_assign deve ser bool.")
        return dados


    def create(self, account_id: int, *, name: str,
               description: str | None = None, allow_auto_assign: bool | None = None,
               icon: str | None = None, icon_color: str | None = None) -> Any:
        """Parâmetros do catálogo de equipes, sem objeto JSON genérico."""
        self._client._validar_id(account_id, "account_id")
        dados = self._dados_equipe(name=name, description=description,
                                  allow_auto_assign=allow_auto_assign,
                                  icon=icon, icon_color=icon_color)
        return self._client._post(f"api/v1/accounts/{account_id}/teams", dados=dados)

    def get(self, account_id: int, team_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/teams/{team_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        caminho = f"api/v1/accounts/{account_id}/teams/{team_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, team_id: int, *,
               name: str | None = None, description: str | None = None,
               allow_auto_assign: bool | None = None, icon: str | None = None,
               icon_color: str | None = None) -> Any:
        """PATCH parcial: campos None são omitidos da requisição."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(team_id, "team_id")
        dados = self._dados_equipe(name=name, description=description,
                                  allow_auto_assign=allow_auto_assign,
                                  icon=icon, icon_color=icon_color)
        return self._client._patch(f"api/v1/accounts/{account_id}/teams/{team_id}", dados=dados)

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

