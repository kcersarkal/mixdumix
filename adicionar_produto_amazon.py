#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adiciona produtos automaticamente ao blog Mix Du Mix a partir de um link ou ASIN da Amazon.

Uso:
    python adicionar_produto_amazon.py <ASIN_OU_LINK>

Exemplos:
    python adicionar_produto_amazon.py B0DCM31SDG
    python adicionar_produto_amazon.py https://www.amazon.com.br/dp/B0DCM31SDG

O script:
1. Extrai o ASIN da entrada.
2. Consulta a página oficial da Amazon e extrai o título real e a imagem principal em alta resolução da CDN.
3. Formata a URL da imagem no padrão oficial permanente: https://m.media-amazon.com/images/I/[ID]._AC_SL1000_.jpg
4. Adiciona o produto ao topo de produtos.js com a sua tag de afiliado configurada.
5. Atualiza o sitemap.xml automaticamente.
"""

import sys
import re
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# CONFIGURAÇÃO DA SUA TAG DE AFILIADO AMAZON
AFFILIATE_TAG = "mdm0c7-20"


def extrair_asin(entrada):
    """Extrai o código ASIN (10 caracteres) de uma URL ou string."""
    entrada = entrada.strip()
    match = re.search(r"/(?:dp|gp/product|d)/([A-Z0-9]{10})", entrada, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    match_direto = re.search(r"\b([A-Z0-9]{10})\b", entrada, re.IGNORECASE)
    if match_direto:
        return match_direto.group(1).upper()
    raise ValueError(f"Não foi possível identificar um ASIN válido em: '{entrada}'")


def consultar_dados_amazon(asin):
    """Acessa a página pública do produto na Amazon e extrai título e imagem limpa."""
    url = f"https://www.amazon.com.br/dp/{asin}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    
    print(f"[*] Consultando produto {asin} na Amazon...")
    with urllib.request.urlopen(req, timeout=25) as resposta:
        html = resposta.read().decode("utf-8", "ignore")

    # Extrai o título
    titulo = None
    m_title = re.search(r'<span[^>]*id=["\']productTitle["\'][^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)
    if m_title:
        titulo = re.sub(r"\s+", " ", m_title.group(1)).strip()
    else:
        m_page_title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        if m_page_title:
            titulo = m_page_title.group(1).split(" : Amazon.com.br")[0].split(" | Amazon.com.br")[0].strip()

    if not titulo:
        titulo = f"Produto Amazon {asin}"

    # Extrai a imagem principal (alta resolução na CDN da Amazon)
    imagem = None
    # 1. Tenta pegar de data-a-dynamic-image
    m_dyn = re.search(r'data-a-dynamic-image=["\'](\{.*?\})["\']', html)
    if m_dyn:
        try:
            dict_imgs = json.loads(m_dyn.group(1).replace("&quot;", '"'))
            # Pega a primeira imagem de maior resolução
            chaves = list(dict_imgs.keys())
            if chaves:
                imagem = chaves[0]
        except Exception:
            pass

    # 2. Se não encontrou, busca padrão de URL de imagem na CDN
    if not imagem:
        m_img = re.search(r'(https://m\.media-amazon\.com/images/I/[A-Za-z0-9+%-]+)\._AC_[^"\'\s]+\.jpg', html)
        if m_img:
            imagem = m_img.group(0)

    # 3. Normaliza para alta resolução _AC_SL1000_.jpg sem parâmetros de widget
    if imagem:
        imagem = imagem.split("?")[0]
        imagem = re.sub(r"\._AC_[^.]+\.", "._AC_SL1000_.", imagem)
        if not re.search(r"\._AC_SL\d+_\.", imagem):
            imagem = re.sub(r"(\.[a-zA-Z]{3,4})$", r"._AC_SL1000_\1", imagem)
    else:
        imagem = f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_SX1000_.jpg"

    return titulo, imagem


def atualizar_produtos_js(asin, titulo, imagem):
    """Adiciona ou atualiza o item em produtos.js mantendo o formato intacto."""
    caminho = Path(__file__).resolve().parent / "produtos.js"
    conteudo = caminho.read_text(encoding="utf-8")
    
    ini = conteudo.find("[")
    fim = conteudo.rfind("]")
    if ini == -1 or fim == -1 or fim <= ini:
        raise ValueError("Não foi possível localizar o array PRODUCTS em produtos.js")

    produtos = json.loads(conteudo[ini : fim + 1])

    # Remove se já existia para reposicionar no topo
    produtos = [p for p in produtos if p.get("asin") != asin]

    novo_item = {
        "asin": asin,
        "title": titulo,
        "source_url": f"https://www.amazon.com.br/dp/{asin}",
        "image": imagem,
        "affiliate_url": f"https://www.amazon.com.br/dp/{asin}?tag={AFFILIATE_TAG}",
        "last_checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    # Insere no início da lista (artigo mais recente)
    produtos.insert(0, novo_item)

    novo_js = "const PRODUCTS = " + json.dumps(produtos, ensure_ascii=False, indent=2) + ";\n"
    caminho.write_text(novo_js, encoding="utf-8")
    print(f"[OK] Produto adicionado com sucesso a produtos.js (Total agora: {len(produtos)})")


def atualizar_sitemap(asin):
    """Garante que a nova URL ?artigo=ASIN esteja registrada no sitemap.xml."""
    caminho = Path(__file__).resolve().parent / "sitemap.xml"
    if not caminho.exists():
        return
    conteudo = caminho.read_text(encoding="utf-8")
    nova_url = f"https://kcersarkal.github.io/mixdumix/?artigo={asin}"
    if nova_url not in conteudo:
        item_xml = f"  <url><loc>{nova_url}</loc></url>\n</urlset>"
        conteudo = conteudo.replace("</urlset>", item_xml)
        caminho.write_text(conteudo, encoding="utf-8")
        print(f"[OK] sitemap.xml atualizado com o novo artigo (?artigo={asin})")


def main():
    if len(sys.argv) < 2:
        print("Uso: python adicionar_produto_amazon.py <ASIN_OU_LINK_DO_PRODUTO>")
        print("Exemplo: python adicionar_produto_amazon.py B0DCM31SDG")
        sys.exit(1)

    entrada = sys.argv[1]
    try:
        asin = extrair_asin(entrada)
        print(f"[*] ASIN Identificado: {asin}")
        titulo, imagem = consultar_dados_amazon(asin)
        print(f"[*] Título: {titulo}")
        print(f"[*] Imagem HD da CDN: {imagem}")
        atualizar_produtos_js(asin, titulo, imagem)
        atualizar_sitemap(asin)
        print("\nPronto! O produto já está disponível como artigo no blog.")
    except Exception as erro:
        print(f"[ERRO] Falha ao adicionar produto: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
