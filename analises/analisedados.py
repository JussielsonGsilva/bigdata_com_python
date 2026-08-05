import pandas as pd
import os
import time

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.formatos import ler_dados, listar_arquivos_de_dados
from src.caminhos import BLOCOS


def analisar_blocos(blocks_dir=str(BLOCOS)):
    inicio = time.time()

    resultados = {
        "total_linhas": 0,
        "total_colunas": None,
        "tipos_colunas": {},
        "nulos_por_coluna": {},
        "total_nulos": 0
    }

    arquivos = listar_arquivos_de_dados(blocks_dir)

    print(f"Encontrados {len(arquivos)} blocos para análise.\n")

    for arquivo in arquivos:
        print(f"🔍 Lendo bloco: {Path(arquivo).name}")

        df = ler_dados(arquivo)

        # Atualiza total de linhas
        resultados["total_linhas"] += len(df)

        # Atualiza total de colunas (apenas uma vez)
        if resultados["total_colunas"] is None:
            resultados["total_colunas"] = len(df.columns)

        # Atualiza tipos de colunas (apenas uma vez)
        if not resultados["tipos_colunas"]:
            resultados["tipos_colunas"] = df.dtypes.astype(str).to_dict()

        # Nulos por coluna
        nulos = df.isnull().sum()

        for col, qtd in nulos.items():
            resultados["nulos_por_coluna"][col] = resultados["nulos_por_coluna"].get(col, 0) + qtd

        # Total de nulos
        resultados["total_nulos"] += nulos.sum()

        print(f"✔ Bloco {arquivo} analisado.\n")

    fim = time.time()
    resultados["tempo_execucao"] = round(fim - inicio, 2)

    return resultados


if __name__ == "__main__":
    resumo = analisar_blocos()

    print("\n===== RESUMO FINAL =====")
    print(f"Total de linhas: {resumo['total_linhas']}")
    print(f"Total de colunas: {resumo['total_colunas']}")
    print(f"Total de valores nulos: {resumo['total_nulos']}")

    print("\nTempo total de execução:")
    print(f"{resumo['tempo_execucao']} segundos")
    print(f"{round(resumo['tempo_execucao'] / 60, 2)} minutos")

    print("\nNulos por coluna:")
    for col, qtd in resumo["nulos_por_coluna"].items():
        print(f"  {col}: {qtd}")

    print("\nTipos das colunas:")
    for col, tipo in resumo["tipos_colunas"].items():
        print(f"  {col}: {tipo}")
