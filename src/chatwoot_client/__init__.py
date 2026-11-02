"""Cliente Python para a Application API Chatwoot 4.19.0."""
from .client import CWClient, ErroAPIChatwoot, ErroConfiguracaoChatwoot
from .attachment_resolver import ErroAnexoChatwoot
from .models import Attachment, TextMessage, MediaMessage
from .enums import MimeType, MessageVisibility, MessageType, MessageContentType

__all__ = [
    "CWClient", "ErroAPIChatwoot", "ErroConfiguracaoChatwoot", "ErroAnexoChatwoot",
    "Attachment", "TextMessage", "MediaMessage",
    "MimeType", "MessageVisibility", "MessageType", "MessageContentType",
]
