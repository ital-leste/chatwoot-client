"""Contratos imutáveis de entrada para texto e mídia."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..enums import MessageType
from .attachments import Attachment


def _validar_publicacao(message_type: MessageType, private: bool) -> None:
    if not isinstance(message_type, MessageType):
        raise TypeError("message_type deve ser MessageType.")
    if not isinstance(private, bool):
        raise TypeError("private deve ser bool.")


@dataclass(frozen=True, slots=True)
class TextMessage:
    content: str
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False

    def __post_init__(self) -> None:
        _validar_publicacao(self.message_type, self.private)
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("TextMessage requer content não vazio.")


@dataclass(frozen=True, slots=True)
class MediaMessage:
    attachments: Sequence[Attachment]
    caption: str | None = None
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False
    is_voice_message: bool = False

    def __post_init__(self) -> None:
        _validar_publicacao(self.message_type, self.private)
        if not isinstance(self.attachments, (tuple, list)) or not self.attachments or any(
            not isinstance(a, Attachment) for a in self.attachments
        ):
            raise ValueError("MediaMessage requer lista não vazia de Attachment.")
        if self.caption is not None and not isinstance(self.caption, str):
            raise TypeError("caption deve ser texto ou None.")
        if not isinstance(self.is_voice_message, bool):
            raise TypeError("is_voice_message deve ser bool.")
        if self.is_voice_message and (
            len(self.attachments) != 1
            or self.attachments[0].mime_type != "audio/ogg"
        ):
            raise ValueError("Mensagem de voz requer um único anexo audio/ogg.")
        object.__setattr__(self, "attachments", tuple(self.attachments))
