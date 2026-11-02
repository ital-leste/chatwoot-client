"""Etiquetas de uma conversa na Application API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import CWClient


class ConversationLabelsResource:
    """Consultar e substituir integralmente etiquetas de conversa."""

    def __init__(self, client: CWClient) -> None:
        self._client = client

    def list(self, account_id: int, conversation_id: int) -> dict[str, Any]:
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/labels"
        resposta = self._client._solicitar_json("GET", caminho)
        return self._client._exigir_objeto(
            resposta, operacao="listar etiquetas da conversa", caminho=caminho
        )

    def replace(
        self, account_id: int, conversation_id: int, labels: list[str]
    ) -> dict[str, Any]:
        """Substitui TODAS as etiquetas; [] remove todas. Não é append."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(labels, list) or any(
            not isinstance(label, str) or not label.strip() for label in labels
        ):
            raise ValueError("labels deve ser lista de strings não vazias.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/labels"
        resposta = self._client._solicitar_json("POST", caminho, dados={"labels": labels})
        return self._client._exigir_objeto(
            resposta, operacao="substituir etiquetas da conversa", caminho=caminho
        )
