"""Classe AnalisadorFII."""

from analisador import Analisador


class AnalisadorFII(Analisador):
    """Classe utilizada para analisar compra ou venda de FIIs."""

    def _prepara_dados(self):
        col_types = {
            "Dividend Yield": float,
            "P/VP": float,
            "Val. patrimonial p/cota": float,
            "DY CAGR": float,
            "Valor CAGR": float}
        self._dados = self._dados.astype(col_types)
        self._dados["Papel"] = self._dados.index

    def _realiza_analise(self):
        # Critérios para compra
        self._dados["Compra"] = 0
        self._dados["Compra"] += self._dados["P/VP"].between(0, 1)
        self._dados["Compra"] += self._dados["Dividend Yield"].gt(7)
        self._dados["Compra"] += self._dados["DY CAGR"].gt(4)
        self._dados["Compra"] += self._dados["Valor CAGR"].gt(0)

        # Critérios para venda
        self._dados["Venda"] = 0
        self._dados["Venda"] += self._dados["P/VP"].gt(1.1)
        self._dados["Compra"] += self._dados["Dividend Yield"].lt(5)

        # Adiciona a coluna de recomendação
        self._dados.loc[self._dados["Compra"] == 4, "Rec."] = "Comprar!"
        self._dados.loc[self._dados["Venda"] > 0, "Rec."] = "Vender!"
        self._dados["Rec."] = self._dados["Rec."].fillna("Manter")

        # Ordena a tabela
        self._dados = self._dados.sort_values(
            ["Rec.", "P/VP", "Dividend Yield"], ascending=[True, True, True])

    def _formata_dados(self):
        # Seleciona apenas algumas colunas para exibir
        colunas_selecionar = [
            "P/VP",
            "Dividend Yield",
            "DY CAGR",
            "Valor CAGR",
            "Rec.",
        ]
        self._dados = self._dados[colunas_selecionar].reset_index(level=0)

        # Renomeia as colunas
        self._dados.rename(columns={
            "index": "Codigo",
            "Dividend Yield": "DY",
        }, inplace=True)
