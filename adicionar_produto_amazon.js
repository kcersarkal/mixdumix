#!/usr/bin/env node
/**
 * Adiciona produtos automaticamente ao blog Mix Du Mix via Node.js
 *
 * Uso:
 *   node adicionar_produto_amazon.js <ASIN_OU_LINK>
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const AFFILIATE_TAG = "mdm0c7-20";

function extrairAsin(entrada) {
  const match = entrada.match(/\/(?:dp|gp\/product|d)\/([A-Z0-9]{10})/i);
  if (match) return match[1].toUpperCase();
  const direto = entrada.match(/\b([A-Z0-9]{10})\b/i);
  if (direto) return direto[1].toUpperCase();
  throw new Error(`Não foi possível identificar o ASIN em: ${entrada}`);
}

function buscarAmazon(asin) {
  return new Promise((resolve, reject) => {
    const url = `https://www.amazon.com.br/dp/${asin}`;
    const options = {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
      }
    };

    console.log(`[*] Consultando ASIN ${asin} na Amazon...`);
    https.get(url, options, (res) => {
      let html = "";
      res.on("data", chunk => html += chunk);
      res.on("end", () => {
        // Título
        let titulo = `Produto Amazon ${asin}`;
        const mTitle = html.match(/<span[^>]*id=["']productTitle["'][^>]*>(.*?)<\/span>/is);
        if (mTitle) {
          titulo = mTitle[1].replace(/\s+/g, " ").trim();
        }

        // Imagem HD da CDN
        let imagem = `https://m.media-amazon.com/images/P/${asin}.01._SCLZZZZZZZ_SX1000_.jpg`;
        const mDyn = html.match(/data-a-dynamic-image=["'](\{.*?\})["']/);
        if (mDyn) {
          try {
            const parsed = JSON.parse(mDyn[1].replace(/&quot;/g, '"'));
            const keys = Object.keys(parsed);
            if (keys.length > 0) imagem = keys[0];
          } catch (e) {}
        } else {
          const mImg = html.match(/https:\/\/m\.media-amazon\.com\/images\/I\/[A-Za-z0-9+%-]+\._AC_[^"'\s]+\.jpg/i);
          if (mImg) imagem = mImg[0];
        }

        imagem = imagem.split("?")[0].replace(/\._AC_[^.]+\./, "._AC_SL1000_.");
        resolve({ asin, titulo, imagem });
      });
    }).on("error", reject);
  });
}

async function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.log("Uso: node adicionar_produto_amazon.js <ASIN_OU_LINK>");
    process.exit(1);
  }

  try {
    const asin = extrairAsin(arg);
    const { titulo, imagem } = await buscarAmazon(asin);

    console.log(`[*] Título: ${titulo}`);
    console.log(`[*] Imagem HD: ${imagem}`);

    const filePath = path.join(__dirname, "produtos.js");
    const content = fs.readFileSync(filePath, "utf8");
    const ini = content.indexOf("[");
    const fim = content.lastIndexOf("]");
    let list = JSON.parse(content.substring(ini, fim + 1));

    list = list.filter(p => p.asin !== asin);
    list.unshift({
      asin,
      title: titulo,
      source_url: `https://www.amazon.com.br/dp/${asin}`,
      image: imagem,
      affiliate_url: `https://www.amazon.com.br/dp/${asin}?tag=${AFFILIATE_TAG}`,
      last_checked_at: new Date().toISOString()
    });

    fs.writeFileSync(filePath, "const PRODUCTS = " + JSON.stringify(list, null, 2) + ";\n", "utf8");
    console.log(`[OK] produtos.js atualizado com sucesso! (Total: ${list.length})`);

    // Atualiza sitemap
    const sitemapPath = path.join(__dirname, "sitemap.xml");
    if (fs.existsSync(sitemapPath)) {
      let sitemap = fs.readFileSync(sitemapPath, "utf8");
      const urlArtigo = `https://kcersarkal.github.io/mixdumix/?artigo=${asin}`;
      if (!sitemap.includes(urlArtigo)) {
        sitemap = sitemap.replace("</urlset>", `  <url><loc>${urlArtigo}</loc></url>\n</urlset>`);
        fs.writeFileSync(sitemapPath, sitemap, "utf8");
        console.log(`[OK] sitemap.xml atualizado com o artigo (?artigo=${asin})`);
      }
    }

    console.log("\nConcluído com sucesso!");
  } catch (err) {
    console.error("[ERRO]", err.message);
    process.exit(1);
  }
}

main();
