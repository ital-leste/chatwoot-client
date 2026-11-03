"""Contrato tipado de entrada para criação de conversas Chatwoot."""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, fields
from datetime import datetime
from typing import Any

from ..enums import ConversationStatus


def _json_objeto(dados: Mapping[str, Any], nome: str) -> dict[str, Any]:
    if not isinstance(dados, Mapping) or any(not isinstance(k, str) for k in dados):
        raise ValueError(f"{nome} deve ser objeto JSON com chaves de texto.")
    convertido = dict(dados)
    try:
        json.dumps(convertido, allow_nan=False)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{nome} deve ser serializável em JSON.") from exc
    return convertido


@dataclass(frozen=True, slots=True, kw_only=True)
class ConversationCreate:
    """Criação com identidade de canal e atributos opcionais.

    Nenhum objeto de resposta é modelado. Campos None não são enviados.
    """

    source_id: str
    inbox_id: int | None = None
    contact_id: int | None = None
    status: ConversationStatus | None = None
    assignee_id: int | None = None
    team_id: int | None = None
    snoozed_until: str | None = None
    additional_attributes: Mapping[str, Any] | None = None
    custom_attributes: Mapping[str, Any] | None = None
    message: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not self.source_id.strip():
            raise ValueError("source_id deve ser texto não vazio.")
        for nome in ("inbox_id", "contact_id", "assignee_id", "team_id"):
            valor = getattr(self, nome)
            if valor is not None and (type(valor) is not int or valor <= 0):
                raise ValueError(f"{nome} deve ser inteiro positivo.")
        if self.status is not None:
            if not isinstance(self.status, ConversationStatus):
                raise TypeError("status deve ser ConversationStatus.")
            if self.status is ConversationStatus.SNOOZED:
                raise ValueError("Criação aceita open, pending ou resolved; para snoozed use set_status().")
        if self.snoozed_until is not None:
            if not isinstance(self.snoozed_until, str) or not self.snoozed_until.strip():
                raise ValueError("snoozed_until deve ser uma data/hora ISO 8601.")
            try:
                datetime.fromisoformat(self.snoozed_until.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError("snoozed_until deve ser uma data/hora ISO 8601.") from exc

        for nome in ("additional_attributes", "custom_attributes", "message"):
            valor = getattr(self, nome)
            if valor is None:
                continue
            objeto = _json_objeto(valor, nome)
            if nome == "message" and (
                not isinstance(objeto.get("content"), str) or not objeto["content"].strip()
            ):
                raise ValueError("message.content deve ser texto não vazio.")

    def to_payload(self) -> dict[str, Any]:
        resultado: dict[str, Any] = {}
        for campo in fields(self):
            valor = getattr(self, campo.name)
            if valor is None:
                continue
            if isinstance(valor, Mapping):
                valor = dict(valor)
            elif isinstance(valor, ConversationStatus):
                valor = valor.value
            resultado[campo.name] = valor
        return resultado
