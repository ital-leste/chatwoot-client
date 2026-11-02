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

    def create_with_attachments(
        self,
        account_id: int,
        conversation_id: int,
        *,
        attachments: list[tuple[str, bytes, str]],
        content: str | None = None,
        message_type: str = "outgoing",
        private: bool = False,
        content_type: str | None = None,
        content_attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Publica multipart. Cada anexo é (nome, bytes, MIME). Não há retry."""
        import json

        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if message_type not in {"outgoing", "incoming"}:
            raise ValueError("message_type deve ser outgoing ou incoming.")
        if not isinstance(private, bool):
            raise ValueError("private deve ser booleano.")
        if content is not None and not isinstance(content, str):
            raise ValueError("content deve ser texto ou None.")
        if not isinstance(attachments, list) or not attachments:
            raise ValueError("attachments deve ser lista não vazia.")
        for item in attachments:
            if (
                not isinstance(item, tuple) or len(item) != 3
                or not isinstance(item[0], str) or not item[0]
                or not isinstance(item[1], bytes)
                or not isinstance(item[2], str) or not item[2]
            ):
                raise ValueError("Anexos devem ser (nome, bytes, MIME).")
        dados: dict[str, str] = {
            "message_type": message_type,
            "private": str(private).lower(),
        }
        if content is not None:
            dados["content"] = content
        if content_type is not None:
            dados["content_type"] = content_type
        if content_attributes is not None:
            if not isinstance(content_attributes, dict):
                raise ValueError("content_attributes deve ser objeto JSON.")
            dados["content_attributes"] = json.dumps(content_attributes)
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        arquivos = [
            ("attachments[]", (nome, conteudo, mime))
            for nome, conteudo, mime in attachments
        ]
        resposta = self._client._solicitar_json(
            "POST", caminho, dados=dados, arquivos=arquivos,
        )
        return self._client._exigir_objeto(
            resposta, operacao="enviar anexos", caminho=caminho
        )

