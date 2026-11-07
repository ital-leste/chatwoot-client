"""Gate estático de rastreabilidade da Application API 4.19.0."""
from pathlib import Path


def test_matriz_preserva_as_124_operacoes_e_75_caminhos():
    matriz = (Path(__file__).resolve().parents[1] / "docs" / "MATRIZ_API.md").read_text(
        encoding="utf-8"
    )
    linhas = [
        [coluna.strip() for coluna in linha.split("|")[1:-1]]
        for linha in matriz.splitlines()
        if linha.startswith("| ") and "`/api/" in linha
    ]
    pares = {(item[1], item[2]) for item in linhas}
    caminhos = {item[2] for item in linhas}
    assert len(linhas) == len(pares) == 124
    assert len(caminhos) == 75
    assert all(item[5] and item[6] and item[7] for item in linhas)
    assert {item[7] for item in linhas} == {"Pendente por rota"}
