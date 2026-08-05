"""
Testes da otimização de tipos.

A economia de memória não pode custar precisão: este é um dataset financeiro,
com valores que chegam a trilhões. Reduzir as colunas de valor para float32
economizaria memória e arredondaria centavos — por isso há um teste explícito
travando esse comportamento.

Como rodar (a partir da raiz do projeto):
    python -m unittest discover -s testes -v
"""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))


def criar_amostra(linhas=200_000):
    """
    Monta um DataFrame com o schema e as características do dataset real:
    poucas moedas distintas, bancos com identificadores pequenos e valores
    monetários de magnitude muito variada.

    @param linhas  Quantidade de linhas a gerar
    @return        DataFrame de amostra
    """
    gerador = np.random.default_rng(11)
    moedas = ["US Dollar", "Euro", "Yuan", "Shekel", "UK Pound", "Ruble"]
    formatos = ["Cheque", "Credit Card", "Wire", "ACH", "Cash"]

    return pd.DataFrame({
        "timestamp": pd.date_range("2022-08-01", periods=linhas, freq="s"),
        "from_bank": gerador.integers(0, 300, linhas),
        "to_bank": gerador.integers(0, 300, linhas),
        "amount_paid": gerador.uniform(1, 100_000, linhas),
        "amount_received": gerador.uniform(1, 100_000, linhas),
        "receiving_currency": gerador.choice(moedas, linhas),
        "payment_currency": gerador.choice(moedas, linhas),
        "payment_format": gerador.choice(formatos, linhas),
        "is_laundering": gerador.integers(0, 2, linhas),
    })


def memoria_mb(df):
    """Consumo de memória de um DataFrame, em MB, contando o texto de verdade."""
    return df.memory_usage(deep=True).sum() / 1024 ** 2


class TesteReducaoDeMemoria(unittest.TestCase):

    def teste_otimizacao_reduz_memoria_em_pelo_menos_metade(self):
        from src.otimizacao import otimizar_tipos

        original = criar_amostra()
        otimizado = otimizar_tipos(original.copy())

        antes, depois = memoria_mb(original), memoria_mb(otimizado)
        self.assertLess(
            depois, antes * 0.5,
            f"otimização reduziu de {antes:.1f} MB para {depois:.1f} MB — "
            f"esperado menos da metade"
        )

    def teste_colunas_de_texto_repetitivo_viram_category(self):
        from src.otimizacao import otimizar_tipos

        otimizado = otimizar_tipos(criar_amostra())

        for coluna in ["receiving_currency", "payment_currency", "payment_format"]:
            self.assertEqual(
                str(otimizado[coluna].dtype), "category",
                f"{coluna} deveria ser category"
            )


class TestePreservacaoDosDados(unittest.TestCase):
    """Economizar memória não pode alterar nenhum valor."""

    def teste_valores_monetarios_permanecem_identicos(self):
        from src.otimizacao import otimizar_tipos

        original = criar_amostra()
        otimizado = otimizar_tipos(original.copy())

        for coluna in ["amount_paid", "amount_received"]:
            pd.testing.assert_series_equal(
                original[coluna], otimizado[coluna],
                check_dtype=False, check_names=False
            )

    def teste_colunas_de_valor_nao_viram_float32(self):
        # float32 tem ~7 dígitos significativos. Com valores na casa dos
        # trilhões, centavos desapareceriam silenciosamente.
        from src.otimizacao import otimizar_tipos

        otimizado = otimizar_tipos(criar_amostra())

        for coluna in ["amount_paid", "amount_received"]:
            self.assertNotEqual(
                str(otimizado[coluna].dtype), "float32",
                f"{coluna} virou float32 — perderia precisão em valores altos"
            )

    def teste_valores_grandes_nao_perdem_centavos(self):
        from src.otimizacao import otimizar_tipos

        df = pd.DataFrame({
            "from_bank": [1, 2],
            "amount_paid": [8_150_000_000_000.55, 1_234_567_890.12],
            "payment_currency": ["US Dollar", "Euro"],
        })
        otimizado = otimizar_tipos(df.copy())

        self.assertEqual(otimizado["amount_paid"].tolist(),
                         [8_150_000_000_000.55, 1_234_567_890.12])

    def teste_identificadores_e_texto_mantem_o_conteudo(self):
        from src.otimizacao import otimizar_tipos

        original = criar_amostra()
        otimizado = otimizar_tipos(original.copy())

        self.assertEqual(otimizado["from_bank"].tolist(),
                         original["from_bank"].tolist())
        self.assertEqual(otimizado["payment_format"].astype(str).tolist(),
                         original["payment_format"].tolist())


if __name__ == "__main__":
    unittest.main()
