"""Serialização dos modelos para os campos oficiais Chatwoot 4.19."""
from __future__ import annotations

from .models import TextMessage, MediaMessage
from .models.messages import _objeto_json


def serialize_text(message: TextMessage) -> dict[str, object]:
    dados: dict[str, object] = {
        "content": message.content,
        "message_type": message.message_type.value,
        "private": message.private,
    }
    if message.content_type is not None:
        dados["content_type"] = message.content_type.value
    if message.content_attributes is not None:
        dados["content_attributes"] = _objeto_json(message.content_attributes, "content_attributes")
    if message.campaign_id is not None:
        dados["campaign_id"] = message.campaign_id
    if message.template_params is not None:
        dados["template_params"] = _objeto_json(message.template_params, "template_params")
    return dados


def serialize_media(message: MediaMessage) -> dict[str, str]:
    fields: dict[str, str] = {
        "message_type": message.message_type.value,
        "private": str(message.private).lower(),
    }
    if message.caption is not None:
        fields["content"] = message.caption
    if message.content_type is not None:
        fields["content_type"] = message.content_type.value
    if message.content_attributes is not None:
        attrs = _objeto_json(message.content_attributes, "content_attributes")
        # Rack transforma content_attributes[nome] em objeto multipart.
        for nome, valor in attrs.items():
            if not nome or "[" in nome or "]" in nome:
                raise ValueError("Chave multipart de content_attributes inválida.")
            if isinstance(valor, str):
                fields[f"content_attributes[{nome}]"] = valor
            elif isinstance(valor, bool):
                fields[f"content_attributes[{nome}]"] = str(valor).lower()
            elif isinstance(valor, (int, float)):
                fields[f"content_attributes[{nome}]"] = str(valor)
            else:
                raise ValueError(
                    "Atributos de mídia multipart aceitam apenas valores escalares; "
                    "objetos aninhados devem usar o envio JSON."
                )
    if message.is_voice_message:
        fields["is_voice_message"] = "true"
    return fields
