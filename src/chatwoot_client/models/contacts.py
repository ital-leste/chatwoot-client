"""Contrato de entrada imutável para criação e atualização de contatos."""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Any


class _NaoInformado:
    """Distingue campo ausente de None explicitamente informado."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NAO_INFORMADO"


_NAO_INFORMADO = _NaoInformado()
_EMAIL_SIMPLES = re.compile(r"[^@\s]+@[^@\s]+")
_TELEFONE_E164 = re.compile(r"\+[1-9]\d{1,14}")


@dataclass(frozen=True, slots=True, kw_only=True)
class Contact:
    """Apenas atributos de escrita; respostas da API permanecem JSON nativo.

    Campos omitidos não entram no payload; None explícito é serializado como
    JSON null (a aceitação da limpeza depende da regra do servidor).
    """

    name: str | None | _NaoInformado = _NAO_INFORMADO
    email: str | None | _NaoInformado = _NAO_INFORMADO
    phone_number: str | None | _NaoInformado = _NAO_INFORMADO
    identifier: str | None | _NaoInformado = _NAO_INFORMADO
    blocked: bool | _NaoInformado = _NAO_INFORMADO
    avatar_url: str | None | _NaoInformado = _NAO_INFORMADO
    additional_attributes: Mapping[str, Any] | None | _NaoInformado = _NAO_INFORMADO
    custom_attributes: Mapping[str, Any] | None | _NaoInformado = _NAO_INFORMADO

    def __post_init__(self) -> None:
        for nome in ("name", "email", "phone_number", "identifier", "avatar_url"):
            valor = getattr(self, nome)
            if valor is _NAO_INFORMADO or valor is None:
                continue
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"{nome} deve ser texto não vazio ou None.")
            if nome == "name" and len(valor) > 255:
                raise ValueError("name deve ter no máximo 255 caracteres.")
            if nome == "email" and not _EMAIL_SIMPLES.fullmatch(valor):
                raise ValueError("email possui formato inválido.")
            if nome == "phone_number" and not _TELEFONE_E164.fullmatch(valor):
                raise ValueError("phone_number deve estar no formato E.164 (+ seguido de 2 a 15 dígitos).")

        if self.blocked is not _NAO_INFORMADO and not isinstance(self.blocked, bool):
            raise ValueError("blocked deve ser bool quando informado.")

        for nome in ("additional_attributes", "custom_attributes"):
            valor = getattr(self, nome)
            if valor is _NAO_INFORMADO or valor is None:
                continue
            if not isinstance(valor, Mapping) or any(not isinstance(chave, str) for chave in valor):
                raise ValueError(f"{nome} deve ser objeto JSON com chaves string, ou None.")
            try:
                json.dumps(dict(valor), allow_nan=False)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{nome} deve conter valores compatíveis com JSON.") from exc

    def to_payload(self) -> dict[str, Any]:
        """Mantém apenas campos informados, inclusive False, {} e None explícitos."""
        resultado: dict[str, Any] = {}
        for campo in fields(self):
            valor = getattr(self, campo.name)
            if valor is _NAO_INFORMADO:
                continue
            resultado[campo.name] = dict(valor) if isinstance(valor, Mapping) else valor
        return resultado
