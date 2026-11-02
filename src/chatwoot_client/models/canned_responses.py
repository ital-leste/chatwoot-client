"""Contrato de entrada para respostas rápidas do Chatwoot 4.19.0."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CannedResponse:
    """Dados para criar ou alterar; campos não enviados ficam como None.

    Requisitos específicos (ambos na criação, ao menos um na atualização)
    são verificados pelo recurso, não pelo construtor compartilhado.
    """

    short_code: str | None = None
    content: str | None = None

    def __post_init__(self) -> None:
        for nome in ("short_code", "content"):
            valor = getattr(self, nome)
            if valor is not None and (not isinstance(valor, str) or not valor.strip()):
                raise ValueError(f"{nome} deve ser texto não vazio ou None.")

    def to_payload(self) -> dict[str, str]:
        """Somente campos efetivamente fornecidos pela aplicação."""
        resultado: dict[str, str] = {}
        if self.short_code is not None:
            resultado["short_code"] = self.short_code
        if self.content is not None:
            resultado["content"] = self.content
        return resultado
