"""Contrato de criação de etiqueta no catálogo da conta."""
from __future__ import annotations
import re
from dataclasses import dataclass

_HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass(frozen=True, slots=True)
class LabelDefinition:
    title: str
    color: str
    description: str | None = None
    show_on_sidebar: bool | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title deve ser texto não vazio.")
        if not isinstance(self.color, str) or not _HEX_COLOR.fullmatch(self.color):
            raise ValueError("color deve ser #RRGGBB.")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("description deve ser texto ou None.")
        if self.show_on_sidebar is not None and not isinstance(self.show_on_sidebar, bool):
            raise TypeError("show_on_sidebar deve ser bool ou None.")

    def to_payload(self) -> dict[str, object]:
        result: dict[str, object] = {"title": self.title, "color": self.color}
        if self.description is not None:
            result["description"] = self.description
        if self.show_on_sidebar is not None:
            result["show_on_sidebar"] = self.show_on_sidebar
        return result
