"""
Testes da recombinação final em streaming.

A promessa do projeto é montar o arquivo final sem nunca ter o dataset inteiro
na memória. Um teste que só verificasse "o arquivo foi criado" passaria também
para a versão que carrega tudo de uma vez — por isso aqui o pico de memória é
medido de verdade, comparando com o método ingênuo.

Cada medição roda em um processo separado, porque `ru_maxrss` registra o pico
do processo e nunca diminui: medir os dois no mesmo processo daria o mesmo
número para ambos.

Como rodar (a partir da raiz do projeto):
    python -m unittest discover -s testes -v
"""
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

LINHAS_POR_BLOCO = 400_000
QUANTIDADE_DE_BLOCOS = 8


def criar_blocos(pasta):
    """
    Gera blocos PKL de teste com o schema do dataset.

    @param pasta  Diretório onde os blocos serão gravados
    @return       Número total de linhas gravadas
    """
    import numpy as np
    import pandas as pd

    gerador = np.random.default_rng(7)
    moedas = ["US Dollar", "Euro", "Yuan", "Shekel"]

    for indice in range(QUANTIDADE_DE_BLOCOS):
        bloco = pd.DataFrame({
            "timestamp": pd.date_range("2022-08-01", periods=LINHAS_POR_BLOCO, freq="s"),
            "from_bank": gerador.integers(0, 300, LINHAS_POR_BLOCO),
            "to_bank": gerador.integers(0, 300, LINHAS_POR_BLOCO),
            "amount_paid": gerador.uniform(1, 100_000, LINHAS_POR_BLOCO),
            "payment_currency": gerador.choice(moedas, LINHAS_POR_BLOCO),
            "is_laundering": gerador.integers(0, 2, LINHAS_POR_BLOCO),
        })
        bloco.to_pickle(Path(pasta) / f"parte_{indice}.pkl")

    return LINHAS_POR_BLOCO * QUANTIDADE_DE_BLOCOS


def medir_pico_de_memoria(imports, operacao):
    """
    Executa uma operação em outro processo e devolve quanta memória ela somou.

    A medição desconta a linha de base tomada logo após os imports: carregar
    pandas e pyarrow custa cerca de 200 MB, o que mascararia completamente a
    diferença entre as duas estratégias se fosse contado junto.

    @param imports    Linhas de import, executadas antes da linha de base
    @param operacao   Código da operação a medir
    @return           Memória adicional consumida pela operação, em MB
    """
    programa = textwrap.dedent(f"""
        import sys, threading, time
        sys.path.insert(0, {str(RAIZ)!r})
        {textwrap.indent(textwrap.dedent(imports), "        ").strip()}

        def rss_atual():
            # Segundo campo de /proc/self/statm é o RSS em páginas de 4 KB.
            with open("/proc/self/statm") as f:
                return int(f.read().split()[1]) * 4096 / 1024 / 1024

        # ru_maxrss não serve aqui: ele guarda o pico de todo o processo e
        # nunca diminui, então o pico transitório dos imports (~200 MB)
        # esconderia o consumo dos dados. Amostrar o RSS apenas durante a
        # operação mede o que realmente interessa.
        amostras = []
        rodando = True

        def amostrar():
            while rodando:
                amostras.append(rss_atual())
                time.sleep(0.01)

        linha_de_base = rss_atual()
        coletor = threading.Thread(target=amostrar, daemon=True)
        coletor.start()

        {textwrap.indent(textwrap.dedent(operacao), "        ").strip()}

        rodando = False
        coletor.join(timeout=2)

        print(max(amostras or [linha_de_base]) - linha_de_base)
    """)
    resultado = subprocess.run(
        [sys.executable, "-c", programa],
        capture_output=True, text=True, timeout=300
    )
    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr)
    return float(resultado.stdout.strip().splitlines()[-1])


class TesteRecombinacaoEmStreaming(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raiz = tempfile.mkdtemp(prefix="blocos_teste_")

        # A saída fica FORA da pasta de entrada: como a listagem passou a
        # aceitar .parquet, gravar o resultado junto dos blocos faria a função
        # reler o próprio arquivo final como se fosse mais um bloco.
        cls.pasta = str(Path(cls.raiz) / "entrada")
        cls.saida = Path(cls.raiz) / "saida"
        Path(cls.pasta).mkdir()
        cls.saida.mkdir()

        cls.total_de_linhas = criar_blocos(cls.pasta)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.raiz, ignore_errors=True)

    def teste_arquivo_final_contem_todas_as_linhas_dos_blocos(self):
        import pandas as pd
        from src.recombine_stream import recombinar_blocos_em_streaming

        destino = self.saida / "final.parquet"
        recombinar_blocos_em_streaming(self.pasta, str(destino))

        self.assertTrue(destino.exists(), "arquivo final não foi criado")
        self.assertEqual(len(pd.read_parquet(destino)), self.total_de_linhas)

    def teste_arquivo_final_preserva_as_colunas(self):
        import pandas as pd
        from src.recombine_stream import recombinar_blocos_em_streaming

        destino = self.saida / "colunas.parquet"
        recombinar_blocos_em_streaming(self.pasta, str(destino))

        primeiro_bloco = pd.read_pickle(Path(self.pasta) / "parte_0.pkl")
        self.assertEqual(
            list(pd.read_parquet(destino).columns),
            list(primeiro_bloco.columns)
        )

    def teste_pico_de_memoria_menor_que_carregar_tudo_de_uma_vez(self):
        consumo_streaming = medir_pico_de_memoria(
            imports="""
                import pandas, pyarrow, pyarrow.parquet
                from src.recombine_stream import recombinar_blocos_em_streaming
            """,
            operacao=f"""
                recombinar_blocos_em_streaming(
                    {self.pasta!r}, {str(self.saida / "s.parquet")!r})
            """,
        )

        consumo_ingenuo = medir_pico_de_memoria(
            imports="""
                import os
                import pandas as pd
                import pyarrow, pyarrow.parquet
            """,
            operacao=f"""
                partes = [pd.read_pickle(os.path.join({self.pasta!r}, a))
                          for a in sorted(os.listdir({self.pasta!r}))
                          if a.endswith(".pkl")]
                pd.concat(partes, ignore_index=True).to_parquet(
                    {str(self.saida / "i.parquet")!r})
            """,
        )

        # A margem existe para o teste não ficar frágil: exige uma diferença
        # real, não uma variação de medição.
        self.assertLess(
            consumo_streaming, consumo_ingenuo * 0.6,
            f"streaming somou {consumo_streaming:.0f} MB e carregar tudo somou "
            f"{consumo_ingenuo:.0f} MB — a economia esperada não apareceu"
        )


if __name__ == "__main__":
    unittest.main()
