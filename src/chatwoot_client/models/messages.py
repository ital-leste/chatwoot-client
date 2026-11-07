"""Contratos imutáveis de entrada para texto e mídia."""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any, Sequence
from copy import deepcopy
import json

from ..enums import MessageType, MessageContentType
from ..input_validation import validar_chaves_json
from .attachments import Attachment


def _validar_publicacao(message_type: MessageType, private: bool) -> None:
    if not isinstance(message_type, MessageType):
        raise TypeError("message_type deve ser MessageType.")
    if not isinstance(private, bool):
        raise TypeError("private deve ser bool.")



def _objeto_json(valor: Mapping[str, Any], nome: str) -> dict[str, Any]:
    if not isinstance(valor, Mapping):
        raise ValueError(f"{nome} deve ser objeto JSON.")
    try:
        copia = deepcopy(dict(valor))
        validar_chaves_json(copia)
        json.dumps(copia, allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise ValueError(f"{nome} requer JSON válido.") from exc
    return copia


def _validar_opcionais(objeto: Any) -> None:
    tipo = objeto.content_type
    if tipo is not None and not isinstance(tipo, MessageContentType):
        raise TypeError("content_type deve ser MessageContentType.")
    attrs = objeto.content_attributes
    if attrs is not None:
        object.__setattr__(objeto, "content_attributes", _objeto_json(attrs, "content_attributes"))
    if isinstance(objeto, TextMessage):
        if objeto.campaign_id is not None and (
            type(objeto.campaign_id) is not int or objeto.campaign_id <= 0
        ):
            raise ValueError("campaign_id deve ser inteiro positivo.")
        if objeto.template_params is not None:
            object.__setattr__(
                objeto, "template_params", _objeto_json(objeto.template_params, "template_params")
            )

@dataclass(frozen=True, slots=True)
class TextMessage:
    content: str
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False
    content_type: MessageContentType | None = None
    content_attributes: Mapping[str, Any] | None = None
    campaign_id: int | None = None
    template_params: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        _validar_publicacao(self.message_type, self.private)
        _validar_opcionais(self)
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("TextMessage requer content não vazio.")


@dataclass(frozen=True, slots=True)
class MediaMessage:
    attachments: Sequence[Attachment]
    caption: str | None = None
    message_type: MessageType = MessageType.OUTGOING
    private: bool = False
    is_voice_message: bool = False
    content_type: MessageContentType | None = None
    content_attributes: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        _validar_publicacao(self.message_type, self.private)
        _validar_opcionais(self)
        if not isinstance(self.attachments, (tuple, list)) or not self.attachments or any(
            not isinstance(a, Attachment) for a in self.attachments
        ):
            raise ValueError("MediaMessage requer lista não vazia de Attachment.")
        if self.caption is not None and not isinstance(self.caption, str):
            raise TypeError("caption deve ser texto ou None.")
        if not isinstance(self.is_voice_message, bool):
            raise TypeError("is_voice_message deve ser bool.")
        if self.is_voice_message and (
            len(self.attachments) != 1
            or self.attachments[0].mime_type != "audio/ogg"
        ):
            raise ValueError("Mensagem de voz requer um único anexo audio/ogg.")
        object.__setattr__(self, "attachments", tuple(self.attachments))
