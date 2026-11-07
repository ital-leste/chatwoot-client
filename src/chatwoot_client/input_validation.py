"""Validações de parâmetros simples compartilhadas, independentes do consumidor."""
from __future__ import annotations
from collections.abc import Sequence


def validar_ids_usuarios(user_ids: Sequence[int]) -> list[int]:
    """IDs positivos e sem duplicatas; rejeita bool, string e lista vazia."""
    if not isinstance(user_ids, (list, tuple)) or not user_ids:
        raise ValueError("user_ids deve ser lista ou tupla não vazia.")
    if any(type(valor) is not int or valor <= 0 for valor in user_ids):
        raise ValueError("Cada user_id deve ser inteiro positivo.")
    if len(user_ids) != len(set(user_ids)):
        raise ValueError("user_ids não deve conter duplicatas.")
    return list(user_ids)

def validar_opcao(valor: str, permitidos: tuple[str, ...], nome: str) -> str:
    """Rejeita opções fora do enum documentado antes de qualquer HTTP."""
    if not isinstance(valor, str) or valor not in permitidos:
        raise ValueError(f"{nome} inválido; permitidos: {', '.join(permitidos)}.")
    return valor


def validar_chaves_json(valor: object) -> None:
    """Rejeita chaves não textuais em qualquer nível do JSON (sem coerção)."""
    from collections.abc import Mapping
    if isinstance(valor, Mapping):
        for chave, filho in valor.items():
            if not isinstance(chave, str):
                raise ValueError("JSON requer chaves string em todos os níveis.")
            validar_chaves_json(filho)
    elif isinstance(valor, (list, tuple)):
        for filho in valor:
            validar_chaves_json(filho)
