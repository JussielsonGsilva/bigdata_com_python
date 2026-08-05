import pandas as pd
import os
import time

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.caminhos import BLOCOS_TRATADOS



def analise_correlacao(blocks_dir=str(BLOCOS_TRATADOS)):
    inicio = time.time()

    arquivos = sorted(os.listdir(blocks_dir))

    colunas = [
        "amount_received",
        "amount_paid",
        "diferenca_valor",
        "hora",
        "dia_semana",
        "from_bank",
        "to_bank",
        "receiving_currency",
        "payment_currency",
        "is_laundering"
    ]

    soma = None
    soma_quadrado = None
    soma_produto = None
    n_total = 0

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:
        if not arquivo.endswith(".pkl"):
            continue

        print(f"📊 Processando: {arquivo}")
        df = pd.read_pickle(os.path.join(blocks_dir, arquivo))

        df = df[colunas].copy()

        # Codificar categorias
        for col in ["from_bank", "to_bank", "receiving_currency", "payment_currency"]:
            df[col], _ = pd.factorize(df[col])

        df = df.astype(float)

        if soma is None:
            soma = df.sum()
            soma_quadrado = (df ** 2).sum()
            soma_produto = df.T.dot(df)
            n_total = len(df)
        else:
            soma += df.sum()
            soma_quadrado += (df ** 2).sum()
            soma_produto += df.T.dot(df)
            n_total += len(df)

    media = soma / n_total
    variancia = (soma_quadrado / n_total) - (media ** 2)
    desvio = variancia ** 0.5

    correlacao = (soma_produto / n_total - media.values.reshape(-1, 1) * media.values) / (
        desvio.values.reshape(-1, 1) * desvio.values
    )

    correlacao_df = pd.DataFrame(correlacao, index=colunas, columns=colunas)

    print("\n📌 Correlação com is_laundering:")
    print(correlacao_df["is_laundering"].sort_values(ascending=False))

    fim = time.time()
    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return correlacao_df


if __name__ == "__main__":
    analise_correlacao()
