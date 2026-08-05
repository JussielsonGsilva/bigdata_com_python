import os
import pandas as pd
from tqdm import tqdm
from src.formatos import ler_dados, listar_arquivos_de_dados, salvar_dados
from src.logger_config import get_logger

logger = get_logger()

def recombine_in_blocks(
    chunks_dir: str,
    output_dir: str,
    block_size: int = 20
):
    """
    Recombina arquivos PKL em blocos menores.
    Cada bloco contém 'block_size' chunks concatenados.
    """

    if not os.path.exists(chunks_dir):
        raise FileNotFoundError(f"Pasta não encontrada: {chunks_dir}")

    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Iniciando recombinação em blocos de {block_size} chunks")
    logger.info(f"Lendo chunks de: {chunks_dir}")

    chunk_files = listar_arquivos_de_dados(chunks_dir)

    total_chunks = len(chunk_files)
    logger.info(f"Total de chunks encontrados: {total_chunks}")

    block_index = 0

    for i in range(0, total_chunks, block_size):
        block_files = chunk_files[i:i + block_size]

        logger.info(f"Processando bloco {block_index} ({len(block_files)} chunks)")

        dfs = []
        for file in tqdm(block_files):
            df = ler_dados(file)
            dfs.append(df)

        block_df = pd.concat(dfs, ignore_index=True)

        output_file = salvar_dados(block_df, output_dir, f"parte_{block_index}")

        logger.info(f"Bloco {block_index} salvo em: {output_file}")

        block_index += 1

    logger.info("Recombinação em blocos concluída com sucesso!")
