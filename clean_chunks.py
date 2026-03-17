import os
import shutil

def clean_chunks():
    chunks_dir = "data/processed/chunks_dados_base"

    if os.path.exists(chunks_dir):
        shutil.rmtree(chunks_dir)
        print(f"Pasta removida: {chunks_dir}")
    else:
        print("Pasta de chunks não encontrada.")

if __name__ == "__main__":
    clean_chunks()
