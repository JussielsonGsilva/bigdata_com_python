"""
Testes dos caminhos do pipeline.

O pipeline tem 4 etapas encadeadas, cada uma lendo o que a anterior escreveu.
Se uma etapa grava numa pasta que a próxima não lê, o fluxo quebra em silêncio
para quem clonar o projeto — foi o que aconteceu com blocks_tratados x
blocos_tratados.

Estes testes travam esse encadeamento.

Como rodar (a partir da raiz do projeto):
    python -m unittest discover -s testes -v
"""
import inspect
import os
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "analises"))


def valor_padrao(funcao, parametro):
    """
    Lê o valor padrão de um parâmetro de uma função.

    @param funcao     Função a inspecionar
    @param parametro  Nome do parâmetro
    @return           Valor padrão declarado na assinatura
    """
    return inspect.signature(funcao).parameters[parametro].default


class TesteEncadeamentoDasEtapas(unittest.TestCase):
    """A saída de cada etapa precisa ser exatamente a entrada da seguinte."""

    def teste_recombinacao_grava_onde_o_tratamento_le(self):
        from analises.tratamento_dados import tratar_blocos
        from src.caminhos import BLOCOS

        self.assertEqual(
            Path(valor_padrao(tratar_blocos, "blocks_dir")).resolve(),
            BLOCOS.resolve()
        )

    def teste_tratamento_grava_onde_as_analises_leem(self):
        from analises.tratamento_dados import tratar_blocos
        from analises.analise_fraude import analise_fraude
        from analises.analise_bancos import analise_bancos
        from analises.analise_moedas import analise_moedas

        saida_tratamento = Path(valor_padrao(tratar_blocos, "output_dir")).resolve()

        for analise in [analise_fraude, analise_bancos, analise_moedas]:
            entrada = Path(valor_padrao(analise, "blocks_dir")).resolve()
            self.assertEqual(
                entrada, saida_tratamento,
                f"{analise.__name__} lê de uma pasta diferente da que o tratamento grava"
            )


class TesteIndependenciaDoDiretorioAtual(unittest.TestCase):
    """
    Os caminhos não podem depender de onde o script foi chamado.
    Com '..' no caminho, rodar da raiz do projeto quebra.
    """

    def teste_caminhos_do_pipeline_sao_absolutos(self):
        from src.caminhos import BRUTOS, CHUNKS, BLOCOS, BLOCOS_TRATADOS

        for caminho in [BRUTOS, CHUNKS, BLOCOS, BLOCOS_TRATADOS]:
            self.assertTrue(
                Path(caminho).is_absolute(),
                f"{caminho} não é absoluto — depende do diretório atual"
            )

    def teste_padroes_das_funcoes_nao_usam_caminho_relativo(self):
        from analises.tratamento_dados import tratar_blocos
        from analises.analise_fraude import analise_fraude

        for funcao, parametro in [
            (tratar_blocos, "blocks_dir"),
            (tratar_blocos, "output_dir"),
            (analise_fraude, "blocks_dir"),
        ]:
            caminho = str(valor_padrao(funcao, parametro))
            self.assertNotIn(
                "..", caminho,
                f"{funcao.__name__}({parametro}) usa caminho relativo: {caminho}"
            )


if __name__ == "__main__":
    unittest.main()
