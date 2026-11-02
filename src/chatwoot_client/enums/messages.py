"""Valores oficiais de mensagens da Application API Chatwoot 4.19."""
from enum import StrEnum


class MessageType(StrEnum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"


class MessageVisibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"

    @property
    def is_private(self) -> bool:
        return self is MessageVisibility.PRIVATE


class MessageContentType(StrEnum):
    TEXT = "text"
    INPUT_EMAIL = "input_email"
    CARDS = "cards"
    INPUT_SELECT = "input_select"
    FORM = "form"
    ARTICLE = "article"
