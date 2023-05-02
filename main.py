#!/usr/bin/env python3
"""Programa para análise de compra ou venda de títulos na Bolsa de Valores."""

from analisador_acao import AnalisadorAcao
from analisador_fii import AnalisadorFII
from status_invest import StatusInvest


def main():
    """Função principal."""
    # Exibe uma análise de compra ou venda de ações
    print("--> Análise de compra ou venda de ações:")
    analisador = AnalisadorAcao("data/acoes.csv", StatusInvest.scrap_acao)
    dados = analisador.get_dados()
    print(dados)

    # Exibe uma análise de compra ou venda de FIIs
    print("\n--> Análise de compra ou venda de FIIs:")
    analisador = AnalisadorFII("data/fiis.csv", StatusInvest.scrap_fii)
    dados = analisador.get_dados()
    print(dados)


if __name__ == "__main__":
    main()
