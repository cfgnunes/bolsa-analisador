"""Classe Analisador."""

from concurrent.futures import ThreadPoolExecutor

import pandas as pd


class Analisador:
    """Classe utilizada para analisar ativos."""

    def __init__(self, arquivo_titulos, funcao_scrap):
        """Método construtor."""
        df = pd.read_csv(arquivo_titulos)
        self._codigos = df["codigo"].tolist()
        self._funcao_scrap = funcao_scrap
        self._dados = None
        self._recebe_dados()
        self._prepara_dados()
        self._realiza_analise()
        self._formata_dados()

    def _recebe_dados(self):
        dic_dados_titulo = {}
        dados = None

        # Busca os dados na Internet paralelamente usando threads.
        with ThreadPoolExecutor(max_workers=8) as executor:
            dados = executor.map(self._funcao_scrap, self._codigos)

        for dado in dados:
            dic_dados_titulo.update(dado)

        self._dados = pd.DataFrame.from_dict(dic_dados_titulo).T

    def _prepara_dados(self):
        raise NotImplementedError

    def _realiza_analise(self):
        raise NotImplementedError

    def _formata_dados(self):
        raise NotImplementedError

    def get_dados(self):
        """Retorna a tabela contendo as recomendações da análise feita."""
        return self._dados
