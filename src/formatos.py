"""
Leitura e escrita dos arquivos intermediários do pipeline.

Existe por dois motivos.

**Compatibilidade de formato.** O pipeline grava em Parquet, que ocupa cerca de
um quarto do espaço do pickle e não executa código ao ser aberto. Mas há blocos
`.pkl` gerados por versões anteriores — reprocessar dezenas de gigabytes só por
causa de mudança de formato não é aceitável. A leitura aceita os dois; a escrita
usa sempre Parquet.

**Ordenação correta.** `sorted()` em nomes de arquivo é alfabético, então
`chunk_10` viria antes de `chunk_2`. Como os blocos representam fatias
sequenciais do dataset, essa ordem importa: a numeração é extraída do nome e
comparada como número.
"""
import os
import re

import pandas as pd

# Formatos que o pipeline sabe ler
EXTENSOES_DE_LEITURA = (".parquet", ".pkl")

# Formato usado em toda escrita nova
EXTENSAO_DE_ESCRITA = ".parquet"

_NUMEROS = re.compile(r"(\d+)")


def _chave_de_ordenacao(caminho):
    """
    Chave que ordena 'chunk_2' antes de 'chunk_10'.

    Quebra o nome em trechos de texto e de número, comparando os números como
    inteiros — o alfabético puro colocaria '10' antes de '2'.

    @param caminho  Caminho do arquivo
    @return         Lista alternando texto e número, usável como chave de sort
    """
    nome = os.path.basename(caminho)
    return [
        int(parte) if parte.isdigit() else parte.lower()
        for parte in _NUMEROS.split(nome)
    ]


def listar_arquivos_de_dados(pasta):
    """
    Lista os arquivos de dados de uma pasta, em ordem numérica.

    Aceita `.parquet` e `.pkl` na mesma pasta, o que permite migrar o formato
    aos poucos. Qualquer outro arquivo é ignorado.

    @param pasta  Diretório a listar
    @return       Lista de caminhos completos, ordenados
    @raises       FileNotFoundError se a pasta não existir
    """
    if not os.path.exists(pasta):
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    arquivos = [
        os.path.join(pasta, nome)
        for nome in os.listdir(pasta)
        if nome.endswith(EXTENSOES_DE_LEITURA)
    ]

    return sorted(arquivos, key=_chave_de_ordenacao)


def ler_dados(caminho):
    """
    Lê um arquivo de dados, escolhendo o leitor pela extensão.

    @param caminho  Caminho do arquivo `.parquet` ou `.pkl`
    @return         DataFrame com o conteúdo do arquivo
    @raises         ValueError se a extensão não for suportada
    """
    caminho = str(caminho)

    if caminho.endswith(".parquet"):
        return pd.read_parquet(caminho)

    if caminho.endswith(".pkl"):
        return pd.read_pickle(caminho)

    raise ValueError(
        f"Formato não suportado: {caminho}. "
        f"Esperado um destes: {', '.join(EXTENSOES_DE_LEITURA)}"
    )


def salvar_dados(df, pasta, nome_base):
    """
    Grava um DataFrame em Parquet dentro da pasta indicada.

    @param df         DataFrame a gravar
    @param pasta      Diretório de destino (criado se não existir)
    @param nome_base  Nome do arquivo sem extensão, ex: "parte_0"
    @return           Caminho completo do arquivo gravado
    """
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"{nome_base}{EXTENSAO_DE_ESCRITA}")

    # index=False porque o índice é apenas a numeração de linhas do pandas,
    # sem significado no dado — gravá-lo só aumentaria o arquivo.
    df.to_parquet(caminho, index=False)

    return caminho
