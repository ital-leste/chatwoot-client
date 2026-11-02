"""Contratos imutáveis para respostas rápidas da Application API Chatwoot 4.19."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


def _texto_nao_vazio(valor: object, campo: str) -> None:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} deve ser texto não vazio.")


@dataclass(frozen=True, slots=True)
class CannedResponseCreate:
    """Campos oficiais exigidos na criação de uma resposta rápida."""

    short_code: str
    content: str

    def __post_init__(self) -> None:
        _texto_nao_vazio(self.short_code, "short_code")
        _texto_nao_vazio(self.content, "content")

    def to_payload(self) -> dict[str, str]:
        return {"short_code": self.short_code, "content": self.content}


@dataclass(frozen=True, slots=True)
class CannedResponseUpdate:
    """PATCH parcial: ao menos um dos dois campos oficiais."""

    short_code: str | None = None
    content: str | None = None

    def __post_init__(self) -> None:
        if self.short_code is None and self.content is None:
            raise ValueError("Informe short_code e/ou content para atualizar.")
        for nome in ("short_code", "content"):
            valor = getattr(self, nome)
            if valor is not None:
                _texto_nao_vazio(valor, nome)

    def to_payload(self) -> dict[str, str]:
        resultado: dict[str, str] = {}
        if self.short_code is not None:
            resultado["short_code"] = self.short_code
        if self.content is not None:
            resultado["content"] = self.content
        return resultado


@dataclass(frozen=True, slots=True)
class CannedResponse:
    """Representação tipada da resposta retornada pelo Chatwoot."""

    id: int
    account_id: int
    short_code: str
    content: str
    created_at: str | None = None
    updated_at: str | None = None

    def __post_init__(self) -> None:
        for nome in ("id", "account_id"):
            valor = getattr(self, nome)
            if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
                raise ValueError(f"{nome} deve ser um inteiro positivo.")
        _texto_nao_vazio(self.short_code, "short_code")
        _texto_nao_vazio(self.content, "content")
        for nome in ("created_at", "updated_at"):
            valor = getattr(self, nome)
            if valor is not None and (not isinstance(valor, str) or not valor.strip()):
                raise ValueError(f"{nome} deve ser texto ISO 8601 ou None.")

    @classmethod
    def from_api(cls, dados: Mapping[str, Any]) -> CannedResponse:
        """Lê apenas os campos conhecidos, tolerando extensões do servidor."""
        if not isinstance(dados, Mapping):
            raise ValueError("A resposta rápida deve ser um objeto JSON.")
        try:
            return cls(
                id=dados["id"],
                account_id=dados["account_id"],
                short_code=dados["short_code"],
                content=dados["content"],
                created_at=dados.get("created_at"),
                updated_at=dados.get("updated_at"),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Resposta rápida retornada com campos inválidos.") from exc
