import pandas as pd
from tqdm import tqdm
import os
from src.formatos import salvar_dados
from src.logger_config import get_logger

logger = get_logger()

def process_csv_in_chunks(
    input_path: str,
    output_dir: str,
    chunk_size: int = 500_000
):
    """
    Lê um CSV gigante em chunks e salva cada lote como PKL.
    Versão otimizada para arquivos muito grandes.
    """

    # Verifica se o arquivo existe
    if not os.path.exists(input_path):
        logger.error(f"Arquivo não encontrado: {input_path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    logger.info(f"Iniciando processamento do arquivo: {input_path}")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Leitura em chunks sem calcular total de linhas (mais eficiente)
        for i, chunk in enumerate(
            tqdm(pd.read_csv(input_path, chunksize=chunk_size))
        ):
            # Grava em Parquet: ocupa cerca de um quarto do espaço do pickle
            # e pode ser lido por outras ferramentas
            output_file = salvar_dados(chunk, output_dir, f"chunk_{i}")

            logger.info(f"Chunk {i} salvo em {output_file}")

        logger.info("Processamento concluído com sucesso!")

    except Exception as e:
        logger.exception(f"Erro durante o processamento: {e}")
        raise
