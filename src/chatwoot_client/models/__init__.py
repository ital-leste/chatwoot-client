"""Contratos de entrada para recursos selecionados."""
from .attachments import Attachment
from .messages import TextMessage, MediaMessage
from .labels import LabelDefinition
from .contacts import Contact

__all__ = ["Attachment", "TextMessage", "MediaMessage", "LabelDefinition", "Contact"]
