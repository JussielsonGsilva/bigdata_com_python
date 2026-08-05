import pandas as pd
import os
import time
from collections import defaultdict

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.caminhos import BLOCOS_TRATADOS



def analise_moedas(blocks_dir=str(BLOCOS_TRATADOS)):
    inicio = time.time()

    arquivos = sorted(os.listdir(blocks_dir))

    freq_moedas = defaultdict(int)
    freq_moedas_fraude = defaultdict(int)

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:
        if not arquivo.endswith(".pkl"):
            continue

        print(f"💱 Processando: {arquivo}")
        df = pd.read_pickle(os.path.join(blocks_dir, arquivo))

        # Moedas de entrada
        moedas_recebidas = df["receiving_currency"].value_counts().to_dict()
        for moeda, qtd in moedas_recebidas.items():
            freq_moedas[moeda] += qtd

        # Moedas de saída
        moedas_pagamento = df["payment_currency"].value_counts().to_dict()
        for moeda, qtd in moedas_pagamento.items():
            freq_moedas[moeda] += qtd

        # Fraudes
        if "is_laundering" in df.columns:
            df_fraude = df[df["is_laundering"] == 1]

            moedas_recebidas_f = df_fraude["receiving_currency"].value_counts(
            ).to_dict()
            for moeda, qtd in moedas_recebidas_f.items():
                freq_moedas_fraude[moeda] += qtd

            moedas_pagamento_f = df_fraude["payment_currency"].value_counts(
            ).to_dict()
            for moeda, qtd in moedas_pagamento_f.items():
                freq_moedas_fraude[moeda] += qtd

    fim = time.time()

    print("\n📌 RESULTADO — MOEDAS MAIS UTILIZADAS")
    for moeda, qtd in sorted(freq_moedas.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{moeda}: {qtd}")

    print("\n📌 RESULTADO — MOEDAS MAIS ASSOCIADAS A FRAUDE")
    for moeda, qtd in sorted(freq_moedas_fraude.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{moeda}: {qtd}")

    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return freq_moedas, freq_moedas_fraude


if __name__ == "__main__":
    analise_moedas()
