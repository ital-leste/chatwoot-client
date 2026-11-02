"""Contratos de entrada para recursos selecionados."""
from .attachments import Attachment
from .messages import TextMessage, MediaMessage
from .labels import LabelDefinition
from .canned_responses import CannedResponse

__all__ = ["Attachment", "TextMessage", "MediaMessage", "LabelDefinition", "CannedResponse"]
