#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera sitemap.xml a partir de produtos.js (Mix Du Mix Store).

Uso:
    python gerar_sitemap.py

Somente biblioteca padrao (json/re/pathlib). Nao instala pacotes,
nao modifica produtos.js nem o restante do site; sobrescreve apenas
sitemap.xml. Gera UTF-8 SEM BOM, sem duplicatas, ordenado de forma
estavel (deterministica) e seguro para execucao repetida.

Regras:
- Home entra uma unica vez (sem ?view=home).
- Views institucionais indexaveis: sobre, contato, privacidade.
  (view=pedidos e area operacional de solicitacoes de visitantes,
   sem valor de busca publica -> fica fora; ?pedido=ID tambem fica fora.)
- Produtos: usa o ASIN real de produtos.js (fonte de verdade),
  deduplicado (ASIN unico = no maximo uma URL).
- Sem lastmod/changefreq/priority (sem datas inventadas).
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape  # garante XML valido mesmo se um ASIN tiver chars especiais

BASE = "https://kcersarkal.github.io/mixdumix/"
VIEWS_INDEXAVEIS = ["sobre", "contato", "privacidade"]


def extrair_asins_unicos(conteudo):
    ini = conteudo.find("[")
    fim = conteudo.rfind("]")
    if ini == -1 or fim == -1 or fim <= ini:
        raise SystemExit("Erro: lista de produtos nao encontrada em produtos.js")
    produtos = json.loads(conteudo[ini : fim + 1])
    asins = set()
    for p in produtos:
        a = p.get("asin")
        if isinstance(a, str) and a.strip():
            asins.add(a.strip())
    return sorted(asins)  # deduplicado + ordenacao estavel


def montar_urls(asins):
    urls = [BASE]  # Home (unica)
    urls += [BASE + "?view=" + v for v in VIEWS_INDEXAVEIS]
    urls += [BASE + "?artigo=" + a for a in asins]
    return urls


def gerar_xml(urls):
    itens = "".join("  <url><loc>%s</loc></url>\n" % escape(u) for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + itens
        + "</urlset>\n"
    )


def main():
    raiz = Path(__file__).resolve().parent
    conteudo = (raiz / "produtos.js").read_text(encoding="utf-8")
    asins = extrair_asins_unicos(conteudo)
    urls = montar_urls(asins)
    xml = gerar_xml(urls)
    # utf-8 padrao nao grava BOM; newline="\\n" evita CRLF
    (raiz / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")
    print(
        "sitemap.xml gerado: %d URLs "
        "(1 home, %d views, %d produtos unicos)" % (len(urls), len(VIEWS_INDEXAVEIS), len(asins))
    )


if __name__ == "__main__":
    main()
