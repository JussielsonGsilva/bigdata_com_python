# Resultados das Análises

Achados obtidos ao rodar o pipeline sobre uma base de **179.702.229 transações
financeiras** (17 GB em CSV), com o objetivo de identificar padrões de lavagem
de dinheiro.

> Este documento registra **o que foi encontrado**.
> Para instalar e executar o projeto, veja o [README](README.md).

---

## Visão geral da base

| | |
|---|---|
| Linhas | 179.702.229 |
| Tamanho original | 17 GB (CSV) |
| Período | agosto/2022 a janeiro/2023 |
| Fraudes identificadas | 225.546 |
| Taxa de fraude | 0,12% |

Tempo de leitura completa da base: **59,65 segundos**.
Tempo de tratamento dos 9 blocos: **6,68 minutos**.

---

## 1. Distribuição dos valores

**Amount Paid**

| Métrica | Valor |
|---|---|
| Mínimo | 0,000001 |
| Máximo | 8,15 trilhões |
| Média | 3,97 milhões |
| Mediana | 1.377 |
| P95 | 485 mil |
| P99 | 9,65 milhões |

**Amount Received**

| Métrica | Valor |
|---|---|
| Mínimo | 0,000001 |
| Máximo | 8,15 trilhões |
| Média | 5,60 milhões |
| Mediana | 1.375 |
| P95 | 505 mil |
| P99 | 10,47 milhões |

**Diferença entre valores:** mediana 0, e todos os percentis de 1 a 99 iguais a
zero — mas com extremos de −5,32 trilhões a +8,06 trilhões.

> A distância entre mediana (1.377) e média (3,97 milhões) mostra uma cauda
> extremamente longa: quase todas as transações são pequenas, e um punhado
> gigantesco puxa a média. Na prática, a maioria das transações não tem
> diferença entre pago e recebido, mas existem casos raros com diferenças
> enormes.

---

## 2. Análise temporal

**Volume por mês**

| Mês | Transações |
|---|---|
| 2022-08 | 59.468.086 |
| 2022-09 | 56.137.066 |
| 2022-10 | 54.821.337 |
| 2022-11 | 9.269.209 |
| 2022-12 | 6.132 |
| 2023-01 | 249 |

**Fraudes por mês**

| Mês | Fraudes |
|---|---|
| 2022-08 | 46.040 |
| 2022-09 | 67.372 |
| 2022-10 | 75.263 |
| 2022-11 | 33.013 |
| 2022-12 | 3.704 |
| 2023-01 | 154 |

> O período de agosto a outubro de 2022 concentra quase todas as transações e
> fraudes. Outubro registra o maior número de fraudes **mesmo tendo volume
> menor** que agosto e setembro — ou seja, a taxa de fraude subiu. Depois de
> novembro o volume despenca, o que sugere fim do dataset ou mudança
> operacional, não queda real de atividade.

---

## 3. Fluxo entre bancos

**Bancos que mais enviam**

| Banco | Envios |
|---|---|
| 70 | 17.140.417 |
| 12 | 956.035 |
| 11 | 945.276 |
| 0 | 920.515 |
| 20 | 901.910 |

**Bancos que mais recebem**

| Banco | Recebimentos |
|---|---|
| 27 | 477.448 |
| 12 | 419.820 |
| 11 | 404.538 |
| 0 | 347.717 |
| 112 | 333.809 |

**Maiores fluxos entre bancos**

| Origem → Destino | Volume |
|---|---|
| 27 → 27 | 91.488 |
| 112 → 112 | 79.871 |
| 12 → 12 | 75.803 |
| 0 → 0 | 60.734 |
| 20 → 20 | 56.064 |

**Fluxos suspeitos (lavagem)**

| Origem → Destino | Fraudes |
|---|---|
| 272142 → 272896 | 192 |
| 272896 → 272142 | 176 |
| 272142 → 272142 | 156 |
| 272140 → 72043 | 141 |
| 72043 → 272140 | 132 |

> Dois achados se destacam. O banco 70 domina os envios com uma margem enorme —
> 17 milhões contra menos de 1 milhão do segundo colocado. E os cinco maiores
> fluxos são **internos** (origem igual ao destino), indicando operações dentro
> da própria instituição.
>
> Mais relevante: os fluxos suspeitos envolvem bancos **completamente
> diferentes** dos que dominam o volume geral, e aparecem em pares recíprocos
> (272142 ↔ 272896, 272140 ↔ 72043). Ida e volta entre os mesmos pares é um
> padrão clássico de circulação para dificultar rastreamento.

---

## 4. Moedas

**Mais utilizadas**

| Moeda | Volume |
|---|---|
| US Dollar | 131.132.778 |
| Euro | 82.504.412 |
| Yuan | 26.041.764 |
| Shekel | 15.981.308 |
| Canadian Dollar | 12.215.891 |

**Mais associadas a fraude**

| Moeda | Fraudes |
|---|---|
| US Dollar | 180.878 |
| Euro | 126.172 |
| Yuan | 34.936 |
| UK Pound | 20.442 |
| Ruble | 18.178 |

> A distribuição de fraude acompanha de perto a distribuição geral: as moedas
> mais usadas são também as mais fraudadas, o que era esperado. O detalhe está
> na proporção — moedas menos comuns (Rupee, Yen, Ruble) aparecem
> proporcionalmente mais em fraude do que no volume total.

---

## 5. Padrões de fraude

**Por hora do dia**

| Faixa | Fraudes |
|---|---|
| 11h–14h | pico (13 a 14 mil) |
| 0h–4h | menor atividade (~6,6 mil) |

**Por dia da semana**

| Dia | Fraudes |
|---|---|
| Quinta | 34.350 |
| Terça | 32.892 |
| Segunda | 32.813 |
| Domingo | 29.596 |

**Bancos mais envolvidos**

| Origem | Fraudes | | Destino | Fraudes |
|---|---|---|---|---|
| 70 | 24.297 | | 20 | 1.916 |
| 0 | 1.835 | | 0 | 1.804 |
| 20 | 1.804 | | 11 | 1.680 |
| 11 | 1.628 | | 12 | 1.521 |
| 12 | 1.431 | | 27 | 989 |

> As fraudes seguem o ritmo normal do sistema: concentram-se no horário
> comercial e em dias úteis. Isso é significativo — indica operações desenhadas
> para se misturar ao fluxo legítimo, e não ações isoladas em horários vazios.

---

## 6. Correlação entre variáveis

Todas as variáveis apresentaram correlação com fraude entre **−0,006 e +0,006**.

| Variável | Correlação |
|---|---|
| Dia da semana | +0,0062 |
| Hora | +0,0048 |
| Amount paid / received | ~+0,001 |
| Moedas e bancos | ~−0,006 |

> **Nenhuma variável isolada explica a fraude.** À primeira vista parece um
> resultado frustrante, mas é o achado mais importante do conjunto: é
> exatamente o que se espera de sistemas financeiros reais, onde fraudadores
> imitam o comportamento normal justamente para não gerar sinal.
>
> Correlação linear não captura combinações de variáveis. Que dia da semana e
> hora sejam as correlações mais altas — ainda que baixíssimas — reforça o que
> as análises 5 e 2 mostraram: o padrão está no *quando*, não no *quanto*.

---

## Próximo passo natural

Como nenhuma variável isolada separa fraude de não fraude, o caminho seria
modelagem capaz de capturar combinações não lineares:

- Random Forest
- XGBoost
- Regressão logística
- Redes neurais

O dataset tratado, já em Parquet e com tipos otimizados, está pronto para servir
de entrada a qualquer um deles.
