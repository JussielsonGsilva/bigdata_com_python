import pandas as pd
import os
import time


def analise_temporal(blocks_dir="../data/processed/blocos_tratados"):
    inicio = time.time()

    arquivos = sorted(os.listdir(blocks_dir))

    # Acumuladores
    volume_por_mes = {}
    fraude_por_mes = {}

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:
        if not arquivo.endswith(".pkl"):
            continue

        print(f"⏳ Processando: {arquivo}")
        df = pd.read_pickle(os.path.join(blocks_dir, arquivo))

        # Garantir que timestamp está no formato datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Criar coluna ano-mes (YYYY-MM)
        df["ano_mes"] = df["timestamp"].dt.to_period("M").astype(str)

        # Volume total por mês
        contagem_mes = df["ano_mes"].value_counts().to_dict()

        for mes, qtd in contagem_mes.items():
            volume_por_mes[mes] = volume_por_mes.get(mes, 0) + qtd

        # Fraude por mês
        if "is_laundering" in df.columns:
            fraude_mes = df[df["is_laundering"] ==
                            1]["ano_mes"].value_counts().to_dict()

            for mes, qtd in fraude_mes.items():
                fraude_por_mes[mes] = fraude_por_mes.get(mes, 0) + qtd

    fim = time.time()

    # Ordenar resultados
    volume_por_mes = dict(sorted(volume_por_mes.items()))
    fraude_por_mes = dict(sorted(fraude_por_mes.items()))

    print("\n📌 RESULTADO FINAL — VOLUME POR MÊS")
    for mes, qtd in volume_por_mes.items():
        print(f"{mes}: {qtd}")

    print("\n📌 RESULTADO FINAL — FRAUDE POR MÊS")
    for mes, qtd in fraude_por_mes.items():
        print(f"{mes}: {qtd}")

    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return volume_por_mes, fraude_por_mes


if __name__ == "__main__":
    analise_temporal()
