# Regras Editoriais e Publicação Mix Du Mix

Sempre que atuar neste projeto (`mixdumix`):
1. **Consulte obrigatoriamente** o arquivo `AGENTS.md` na raiz do repositório como a fonte de verdade inegociável.
2. **Link de Compra**: Sempre e exclusivamente `https://www.amazon.com.br/dp/<ASIN>?tag=mdm0c7-20`.
3. **Imagens**: NUNCA usar imagens de servidores da Amazon (`m.media-amazon.com`). Utilizar apenas foto oficial do fabricante (VTEX, Shopify, catálogos) tratada em JPG 800x800 com fundo branco, ou `assets/logo.png`.
4. **Tom Humanizado (Seção 5 do AGENTS.md)**:
   - Começar pela dor/situação real do leitor ("você");
   - Traduzir especificações técnicas em benefícios práticos do dia a dia;
   - Nunca inventar dados; sempre citar "segundo a <marca>" ou análises de imprensa de confiança;
   - O último parágrafo da `visao_geral` deve sempre abrir com `"Um último cuidado:"` tirando a última dúvida (voltagem, modelos, acabamento);
   - Proibido citar preço, estrelas, frete, descontos ou dizer que testou pessoalmente o item.
5. **Rotina de Publicação**:
   - Inserir objeto JSON válido em `produtos.js` (ou `pedidos.js`);
   - Atualizar sitemap: `python gerar_sitemap.py`;
   - Incrementar versão de cache `?v=` em `index.html`;
   - Validar com `node` e subir commit `feat: novo guia <produto>` para `origin main`.
