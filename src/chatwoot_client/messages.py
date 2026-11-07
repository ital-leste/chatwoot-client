"""Consultas de mensagens na API Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any, Literal

from .models import MediaMessage, TextMessage
from .attachment_resolver import DEFAULT_MAX_BYTES, preparar_anexos
from .message_payload import serialize_text, serialize_media

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
        for nome, cursor in (("before", before), ("after", after)):
            if cursor is not None and (type(cursor) is not int or cursor < 0):
                raise ValueError(f"{nome} deve ser inteiro não negativo quando informado.")
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

    @staticmethod
    def _caminho_mensagens(account_id: int, conversation_id: int) -> str:
        return f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"

    def send_text(
        self, account_id: int, conversation_id: int, message: TextMessage,
    ) -> dict[str, Any]:
        """Publica texto ou nota privada pelo endpoint oficial JSON."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(message, TextMessage):
            raise TypeError("message deve ser TextMessage.")
        caminho = self._caminho_mensagens(account_id, conversation_id)
        response = self._client._post(caminho, dados=serialize_text(message))
        return self._client._exigir_objeto(
            response, operacao="enviar texto", caminho=caminho,
        )

    def send_media(
        self, account_id: int, conversation_id: int, message: MediaMessage,
        *, max_bytes: int = DEFAULT_MAX_BYTES, url_timeout: float = 30.0,
        allowed_hosts: set[str] | frozenset[str] | None = None,
    ) -> dict[str, Any]:
        """Publica mídia e legenda em uma única requisição multipart.

        Caminhos locais, bytes, streams e URLs HTTPS são resolvidos nesta camada.
        """
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        if not isinstance(message, MediaMessage):
            raise TypeError("message deve ser MediaMessage.")
        caminho = self._caminho_mensagens(account_id, conversation_id)
        with preparar_anexos(
            message.attachments, max_bytes=max_bytes, timeout=url_timeout,
            allowed_hosts=allowed_hosts,
        ) as arquivos:
            response = self._client._post(
                caminho, dados=serialize_media(message), arquivos=arquivos,
            )
        return self._client._exigir_objeto(
            response, operacao="enviar mídia", caminho=caminho,
        )


    def update_status(
        self, account_id: int, conversation_id: int, message_id: int,
        *, status: Literal["sent", "delivered", "read", "failed"], external_error: str | None = None,
    ) -> Any:
        """Atualiza status de mensagem sem converter os valores da API."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        self._client._validar_id(message_id, "message_id")
        if not isinstance(status, str) or status not in ("sent", "delivered", "read", "failed"):
            raise ValueError("status deve ser sent, delivered, read ou failed.")
        dados = {"status": status}
        if external_error is not None:
            if not isinstance(external_error, str):
                raise ValueError("external_error deve ser string.")
            dados["external_error"] = external_error
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        return self._client._patch(caminho, dados=dados)

    def delete(self, account_id: int, conversation_id: int, message_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        self._client._validar_id(message_id, "message_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
