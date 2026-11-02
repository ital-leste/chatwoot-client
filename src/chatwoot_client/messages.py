"""Consultas de mensagens na API Chatwoot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class MessagesResource:
    """Operações de leitura de mensagens e anexos."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(
        self,
        account_id: int,
        conversation_id: int,
        *,
        before: int | None = None,
        after: int | None = None,
    ) -> dict[str, Any]:
        """GET /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages.

        Os cursores ``before`` e ``after`` são IDs de mensagem; a resposta
        conserva o envelope ``meta`` e ``payload`` sem juntar páginas.
        """
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        path = (
            f"api/v1/accounts/{account_id}/conversations/"
            f"{conversation_id}/messages"
        )
        parameters = {
            name: value
            for name, value in (("before", before), ("after", after))
            if value is not None
        }
        response = self._client._solicitar_json("GET", path, parametros=parameters)
        return self._client._exigir_objeto(
            response,
            operacao="listar mensagens",
            caminho=path,
        )

    def create(
        self,
        account_id: int,
        conversation_id: int,
        *,
        content: str,
        message_type: str = "outgoing",
        private: bool = False,
    ) -> dict[str, Any]:
        """Cria mensagem textual via JSON, sem retry automático ou multipart."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("content deve ser texto não vazio.")
        if message_type not in {"outgoing", "incoming"}:
            raise ValueError("message_type deve ser outgoing ou incoming.")
        if not isinstance(private, bool):
            raise ValueError("private deve ser booleano.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        resposta = self._client._solicitar_json(
            "POST", caminho,
            dados={"content": content, "message_type": message_type, "private": private},
        )
        return self._client._exigir_objeto(
            resposta, operacao="criar mensagem", caminho=caminho
        )
