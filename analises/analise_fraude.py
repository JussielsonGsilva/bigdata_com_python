import pandas as pd
import os
import time
from collections import defaultdict

def analise_fraude(blocks_dir="../data/processed/blocos_tratados"):
    inicio = time.time()

    arquivos = sorted(os.listdir(blocks_dir))

    # Acumuladores
    total_fraudes = 0
    total_transacoes = 0

    fraude_por_hora = defaultdict(int)
    fraude_por_dia_semana = defaultdict(int)
    fraude_por_banco_origem = defaultdict(int)
    fraude_por_banco_destino = defaultdict(int)
    fraude_por_moeda = defaultdict(int)

    print(f"Analisando {len(arquivos)} blocos tratados...\n")

    for arquivo in arquivos:
        if not arquivo.endswith(".pkl"):
            continue

        print(f"🕵️ Processando: {arquivo}")
        df = pd.read_pickle(os.path.join(blocks_dir, arquivo))

        total_transacoes += len(df)

        df_fraude = df[df["is_laundering"] == 1]
        total_fraudes += len(df_fraude)

        # Hora
        for h, qtd in df_fraude["hora"].value_counts().to_dict().items():
            fraude_por_hora[h] += qtd

        # Dia da semana
        for d, qtd in df_fraude["dia_semana"].value_counts().to_dict().items():
            fraude_por_dia_semana[d] += qtd

        # Bancos
        for b, qtd in df_fraude["from_bank"].value_counts().to_dict().items():
            fraude_por_banco_origem[b] += qtd

        for b, qtd in df_fraude["to_bank"].value_counts().to_dict().items():
            fraude_por_banco_destino[b] += qtd

        # Moedas
        moedas_rec = df_fraude["receiving_currency"].value_counts().to_dict()
        moedas_pag = df_fraude["payment_currency"].value_counts().to_dict()

        for m, qtd in moedas_rec.items():
            fraude_por_moeda[m] += qtd

        for m, qtd in moedas_pag.items():
            fraude_por_moeda[m] += qtd

    fim = time.time()

    print("\n📌 TOTAL DE FRAUDES")
    print(f"{total_fraudes} de {total_transacoes} transações")

    print("\n📌 FRAUDE POR HORA")
    print(dict(sorted(fraude_por_hora.items())))

    print("\n📌 FRAUDE POR DIA DA SEMANA")
    print(dict(sorted(fraude_por_dia_semana.items())))

    print("\n📌 TOP BANCOS DE ORIGEM EM FRAUDE")
    for b, qtd in sorted(fraude_por_banco_origem.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{b}: {qtd}")

    print("\n📌 TOP BANCOS DE DESTINO EM FRAUDE")
    for b, qtd in sorted(fraude_por_banco_destino.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{b}: {qtd}")

    print("\n📌 MOEDAS MAIS USADAS EM FRAUDE")
    for m, qtd in sorted(fraude_por_moeda.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{m}: {qtd}")

    print(f"\n⏳ Tempo total: {round(fim - inicio, 2)} segundos")
    print(f"   ({round((fim - inicio)/60, 2)} minutos)")

    return {
        "total_fraudes": total_fraudes,
        "total_transacoes": total_transacoes,
        "fraude_por_hora": fraude_por_hora,
        "fraude_por_dia_semana": fraude_por_dia_semana,
        "fraude_por_banco_origem": fraude_por_banco_origem,
        "fraude_por_banco_destino": fraude_por_banco_destino,
        "fraude_por_moeda": fraude_por_moeda,
    }


if __name__ == "__main__":
    analise_fraude()
