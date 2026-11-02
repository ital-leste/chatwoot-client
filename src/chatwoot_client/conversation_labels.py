"""Etiquetas de uma conversa na Application API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from collections.abc import Sequence

if TYPE_CHECKING:
    from .client import CWClient


class ConversationLabelsResource:
    """Consultar, substituir, acrescentar e remover etiquetas de conversa."""

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

    @staticmethod
    def _validate_labels(labels: str | Sequence[str]) -> list[str]:
        if isinstance(labels, str):
            labels = [labels]
        if not isinstance(labels, (list, tuple)) or not labels:
            raise ValueError("labels deve conter ao menos uma etiqueta.")
        if any(not isinstance(item, str) or not item.strip() for item in labels):
            raise ValueError("etiquetas devem ser strings não vazias.")
        return list(dict.fromkeys(item.strip() for item in labels))

    @staticmethod
    def _extract_payload(response: dict[str, Any]) -> list[str]:
        """Falha fechada: resposta inesperada não pode apagar etiquetas."""
        labels = response.get("payload")
        if not isinstance(labels, list) or any(
            not isinstance(item, str) or not item.strip() for item in labels
        ):
            raise ValueError("Chatwoot não retornou uma lista válida de etiquetas.")
        return labels

    def add(
        self, account_id: int, conversation_id: int, labels: str | Sequence[str],
    ) -> dict[str, Any]:
        """GET + união estável + POST se mudou; preserva as etiquetas existentes.

        Não é operação atômica. Alterações simultâneas requerem serialização
        pelo sistema consumidor.
        """
        extras = self._validate_labels(labels)
        before = self.list(account_id, conversation_id)
        existing = self._extract_payload(before)
        combined = list(dict.fromkeys([*existing, *extras]))
        if combined == existing:
            return before
        return self.replace(account_id, conversation_id, combined)

    def remove(
        self, account_id: int, conversation_id: int, labels: str | Sequence[str],
    ) -> dict[str, Any]:
        """Remove seletivamente, preservando as demais etiquetas."""
        targets = set(self._validate_labels(labels))
        before = self.list(account_id, conversation_id)
        existing = self._extract_payload(before)
        remaining = [name for name in existing if name not in targets]
        if remaining == existing:
            return before
        return self.replace(account_id, conversation_id, remaining)
