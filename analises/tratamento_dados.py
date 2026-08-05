import pandas as pd
import os
import time

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.caminhos import BLOCOS, BLOCOS_TRATADOS



def tratar_blocos(
    blocks_dir=str(BLOCOS),
    output_dir=str(BLOCOS_TRATADOS)
):
    inicio = time.time()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    arquivos = sorted(os.listdir(blocks_dir))

    print(f"Encontrados {len(arquivos)} blocos para tratamento.\n")

    for arquivo in arquivos:
        if not arquivo.endswith(".pkl"):
            continue

        caminho = os.path.join(blocks_dir, arquivo)
        print(f"🔧 Tratando bloco: {arquivo}")

        df = pd.read_pickle(caminho)

        # -----------------------------
        # 1. Padronizar nomes das colunas
        # -----------------------------
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(".", "_")
        )

        # -----------------------------
        # 2. Converter Timestamp para datetime
        # -----------------------------
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # -----------------------------
        # 3. Criar colunas derivadas
        # -----------------------------
        df["ano"] = df["timestamp"].dt.year
        df["mes"] = df["timestamp"].dt.month
        df["dia"] = df["timestamp"].dt.day
        df["hora"] = df["timestamp"].dt.hour
        df["dia_semana"] = df["timestamp"].dt.dayofweek

        # Diferença entre valores
        df["diferenca_valor"] = df["amount_received"] - df["amount_paid"]

        # -----------------------------
        # 4. Padronizar moedas
        # -----------------------------
        df["receiving_currency"] = df["receiving_currency"].str.upper()
        df["payment_currency"] = df["payment_currency"].str.upper()

        # -----------------------------
        # 5. Remover duplicatas
        # -----------------------------
        df = df.drop_duplicates()

        # -----------------------------
        # 6. Validar valores negativos
        # -----------------------------
        df = df[(df["amount_received"] >= 0) & (df["amount_paid"] >= 0)]

        # -----------------------------
        # 7. Salvar bloco tratado
        # -----------------------------
        output_path = os.path.join(output_dir, arquivo)
        df.to_pickle(output_path)

        print(f"✔ Bloco tratado e salvo: {arquivo}\n")

    fim = time.time()
    print(f"Tempo total de tratamento: {round(fim - inicio, 2)} segundos")
    print(f"{round((fim - inicio) / 60, 2)} minutos")


if __name__ == "__main__":
    tratar_blocos()
