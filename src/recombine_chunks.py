import os
import pandas as pd
from tqdm import tqdm
from src.logger_config import get_logger

logger = get_logger()

def recombine_pkls(
    chunks_dir: str,
    output_file: str
):
    """
    Recombina vários arquivos PKL gerados em chunks
    em um único DataFrame final salvo como PKL.

    Parâmetros:
    - chunks_dir: pasta contendo os arquivos chunk_*.pkl
    - output_file: caminho do arquivo final .pkl
    """

    if not os.path.exists(chunks_dir):
        logger.error(f"Pasta não encontrada: {chunks_dir}")
        raise FileNotFoundError(f"Pasta não encontrada: {chunks_dir}")

    logger.info(f"Iniciando recombinação dos chunks em: {chunks_dir}")

    # Lista todos os arquivos PKL na pasta
    chunk_files = sorted([
        os.path.join(chunks_dir, f)
        for f in os.listdir(chunks_dir)
        if f.endswith(".pkl")
    ])

    if not chunk_files:
        logger.error("Nenhum arquivo PKL encontrado para recombinar.")
        raise ValueError("Nenhum arquivo PKL encontrado.")

    logger.info(f"Total de chunks encontrados: {len(chunk_files)}")

    # Lista para armazenar os DataFrames
    dfs = []

    # Carrega cada chunk
    for file in tqdm(chunk_files):
        df = pd.read_pickle(file)
        dfs.append(df)

    # Concatena tudo
    final_df = pd.concat(dfs, ignore_index=True)

    # Salva o resultado final
    final_df.to_pickle(output_file)

    logger.info(f"Arquivo final salvo em: {output_file}")
    logger.info("Recombinação concluída com sucesso!")
