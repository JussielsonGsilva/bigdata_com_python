import os
import pandas as pd
from src.logger_config import get_logger

logger = get_logger()

def recombine_final(blocks_dir: str, output_file: str):
    logger.info(f"Lendo blocos de: {blocks_dir}")

    block_files = sorted([
        os.path.join(blocks_dir, f)
        for f in os.listdir(blocks_dir)
        if f.endswith(".pkl")
    ])

    logger.info(f"Total de blocos encontrados: {len(block_files)}")

    dfs = []
    for file in block_files:
        logger.info(f"Lendo bloco: {file}")
        df = pd.read_pickle(file)
        dfs.append(df)

    logger.info("Concatenando blocos...")
    final_df = pd.concat(dfs, ignore_index=True)

    logger.info(f"Salvando arquivo final em: {output_file}")
    final_df.to_pickle(output_file)

    logger.info("Recombinação final concluída com sucesso!")


if __name__ == "__main__":
    recombine_final(
        blocks_dir="data/processed/blocos",
        output_file="data/processed/dados_base_final.pkl"
    )
