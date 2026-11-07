"""Rastreabilidade funcional de todos os 124 pares verbo/rota para CWClient.

Não executa HTTP nem exige uma instalação de Chatwoot.
"""
from __future__ import annotations

import re
from pathlib import Path

from chatwoot_client import CWClient


def _linhas_matriz():
    tabela = (Path(__file__).resolve().parents[1] / "docs" / "MATRIZ_API.md").read_text(
        encoding="utf-8"
    )
    return [
        [col.strip() for col in linha.split("|")[1:-1]]
        for linha in tabela.splitlines()
        if linha.startswith("| ") and "`/api/" in linha
    ]


def test_todos_os_124_endpoints_tem_metodo_publico():
    linhas = _linhas_matriz()
    assert len(linhas) == 124
    assert len({(col[1], col[2]) for col in linhas}) == 124
    assert len({col[2] for col in linhas}) == 75

    with CWClient("https://chatwoot.example", "token-ficticio") as cw:
        for col in linhas:
            encontrou = re.search(r"cw\.([a-z_]+)\.([a-z_]+)\(", col[3])
            assert encontrou, f"Sem recurso/método na matriz: {col[3]}"
            recurso, metodo = encontrou.groups()
            objeto = getattr(cw, recurso, None)
            assert objeto is not None, f"Recurso ausente: {recurso}"
            assert callable(getattr(objeto, metodo, None)), (
                f"Operação sem implementação: {col[1]} {col[2]} -> {col[3]}"
            )
        assert callable(cw.messages.send_media)  # formato multipart da mesma rota
        assert callable(cw.profile.update_multipart)
        assert callable(cw.account.update_form)
