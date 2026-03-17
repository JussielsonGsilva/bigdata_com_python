import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from src.logger_config import get_logger

logger = get_logger()

def recombine_final_stream(blocks_dir: str, output_file: str):
    logger.info("Iniciando recombinação final em streaming")
    logger.info(f"Lendo blocos de: {blocks_dir}")

    block_files = sorted([
        os.path.join(blocks_dir, f)
        for f in os.listdir(blocks_dir)
        if f.endswith(".pkl")
    ])

    logger.info(f"Total de blocos encontrados: {len(block_files)}")

    writer = None  # ParquetWriter será criado no primeiro bloco

    for file in block_files:
        logger.info(f"Lendo bloco: {file}")
        df = pd.read_pickle(file)

        # Converte para tabela Arrow
        table = pa.Table.from_pandas(df)

        if writer is None:
            # Cria o arquivo Parquet com o schema do primeiro bloco
            writer = pq.ParquetWriter(output_file, table.schema)
            logger.info(f"Arquivo Parquet criado: {output_file}")

        # Escreve o bloco no arquivo
        writer.write_table(table)
        logger.info("Bloco escrito com sucesso")

    if writer:
        writer.close()

    logger.info("Recombinação final concluída com sucesso!")
    logger.info(f"Arquivo final salvo em: {output_file}")


if __name__ == "__main__":
    recombine_final_stream(
        blocks_dir="data/processed/blocos",
        output_file="data/processed/dados_base_final.parquet"
    )
