"""Valores oficiais de mensagens da Application API Chatwoot 4.19."""
from enum import StrEnum


class MessageType(StrEnum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"


class MessageContentType(StrEnum):
    TEXT = "text"
    INPUT_EMAIL = "input_email"
    CARDS = "cards"
    INPUT_SELECT = "input_select"
    FORM = "form"
    ARTICLE = "article"
