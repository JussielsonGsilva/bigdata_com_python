"""
Etapa 4 do pipeline: junta todos os blocos tratados num único arquivo Parquet,
em streaming — sem carregar o conjunto inteiro na memória.

Executar a partir da raiz do projeto:
    python run_recombine_final_stream.py
"""
from src.caminhos import ARQUIVO_FINAL, BLOCOS_TRATADOS
from src.recombine_stream import recombinar_blocos_em_streaming

if __name__ == "__main__":
    recombinar_blocos_em_streaming(
        blocos_dir=str(BLOCOS_TRATADOS),
        arquivo_saida=str(ARQUIVO_FINAL),
    )
