"""
Remove a pasta de chunks depois que os blocos já foram gerados.

Executar a partir da raiz do projeto:
    python clean_chunks.py
"""
import shutil

from src.caminhos import CHUNKS


def clean_chunks():
    """Apaga a pasta de chunks intermediários, se existir."""
    if CHUNKS.exists():
        shutil.rmtree(CHUNKS)
        print(f"Pasta removida: {CHUNKS}")
    else:
        print("Pasta de chunks não encontrada.")


if __name__ == "__main__":
    clean_chunks()
