from src.pipeline_chunks import process_csv_in_chunks

if __name__ == "__main__":
    process_csv_in_chunks(
        input_path="data/raw/dados_base.csv",
        output_dir="data/processed/chunks_dados_base",     # pasta de saída
        # aqui determinamos quantas linhas teram cada chunk
        chunk_size=2_000_000
    )

# Para rodar o código--> python run_pipeline.py
