from src.pipeline_chunks import process_csv_in_chunks

if __name__ == "__main__":
    process_csv_in_chunks(
        input_path="data/raw/dados_base.csv",
        output_dir="data/processed/chunks_dados_base",     # pasta de saída
        chunk_size=1_000_000                               # aqui determinamos quantas linhas teram cada chunk 
    )

# Para rodar o código--> python run_pipeline.py
