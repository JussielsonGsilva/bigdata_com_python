import pandas as pd
import os
import time

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.formatos import ler_dados, listar_arquivos_de_dados, salvar_dados
from src.caminhos import BLOCOS, BLOCOS_TRATADOS
from src.otimizacao import otimizar_tipos, resumo_de_memoria



def tratar_blocos(
    blocks_dir=str(BLOCOS),
    output_dir=str(BLOCOS_TRATADOS)
):
    inicio = time.time()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    arquivos = listar_arquivos_de_dados(blocks_dir)

    print(f"Encontrados {len(arquivos)} blocos para tratamento.\n")

    for arquivo in arquivos:
        print(f"🔧 Tratando bloco: {Path(arquivo).name}")

        df = ler_dados(arquivo)

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
        # 7. Otimizar tipos antes de salvar
        # -----------------------------
        # Feito por último, depois das colunas derivadas existirem, para que
        # elas também sejam reduzidas. Não altera nenhum valor — as colunas
        # monetárias ficam de fora justamente para não perder precisão.
        memoria_antes = resumo_de_memoria(df)
        df = otimizar_tipos(df)
        memoria_depois = resumo_de_memoria(df)

        # -----------------------------
        # 8. Salvar bloco tratado
        # -----------------------------
        nome_base = Path(arquivo).stem
        output_path = salvar_dados(df, output_dir, nome_base)

        print(f"✔ Bloco tratado e salvo: {Path(output_path).name}")
        print(f"  memória: {memoria_antes:.1f} MB → {memoria_depois:.1f} MB "
              f"({100 * (1 - memoria_depois / memoria_antes):.0f}% menos)\n")

    fim = time.time()
    print(f"Tempo total de tratamento: {round(fim - inicio, 2)} segundos")
    print(f"{round((fim - inicio) / 60, 2)} minutos")


if __name__ == "__main__":
    tratar_blocos()
