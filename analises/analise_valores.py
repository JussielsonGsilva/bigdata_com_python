import pandas as pd
import os
import numpy as np
import time

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.formatos import ler_dados, listar_arquivos_de_dados
from src.caminhos import BLOCOS_TRATADOS



def analisar_valores(
    blocks_dir=str(BLOCOS_TRATADOS)
):
    inicio = time.time()

    arquivos = listar_arquivos_de_dados(blocks_dir)

    estatisticas = {
        "amount_paid": [],
        "amount_received": [],
        "diferenca_valor": []
    }

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:

        print(f"📊 Processando: {arquivo}")
        df = ler_dados(arquivo)

        for coluna in estatisticas.keys():
            serie = df[coluna]

            estatisticas[coluna].append({
                "min": serie.min(),
                "max": serie.max(),
                "mean": serie.mean(),
                "median": serie.median(),
                "std": serie.std(),
                "p1": serie.quantile(0.01),
                "p5": serie.quantile(0.05),
                "p25": serie.quantile(0.25),
                "p50": serie.quantile(0.50),
                "p75": serie.quantile(0.75),
                "p95": serie.quantile(0.95),
                "p99": serie.quantile(0.99),
                "count": len(serie)
            })

    # Consolidar estatísticas
    resumo_final = {}

    for coluna, lista in estatisticas.items():
        df_est = pd.DataFrame(lista)

        resumo_final[coluna] = {
            "min": df_est["min"].min(),
            "max": df_est["max"].max(),
            "mean": df_est["mean"].mean(),
            "median": df_est["median"].median(),
            "std": df_est["std"].mean(),
            "p1": df_est["p1"].mean(),
            "p5": df_est["p5"].mean(),
            "p25": df_est["p25"].mean(),
            "p50": df_est["p50"].mean(),
            "p75": df_est["p75"].mean(),
            "p95": df_est["p95"].mean(),
            "p99": df_est["p99"].mean(),
            "total_linhas": df_est["count"].sum()
        }

    fim = time.time()

    print("\n📌 **Resumo Final da Análise de Valores**")
    for coluna, valores in resumo_final.items():
        print(f"\n🔹 {coluna.upper()}:")
        for k, v in valores.items():
            print(f"   {k}: {v}")

    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return resumo_final


if __name__ == "__main__":
    analisar_valores()
