# Big Data com Python — Processamento de CSV em Chunks

Pipeline para processar arquivos CSV grandes demais para caber na memória.
Foi construído para uma base de **179,7 milhões de transações financeiras
(17 GB)** e roda em máquina comum, lendo os dados em lotes e nunca carregando
o conjunto inteiro de uma vez.

📊 **Os achados das análises estão em [RESULTADOS.md](RESULTADOS.md).**

---

## Como funciona

O pipeline tem 4 etapas encadeadas. Cada uma lê o que a anterior gravou:

```
CSV bruto  →  chunks  →  blocos  →  blocos tratados  →  arquivo único
   17 GB       (1)        (2)            (3)                (4)
```

| # | Etapa | Script | O que faz |
|---|---|---|---|
| 1 | Leitura em chunks | `run_pipeline.py` | Lê o CSV em lotes de 2 milhões de linhas e grava cada lote separado |
| 2 | Agrupamento | `run_recombine_blocks.py` | Junta os chunks em blocos maiores, 10 por vez |
| 3 | Tratamento | `analises/tratamento_dados.py` | Padroniza colunas, cria campos derivados, otimiza tipos |
| 4 | Consolidação | `run_recombine_final_stream.py` | Monta o arquivo final em streaming |

A etapa 4 lê um bloco por vez, grava e descarta antes de ler o próximo. O
consumo de memória fica próximo do tamanho de **um** bloco, e não da soma de
todos — é o que permite consolidar 179 milhões de linhas sem estourar a RAM.

---

## Decisões técnicas

**Formato Parquet.** A escrita usa Parquet, que ocupa cerca de um quarto do
espaço do pickle e pode ser lido por outras ferramentas. A leitura aceita
`.parquet` e `.pkl`, para que dados gerados por versões anteriores continuem
funcionando sem reprocessamento.

**Otimização de tipos.** Colunas de texto repetitivo (moeda, formato de
pagamento) viram `category`; identificadores inteiros são reduzidos ao menor
tipo que comporta a faixa de valores. Reduz o uso de memória pela metade.

**Valores monetários ficam em `float64`.** Reduzi-los para `float32`
economizaria mais memória, mas `float32` tem cerca de 7 dígitos significativos
— com valores que chegam a trilhões, centavos seriam arredondados. Há testes
travando esse comportamento.

**A remoção de duplicatas é por bloco, não global.** A etapa 3 trata um bloco
por vez, então duas linhas idênticas só são reduzidas a uma se estiverem no
mesmo bloco — um par que caiu em blocos diferentes sobrevive ao tratamento.
Deduplicar globalmente exigiria manter as 179 milhões de linhas comparáveis ao
mesmo tempo, que é exatamente o que este pipeline existe para evitar. Quem
precisar da garantia global tem duas saídas: ordenar o CSV pela chave de
duplicidade antes da etapa 1, para que as repetições caiam no mesmo bloco, ou
rodar um `DISTINCT` sobre o Parquet final com uma ferramenta que trabalhe fora
da memória (DuckDB, por exemplo).

**Ordenação numérica.** Os arquivos são ordenados pelo número no nome, não
alfabeticamente: `chunk_10` vem depois de `chunk_2`, e não antes.

---

## Pré-requisitos

- Python 3.10 ou superior
- Espaço em disco equivalente a cerca de 2× o tamanho do CSV de entrada

---

## Instalação

```bash
git clone https://github.com/JussielsonGsilva/bigdata_com_python.git
cd bigdata_com_python

python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## Executando

Coloque o CSV em `data/raw/dados_base.csv` e rode as etapas em ordem:

```bash
python run_pipeline.py                  # 1. CSV → chunks
python run_recombine_blocks.py          # 2. chunks → blocos

cd analises
python tratamento_dados.py              # 3. blocos → blocos tratados
cd ..

python run_recombine_final_stream.py    # 4. → arquivo único em Parquet
```

Depois da etapa 2, os chunks podem ser removidos:

```bash
python clean_chunks.py
```

### Análises

Depois da etapa 2, a base já pode ser inspecionada:

```bash
cd analises
python analisedados.py        # visão geral da base — lê os blocos da etapa 2
```

As demais precisam dos **blocos tratados** (etapa 3): é ela que padroniza os
nomes das colunas (`Amount Paid` → `amount_paid`) e cria as derivadas que
várias delas usam (`hora`, `dia_semana`, `diferenca_valor`).

```bash
python analise_valores.py     # distribuição dos valores
python analise_temporal.py    # volume e fraude ao longo do tempo
python analise_bancos.py      # fluxo entre bancos
python analise_moedas.py      # moedas e sua relação com fraude
python analise_fraude.py      # padrões de fraude
python analise_correlacao.py  # correlação entre variáveis
```

A diferença importa na hora de comparar os números: `analisedados.py` conta a
base **antes** do tratamento, então o total de linhas dele é maior que o das
outras análises — a etapa 3 descarta duplicatas e valores negativos pelo
caminho.

Os scripts funcionam sendo chamados de qualquer diretório — os caminhos são
resolvidos a partir da raiz do projeto.

---

## Testes

```bash
python -m unittest discover -s testes -v
```

Cobrem o encadeamento das etapas, a leitura dos dois formatos, a ordenação
numérica, a preservação dos valores na otimização de tipos e — medindo o
consumo real de memória — a economia da recombinação em streaming.

---

## Estrutura do Projeto

```
.
├── run_pipeline.py                  # etapa 1
├── run_recombine_blocks.py          # etapa 2
├── run_recombine_final_stream.py    # etapa 4
├── clean_chunks.py                  # limpeza dos chunks intermediários
├── requirements.txt
│
├── src/
│   ├── caminhos.py                  # caminhos do pipeline, em um lugar só
│   ├── formatos.py                  # leitura/escrita e ordenação dos arquivos
│   ├── otimizacao.py                # redução de memória por tipo de coluna
│   ├── pipeline_chunks.py           # etapa 1
│   ├── recombine_in_blocks.py       # etapa 2
│   ├── recombine_stream.py          # etapa 4
│   └── logger_config.py             # logs com rotação
│
├── analises/
│   ├── tratamento_dados.py          # etapa 3
│   └── analise_*.py                 # análises sobre os blocos tratados
│
├── testes/
├── logs/                            # pipeline.log (rotação a cada 10 MB)
│
└── data/                            # não versionado
    ├── raw/                         # CSV de entrada
    └── processed/                   # chunks, blocos e arquivo final
```

---

## Hooks do Git

O repositório traz um hook de `pre-commit` em `.githooks/` que aborta o commit se
`.env` ou arquivos de backup (`.bak`, `.old`, `.orig`, `~`) entrarem no stage.

Ative uma vez após clonar:

```bash
git config core.hooksPath .githooks
```

A configuração é local a cada clone — o Git não permite que um repositório ative
hooks sozinho, justamente para que baixar um projeto não execute código na sua
máquina sem você pedir.

O `.gitignore` já evita o acidente comum, mas não protege contra um `git add -f`
distraído. E vale lembrar que ele **não** deixa de rastrear arquivo que já foi
commitado antes de constar na lista: para isso é preciso `git rm --cached`.

---

## Tecnologias

- **Python 3** — pandas, numpy
- **PyArrow** — leitura e escrita em Parquet
- **Loguru** — logs com rotação automática
- **TQDM** — barra de progresso

---

## Autor

**Jussielson G. Silva** — Analista e Desenvolvedor de Sistemas
