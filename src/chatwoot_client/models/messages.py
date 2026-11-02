"""Contratos de mensagens, com validação antes de chamadas HTTP."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..enums import MessageType, MessageVisibility
from .attachments import Attachment


def _validar_tipo_visibilidade(
    message_type: MessageType, visibility: MessageVisibility
) -> None:
    if not isinstance(message_type, MessageType):
        raise TypeError("message_type deve ser MessageType.")
    if not isinstance(visibility, MessageVisibility):
        raise TypeError("visibility deve ser MessageVisibility.")


@dataclass(frozen=True, slots=True)
class TextMessage:
    content: str
    visibility: MessageVisibility = MessageVisibility.PUBLIC
    message_type: MessageType = MessageType.OUTGOING

    def __post_init__(self) -> None:
        _validar_tipo_visibilidade(self.message_type, self.visibility)
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("TextMessage requer content não vazio.")


@dataclass(frozen=True, slots=True)
class MediaMessage:
    attachments: Sequence[Attachment]
    caption: str | None = None
    visibility: MessageVisibility = MessageVisibility.PUBLIC
    message_type: MessageType = MessageType.OUTGOING

    def __post_init__(self) -> None:
        _validar_tipo_visibilidade(self.message_type, self.visibility)
        if isinstance(self.attachments, (str, bytes)) or not isinstance(
            self.attachments, (tuple, list)
        ) or not self.attachments or any(
            not isinstance(a, Attachment) for a in self.attachments
        ):
            raise ValueError("MediaMessage requer uma lista não vazia de Attachment.")
        if self.caption is not None and not isinstance(self.caption, str):
            raise TypeError("caption deve ser texto ou None.")
        object.__setattr__(self, "attachments", tuple(self.attachments))
