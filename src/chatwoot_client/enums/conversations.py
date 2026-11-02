"""Estados públicos documentados da API de conversas Chatwoot."""
from enum import StrEnum


class ConversationStatus(StrEnum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"
    SNOOZED = "snoozed"
