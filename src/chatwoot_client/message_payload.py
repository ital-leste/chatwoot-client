"""Conversão dos contratos de mensagens para os campos oficiais da API."""
from __future__ import annotations

from .models import TextMessage, MediaMessage


def serialize_text(message: TextMessage) -> dict[str, object]:
    return {
        "content": message.content,
        "message_type": message.message_type.value,
        "private": message.visibility.is_private,
    }


def serialize_media(message: MediaMessage) -> dict[str, str]:
    fields = {
        "message_type": message.message_type.value,
        "private": str(message.visibility.is_private).lower(),
    }
    if message.caption is not None:
        fields["content"] = message.caption
    return fields
