"""Consultas de atendentes da Application API do Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from .client import CWClient


class AgentsResource:
    """Operações da categoria Agents."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int) -> list[Any]:
        """GET /api/v1/accounts/{account_id}/agents: atendentes da conta."""
        self._client._validar_id(account_id, "account_id")
        path = f"api/v1/accounts/{account_id}/agents"
        response = self._client._solicitar_json("GET", path)
        return self._client._exigir_lista(
            response, operacao="listar os atendentes", caminho=path
        )


    def create(
        self, account_id: int, *, name: str, email: str,
        role: Literal["agent", "administrator"],
        availability: Literal["online", "busy", "offline"] | None = None,
        auto_offline: bool | None = None,
    ) -> Any:
        """Campos obrigatórios conforme Application API 4.19.0."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name deve ser texto não vazio.")
        if not isinstance(email, str) or not email.strip() or "@" not in email or any(c.isspace() for c in email):
            raise ValueError("email deve ser texto de email válido.")
        if role not in ("agent", "administrator"):
            raise ValueError("role deve ser agent ou administrator.")
        dados: dict[str, Any] = {"name": name, "email": email, "role": role}
        if availability is not None:
            if availability not in ("online", "busy", "offline"):
                raise ValueError("availability inválida.")
            dados["availability"] = availability
        if auto_offline is not None:
            if type(auto_offline) is not bool:
                raise ValueError("auto_offline deve ser bool.")
            dados["auto_offline"] = auto_offline
        return self._client._post(f"api/v1/accounts/{account_id}/agents", dados=dados)


    def update(
        self, account_id: int, agent_id: int, *,
        role: Literal["agent", "administrator"],
        availability: Literal["online", "busy", "offline"] | None = None,
        auto_offline: bool | None = None,
    ) -> Any:
        """Atualização de agente exige role na API 4.19.0."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(agent_id, "agent_id")
        if role not in ("agent", "administrator"):
            raise ValueError("role deve ser agent ou administrator.")
        dados: dict[str, Any] = {"role": role}
        if availability is not None:
            if availability not in ("online", "busy", "offline"):
                raise ValueError("availability inválida.")
            dados["availability"] = availability
        if auto_offline is not None:
            if type(auto_offline) is not bool:
                raise ValueError("auto_offline deve ser bool.")
            dados["auto_offline"] = auto_offline
        return self._client._patch(f"api/v1/accounts/{account_id}/agents/{agent_id}", dados=dados)

    def delete(self, account_id: int, agent_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/agents/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(agent_id, "agent_id")
        caminho = f"api/v1/accounts/{account_id}/agents/{agent_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
