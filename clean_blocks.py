import os
import shutil

def clean_blocks():
    blocks_dir = "data/processed/blocos"

    if os.path.exists(blocks_dir):
        shutil.rmtree(blocks_dir)
        print(f"Pasta removida: {blocks_dir}")
    else:
        print("Pasta de blocos não encontrada.")

if __name__ == "__main__":
    clean_blocks()
