from src.recombine_in_blocks import recombine_in_blocks

if __name__ == "__main__":
    recombine_in_blocks(
        chunks_dir="data/processed/chunks_dados_base",
        output_dir="data/processed/blocos",
        block_size=20
    )
