# Big Data com Python — Processamento de Arquivos Gigantes em Chunks

Este projeto demonstra um pipeline profissional para processamento de dados em larga escala utilizando Python, Pandas e leitura em chunks.  
Ele foi desenvolvido para lidar com arquivos CSV gigantes (ex.: 16 GB) de forma eficiente, modular e escalável.

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
└── notebooks/

---

## 🧠 Tecnologias Utilizadas

Python 3
Pandas — leitura e manipulação de dados
TQDM — barra de progresso
Loguru — logging moderno
PyArrow — escrita otimizada em Parquet **PyArrow** — otimizações internas
---

# TRABALHADO COM UMA BASE DE DADOS DE 17G
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
    input_path="data/raw/arquivo_gigante.csv",
    output_dir="data/processed/chunks",
    chunk_size=1_000_000
)

✔ Arquivo responsável
run_pipeline.py

✔ Diretório onde os chunks são salvos
data/processed/chunks_dados_base/

✔ Quantidade de chunks gerados
180 chunks

✔ Linhas por chunk
1.000.000 linhas por chunk

✔ Tempo total para gerar os chunks
5 minutos

✔ Tempo médio por chunk
1.6 a 2.1 segundos


🧩 Recombinação em Blocos (20 chunks por vez)
✔ Arquivo responsável
run_recombine_blocks.py

✔ Diretório onde os blocos são salvos
data/processed/blocos/

✔ Quantidade de blocos gerados
9 blocos (parte_0.pkl até parte_8.pkl)

✔ Linhas por bloco
20 milhões de linhas por bloco

✔ Tempo por bloco
6 a 10 segundos


🧹 Limpeza dos Chunks Inúteis
Após gerar os blocos, os 180 chunks podem ser removidos.
✔ Arquivo responsável
clean_chunks.py

✔ Código utilizado
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

✔ Executar limpeza
python clean_chunks.py

🧠 Recombinação Final em Streaming (sem estourar RAM)
✔ Arquivo responsável
run_recombine_final_stream.py

✅ instalando o loguru dentro do ambiente virtual:
pip install loguru

🚀 Como executar
python run_recombine_final_stream.py

O processo vai:
ler cada bloco (20 milhões de linhas)
escrever no arquivo final
descartar da memória
manter a RAM sempre baixa

✔ Formato final
Parquet (otimizado para Big Data)

✔ Arquivo final gerado
data/processed/dados_base_final.parquet

🔥 O que isso significa na prática
✔ Um arquivo final Parquet com 180 milhões de linhas
✔ Criado sem estourar memória
✔ Usando escrita incremental real
✔ Com logs profissionais
✔ Com arquitetura modular
✔ Com limpeza automática dos intermediários
✔ Com recombinação em blocos e recombinação final em streaming

🧹 Remover os blocos (parte_0.pkl … parte_8.pkl)
criar arquvo--> clean_blocks.py
dentro colocar:

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

🚀 Executar a limpeza
python clean_blocks.py

🧹 Remover pastas antigas (chunks e chunks_teste)
Criando o arquivo--> clean_old_dirs.py
dentro colocar:

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

🚀 Executar a limpeza
python clean_old_dirs.py

CRIANDO UM ARQUIVO NA RAIS .gitignore para não enviar arquivos grandes para o github
❌ O GitHub NÃO aceita arquivos maiores que 100 MB.
nano .gitignore

# Ignorar arquivos grandes
*.parquet
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


