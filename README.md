# Big Data com Python — Processamento de Arquivos Gigantes em Chunks

Este projeto demonstra um pipeline profissional para processamento de dados em larga escala utilizando Python, Pandas e leitura em chunks.  
Ele foi desenvolvido para lidar com arquivos CSV gigantes (ex.: 17 GB) de forma eficiente, modular e escalável.

---

## 🚀 Objetivo

Criar um pipeline robusto capaz de
Ler arquivos CSV muito grandes sem estourar memória
Processar os dados em chunks (lotes)
Salvar cada lote em formato .pkl
Registrar logs profissionais
Recombinar os chunks em blocos
Recombinar os blocos em streaming sem usar RAM excessiva
Manter uma arquitetura limpa e pronta para produção
---

## 📂 Estrutura do Projeto

bbigdata_com_python/
│
├── run_pipeline.py
├── run_recombine_blocks.py
├── run_recombine_final_stream.py
├── clean_chunks.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── pipeline_chunks.py
│   ├── recombine_in_blocks.py
│   ├── logger_config.py
│   └── __init__.py
│
├── data/
│   ├── raw/
│   │   └── arquivo_gigante.csv
│   └── processed/
│       ├── chunks_dados_base/      ← (180 chunks gerados)
│       ├── blocos/                 ← (9 blocos gerados)
│       └── dados_base_final.parquet
│
├── logs/
│   └── pipeline.log
│
└── analise/

---

## 🧠 Tecnologias Utilizadas

Python 3
Pandas — leitura e manipulação de dados
TQDM — barra de progresso
Loguru — logging moderno
PyArrow — escrita otimizada em Parquet **PyArrow** — otimizações internas
---

# TRABALHADO COM UMA BASE DE DADOS DE 17G
🟩 base com 179 milhões de linhas.
## ⚙️ Como Executar

1. Criar ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate

2. Instalar dependências:
pip install -r requirements.txt

3. Colocar o arquivo CSV gigante em:
data/raw/

4. Executar o pipeline:
python run_pipeline.py

🧱 📌 Geração dos Chunks — Detalhamento Completo
🏗️ Pipeline em Chunks
O pipeline lê o CSV em lotes (chunks) e salva cada lote como .pkl:
process_csv_in_chunks(
    input_path="data/raw/dados_base.csv",
    output_dir="data/processed/chunks",
    chunk_size=2_000_000
)

✔ Arquivo responsável
run_pipeline.py

✔ Diretório onde os chunks são salvos
data/processed/chunks_dados_base/

✔ Quantidade de chunks gerados
89 chunks

✔ Linhas por chunk
2.000.000 linhas por chunk

🧩 Recombinação em Blocos (10 chunks por vez)
✔ Arquivo responsável
run_recombine_blocks.py

✔ Diretório onde os blocos são salvos
data/processed/blocos/

✔ Quantidade de blocos gerados
9 blocos do bloco 0 ao 8
🟧 cada blocos com 38 milhões de linhas.


🧹 Limpeza dos Chunks Inúteis
Após gerar os blocos, os 180 chunks podem ser removidos.
✔ Arquivo responsável
clean_chunks.py

CRIANDO UM ARQUIVO NA RAIS .gitignore para não enviar arquivos grandes para o github
❌ O GitHub NÃO aceita arquivos maiores que 100 MB.
nano .gitignore

# Ignorar arquivos grandes
*.pkl

# Ignorar diretórios de dados
data/processed/*
data/raw/*

# Exceto se quiser manter alguma estrutura vazia
!data/
!data/processed/
!data/raw/

# Ambiente virtual
.venv/

# Arquivos temporários
__pycache__/
*.log

Depois adicione e faça commit:
git add .gitignore
git commit -m "Adicionando .gitignore para ignorar arquivos grandes e temporários"


📜 Logs
Todos os logs são salvos automaticamente em:
logs/pipeline.log

👨‍💻 Autor
Projeto desenvolvido por Jussielson como parte de um portfólio profissional de Big Data com Python.

INICIANDO AS ANÁLISES PRELIMINARES DOS DADOS
/analises  analisedados.py
179.702.229 linhas
Tempo total: 59,65 segundos

INICIANDO TRATAMENTO DOS DADOS
/analises tratamento_dados.py
✔ Padronizar nomes das colunas
✔ Converter Timestamp para datetime
✔ Criar colunas derivadas (dia, mês, hora, dia da semana)
✔ Criar coluna de diferença entre valores
✔ Padronizar moedas
✔ Remover duplicatas
✔ Validar valores negativos
✔ Salvar blocos tratados
Tempo total de tratamento: 6.68 minutos
9 blocos tratados
todos salvos corretamente
nenhum erro
pipeline estável
tempo excelente para o volume de dados

agora temos os blocos tratados, vamos excluir os blocos antigos
na pasta raiz--> rm -r data/processed/blocos

