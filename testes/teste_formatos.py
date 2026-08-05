"""
Testes da camada de leitura e escrita de dados.

O pipeline passou a gravar em Parquet, mas há blocos .pkl gerados por versões
anteriores que precisam continuar legíveis — reprocessar 28 GB só por causa de
mudança de formato não é aceitável. Por isso a leitura aceita os dois.

Aqui também fica travada a ordenação numérica dos arquivos: 'chunk_10' vem
depois de 'chunk_2', e não antes como o sorted() alfabético faria.

Como rodar (a partir da raiz do projeto):
    python -m unittest discover -s testes -v
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))


def amostra():
    """DataFrame pequeno para testes de ida e volta."""
    return pd.DataFrame({
        "from_bank": [1, 2, 3],
        "amount_paid": [10.5, 20.25, 8_150_000_000_000.55],
        "payment_currency": ["US Dollar", "Euro", "Yuan"],
    })


class TesteLeituraDosDoisFormatos(unittest.TestCase):

    def setUp(self):
        self.pasta = Path(tempfile.mkdtemp(prefix="formatos_"))
        self.addCleanup(shutil.rmtree, self.pasta, True)

    def teste_le_arquivo_pkl_de_versoes_anteriores(self):
        from src.formatos import ler_dados

        caminho = self.pasta / "bloco.pkl"
        amostra().to_pickle(caminho)

        pd.testing.assert_frame_equal(ler_dados(caminho), amostra())

    def teste_le_arquivo_parquet(self):
        from src.formatos import ler_dados

        caminho = self.pasta / "bloco.parquet"
        amostra().to_parquet(caminho, index=False)

        pd.testing.assert_frame_equal(ler_dados(caminho), amostra())

    def teste_recusa_extensao_desconhecida(self):
        from src.formatos import ler_dados

        caminho = self.pasta / "bloco.csv"
        caminho.write_text("a,b\n1,2\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            ler_dados(caminho)


class TesteEscrita(unittest.TestCase):

    def setUp(self):
        self.pasta = Path(tempfile.mkdtemp(prefix="escrita_"))
        self.addCleanup(shutil.rmtree, self.pasta, True)

    def teste_escrita_gera_parquet(self):
        from src.formatos import salvar_dados

        caminho = salvar_dados(amostra(), self.pasta, "parte_0")

        self.assertTrue(str(caminho).endswith(".parquet"))
        self.assertTrue(Path(caminho).exists())

    def teste_ida_e_volta_preserva_valores(self):
        from src.formatos import ler_dados, salvar_dados

        caminho = salvar_dados(amostra(), self.pasta, "parte_0")

        pd.testing.assert_frame_equal(ler_dados(caminho), amostra())


class TesteListagem(unittest.TestCase):

    def setUp(self):
        self.pasta = Path(tempfile.mkdtemp(prefix="listagem_"))
        self.addCleanup(shutil.rmtree, self.pasta, True)

    def teste_ordena_numericamente_e_nao_alfabeticamente(self):
        from src.formatos import listar_arquivos_de_dados

        for indice in [0, 1, 2, 10, 11]:
            amostra().to_parquet(self.pasta / f"chunk_{indice}.parquet", index=False)

        nomes = [Path(c).stem for c in listar_arquivos_de_dados(self.pasta)]

        self.assertEqual(
            nomes,
            ["chunk_0", "chunk_1", "chunk_2", "chunk_10", "chunk_11"],
            "chunk_10 precisa vir depois de chunk_2"
        )

    def teste_lista_pkl_e_parquet_na_mesma_pasta(self):
        from src.formatos import listar_arquivos_de_dados

        amostra().to_pickle(self.pasta / "parte_0.pkl")
        amostra().to_parquet(self.pasta / "parte_1.parquet", index=False)

        self.assertEqual(len(listar_arquivos_de_dados(self.pasta)), 2)

    def teste_ignora_arquivos_que_nao_sao_dados(self):
        from src.formatos import listar_arquivos_de_dados

        amostra().to_parquet(self.pasta / "parte_0.parquet", index=False)
        (self.pasta / "anotacoes.txt").write_text("nada", encoding="utf-8")

        self.assertEqual(len(listar_arquivos_de_dados(self.pasta)), 1)


if __name__ == "__main__":
    unittest.main()
