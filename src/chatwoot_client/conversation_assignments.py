"""Atribuições de conversas na Application API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ConversationAssignmentsResource:
    """Atribui a um atendente OU equipe; sem desatribuição implícita."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def assign(
        self,
        account_id: int,
        conversation_id: int,
        *,
        assignee_id: int | None = None,
        team_id: int | None = None,
    ) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if (assignee_id is None) == (team_id is None):
            raise ValueError("Forneça exatamente um: assignee_id ou team_id.")
        if assignee_id is not None:
            self._client._validar_id(assignee_id, "assignee_id")
            dados = {"assignee_id": assignee_id}
        else:
            self._client._validar_id(team_id, "team_id")
            dados = {"team_id": team_id}
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments"
        resposta = self._client._solicitar_json("POST", caminho, dados=dados)
        return self._client._exigir_objeto(
            resposta, operacao="atribuir conversa", caminho=caminho
        )
