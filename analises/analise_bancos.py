import pandas as pd
import os
import time
from collections import defaultdict

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.formatos import ler_dados, listar_arquivos_de_dados
from src.caminhos import BLOCOS_TRATADOS



def analise_bancos(blocks_dir=str(BLOCOS_TRATADOS)):
    inicio = time.time()

    arquivos = listar_arquivos_de_dados(blocks_dir)

    # Acumuladores
    enviados_por_banco = defaultdict(int)
    recebidos_por_banco = defaultdict(int)
    fluxo_banco_para_banco = defaultdict(int)
    fluxo_suspeito = defaultdict(int)

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:

        print(f"🏦 Processando: {arquivo}")
        df = ler_dados(arquivo)

        # Volume enviado por banco
        enviados = df["from_bank"].value_counts().to_dict()
        for banco, qtd in enviados.items():
            enviados_por_banco[banco] += qtd

        # Volume recebido por banco
        recebidos = df["to_bank"].value_counts().to_dict()
        for banco, qtd in recebidos.items():
            recebidos_por_banco[banco] += qtd

        # Fluxo origem → destino
        pares = df.groupby(["from_bank", "to_bank"]).size().to_dict()
        for (origem, destino), qtd in pares.items():
            fluxo_banco_para_banco[(origem, destino)] += qtd

        # Fluxo suspeito
        if "is_laundering" in df.columns:
            suspeitos = df[df["is_laundering"] == 1].groupby(
                ["from_bank", "to_bank"]).size().to_dict()
            for (origem, destino), qtd in suspeitos.items():
                fluxo_suspeito[(origem, destino)] += qtd

    fim = time.time()

    print("\n📌 RESULTADO — TOP BANCOS QUE MAIS ENVIAM")
    for banco, qtd in sorted(enviados_por_banco.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{banco}: {qtd}")

    print("\n📌 RESULTADO — TOP BANCOS QUE MAIS RECEBEM")
    for banco, qtd in sorted(recebidos_por_banco.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{banco}: {qtd}")

    print("\n📌 RESULTADO — TOP FLUXOS ENTRE BANCOS")
    for (origem, destino), qtd in sorted(fluxo_banco_para_banco.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{origem} → {destino}: {qtd}")

    print("\n📌 RESULTADO — FLUXOS SUSPEITOS ENTRE BANCOS")
    for (origem, destino), qtd in sorted(fluxo_suspeito.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{origem} → {destino}: {qtd}")

    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return enviados_por_banco, recebidos_por_banco, fluxo_banco_para_banco, fluxo_suspeito


if __name__ == "__main__":
    analise_bancos()
