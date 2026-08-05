"""
Caminhos do projeto, em um lugar só.

Motivo de existir: o pipeline tem 4 etapas encadeadas, cada uma lendo o que
a anterior escreveu. Quando cada arquivo declara seu próprio caminho, basta
uma letra de diferença para o fluxo quebrar em silêncio — foi o que acontecia
entre 'blocks_tratados' (onde o tratamento gravava) e 'blocos_tratados' (onde
as análises liam).

Todos os caminhos são absolutos, calculados a partir da localização deste
arquivo. Assim os scripts funcionam sendo chamados da raiz do projeto ou de
dentro de analises/ — antes, o '..' nos caminhos fazia a pasta data/ ser
procurada fora do projeto.
"""
from pathlib import Path

# Raiz do projeto: este arquivo está em <raiz>/src/caminhos.py
RAIZ_PROJETO = Path(__file__).resolve().parent.parent

DADOS = RAIZ_PROJETO / "data"

# Etapa 0 — CSV original, como veio da fonte
BRUTOS = DADOS / "raw"
ARQUIVO_BRUTO = BRUTOS / "dados_base.csv"

PROCESSADOS = DADOS / "processed"

# Etapa 1 — CSV lido em lotes e salvo pedaço a pedaço
CHUNKS = PROCESSADOS / "chunks_dados_base"

# Etapa 2 — chunks reagrupados em blocos maiores
BLOCOS = PROCESSADOS / "blocos"

# Etapa 3 — blocos com colunas padronizadas e derivadas (o que as análises leem)
BLOCOS_TRATADOS = PROCESSADOS / "blocos_tratados"

# Etapa 4 — arquivo único final, montado em streaming
ARQUIVO_FINAL = PROCESSADOS / "dados_final.parquet"

LOGS = RAIZ_PROJETO / "logs"
