"""
Etapa 2 do pipeline: reagrupa os chunks em blocos maiores.

Executar a partir da raiz do projeto:
    python run_recombine_blocks.py
"""
from src.caminhos import BLOCOS, CHUNKS
from src.recombine_in_blocks import recombine_in_blocks

if __name__ == "__main__":
    recombine_in_blocks(
        chunks_dir=str(CHUNKS),
        output_dir=str(BLOCOS),
        block_size=10,
    )
