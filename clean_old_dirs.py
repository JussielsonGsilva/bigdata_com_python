import os
import shutil

def remove_if_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Pasta removida: {path}")
    else:
        print(f"Pasta não encontrada: {path}")

if __name__ == "__main__":
    remove_if_exists("data/processed/chunks")
    remove_if_exists("data/processed/chunks_teste")
