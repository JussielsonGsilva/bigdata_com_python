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
│
├── logs/
│   └── pipeline.log
│
└── analises/

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


🟩 1. Análise estatística avançada dos valores
analide_valores.py

1: Distribuição dos Valores
Amount Paid
Min: 0.000001
Max: 8.15 trilhões
Média: 3.97 milhões
Mediana: 1.377
P95: 485 mil
P99: 9.65 milhões
Linhas: 179.7 milhões

Amount Received
Min: 0.000001
Max: 8.15 trilhões
Média: 5.60 milhões
Mediana: 1.375
P95: 505 mil
P99: 10.47 milhões
Linhas: 179.7 milhões

Diferença entre Valores
Min: -5.32 trilhões
Max: 8.06 trilhões
Média: 1.63 milhões
Mediana: 0
Percentis (1–99): todos 0
Linhas: 179.7 milhões

Resumo: a maioria das transações não tem diferença entre pago e recebido, mas existem casos raros com diferenças gigantescas.

📘 2 Análise Temporal (por mês + fraude ao longo do tempo)
analise_temporal.py

Volume Total por Mês
  Mês	Transações
2022-08	59.468.086
2022-09	56.137.066
2022-10	54.821.337
2022-11	9.269.209
2022-12	6.132
2023-01	249

Transações Suspeitas por Mês

  Mês	Fraudes
2022-08	46.040
2022-09	67.372
2022-10	75.263
2022-11	33.013
2022-12	3.704
2023-01	154

O período 2022-08 a 2022-10 concentra quase todas as transações e fraudes.
Outubro/2022 apresenta o maior número de fraudes, mesmo com volume menor que agosto e setembro.
Após novembro, o volume despenca, sugerindo fim do dataset ou mudança operacional.


🟦 Análise 3 — Fluxo entre Bancos (origem → destino)
analise_bancos.py

Bancos que Mais Enviam
Banco	Envios
70	17.140.417
12	956.035
11	945.276
0	920.515
20	901.910
Resumo: o banco 70 domina completamente o volume de envios, muito acima dos demais.

Bancos que Mais Recebem
Banco	Recebimentos
27	477.448
12	419.820
11	404.538
0	347.717
112	333.809
Resumo: o banco 27 é o principal destino das transações.

Maiores Fluxos Entre Bancos
Origem → Destino	Volume
27 → 27	91.488
112 → 112	79.871
12 → 12	75.803
0 → 0	60.734
20 → 20	56.064
Resumo: há forte concentração de transações dentro do próprio banco, indicando operações
        internas intensas.

Fluxos Suspeitos (Lavagem)
Origem → Destino	Fraudes
272142 → 272896	     192
272896 → 272142	     176
272142 → 272142	     156
272140 → 72043	     141
72043  → 272140	     132
Resumo: os fluxos suspeitos envolvem bancos completamente diferentes dos que dominam o volume geral, sugerindo redes específicas de movimentação ilícita.

🪙 Análise 4 — Moedas (Currency Analysis)
analise_moedas.py

💱 Moedas Mais Utilizadas
Moeda	Volume
US DOLLAR	131.132.778
EURO	82.504.412
YUAN	26.041.764
SHEKEL	15.981.308
CANADIAN DOLLAR	12.215.891
Resumo: o sistema é fortemente dominado por USD e EUR, que juntos representam a maior parte das transações.

💱 Moedas Mais Associadas a Fraude
Moeda	Fraudes
US DOLLAR	180.878
EURO	126.172
YUAN	34.936
UK POUND	20.442
RUBLE	18.178
Resumo: USD e EUR também lideram nas transações suspeitas, indicando que a maior parte das fraudes ocorre nas moedas mais populares.

nsights Rápidos
A distribuição de fraude acompanha a distribuição geral de moedas.
Moedas menos comuns (como RUPEE, YEN, RUBLE) aparecem proporcionalmente mais em fraudes do que no volume total.
USD domina tanto o volume quanto as operações suspeitas.

🕵️ Análise 5 — Padrões de Fraude (is_laundering)
analise_fraude.py
Resumo Geral
Fraudes detectadas: 225.546
Total de transações: 179.702.079
Taxa de fraude: 0,12%

⏰ Fraude por Hora
Hora	Fraudes
11h–14h	pico (13k–14k fraudes)
0h–4h	menor atividade (~6,6k fraudes)
Resumo: fraudes se concentram no horário comercial, sugerindo operações automatizadas ou mascaradas em meio ao fluxo normal.

⏰ Fraude Dia sa Semana
Dia	Fraudes
Quinta (4)	34.350
Terça (2)	32.892
Segunda (1)	32.813
Domingo (6)	29.596
Resumo: quinta‑feira é o dia mais crítico; finais de semana têm menos fraude.

🏦 Bancos Mais Envolvidos (Origem)
Banco	Fraudes
70	24.297
0	1.835
20	1.804
11	1.628
12	1.431
Resumo: o banco 70 domina a origem das transações suspeitas.

🏦 Bancos Mais Envolvidos (Destino)
Banco	Fraudes
20	1.916
0	1.804
11	1.680
12	1.521
27	989
Resumo: o banco 20 é o principal destino de fraudes.

💱 Moedas Mais Usadas em Fraude
Moeda	Fraudes
US DOLLAR	180.878
EURO	126.172
YUAN	34.936
UK POUND	20.442
RUBLE	18.178
Resumo: USD e EUR concentram a maior parte das fraudes, refletindo seu uso predominante no sistema.

🔍 Insights Rápidos
Fraudes seguem o fluxo normal do sistema (horário comercial e dias úteis).
Banco 70 é o maior emissor de transações suspeitas.
Banco 20 é o principal receptor.
Moedas mais comuns também são as mais usadas em fraude.
Padrão indica operações automatizadas, não ações manuais isoladas.


Análise 6 — Correlação Entre Variáveis
analise_correlacao.py

ob: Instalar o pyarrow
pip install pyarrow

📌 1. A correlação é extremamente baixa
Todas as variáveis têm correlação entre –0.006 e +0.006 com fraude.
Isso significa:
👉 Nenhuma variável isolada explica a fraude.
👉 Não existe um “sinal óbvio” que diferencia fraude de não fraude.
Isso é exatamente o que acontece em sistemas financeiros reais:
fraudadores tentam imitar o comportamento normal
padrões são sutis
não existe um único indicador forte
Isso é um achado importante.

📌 2. As variáveis mais correlacionadas (ainda que fracas)
+ dia da semana (0.0062)
Fraudes acontecem um pouco mais em dias úteis, especialmente quinta-feira (como vimos na Análise 5).
+ hora (0.0048)
Fraudes se concentram no horário comercial.
+ amount_paid / amount_received (~0.001)
Valores maiores têm uma tendência mínima de aparecer em fraude, mas nada forte.

📌 3. Variáveis com correlação negativa
– moedas e bancos (~ –0.006)
Isso significa:
não existe uma moeda “forte” para fraude
não existe um banco “forte” para fraude
fraudadores distribuem operações para parecerem normais
Isso confirma que o comportamento fraudulento é disperso, não concentrado.

✔ A fraude não é linear
Correlação linear não captura padrões complexos.

✔ A fraude depende de combinações de variáveis, não de uma só
Isso é típico de:
lavagem de dinheiro
fraude bancária
transações estruturadas

✔ O próximo passo natural seria usar modelos de machine learning
Como:
Random Forest
XGBoost
Regressão logística
Redes neurais

