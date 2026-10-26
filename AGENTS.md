# Instruções para agentes no Mix Du Mix

Este arquivo descreve como criar e revisar conteúdo no site Mix Du Mix. Qualquer agente (Antigravity, Claude ou outro) deve seguir estas regras sempre.

## 1. O que é o site

- Site estático no GitHub Pages: https://kcersarkal.github.io/mixdumix/ (repositório `kcersarkal/mixdumix`, branch `main`).
- Objetivo: ser aprovado e permanecer no Programa de Associados da Amazon Brasil e ser encontrado no Google com conteúdo original e útil.
- Dois tipos de conteúdo:
  - **Guias/artigos**: `produtos.js`, array `window.PRODUTOS_INFORMATIVOS`. URL: `?artigo=<ASIN>`.
  - **Pedidos da Comunidade**: `pedidos.js`, array `window.PEDIDOS`. URL: `?pedido=<ASIN>`. Os dois usam o mesmo formato de review completo.
- `index.html` carrega `produtos.js?v=...` e `pedidos.js?v=...`. Sempre que mudar um desses arquivos, troque o `?v=` em `index.html` (ex.: `?v=20261027-1`) para furar o cache dos leitores.

## 2. Regras que nunca podem ser quebradas

1. Link de compra sempre limpo: `https://www.amazon.com.br/dp/<ASIN>?tag=mdm0c7-20`. Nunca outra tag, nunca link encurtado, nunca parâmetros extras.
2. **Nenhuma imagem da Amazon** (`m.media-amazon.com`, `images-amazon.com` ou print da página). Isso viola o contrato de Associados. Use apenas foto oficial do fabricante ou de loja brasileira; sem foto confiável do modelo exato, use `assets/logo.png`.
3. Nunca dizer que a equipe testou, usou ou auditou o produto.
4. Nunca citar preço, desconto, Prime, frete grátis ou garantia "da Amazon", nem nota/estrelas/avaliações de clientes da Amazon.
5. Nunca copiar texto da Amazon nem colar trechos de outros sites: escreva com palavras próprias.
6. Dado técnico só entra se confirmado em fonte confiável (fabricante primeiro). Número que vem do fabricante leva "segundo a <marca>". Se não confirmar, deixe de fora ou escreva "confira no anúncio".
7. Não fazer scraping nem contornar bloqueio da Amazon. A Amazon pode ser consultada só para confirmar o título/modelo do ASIN.
8. Evitar produtos genéricos, sem marca clara (ex.: "bicicleta elétrica 1000W" sem fabricante). Prefira marcas conhecidas com ficha técnica pública.
9. Publicar aos poucos: no máximo 2 ou 3 artigos novos por semana. Conteúdo automático em massa é punido pelo Google.

## 3. Fluxo para um artigo novo

1. **Escolher o produto**: categorias que vendem bem (cozinha, casa, beleza, eletrônicos de marca, suplementos de marca). Produto de marca conhecida, com ficha técnica no site do fabricante.
2. **Achar o ASIN**: pesquise na web por `amazon.com.br <marca> <modelo>`; o resultado `amazon.com.br/.../dp/<ASIN>` traz o título do anúncio. Confira que o título bate com o modelo, a cor, a capacidade e a voltagem exatos. Se o ASIN já existir em `produtos.js` ou `pedidos.js`, pare.
3. **Pesquisar fora da Amazon** (pelo menos 3 fontes, guarde as URLs):
   - Lojas oficiais em VTEX têm API pública com descrição, ficha técnica e fotos:
     `https://<loja>/api/catalog_system/pub/products/search?ft=<modelo>`
     Funciona em: `www.mondial.com.br`, `loja.wap.ind.br`, `www.elgin.com.br`, `www.philco.com.br`, `loja.electrolux.com.br`, `www.motorola.com.br`.
   - Lojas em Shopify: `https://<loja>/products.json?limit=250` (ex.: `www.darklabsuplementos.com.br`).
   - Fichas em PDF do fabricante (Philips: `documents.philips.com`; TP-Link: `static.tp-link.com`; Apple: `apple.com/br/.../specs`).
   - Análises de imprensa: Canaltech, Tecnoblog, Hardware.com.br, Oficina da Net.
   - Comparadores (Buscapé, Zoom) só para conferir medidas e código do modelo.
4. **Foto**: baixe a foto principal do fabricante (VTEX `imageUrl`, Shopify `images[0].src`) ou de loja brasileira (KaBuM `images.kabum.com.br`, Buscapé `i.zst.com.br`). Converta para JPG com fundo branco, no máximo 1000x1000, e salve em `assets/produtos/<id>.jpg` (artigos) ou `assets/pedidos/<ASIN>.jpg` (Pedidos). **Abra a imagem e confira** que é o mesmo modelo, cor e versão do anúncio. Se não for, use `assets/logo.png`.
5. **Escrever** no tom da seção 5 e no formato da seção 4.
6. **Adicionar** o objeto ao final do array em `produtos.js` (ou atualizar o Pedido em `pedidos.js`). Mantenha o JSON válido, com indentação de 2 espaços.
7. **Atualizar** o sitemap: `python gerar_sitemap.py`.
8. **Trocar o `?v=`** de `produtos.js`/`pedidos.js` em `index.html`.
9. **Validar**:
   - `node -e "global.window={};require('./produtos.js');require('./pedidos.js');console.log(window.PRODUTOS_INFORMATIVOS.length, window.PEDIDOS.length)"` sem erro.
   - Subir um servidor local (`python -m http.server 8765`) e abrir `http://localhost:8765/?artigo=<ASIN>` (ou `?pedido=<ASIN>`): a página precisa mostrar título, foto, veredito, "Visão Geral", ficha técnica e pontos, sem erro no console.
10. **Publicar**: `git pull --rebase origin main`, commit `feat: novo guia <produto>` e `git push origin main`. Outro processo (bot de Pedidos) também grava em `pedidos.js`, por isso sempre faça pull antes.
11. **Relatar**: título, URL publicada e lista de fontes usadas.

## 4. Formato do objeto (artigo ou Pedido)

```json
{
  "asin": "B093MK3Z12",
  "id": "air-fryer-mondial-family-afn-40-bi-4l-110v",
  "titulo": "Air Fryer Mondial Family AFN-40-BI 4L (Preto/Inox, 1500 W, 110V)",
  "subtitulo": "Uma frase com gancho, do ponto de vista do leitor",
  "categoria": "Cozinha & Utilidades",
  "imagem": "assets/produtos/air-fryer-mondial-family-afn-40-bi-4l-110v.jpg",
  "data_revisao": "AAAA-MM-DD",
  "tempo_leitura": "5 min de leitura",
  "veredito_resumo": "Um parágrafo: para quem é, o que resolve e o principal motivo para escolher.",
  "links_compra": [
    { "loja": "Amazon", "url": "https://www.amazon.com.br/dp/B093MK3Z12?tag=mdm0c7-20",
      "destaque": "Confira preço, versão e condições de entrega na página do produto", "tipo": "amazon" }
  ],
  "visao_geral": ["5 a 7 parágrafos, ver seção 5"],
  "especificacoes": [{ "chave": "Capacidade", "valor": "4 litros" }],
  "pontos_fortes": ["5 a 7 benefícios práticos"],
  "pontos_atencao": ["3 a 5 limitações reais"],
  "para_quem_e": "Uma frase.",
  "para_quem_nao_e": "Uma frase."
}
```

- `categoria`: use uma das existentes: Tecnologia, Casa & Eletro, Cozinha & Utilidades, Saúde & Nutrição, Saúde & Beleza, Festas & Doces, Moda & Acessórios, Brinquedos.
- `id`: slug em minúsculas com hífens, com marca e modelo.
- Nos **Pedidos**, mantenha os campos que já existem (`id`, `asin`, `titulo`, `link`, `preco`) e preencha também `descricao` com uma frase curta e atraente (é o resumo do card na lista).

## 5. Tom do texto (o mais importante)

O texto precisa convencer sem parecer propaganda e soar como uma pessoa conversando, não como catálogo.

- **Abra pela situação do leitor**, não pelo produto. Ex.: "Sabe aquela batata frita que deixa a cozinha cheirando a óleo por horas e a panela que ninguém quer lavar?"
- **Fale com o leitor** ("você"), frases curtas, linguagem do dia a dia.
- **Transforme número em benefício**: não só "timer de 60 min com desligamento automático", mas "ela apita e desliga sozinha, então dá para ir tomar banho sem medo de queimar".
- **Dê uma dica de uso real** (ex.: "mexa as batatas na metade do preparo").
- **Seja honesto nos pontos de atenção**: limitações verdadeiras aumentam a confiança e a conversão.
- **Termine a visão geral com "Um último cuidado:"** tirando a última dúvida (voltagem, versão, cor, tamanho), que é o que leva ao clique com segurança.
- Atribua números de terceiros: "segundo a Mondial", "no teste do Canaltech".
- Proibido: "o melhor do mundo", "imperdível", "corra", "testamos", "na nossa experiência", preço, estrelas.

Estrutura sugerida para `visao_geral`:
1. A dor ou situação do leitor.
2. O diferencial principal do produto e por que ele importa.
3. Como é usar no dia a dia.
4. Dado técnico ou teste de terceiros, traduzido em benefício.
5. Cuidados de uso, limpeza ou instalação.
6. "Um último cuidado:" sobre a versão do anúncio.

## 6. Revisão de conteúdo existente

Ao revisar artigos ou Pedidos antigos:
- Reescreva `subtitulo`, `veredito_resumo`, `visao_geral`, `pontos_fortes`, `para_quem_e` e `para_quem_nao_e` no tom da seção 5, mantendo os dados técnicos já confirmados.
- Remova afirmações sem fonte (ex.: gás refrigerante, consumo de energia, classificação Procel que não batem entre fontes) ou troque por "confira no anúncio".
- Troque qualquer imagem `m.media-amazon.com` pela foto do fabricante ou por `assets/logo.png`.
- Atualize `data_revisao`.

## 7. Atenção: bot de Pedidos

O bot que cria Pedidos (commits "Novo pedido via bot") grava a foto direto da Amazon (`m.media-amazon.com`). Ao revisar, sempre troque essas imagens e complete o review do Pedido novo.
