"""Transporte HTTP do pacote; não aplica retry automático."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any
import httpx


def executar(
    sessao: httpx.Client,
    base_path: str,
    metodo: str,
    caminho: str,
    *,
    dados: Mapping[str, Any] | None = None,
    parametros: Mapping[str, Any] | None = None,
    arquivos: Sequence[tuple[str, tuple[str, bytes, str]]] | None = None,
) -> httpx.Response:
    relativo = caminho.lstrip("/")
    if base_path:
        relativo = f"{base_path}/{relativo}"
    if arquivos is not None:
        return sessao.request(
            metodo, relativo, data=dict(dados or {}),
            files=list(arquivos), params=parametros,
        )
    return sessao.request(
        metodo, relativo, json=dict(dados) if dados is not None else None,
        params=parametros,
    )
