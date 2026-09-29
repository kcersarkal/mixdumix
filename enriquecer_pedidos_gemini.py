"""Enriquece somente pedidos novos, depois de confirmados no site.

Executar na raiz de conversor-shopee-noweb, no ambiente Ubuntu do M21s.
Não altera app.py nem amazon/amazon.py.
"""

import base64
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from playwright.sync_api import sync_playwright

from amazon.amazon import ARQUIVO, GITHUB_API, REPO, _config, _requisicao_github


ESPERA_APOS_PUBLICACAO = 300
INTERVALO_CONFIRMACAO = 15
MAX_CONFIRMACOES = 20
URL_PUBLICA = "https://kcersarkal.github.io/mixdumix/pedidos.js"
ESTADO = Path(__file__).with_name("estado_descricoes_gemini.json")
PROIBIDOS = ("tag=", "ref_", "linkcode=", "creativeasin", "mdm0c7-20")


def source_url(asin):
    return "https://www.amazon.com.br/dp/" + str(asin).strip().upper()


def validar_consulta(url):
    texto = str(url or "").lower()
    if any(item in texto for item in PROIBIDOS):
        raise ValueError("URL afiliada bloqueada para consulta")
    return url


def ler_estado():
    if not ESTADO.exists():
        return {"conhecidos": [], "processados": []}
    try:
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    except Exception:
        return {"conhecidos": [], "processados": []}


def salvar_estado(estado):
    ESTADO.write_text(
        json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def ler_pedidos(token):
    url = f"{GITHUB_API}/repos/{REPO}/contents/{ARQUIVO}"
    resposta = _requisicao_github("GET", token, url)
    texto = base64.b64decode(resposta.get("content", "")).decode("utf-8")
    encontrado = re.search(r"window\.PEDIDOS\s*=\s*(\[[\s\S]*?\]);", texto)
    pedidos = json.loads(encontrado.group(1)) if encontrado else []
    return url, resposta.get("sha"), pedidos


def publicar(token, url, sha, pedidos, mensagem):
    texto = "window.PEDIDOS = " + json.dumps(
        pedidos, ensure_ascii=False, indent=2
    ) + ";\n"
    conteudo = base64.b64encode(texto.encode("utf-8")).decode("ascii")
    _requisicao_github(
        "PUT",
        token,
        url,
        {"message": mensagem, "content": conteudo, "sha": sha},
    )


def confirmar_publicacao(asin, source):
    for tentativa in range(1, MAX_CONFIRMACOES + 1):
        try:
            url = URL_PUBLICA + "?v=" + str(int(time.time()))
            req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=20) as resposta:
                texto = resposta.read().decode("utf-8", "replace")
            if asin in texto and source in texto:
                print(f"[{asin}] publicação confirmada na tentativa {tentativa}")
                return True
        except Exception as erro:
            print(f"[{asin}] confirmação falhou: {erro}")
        time.sleep(INTERVALO_CONFIRMACAO)
    return False


def coletar_amazon(url):
    validar_consulta(url)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(validar_consulta(url), wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        titulo = page.locator("#productTitle").first.text_content() or page.title()
        seletores = (
            "#feature-bullets",
            "#productDescription",
            "#bookDescription_feature_div",
            "#aplus",
        )
        partes = []
        for seletor in seletores:
            loc = page.locator(seletor).first
            if loc.count():
                texto = loc.text_content() or ""
                if texto.strip():
                    partes.append(texto.strip())
        corpo = "\n".join(partes)[:12000]
        browser.close()
    return titulo.strip(), corpo


def gerar_descricao(client, titulo, detalhes):
    prompt = f"""Escreva uma descrição profissional curta, clara e natural em português do Brasil para uma página de pedidos.
Use somente as informações fornecidas. Não invente características, medidas, garantia, desconto ou disponibilidade.
Não use emojis, links, hashtags, preço ou menção a afiliados. Entregue apenas um parágrafo de 2 a 4 frases.

Título: {titulo}
Informações reais do produto:
{detalhes}
"""
    resposta = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )
    texto = (getattr(resposta, "text", "") or "").strip()
    if not texto:
        raise RuntimeError("Gemini retornou descrição vazia")
    return texto


def principal(processar_existentes=False):
    config = _config()
    token = config["token"]
    if not token:
        raise RuntimeError("GITHUB_TOKEN não configurado")
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY não configurada")

    estado = ler_estado()
    url_api, sha, pedidos = ler_pedidos(token)
    atuais = {p.get("asin") for p in pedidos if p.get("asin")}

    # Primeira execução: cadastra os pedidos existentes, sem chamar o Gemini.
    if not estado["conhecidos"]:
        alterado = False
        for pedido in pedidos:
            asin = pedido.get("asin")
            if asin and not pedido.get("source_url"):
                pedido["source_url"] = source_url(asin)
                alterado = True
        if alterado:
            publicar(token, url_api, sha, pedidos, "Adicionar URLs originais aos pedidos")
            print("source_url adicionados. Execute novamente após a publicação.")
        estado["conhecidos"] = sorted(atuais)
        salvar_estado(estado)
        if not processar_existentes:
            return
        url_api, sha, pedidos = ler_pedidos(token)

    if processar_existentes:
        alvo = [p for p in pedidos if p.get("asin") and not p.get("descricao_profissional")]
        mensagem_vazia = "Nenhum pedido existente sem descrição profissional."
    else:
        alvo = [p for p in pedidos if p.get("asin") not in estado["conhecidos"]]
        mensagem_vazia = "Nenhum pedido novo para enriquecer."

    if not alvo:
        print(mensagem_vazia)
        return

    client = genai.Client()
    for pedido in alvo:
        asin = pedido["asin"]
        original = validar_consulta(pedido.get("source_url") or source_url(asin))

        if not pedido.get("source_url"):
            pedido["source_url"] = original
            publicar(token, url_api, sha, pedidos, "Adicionar URL original ao novo pedido")
            print(f"[{asin}] source_url publicado; aguardando confirmação")
            if not confirmar_publicacao(asin, original):
                print(f"[{asin}] não confirmado; ficará para a próxima execução")
                continue
            url_api, sha, pedidos = ler_pedidos(token)
            pedido = next(p for p in pedidos if p.get("asin") == asin)

        print(f"[{asin}] confirmação pública verificada")
        if not confirmar_publicacao(asin, original):
            continue
        if processar_existentes:
            print(f"[{asin}] pedido existente; espera de 5 minutos dispensada")
        else:
            print(f"[{asin}] aguardando 5 minutos após confirmação")
            time.sleep(ESPERA_APOS_PUBLICACAO)

        titulo, detalhes = coletar_amazon(original)
        descricao = gerar_descricao(client, titulo, detalhes)
        pedido["descricao_original"] = pedido.get("descricao_original") or pedido.get("descricao", "")
        pedido["descricao"] = descricao
        pedido["descricao_profissional"] = descricao
        pedido["descricao_gerada_em"] = datetime.now(timezone.utc).isoformat()
        publicar(token, url_api, sha, pedidos, "Gerar descrição profissional do pedido")
        estado["processados"].append(asin)
        estado["conhecidos"].append(asin)
        salvar_estado(estado)
        print(f"[{asin}] descrição publicada com sucesso")
        url_api, sha, pedidos = ler_pedidos(token)


if __name__ == "__main__":
    principal(processar_existentes="--processar-existentes" in sys.argv)
