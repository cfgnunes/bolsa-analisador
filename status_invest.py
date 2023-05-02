"""Classe StatusInvest."""

from bs4 import BeautifulSoup
import requests


class StatusInvest:
    """Classe utilizada para obter os dados do site StatusInvest."""

    @staticmethod
    def _processa_pagina(url, codigo):
        # Header request
        ua_part1 = "Mozilla/5.0 (Linux; Android 12) "
        ua_part2 = "AppleWebKit/537.36 (KHTML, like Gecko) "
        ua_part3 = "Chrome/112.0.0.0 Mobile "
        ua_part4 = "Safari/537.36"
        headers = {
            "User-Agent": f"{ua_part1}{ua_part2}{ua_part3}{ua_part4}"
        }

        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "lxml")

        # Procura por todos item "bloco de informação"
        lista_info = soup.find_all(
            ["div", {"class": "w-50"}, "div", {"class": "info"}])

        # Coloca o código no dicionário
        info_data = {}
        info_data.update({codigo: {}})

        for info in lista_info:

            # Procura o "Título" dentro do "bloco de informação"
            titulo = info.find("h3", attrs={"class": "title"})

            # Para encontrar o campo "Tag along"
            if not titulo:
                titulo = info.find("span", attrs={"class": "d-inline-block"})
                if titulo:
                    titulo = titulo.find(
                        "span", attrs={"class": "d-inline-block"})

            # Para encontrar o campo "PATRIMÔNIO LÍQUIDO"
            if titulo and len(titulo) == 0:
                titulo = info.find("a")
                if titulo:
                    titulo = titulo.find("h3")

            # Procura o "Valor" dentro do "bloco de informação"
            valor = info.find(attrs={"class": "value"})

            # Caso não encontre "Título" ou "Valor" então ignora
            if not titulo or not valor:
                continue
            if len(titulo) == 0 or len(valor) == 0:
                continue

            # Retira espaços nos campos de "Título"
            str_titulo = str(titulo.contents[0]).strip()

            # Retira pontos e outros símbolos de "Valor"
            str_valor = str(
                valor.contents[0]).replace(
                "%", "").replace(".", "").replace(",", ".").strip()

            # Caso não encontre "Título" ou "Valor" então ignora
            if not str_titulo or not str_valor:
                continue

            # Zera os valores que possuem o símbolo "-" ou "--"
            if str_valor in ("-", "--"):
                str_valor = "0"

            if str_titulo not in info_data[codigo]:
                info_data[codigo][str_titulo] = str_valor
            else:
                if info_data[codigo][str_titulo] == "0" and str_valor != "0":
                    info_data[codigo][str_titulo] = str_valor

        return info_data

    @staticmethod
    def scrap_acao(codigo):
        """Retorna os dados das ações, baixados da Internet."""
        url = f"https://statusinvest.com.br/acoes/{codigo}"
        return StatusInvest._processa_pagina(url, codigo)

    @staticmethod
    def scrap_fii(codigo):
        """Retorna os dados das ações, baixados da Internet."""
        url = f"https://statusinvest.com.br/fundos-imobiliarios/{codigo}"
        return StatusInvest._processa_pagina(url, codigo)
