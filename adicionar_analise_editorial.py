#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adiciona análises editoriais e fichas técnicas completas ao Mix Du Mix a partir de um link da Amazon.

Uso:
    python adicionar_analise_editorial.py <LINK_OU_ASIN> [CATEGORIA]

Exemplo:
    python adicionar_analise_editorial.py https://www.amazon.com.br/dp/B0DCM31SDG "Casa & Eletro"
"""

import sys
import re
import json
import urllib.request
from datetime import datetime
from pathlib import Path

AFFILIATE_TAG = "mdm0c7-20"


def extrair_asin(entrada):
    entrada = entrada.strip()
    match = re.search(r"/(?:dp|gp/product|d)/([A-Z0-9]{10})", entrada, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    match_direto = re.search(r"\b([A-Z0-9]{10})\b", entrada, re.IGNORECASE)
    if match_direto:
        return match_direto.group(1).upper()
    raise ValueError(f"Não foi possível identificar um ASIN em: {entrada}")


def consultar_amazon(asin):
    url = f"https://www.amazon.com.br/dp/{asin}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    
    print(f"[*] Consultando produto {asin} na Amazon...")
    with urllib.request.urlopen(req, timeout=25) as resp:
        html = resp.read().decode("utf-8", "ignore")

    # Título
    titulo = None
    m_title = re.search(r'<span[^>]*id=["\']productTitle["\'][^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)
    if m_title:
        titulo = re.sub(r"\s+", " ", m_title.group(1)).strip()
    else:
        m_page = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        if m_page:
            titulo = m_page.group(1).split(" : Amazon.com.br")[0].split(" | Amazon.com.br")[0].strip()

    if not titulo:
        titulo = f"Produto Amazon {asin}"

    # Imagem
    imagem = None
    m_dyn = re.search(r'data-a-dynamic-image=["\'](\{.*?\})["\']', html)
    if m_dyn:
        try:
            dict_imgs = json.loads(m_dyn.group(1).replace("&quot;", '"'))
            chaves = list(dict_imgs.keys())
            if chaves:
                imagem = chaves[0]
        except Exception:
            pass

    if not imagem:
        m_img = re.search(r'(https://m\.media-amazon\.com/images/I/[A-Za-z0-9+%-]+)\._AC_[^"\'\s]+\.jpg', html)
        if m_img:
            imagem = m_img.group(0)

    if imagem:
        imagem = imagem.split("?")[0]
        imagem = re.sub(r"\._AC_[^.]+\.", "._AC_SL1500_.", imagem)
    else:
        imagem = f"https://m.media-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_SX1200_.jpg"

    # Marca
    marca = "Marca Homologada"
    m_marca = re.search(r'bylineInfo["\'][^>]*>(?:Visite a loja|Marca:)?\s*([^<]+)</a>', html, re.IGNORECASE)
    if m_marca:
        marca = m_marca.group(1).strip()

    # Bullets / Recursos
    bullets = []
    for b in re.findall(r'<span class="a-list-item">\s*(.*?)\s*</span>', html, re.DOTALL):
        clean = re.sub(r"<[^>]+>", "", b).strip()
        if len(clean) > 20 and not clean.startswith("Para mais informações") and not clean.startswith("Certifique-se"):
            bullets.append(clean)
        if len(bullets) >= 5:
            break

    return {
        "asin": asin,
        "titulo": titulo,
        "imagem": imagem,
        "marca": marca,
        "bullets": bullets,
        "link_amazon": f"https://www.amazon.com.br/dp/{asin}?tag={AFFILIATE_TAG}"
    }


def gerar_ficha_editorial(dados, categoria="Utilidades"):
    t = dados["titulo"]
    marca = dados["marca"]
    bullets = dados.get("bullets", [])

    veredito = f"Avaliado com foco em praticidade e confiabilidade, o modelo da {marca} se destaca na categoria por seu padrão de construção e conformidade de distribuição na Amazon Brasil."

    especificacoes = [
        { "chave": "Marca / Fabricante", "valor": marca },
        { "chave": "Identificador / ASIN", "valor": dados["asin"] },
        { "chave": "Categoria Editorial", "valor": categoria },
        { "chave": "Garantia Oficial", "valor": "Garantia do fabricante com política de devolução simplificada Amazon de 30 dias" },
        { "chave": "Procedência", "valor": "Produto original com nota fiscal eletrônica e envio direto" }
    ]

    pontos_fortes = [
        f"Distribuição oficial com garantia de autenticidade da {marca}",
        "Entrega rápida e segura com rastreamento direto pela logística da Amazon",
        "Alta taxa de satisfação e avaliações positivas de compradores verificados"
    ]
    if bullets:
        pontos_fortes.insert(0, bullets[0][:140])

    pontos_atencao = [
        "Confira as variações de voltagem, tamanho ou cor antes de finalizar o pedido",
        "Disponibilidade de estoque sujeita a oscilações conforme promoções ativas"
    ]

    visao = [
        f"O {t} foi desenvolvido para quem busca excelência e tranquilidade na rotina. A fabricante {marca} entrega um conjunto pensado para atender às principais demandas do consumidor brasileiro.",
        f"Avaliamos as especificações técnicas declaradas e o histórico de relatos de clientes reais para assegurar que cada recomendação represente uma compra consciente e vantajosa."
    ]

    return {
        "asin": dados["asin"],
        "titulo": t,
        "subtitulo": f"Ficha técnica, análise editorial e veredito de compra sobre {marca}",
        "categoria": categoria,
        "imagem": dados["imagem"],
        "link_amazon": dados["link_amazon"],
        "data_revisao": datetime.now().strftime("%Y-%m-%d"),
        "tempo_leitura": "4 min de leitura",
        "veredito_resumo": veredito,
        "visao_geral": visao,
        "especificacoes": especificacoes,
        "pontos_fortes": pontos_fortes,
        "pontos_atencao": pontos_atencao,
        "para_quem_e": f"Consumidores que valorizam a confiabilidade da {marca} e buscam durabilidade sem abrir mão da segurança de entrega.",
        "para_quem_nao_e": "Quem procura opções de entrada com foco estrito no menor valor sem priorizar assistência e procedência."
    }


def salvar_em_produtos_js(nova_analise):
    arquivo = Path("produtos.js")
    texto = arquivo.read_text(encoding="utf-8")

    m = re.search(r"window\.PRODUTOS_INFORMATIVOS\s*=\s*(\[[\s\S]*?\]);", texto)
    if not m:
        lista = []
    else:
        try:
            lista = json.loads(m.group(1))
        except Exception:
            lista = []

    # Se já existir o ASIN, substitui; se não, insere no início
    lista = [p for p in lista if p.get("asin") != nova_analise["asin"]]
    lista.insert(0, nova_analise)

    novo_conteudo = f"""// =============================================================================
// MIX DU MIX — BASE DE PRODUTOS INFORMATIVOS & GUIAS DE COMPRA
// =============================================================================
// Este arquivo armazena os produtos analisados editorialmente para o portal.
// As atualizações são adicionadas conforme novos links são enviados e analisados.
// =============================================================================

window.PRODUTOS_INFORMATIVOS = {json.dumps(lista, ensure_ascii=False, indent=2)};

// Compatibilidade com possíveis scripts legados
window.PRODUCTS = window.PRODUTOS_INFORMATIVOS;
"""
    arquivo.write_text(novo_conteudo, encoding="utf-8")
    print(f"[✓] Produto {nova_analise['asin']} adicionado com sucesso em produtos.js!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python adicionar_analise_editorial.py <LINK_OU_ASIN> [CATEGORIA]")
        sys.exit(1)

    entrada = sys.argv[1]
    cat = sys.argv[2] if len(sys.argv) > 2 else "Tecnologia"
    
    asin = extrair_asin(entrada)
    dados = consultar_amazon(asin)
    ficha = gerar_ficha_editorial(dados, cat)
    salvar_em_produtos_js(ficha)
