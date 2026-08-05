"""
Recombinação final dos blocos em um único arquivo, em streaming.

É a última etapa do pipeline. A anterior (recombine_in_blocks) agrupa chunks
em blocos maiores; esta junta todos os blocos num arquivo só.

A diferença em relação a concatenar tudo com pd.concat é o consumo de memória:
aqui cada bloco é lido, gravado e descartado antes do próximo. O pico fica
próximo do tamanho de UM bloco, não da soma de todos — que é a única forma de
montar um arquivo de 179 milhões de linhas numa máquina comum.

A saída é Parquet, e não PKL: além de ocupar cerca de 4 vezes menos espaço,
Parquet é legível por outras ferramentas e não executa código ao ser aberto,
diferente do pickle.
"""
import os

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

from src.formatos import ler_dados, listar_arquivos_de_dados
from src.logger_config import get_logger

logger = get_logger()


def recombinar_blocos_em_streaming(blocos_dir, arquivo_saida):
    """
    Junta todos os blocos PKL de uma pasta em um único arquivo Parquet,
    gravando incrementalmente e sem acumular os blocos na memória.

    @param blocos_dir     Pasta contendo os arquivos parte_*.pkl
    @param arquivo_saida  Caminho do arquivo Parquet final
    @return               Número total de linhas gravadas
    @raises               FileNotFoundError se a pasta não existir
                          ValueError se não houver nenhum bloco na pasta
    """
    if not os.path.exists(blocos_dir):
        logger.error(f"Pasta não encontrada: {blocos_dir}")
        raise FileNotFoundError(f"Pasta não encontrada: {blocos_dir}")

    arquivos = listar_arquivos_de_dados(blocos_dir)

    if not arquivos:
        logger.error(f"Nenhum bloco encontrado em: {blocos_dir}")
        raise ValueError(f"Nenhum bloco encontrado em: {blocos_dir}")

    logger.info(f"Recombinação em streaming: {len(arquivos)} blocos")
    logger.info(f"Arquivo de saída: {arquivo_saida}")

    os.makedirs(os.path.dirname(os.path.abspath(arquivo_saida)), exist_ok=True)

    escritor = None
    total_de_linhas = 0

    try:
        for caminho in tqdm(arquivos, desc="Recombinando blocos"):
            bloco = ler_dados(caminho)
            tabela = pa.Table.from_pandas(bloco, preserve_index=False)

            # O escritor é criado com o schema do primeiro bloco e reaproveitado
            # nos demais — é o que permite gravar sem juntar tudo antes.
            if escritor is None:
                escritor = pq.ParquetWriter(arquivo_saida, tabela.schema)

            escritor.write_table(tabela)
            total_de_linhas += len(bloco)

            logger.info(f"Bloco gravado: {os.path.basename(caminho)} "
                        f"({len(bloco):,} linhas)")

            # Libera o bloco antes de ler o próximo: sem isso, a referência
            # sobreviveria até a próxima atribuição e dois blocos coexistiriam.
            del bloco, tabela

    except Exception as erro:
        logger.exception(f"Erro durante a recombinação em streaming: {erro}")
        raise

    finally:
        if escritor is not None:
            escritor.close()

    logger.info(f"Recombinação concluída: {total_de_linhas:,} linhas em "
                f"{arquivo_saida}")

    return total_de_linhas
