from src.recombine_chunks import recombine_pkls

if __name__ == "__main__":
    recombine_pkls(
        chunks_dir="data/processed/chunks_teste",
        output_file="data/processed/final.pkl"
    )
