"""Contratos imutáveis de mensagens, com validação em tempo de execução."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..enums import MessageType, MessageVisibility
from .attachments import Attachment


def _validate_flags(
    message_type: MessageType,
    private: bool,
    visibility: MessageVisibility | None,
) -> bool:
    if not isinstance(message_type, MessageType):
        raise TypeError("message_type deve ser MessageType.")
    if not isinstance(private, bool):
        raise TypeError("private deve ser bool.")
    if visibility is not None:
        if not isinstance(visibility, MessageVisibility):
            raise TypeError("visibility deve ser MessageVisibility ou None.")
        if private and visibility is MessageVisibility.PUBLIC:
            raise ValueError("private=True conflita com visibility=PUBLIC.")
        # Alias de compatibilidade: priorizar private na interface nova.
        return visibility.is_private or private
    return private


@dataclass(frozen=True, slots=True)
class TextMessage:
    content: str
    # Alias de compatibilidade da primeira interface tipada; preferir private.
    visibility: MessageVisibility | None = None
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "private", _validate_flags(self.message_type, self.private, self.visibility)
        )
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("TextMessage requer content não vazio.")


@dataclass(frozen=True, slots=True)
class MediaMessage:
    attachments: Sequence[Attachment]
    caption: str | None = None
    # Alias antigo mantido para não quebrar código tipado já escrito.
    visibility: MessageVisibility | None = None
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False
    is_voice_message: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "private", _validate_flags(self.message_type, self.private, self.visibility)
        )
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
