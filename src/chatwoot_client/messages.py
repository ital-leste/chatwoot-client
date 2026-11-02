"""Consultas de mensagens na API Chatwoot."""

from __future__ import annotations

from collections.abc import Mapping

from typing import TYPE_CHECKING, Any

from .models import Attachment, MediaMessage, TextMessage
from .enums import MessageType, MessageVisibility
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

    def _send_kind(
        self, account_id: int, conversation_id: int, attachment: Attachment,
        *, kind: str, caption: str | None, visibility: MessageVisibility,
        message_type: MessageType, max_bytes: int, url_timeout: float,
        allowed_hosts: set[str] | frozenset[str] | None,
    ) -> dict[str, Any]:
        if not isinstance(attachment, Attachment):
            raise TypeError("attachment deve ser Attachment.")
        mime = attachment.mime_type
        matched = (
            mime.startswith(f"{kind}/")
            if kind != "document"
            else mime.startswith(("application/", "text/"))
        )
        if not matched:
            raise ValueError(f"O MIME do anexo não corresponde ao tipo {kind}.")
        return self.send_media(
            account_id, conversation_id,
            MediaMessage(
                attachments=(attachment,), caption=caption,
                private=visibility.is_private, message_type=message_type,
            ),
            max_bytes=max_bytes, url_timeout=url_timeout,
            allowed_hosts=allowed_hosts,
        )

    def send_image(
        self, account_id: int, conversation_id: int, attachment: Attachment,
        *, caption: str | None = None,
        visibility: MessageVisibility = MessageVisibility.PUBLIC,
        message_type: MessageType = MessageType.OUTGOING,
        max_bytes: int = DEFAULT_MAX_BYTES, url_timeout: float = 30.0,
        allowed_hosts: set[str] | frozenset[str] | None = None,
    ) -> dict[str, Any]:
        return self._send_kind(
            account_id, conversation_id, attachment, kind="image",
            caption=caption, visibility=visibility, message_type=message_type,
            max_bytes=max_bytes, url_timeout=url_timeout, allowed_hosts=allowed_hosts,
        )

    def send_audio(
        self, account_id: int, conversation_id: int, attachment: Attachment,
        *, caption: str | None = None,
        visibility: MessageVisibility = MessageVisibility.PUBLIC,
        message_type: MessageType = MessageType.OUTGOING,
        max_bytes: int = DEFAULT_MAX_BYTES, url_timeout: float = 30.0,
        allowed_hosts: set[str] | frozenset[str] | None = None,
    ) -> dict[str, Any]:
        return self._send_kind(
            account_id, conversation_id, attachment, kind="audio",
            caption=caption, visibility=visibility, message_type=message_type,
            max_bytes=max_bytes, url_timeout=url_timeout, allowed_hosts=allowed_hosts,
        )

    def send_video(
        self, account_id: int, conversation_id: int, attachment: Attachment,
        *, caption: str | None = None,
        visibility: MessageVisibility = MessageVisibility.PUBLIC,
        message_type: MessageType = MessageType.OUTGOING,
        max_bytes: int = DEFAULT_MAX_BYTES, url_timeout: float = 30.0,
        allowed_hosts: set[str] | frozenset[str] | None = None,
    ) -> dict[str, Any]:
        return self._send_kind(
            account_id, conversation_id, attachment, kind="video",
            caption=caption, visibility=visibility, message_type=message_type,
            max_bytes=max_bytes, url_timeout=url_timeout, allowed_hosts=allowed_hosts,
        )

    def send_document(
        self, account_id: int, conversation_id: int, attachment: Attachment,
        *, caption: str | None = None,
        visibility: MessageVisibility = MessageVisibility.PUBLIC,
        message_type: MessageType = MessageType.OUTGOING,
        max_bytes: int = DEFAULT_MAX_BYTES, url_timeout: float = 30.0,
        allowed_hosts: set[str] | frozenset[str] | None = None,
    ) -> dict[str, Any]:
        return self._send_kind(
            account_id, conversation_id, attachment, kind="document",
            caption=caption, visibility=visibility, message_type=message_type,
            max_bytes=max_bytes, url_timeout=url_timeout, allowed_hosts=allowed_hosts,
        )

    def update_status(self, account_id: int, conversation_id: int, message_id: int, data: Mapping[str, Any], *, parametros: Mapping[str, Any] | None = None) -> Any:
        """PATCH /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        self._client._validar_id(message_id, "message_id")
        if not isinstance(data, Mapping):
            raise ValueError("data deve ser objeto JSON.")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        consulta = parametros
        return self._client._solicitar_json("PATCH", caminho, dados=data, parametros=consulta)

    def delete(self, account_id: int, conversation_id: int, message_id: int, *, parametros: Mapping[str, Any] | None = None) -> Any:
        """DELETE /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}; retorna JSON ou None."""
        self._client._validar_id(account_id, "account_id")
        self._client._validar_id(conversation_id, "conversation_id")
        self._client._validar_id(message_id, "message_id")
        caminho = f"api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        consulta = parametros
        return self._client._solicitar_json("DELETE", caminho, parametros=consulta)
