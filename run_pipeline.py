"""
Etapa 1 do pipeline: lê o CSV bruto em lotes e salva cada lote como PKL.

Executar a partir da raiz do projeto:
    python run_pipeline.py
"""
from src.caminhos import ARQUIVO_BRUTO, CHUNKS
from src.pipeline_chunks import process_csv_in_chunks

if __name__ == "__main__":
    process_csv_in_chunks(
        input_path=str(ARQUIVO_BRUTO),
        output_dir=str(CHUNKS),
        # quantas linhas cada chunk terá
        chunk_size=2_000_000,
    )
