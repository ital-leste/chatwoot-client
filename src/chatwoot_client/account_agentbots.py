"""Account AgentBots: operações da Application API do Chatwoot."""

from __future__ import annotations
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from .models.application import AgentBotInput

if TYPE_CHECKING:
    from .client import CWClient


class AccountAgentBotsResource:
    """Recurso Account AgentBots."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/agent_bots; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        caminho = f"api/v1/accounts/{account_id}/agent_bots"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def create(self, account_id: int, bot: AgentBotInput) -> Any:
        """POST com contrato de entrada AgentBotInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        if not isinstance(bot, AgentBotInput):
            raise TypeError("bot deve ser AgentBotInput.")
        dados = bot.to_payload(required=["name"])
        consulta = None
        return self._client._solicitar_json("POST", f"api/v1/accounts/{account_id}/agent_bots", dados=dados, parametros=consulta)

    def get(self, account_id: int, agent_bot_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """GET /api/v1/accounts/{account_id}/agent_bots/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(agent_bot_id, "agent_bot_id")
        caminho = f"api/v1/accounts/{account_id}/agent_bots/{agent_bot_id}"
        consulta = parametros
        return self._client._solicitar_json("GET", caminho, parametros=consulta)

    def update(self, account_id: int, agent_bot_id: int, bot: AgentBotInput) -> Any:
        """PATCH com contrato de entrada AgentBotInput; saída JSON nativa."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(agent_bot_id, "agent_bot_id")
        if not isinstance(bot, AgentBotInput):
            raise TypeError("bot deve ser AgentBotInput.")
        dados = bot.to_payload()
        consulta = None
        return self._client._solicitar_json("PATCH", f"api/v1/accounts/{account_id}/agent_bots/{agent_bot_id}", dados=dados, parametros=consulta)

    def delete(self, account_id: int, agent_bot_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/agent_bots/{id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(agent_bot_id, "agent_bot_id")
        caminho = f"api/v1/accounts/{account_id}/agent_bots/{agent_bot_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
