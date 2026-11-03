"""Condição estruturada compartilhada por Contacts e Conversations."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class FilterCondition:
    """Condição de filtragem da Application API; não é um DTO de resposta."""

    attribute_key: str
    filter_operator: str
    values: Sequence[str]
    query_operator: str | None = None
    timezone: str | None = None

    def __post_init__(self) -> None:
        for campo in ("attribute_key", "filter_operator"):
            valor = getattr(self, campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"{campo} deve ser texto não vazio.")
        if isinstance(self.values, (str, bytes)) or not isinstance(self.values, (list, tuple)):
            raise ValueError("values deve ser lista/tupla de strings.")
        if any(not isinstance(v, str) for v in self.values):
            raise ValueError("values deve conter somente strings.")
        object.__setattr__(self, "values", tuple(self.values))
        if self.query_operator is not None and self.query_operator not in ("AND", "OR"):
            raise ValueError("query_operator deve ser AND, OR ou None.")
        if self.timezone is not None and (
            not isinstance(self.timezone, str) or not self.timezone.strip()
        ):
            raise ValueError("timezone deve ser texto não vazio.")

    def to_payload(self) -> dict[str, Any]:
        item: dict[str, Any] = {
            "attribute_key": self.attribute_key,
            "filter_operator": self.filter_operator,
            "values": list(self.values),
        }
        if self.query_operator is not None:
            item["query_operator"] = self.query_operator
        if self.timezone is not None:
            item["timezone"] = self.timezone
        return item


def _serializar_filtros(filtros: Sequence[FilterCondition]) -> list[dict[str, Any]]:
    if isinstance(filtros, (str, bytes)) or not isinstance(filtros, (list, tuple)) or not filtros:
        raise ValueError("filters deve ser lista/tupla não vazia de FilterCondition.")
    if any(not isinstance(f, FilterCondition) for f in filtros):
        raise TypeError("filters deve conter apenas FilterCondition.")
    return [f.to_payload() for f in filtros]
