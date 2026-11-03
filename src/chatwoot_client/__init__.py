"""Cliente Python para a Application API Chatwoot 4.19.0."""
from .client import CWClient, ErroAPIChatwoot, ErroConfiguracaoChatwoot
from .attachment_resolver import ErroAnexoChatwoot
from .models import Attachment, TextMessage, MediaMessage, LabelDefinition, Contact
from .enums import MimeType, MessageType, MessageContentType, ConversationStatus

__all__ = [
    "CWClient", "ErroAPIChatwoot", "ErroConfiguracaoChatwoot", "ErroAnexoChatwoot",
    "Attachment", "TextMessage", "MediaMessage", "LabelDefinition", "Contact",
    "MimeType", "MessageType", "MessageContentType", "ConversationStatus",
]
