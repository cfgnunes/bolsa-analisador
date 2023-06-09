"""Classe AnalisadorAcoes."""

from analisador import Analisador


class AnalisadorAcoes(Analisador):
    """Classe utilizada para analisar compra ou venda de ações."""

    def _prepara_dados(self):
        col_types = {
            "Valor atual": float,
            "Dividend Yield": float,
            "P/L": float,
            "Tag Along": float,
            "P/VP": float,
            "P/EBIT": float,
            "ROE": float,
            "LPA": float,
            "M. Líquida": float,
            "Liq. corrente": float,
            "CAGR Receitas 5 anos": float,
            "EV/EBITDA": float,
            "P/SR": float,
            "Patrimônio líquido": float,
            "Dívida bruta": float,
            "Valorização (12m)": float,
            "Free Float": float,
            "Dív. líquida/PL": float,
            "Dív. líquida/EBITDA": float,
            "CAGR Lucros 5 anos": float
        }
        self._dados = self._dados.astype(col_types)
        self._dados["Papel"] = self._dados.index

    def _realiza_analise(self):
        # Critérios para compra
        self._dados["Compra"] = 0
        self._dados["Compra"] += self._dados["P/VP"].between(0, 2)
        self._dados["Compra"] += self._dados["Dividend Yield"].gt(7)
        self._dados["Compra"] += self._dados["P/L"].between(0, 6)
        self._dados["Compra"] += self._dados["ROE"].gt(13)
        self._dados["Compra"] += self._dados["Dív. líquida/EBITDA"].lt(2)
        self._dados["Compra"] += self._dados["CAGR Lucros 5 anos"].ge(0)

        # Critérios para venda
        self._dados["Venda"] = 0
        self._dados["Venda"] += self._dados["P/VP"].gt(10)
        self._dados["Venda"] += self._dados["P/L"].gt(20)
        self._dados["Venda"] += self._dados["P/VP"].lt(0)
        self._dados["Venda"] += self._dados["P/L"].lt(0)
        self._dados["Venda"] += self._dados["ROE"].lt(5)
        self._dados["Venda"] += self._dados["Dív. líquida/EBITDA"].gt(5)
        self._dados["Venda"] += self._dados["CAGR Lucros 5 anos"].lt(-4)
        self._dados["Venda"] += self._dados["Valor atual"].lt(2)

        # Adiciona a coluna de recomendação
        self._dados.loc[self._dados["Compra"] == 6, "Rec."] = "Comprar!"
        self._dados.loc[self._dados["Venda"] > 0, "Rec."] = "Vender!"
        self._dados["Rec."] = self._dados["Rec."].fillna("Manter")

        # Ordena a tabela
        self._dados = self._dados.sort_values(
            ["Rec.", "P/L", "Dividend Yield"], ascending=[True, True, True])

    def _formata_dados(self):
        # Seleciona apenas algumas colunas para exibir
        colunas_selecionar = [
            "Valor atual",
            "P/L",
            "Dividend Yield",
            "P/VP",
            "ROE",
            "Dív. líquida/EBITDA",
            "CAGR Lucros 5 anos",
            "Rec.",
        ]
        self._dados = \
            self._dados[colunas_selecionar].reset_index(level=0)

        # Renomeia as colunas
        self._dados.rename(columns={
            "index": "Codigo",
            "Valor atual": "Preço",
            "Dív. líquida/EBITDA": "D/EBITDA",
            "Dividend Yield": "DY",
            "CAGR Lucros 5 anos": "CAGR Luc.",
        }, inplace=True)
