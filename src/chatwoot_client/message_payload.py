"""Serialização dos modelos para os campos oficiais Chatwoot 4.19."""
from __future__ import annotations

from .models import TextMessage, MediaMessage


def serialize_text(message: TextMessage) -> dict[str, object]:
    return {
        "content": message.content,
        "message_type": message.message_type.value,
        "private": message.private,
    }


def serialize_media(message: MediaMessage) -> dict[str, str]:
    fields: dict[str, str] = {
        "message_type": message.message_type.value,
        "private": str(message.private).lower(),
    }
    if message.caption is not None:
        fields["content"] = message.caption
    if message.is_voice_message:
        fields["is_voice_message"] = "true"
    return fields
