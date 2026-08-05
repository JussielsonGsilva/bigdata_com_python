"""
Otimização de tipos dos DataFrames.

Ler um CSV com os padrões do pandas gera colunas mais largas do que os dados
precisam: todo inteiro vira int64, todo texto vira object. Num dataset de 179
milhões de linhas isso custa gigabytes de RAM sem nenhum ganho.

O ajuste é de duas naturezas:

  - texto que se repete muito (moeda, formato de pagamento) vira `category`,
    que guarda cada valor distinto uma única vez e usa um código por linha;
  - identificadores inteiros (banco, ano, mês, hora) são reduzidos ao menor
    tipo que comporta a faixa de valores presente.

O que NÃO é otimizado, de propósito: as colunas de valor monetário. Reduzi-las
para float32 economizaria memória, mas float32 tem cerca de 7 dígitos
significativos — com valores que chegam a trilhões, centavos seriam
arredondados em silêncio. Precisão vale mais que memória em dado financeiro.
"""
import pandas as pd

# Texto com poucos valores distintos em relação ao número de linhas.
# Guardar como category troca o texto repetido por um código por linha.
COLUNAS_CATEGORICAS = (
    "receiving_currency",
    "payment_currency",
    "payment_format",
)

# Identificadores e componentes de data: inteiros de faixa pequena.
COLUNAS_INTEIRAS = (
    "from_bank",
    "to_bank",
    "is_laundering",
    "ano",
    "mes",
    "dia",
    "hora",
    "dia_semana",
)

# Nunca reduzir: perder precisão aqui é corromper o dado.
COLUNAS_DE_VALOR = (
    "amount_paid",
    "amount_received",
    "diferenca_valor",
)


def otimizar_tipos(df):
    """
    Reduz o consumo de memória de um DataFrame sem alterar nenhum valor.

    Só mexe nas colunas que existirem — o mesmo DataFrame passa por aqui
    antes e depois das colunas derivadas serem criadas.

    @param df  DataFrame a otimizar (alterado no lugar e também devolvido)
    @return    O próprio DataFrame, com os tipos ajustados
    """
    for coluna in COLUNAS_CATEGORICAS:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype("category")

    for coluna in COLUNAS_INTEIRAS:
        if coluna in df.columns and pd.api.types.is_integer_dtype(df[coluna]):
            # 'unsigned' quando não há negativos economiza mais um bit de faixa
            tipo_alvo = "unsigned" if df[coluna].min() >= 0 else "integer"
            df[coluna] = pd.to_numeric(df[coluna], downcast=tipo_alvo)

    return df


def resumo_de_memoria(df):
    """
    Consumo de memória do DataFrame em MB, contando o conteúdo real do texto.

    @param df  DataFrame a medir
    @return    Consumo em megabytes
    """
    return df.memory_usage(deep=True).sum() / 1024 ** 2
