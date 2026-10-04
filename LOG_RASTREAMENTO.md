# Log de Rastreamento - Clique "Ver oferta" → Webhook n8n

## Data: 2026-09-01

### Etapas Executadas

1. ✅ **Backup inicial** — Criado backup do `index.html` em `E:\codex\2026-09-01\referenced-chatgpt-conversation-this-is-an-3\work\index.html.backup.before-clique-tracking.txt`
2. ✅ **Função `registrarCliqueOferta()`** — Atualizada para receber `(asin, pagina, linkAfiliado)`
3. ✅ **Payload do webhook** — Adicionado `link_afiliado` no `URLSearchParams`
4. ✅ **onclick Home** — Atualizado para enviar o link afiliado já presente no `href`
5. ✅ **onclick Produto** — Atualizado para enviar o link afiliado já presente no `href`
6. ✅ **onclick Pedido** — Atualizado para enviar o link afiliado já presente no `href`
7. ✅ **Validação de tamanho** — Comparado tamanho antes/depois do `index.html` para checar integridade do arquivo
8. ✅ **Validação de scripts** — Extraídos apenas scripts JavaScript normais, ignorando `application/ld+json`
9. ✅ **Validação sintática** — `node --check` executado no JavaScript extraído
10. ✅ **git diff** — Revisado antes de qualquer commit

### Arquivos Alterados

- `index.html` — Apenas o rastreamento de cliques foi ajustado
- `LOG_RASTREAMENTO.md` — Atualizado com as etapas, resultados e validações desta rodada
- `work/index.html.backup.before-clique-tracking.txt` — Backup de segurança fora do projeto original

### Trechos Modificados

- `registrarCliqueOferta(asin, pagina, linkAfiliado)` agora envia `link_afiliado`
- Home: `onclick="registrarCliqueOferta(..., 'home', safeUrl)"`
- Produto: `onclick="registrarCliqueOferta(..., 'produto', ensureAffiliateTag(p.affiliate_url))"`
- Pedido: `onclick="registrarCliqueOferta(..., 'pedido', ensureAffiliateTag(p.link) || '#')"`

### Validações

- Tamanho do arquivo: mantido íntegro, com aumento esperado por inclusão do novo campo de rastreamento
- `node --check`: OK no JavaScript extraído
- Scripts analisados: apenas os blocos JavaScript normais do arquivo, sem `application/ld+json`
- HTML: tags de fechamento principais preservadas, sem sinal de truncamento

### Resultado

- O evento de clique continua funcionando e agora carrega também o link afiliado correspondente ao `href`
- Nenhum outro comportamento do `index.html` foi alterado intencionalmente
- Commit criado: `4c9b98a Corrige rastreamento do link afiliado`
- Push concluído com sucesso para `origin/main`

### Último Ponto Concluído

✅ Alteração de rastreamento aplicada, validada, commitada e publicada no GitHub. Último ponto concluído: push de `origin/main` realizado com sucesso.

---

# Log de Rastreamento - Correção da Página Individual de Pedidos

## Data: 2026-09-03

### Backup Realizado

1. ✅ **Backup do `index.html`** — criado `index.html.backup.before-pedido-fix.txt` (47.950 bytes, idêntico ao original antes da edição), mantido no diretório do projeto

### Arquivos Alterados

- `index.html` — correção da função `renderPedido()` e adições pontuais de CSS/helper
- `LOG_RASTREAMENTO.md` — este registro

> Sem commit e sem push, conforme solicitado.

### Problema Encontrado

- A página individual do pedido (rota `?pedido=ID`, renderizada por `renderPedido()`) **não exibia a imagem do produto** (`p.imagem` nunca era usada) e **não exibia o preço** quando existia (`p.preco` era ignorado)
- A identificação do pedido dependia de `(item.id||item.asin) === id` (frágil quando apenas um dos campos existe)

### Solução Aplicada

1. `renderPedido()` agora renderiza a **imagem** (`p.imagem`, validada por `safeHttpUrl`, com `onerror` ocultando o bloco se a imagem falhar) e o **preço** formatado em BRL quando `p.preco` existe — layout no mesmo padrão visual da página de produto (`.product-detail`, `.product-info`, `.price-current`, botões reutilizados)
2. Busca do pedido corrigida nas três funções (`renderPedido`, `sharePedidoWhatsApp`, `copyPedidoLink`) para aceitar `id` **ou** `asin`: `item.id === id || item.asin === id`
3. Novo helper `formatPrice()` (formatação `pt-BR` via `toLocaleString`, retorna `null` sem preço)
4. Nova classe CSS `.product-image` (desktop e mobile via media query)
5. Botão **Ver oferta** continua usando `ensureAffiliateTag(p.link) || "#"`, preservando a tag `tag=mdm0a40-20`; botões WhatsApp, Copiar link e Voltar mantidos intactos

### Validações

- ✅ **Todos os pedidos abrem por `?pedido=ID`** — 7 pedidos testados pelas rotas de `id` e de `asin` (14 rotas), nenhum pedido válido mostrou “Pedido não encontrado”
- ✅ **Imagem exibida** — bloco `.product-image` presente no HTML renderizado de todos os pedidos com `p.imagem` válida
- ✅ **Preço** — exibido formatado (ex.: R$ 279,91 / R$ 2.399,00) quando `p.preco` existe; oculto quando `p.preco` é `null` (caso do 1º pedido)
- ✅ **Título, descrição e botões** (Ver oferta, WhatsApp, Copiar link, Voltar) presentes em todas as renderizações
- ✅ **Link afiliado** — `ensureAffiliateTag` preserva `tag=mdm0a40-20` já existente e adiciona quando ausente
- ✅ **HTML íntegro** — uma única ocorrência de `</html>`, `</body>`, `</main>` e `</style>`; arquivo termina em `</html>` (sem truncamento)
- ✅ **Extração de scripts** — extraídos apenas os blocos JavaScript normais (2 blocos), ignorando `type="application/ld+json"`
- ✅ **`node --check`** — OK no JavaScript extraído
- ✅ **Tamanho do arquivo** — antes: 47.950 bytes; depois: 48.905 bytes (+955 bytes, aumento esperado); backup confere com o original
- ✅ **`git diff`** — apenas `index.html` alterado (21 inserções, 6 remoções), sem alterações não relacionadas

### Erros Encontrados

- Nenhum erro no código final. Durante a validação, apenas falhas no próprio script de teste (asserções sobre quebra de linha nos botões e URL do WhatsApp codificada) foram corrigidas no harness — o HTML renderizado já estava correto

### Último Ponto Concluído

✅ Correção da página individual de pedidos aplicada e validada em `index.html` (backup mantido em `index.html.backup.before-pedido-fix.txt`). Último ponto concluído: validações executadas com sucesso — sem commit e sem push, aguardando revisão do usuário.

---

# Log de Rastreamento - Remoção das Páginas Individuais e Botão Compartilhar nos Cards

## Data: 2026-09-03

### Backup Realizado

1. ✅ **Backup do `index.html`** — criado `index.html.backup.before-remover-paginas-individuais.txt` (48.905 bytes, idêntico ao original antes desta rodada), mantido no diretório do projeto

### Arquivos Alterados

- `index.html` — única página com código alterado nesta rodada (48.905 → 35.393 bytes)
- `LOG_RASTREAMENTO.md` — este registro

> Sem commit e sem push, conforme solicitado. `produtos.js`, `pedidos.js`, SEO estático, textos de rodapé/sobre e o rastreamento de cliques não foram alterados.

### Problema Encontrado

- O site ainda possuía **páginas individuais** (`?produto=ID` e `?pedido=ID`), contrariando o requisito final de que não deve existir página individual de produto (nem na principal, nem em Pedidos)
- Os cards da seção Pedidos navegavam para o detalhe ao clicar; os botões de WhatsApp/Copiar link separados existiam apenas nessas páginas de detalhe

### Solução Aplicada

1. **Rotas removidas/desativadas por completo**: removidas as seções `data-view="produto"` e `data-view="pedido"` do HTML e toda a lógica de roteamento de detalhe (`renderProduct`, `renderPedido`, `goBack`, `previousMainView`, tratamentos de `?produto`/`?pedido` em `currentRoute`/`navigate`/`routeFromInitialUrl`/`showView`); acesso direto a `?produto=…` ou `?pedido=…` agora cai na Home (URL é limpa)
2. **SEO de produto removido**: `injectProductLD`, `applyProductSeo` + helpers (`productSeoTitle`, `productSeoDescription`, `productCanonicalUrl`, `truncateAt`, `removeProductLd`, `applyHomeSeo`) e `formatPrice`/`safeHttpUrl`/`validImageUrl` (órfãos das páginas removidas); SEO estático e dinâmico das views atuais preservados
3. **Cards sem navegação interna**: `productCard` (Home) e `pedidoCard` (Pedidos) agora possuem somente dois botões — **Ver oferta** (abre direto o link afiliado `ensureAffiliateTag`, preserva `tag=mdm0a40-20`, mantém `registrarCliqueOferta` com página `home`/`pedidos`) e **Compartilhar**; clicar no card não navega para nenhuma rota de detalhe
4. **Botão Compartilhar**: novo `compartilharOferta`/`compartilharOfertaPedido` → `abrirCompartilhamento` usa **Web Share API** (`navigator.share`, menu nativo do celular: WhatsApp, Instagram, Telegram etc.) compartilhando título + link afiliado; sem suporte, `copiarLinkCompartilhamento` copia o link afiliado e mostra “✓ Link copiado!” no botão (fallback `prompt` sem Clipboard API)
5. **Botões antigos removidos**: WhatsApp e Copiar link separados (das páginas de detalhe) removidos junto com as funções `shareWhatsApp`, `copyProductLink`, `sharePedidoWhatsApp`, `copyPedidoLink`; CSS órfão `.product-image` removido; novo CSS `.btn-share` (botão secundário pequeno, responsivo via classes existentes)
6. Texto de introdução da seção Pedidos atualizado (não menciona mais “clique para ver detalhes”)

### Validações

- ✅ **Nenhum card gera rota `?produto`/`?pedido`** — cards testados não contêm `navigate(` nem links internos; acesso direto a `?produto=…`/`?pedido=…` carrega a Home e limpa a URL
- ✅ **Todos os cards possuem somente “Ver oferta” + “Compartilhar”** — verificados cards da Home e de Pedidos (7/7 pedidos renderizados na grade, 1 Compartilhar por card)
- ✅ **`navigator.share` no celular** — chamado com `title` “Mix Du Mix Store” e `text` com título + link afiliado; cancelamento pelo usuário tratado (`.catch`)
- ✅ **Fallback desktop** — sem `navigator.share`, o link afiliado correto é copiado via Clipboard API e o botão mostra “✓ Link copiado!”; sem Clipboard, `prompt`
- ✅ **Link compartilhado é o afiliado** — `ensureAffiliateTag` preserva `tag=mdm0a40-20` nos links de produto (`p.affiliate_url`) e de pedido (`p.link`)
- ✅ **Clique nos botões não dispara navegação do card** — cards sem `onclick` de navegação; `Ver oferta` abre a Amazon em nova aba com rastreamento preservado
- ✅ **HTML íntegro** — uma ocorrência de `</html>`, `</body>`, `</main>`, `</style>`; arquivo termina em `</html>` (sem truncamento)
- ✅ **Extração de scripts** — apenas os blocos JavaScript normais (2 blocos), ignorando `type="application/ld+json"`
- ✅ **`node --check`** — OK no JavaScript extraído
- ✅ **Tamanho** — antes: 48.905 bytes; depois: 35.393 bytes (−13.512, remoções esperadas)
- ✅ **`git diff`** — apenas `index.html` com alterações relacionadas (+117/−310 nesta rodada somadas ao diff pendente da rodada anterior)

### Erros Encontrados

- Nenhum erro no código final. Durante a validação automatizada, apenas falhas do próprio harness de teste (regex com parêntese e stub global `history`/`viewFake`) foram corrigidas — o HTML gerado estava correto desde o início

### Último Ponto Concluído

✅ Páginas individuais removidas (rotas `?produto`/`?pedido` inativas) e cards da Home e de Pedidos com apenas “Ver oferta” (link afiliado direto com rastreamento) e “Compartilhar” (Web Share API + fallback de cópia). Validações concluídas com sucesso — sem commit e sem push, aguardando revisão do usuário.

---

# Log de Rastreamento - Restauração da Página Individual de Pedidos (?pedido=ID)

## Data: 2026-09-03

### Problema Identificado

- Na rodada anterior, a remoção das páginas individuais eliminou **também** a página individual de **Pedidos** (`?pedido=ID`), o que foi um erro de decisão: links compartilhados do tipo `https://kcersarkal.github.io/mixdumix-store/?pedido=ASIN` deixaram de abrir o pedido
- O requisito desta rodada: **restaurar somente o sistema de Pedidos** ao estado anterior (fonte de verdade: backup `index.html.backup.before-remover-paginas-individuais.txt`), **sem** restaurar a página individual dos produtos da Home (`?produto=ID`)

### Backup Utilizado

- ✅ **Fonte de verdade**: `index.html.backup.before-remover-paginas-individuais.txt` (48.905 bytes) — estado anterior à última rodada, usado para recuperar o código original de Pedidos

### Novo Backup Criado

- ✅ **Backup do estado atual**: `index.html.backup.before-restaurar-pagina-pedidos.txt` (35.393 bytes, idêntico ao `index.html` antes desta rodada), mantido no diretório do projeto

### Arquivos Alterados

- `index.html` — restauração do sistema de Pedidos (35.393 → 42.432 bytes nesta rodada)
- `LOG_RASTREAMENTO.md` — este registro

> Sem commit e sem push, conforme solicitado. `produtos.js`, `pedidos.js`, SEO e páginas institucionais não foram alterados. Home preservada (cards continuam com “Ver oferta” + “Compartilhar”).

### Trechos Restaurados (copiados do backup)

1. **Rota `?pedido=ID`** — `currentRoute()`/`routeFromInitialUrl()` reconhecem `?pedido=` (prioridade antes de `?view=`); `navigate(view, id, replace)` monta a URL `?pedido=ID` e `showView(view, id)` ativa a view `pedido` (highlight “Pedidos” no menu) e chama `renderPedido(id)`; `document.title` = “Pedido - Mix Du Mix Store”; back/forward via `popstate` preservado
2. **Página individual de Pedido** — seção HTML `data-view="pedido"` com `#pedido-container` reinserida entre as seções Pedidos e Sobre (markup idêntico ao backup)
3. **`renderPedido()`** — renderiza imagem (`p.imagem` via `safeHttpUrl`, `onerror` oculta se falhar), título, preço formatado quando existe (`formatPrice`), descrição, botão **Ver oferta** (link afiliado `ensureAffiliateTag(p.link) || "#"` com `tag=mdm0a40-20` e `registrarCliqueOferta(..., 'pedido', ...)`), botões **WhatsApp** (`sharePedidoWhatsApp`) e **Copiar link** (`copyPedidoLink`), botão **Voltar** (`navigate('pedidos')`), aviso “Pedido não encontrado” para id inexistente — busca por `id` **ou** `asin`
4. **`pedidoCard()`** (backup) — card clicável navega para `?pedido=` (`onclick`/`onkeydown` + `data-pid`), CTA “Ver pedido”; sem botões de Ver oferta/Compartilhar no card
5. **Funções/helpers** — `formatPrice()`, `validImageUrl()`, `safeHttpUrl()`, `sharePedidoWhatsApp()`, `copyPedidoLink()` (todas byte a byte idênticas ao backup, verificadas por comparação automática)
6. **CSS necessário** — `.product-image` (desktop `max-height:420px`) e regra responsiva `@media (max-width:640px)` (`max-height:260px`); texto de introdução de Pedidos voltou a “Clique para ver detalhes.”
7. **Removido nesta rodada** — `compartilharOfertaPedido()` (função da rodada anterior, sem uso após o card de pedido voltar a navegar); `goBack`/`previousMainView` **não** restaurados (só serviam à página de produto)

### NÃO Restaurado (proposital)

- ❌ `?produto=ID` continua **removido** — não existe seção `data-view="produto"`, `renderProduct`, `injectProductLD`/SEO de produto nem tratamento de `?produto` no roteador; acesso a `?produto=X` cai na Home e limpa a URL

### Testes Executados (0 falhas)

- ✅ **Rota `?pedido=ID`** — 7 pedidos × {`id`, `asin`} = **14 deep links** abertos via `routeFromInitialUrl`; todos renderizam `renderPedido` sem “Pedido não encontrado”; id inexistente mostra o aviso com Voltar
- ✅ **Página individual** — imagem (`m.media-amazon…`), título, descrição e preços formatados (R$ 279,91 / R$ 2.399,00 / R$ 125,90 etc.) presentes; pedido sem `preco` (1º) não exibe preço nem `NaN`
- ✅ **Botões** — “Ver oferta” abre link afiliado da Amazon com `tag=mdm0a40-20` e `registrarCliqueOferta(..., 'pedido', ...)`; WhatsApp e Copiar link presentes; Voltar navega para `pedidos`; rastreamento preservado
- ✅ **Navegação dos cards** — 7/7 cards na grade de Pedidos com `onclick="navigate('pedido', this.dataset.pid)"`, `data-pid`, CTA “Ver pedido”, sem botão Ver oferta/Compartilhar e sem `?pedido=` no `href` do card
- ✅ **Share/WhatsApp/Copiar** — `sharePedidoWhatsApp` abre `wa.me` com título + `?pedido=ASIN`; `copyPedidoLink` copia a URL `?pedido=…` e mostra “✅ Link copiado!”; nenhum usa `?produto`
- ✅ **`?produto=ID` NÃO restaurado** — nenhuma referência a `?produto`, `data-view="produto"` ou `renderProduct` no arquivo; rota cai na Home e limpa a URL
- ✅ **Home intacta** — card da Home mantém “Ver oferta” + “Compartilhar” (Web Share API + fallback); `compartilharOferta`/`abrirCompartilhamento`/`copiarLinkCompartilhamento` preservados
- ✅ **Comparação final com o backup** — `renderPedido`, `pedidoCard`, `sharePedidoWhatsApp`, `copyPedidoLink`, `formatPrice`, `safeHttpUrl`, `validImageUrl`, seção `PEDIDO DETALHE`, texto de introdução e CSS `.product-image` **byte a byte idênticos** ao backup (restaurados, não recriados)
- ✅ **HTML íntegro** — uma ocorrência de `</html>`, `</body>`, `</main>`, `</style>`; arquivo termina em `</html>`
- ✅ **Extração de scripts** — apenas blocos JavaScript normais (2), ignorando `application/ld+json`; **`node --check` OK**
- ✅ **Tamanho** — antes: 35.393 bytes; depois: 42.432 bytes (+7.039, código de Pedidos restaurado)
- ✅ **`git diff --check`** — sem erros; revisão do diff desta rodada: somente alterações relacionadas a Pedidos (+150/−39)

### Erros Encontrados

- Nenhum erro no código final. Durante a validação, apenas ajustes no harness de teste (preço com espaço não separável NBSP do `toLocaleString` pt-BR, texto “não encontrado” decodificado, e expectativas de URL do stub `history`/`location`) foram corrigidos — o HTML gerado e o comportamento estavam corretos

### Último Ponto Concluído

✅ Página individual de Pedidos restaurada exatamente como no backup (`?pedido=ID`, `renderPedido`, cards navegando para o detalhe, botões Ver oferta/WhatsApp/Copiar link/Voltar e CSS). `?produto=ID` permanece removido e a Home permanece intacta. Validações concluídas com sucesso — sem commit e sem push, aguardando revisão do usuário.

---

# Log de Rastreamento - Remoção da Imagem da Página Individual de Pedidos (?pedido=ID)

## Data: 2026-09-03

### Objetivo da Alteração

- Remover **somente a exibição da imagem** na página individual aberta por `?pedido=ID`, mantendo todo o restante do sistema de Pedidos (que acabara de ser restaurado e estava funcionando) intacto: rota, `renderPedido()`, cards, título, preço, descrição, Ver oferta, WhatsApp, Copiar link, Voltar e avisos
- **Não** remover o campo `imagem` nem as imagens de `pedidos.js` (arquivo não foi tocado)

### Backup Criado

- ✅ `index.html.backup.before-remover-imagem-pedido.txt` (42.432 bytes, idêntico ao `index.html` antes desta rodada), mantido no diretório do projeto

### Trecho Removido (somente isso, em `renderPedido()`)

```js
  const imagem = safeHttpUrl(p.imagem, "");
  // ... e dentro do template HTML: ...
  ${imagem ? `<div class="product-image"><img src="${escapeHtml(imagem)}" alt="${escapeHtml(p.titulo)}" loading="lazy" onerror="this.closest('.product-image').style.display='none'"></div>` : ""}
```

- O diff completo desta rodada contra o backup contém **exatamente essas 2 linhas removidas** (−247 bytes, 42.432 → 42.185) e nada mais

### CSS/Helpers — preservados (decisão) e por quê

- ✅ `safeHttpUrl`, `validImageUrl` e o CSS `.product-image` foram **preservados**: busca no projeto confirmou que eram usados apenas pela imagem da página individual, mas, conforme instrução, é preferível manter código auxiliar existente do que arriscar quebrar outra parte do site — ficam inertes e inofensivos

### Arquivos Alterados

- `index.html` — remoção das 2 linhas da imagem em `renderPedido()` (42.432 → 42.185 bytes)
- `LOG_RASTREAMENTO.md` — este registro

> Sem commit e sem push. `pedidos.js` e `produtos.js` **não alterados** (verificado via `git diff --quiet`).

### Validações Executadas (0 falhas, 34 checks)

- ✅ `?pedido=ID` reconhecido pelo roteamento (view `pedido` ativa) e pedidos reais de `pedidos.js` abrem a página individual
- ✅ **Página individual SEM imagem** — nenhum `<img>`, `product-image` ou `m.media-amazon` no HTML renderizado (7/7 pedidos testados)
- ✅ Cards da listagem continuam como estavam (antes não exibiam imagem — estado preservado; 7/7 cards com `navigate('pedido', …)`, CTA “Ver pedido”, `data-pid`)
- ✅ Título, preço (R$ 279,91; ausente no pedido sem preço, sem `NaN`), descrição presentes
- ✅ Ver oferta com link afiliado Amazon contendo `tag=mdm0a40-20` e `registrarCliqueOferta(…, 'pedido', …)` com o link afiliado
- ✅ Rastreamento: payload do webhook com `evento`, `asin`, `pagina=pedido` e `link_afiliado` com a tag
- ✅ WhatsApp abre `wa.me` com `?pedido=`; Copiar link copia a URL `?pedido=…` e confirma; Voltar (`navigate('pedidos')`) volta à listagem
- ✅ Home intacta (cards com Ver oferta + Compartilhar) e `?produto=ID` continua removido (cai na Home)
- ✅ HTML íntegro (1× `</html>`, `</body>`, `</main>`, `</style>`, termina em `</html>`); extração apenas de blocos JS normais (2), ignorando `application/ld+json`
- ✅ `node --check` OK no JavaScript extraído
- ✅ `git diff --check` sem erros; revisão do `git diff`: apenas as 2 linhas da imagem (nenhuma alteração não relacionada)

### Erros Encontrados

- Nenhum erro no código final nem durante a validação

### Último Ponto Concluído

✅ Imagem removida somente da página individual de Pedidos (`?pedido=ID`); rota, conteúdo, botões, rastreamento, tag `mdm0a40-20`, Home e `?produto` removido — todos confirmados por validação. Sem commit e sem push, aguardando revisão do usuário.

---

# Log de Rastreamento - Reformulação Completa para Blog Editorial e Conformidade Amazon

## Data: 2026-09-26

### Objetivo da Alteração
- Transformar a plataforma em um **blog editorial de guias e avaliações de produtos** no padrão revista/portal, eliminando a aparência de loja ("Store" / "thin affiliate").
- Atender com rigor a todas as diretrizes do **Programa de Associados da Amazon**:
  1. Remoção completa de redirecionamentos intermediários, popups ocultos (`window.open("about:blank")` com `setTimeout`) e webhooks bloqueantes que pudessem mascarar links.
  2. Inclusão da caixa de transparência obrigatória da Amazon em destaque antes de qualquer recomendação ("Como participante do Programa de Associados da Amazon, sou remunerado pelas compras qualificadas efetuadas").
  3. Substituição de botões diretos de compra na Home por cards de artigos informativos com botão "Saiba mais", que abrem a análise completa do produto (`?artigo=ASIN`).
  4. Manutenção de duas abas independentes: "Guias & Artigos" e "Pedidos da Comunidade".
  5. Atualização do sitemap e roteamento seguro.

### Backup Criado
- `index.html.backup.before-blog-redesign.txt`

### Arquivos Modificados
- `index.html` — Novo layout responsivo estilo portal/revista com Hero Banner de destaque, filtros por categoria, cards de artigos com resumo de 2 linhas, páginas de artigos ricas com aviso obrigatório da Amazon e botões diretos seguros.
- `gerar_sitemap.py` — Rota atualizada para `?artigo=ASIN`.

---

# Log de Rastreamento - Transição para Cloudflare Pages e Redesign Editorial de Alto Padrão

## Data: 2026-10-03

### Objetivo da Alteração
- Mudar totalmente o design do site para um padrão **Editorial Clean & Elegante** (inspirado em The Wirecutter / NYT / Monocle), focado em fichas técnicas detalhadas, análises práticas, prós e contras e decisões conscientes de compra.
- **Preservação Integral dos Pedidos da Comunidade**: o esquema de pedidos da comunidade (`pedidos.js`, rota `?view=pedidos` e página individual `?pedido=ID`) permanece 100% ativo e intocado em sua regra de negócio e funcionamento.
- **Preparação e Otimização para Cloudflare Pages**:
  - Eliminação de qualquer dependência de runtime externo/Vercel.
  - Criação de `_headers` com regras de cache para assets estáticos e cabeçalhos de segurança (X-Frame-Options, X-Content-Type-Options, Referrer-Policy).
  - Criação de `_redirects` com fallback SPA (`/* /index.html 200`).
  - Criação de `404.html` resiliente.
- **Fim da Coleta Automática em Massa**:
  - Interrompida a raspagem automática em lote de centenas de produtos.
  - Limpeza do catálogo de promoções antigas em `produtos.js`, abrindo espaço para análises ricas e aprofundadas.
  - Criação de `adicionar_analise_editorial.py` para permitir que o usuário envie o link de um produto e a análise completa (ficha técnica, prós, contras e veredito) seja cadastrada individualmente com alta precisão editorial.

### Backups Criados
- `index.html.backup.before-cloudflare-editorial.txt`
- `produtos.js.backup.before-clean.txt`

### Arquivos Modificados / Criados
- `index.html` — Novo layout editorial responsivo com tipografia Newsreader + Plus Jakarta Sans, navegação simplificada, busca universal, conformidade Amazon Associates permanente, renderização das análises em abas claras e preservação da experiência de pedidos.
- `produtos.js` — Base reformulada para suportar fichas técnicas completas com subtítulos, especificações em tabela, prós, contras e perfis de indicação ("Para quem é / Para quem não é").
- `_headers` — Cabeçalhos de segurança e cache para Cloudflare Pages.
- `_redirects` — Fallback SPA para Cloudflare Pages.
- `404.html` — Fallback HTML amigável para Cloudflare.
- `adicionar_analise_editorial.py` — Script especializado no fluxo sob demanda: recebe o link da Amazon e adiciona a análise completa ao portal.
- `gerar_sitemap.py` / `sitemap.xml` — Sitemap atualizado.
- `LOG_RASTREAMENTO.md` — Este registro.

---

# Log de Rastreamento - Cadastro da Creatina Soldiers Nutrition 1kg (Mercado Livre + Shopee)

## Data: 2026-10-03

### Ação Realizada
- Cadastrada a análise editorial aprofundada da **Creatina Monohidratada 100% Pura 1Kg - Soldiers Nutrition** em `produtos.js`.
- Configurado suporte a botões multiloja:
  - **Mercado Livre**: `https://meli.la/2LS8xt7` (com destaque de envio rápido Full).
  - **Shopee**: `https://s.shopee.com.br/2VsDk00PDr` (com destaque de cupons de frete e moedas).
- Ficha técnica detalhada com pureza, rendimento de 200 doses, prós, contras, veredito da redação e perfis de indicação de compra.
- Sitemap regenerado.

---

# Log de Rastreamento - Restauração da Identidade Visual Laranja Oficial (#EA580C)

## Data: 2026-10-03

### Ação Realizada
- Restaurada a cor laranja oficial da identidade visual do **Mix Du Mix** (`#EA580C` / hover `#C2410C` / claro `#FFEDD5`):
  - `theme-color` atualizado para `#EA580C`.
  - Inclusão do logotipo oficial `assets/logo.png` no cabeçalho e rodapé do portal.
  - Botões de navegação, abas ativas, filtros de categoria, caixas de veredito e badges com o laranja característico da marca.
  - Destaques de preço e selo dos **Pedidos da Comunidade** padronizados no tom laranja oficial.

---

# Log de Rastreamento - Layout Buy Box Horizontal (Imagem na Esquerda + Botão na Direita)

## Data: 2026-10-03

### Ação Realizada
- Implementado o padrão **Buy Box Horizontal** para as opções de compra:
  - **Lado Esquerdo**: Miniatura nítida e enquadrada do produto (78x78px com padding e fundo neutro).
  - **Centro**: Nome do marketplace/loja oficial, título do produto e destaque de benefício (ex: Envio Full / Cupons).
  - **Lado Direito**: Botão de compra destacado ("Comprar no Mercado Livre", "Comprar na Shopee", "Conferir Oferta").
- Disponibilizado tanto no topo da análise (após o Veredito da Redação) quanto na caixa de oferta ao final do artigo.
- Aplicado também na página individual de cada **Pedido da Comunidade**.
- Layout 100% responsivo para dispositivos móveis com empilhamento natural do botão.

---

# Log de Rastreamento - Caixa de Compra Neutra com Identificação de Destino Exclusiva no Botão

## Data: 2026-10-03

### Ação Realizada
- **Remoção de referências a lojas específicas no cabeçalho ou corpo do card**:
  - Título do card padronizado de forma neutra: **"Opções de Compra"** (e "Acessar Oferta do Pedido" nos pedidos da comunidade).
  - Texto explicativo neutro: *"Acesse com segurança a página oficial deste produto para conferir avaliações de outros compradores, disponibilidade de entrega e valores atualizados."*
  - O nome do marketplace/loja de destino não aparece no título ou texto da caixa, evitando vincular o produto a uma única loja.
- **Identificação da Loja Exclusivamente no Botão de Ação**:
  - Cada botão informa com precisão para onde o usuário será direcionado:
    - **[ Conferir no Mercado Livre ↗ ]** (Mercado Livre)
    - **[ Conferir na Shopee ↗ ]** (Shopee)
    - **[ Conferir na Amazon ↗ ]** (Amazon)
    - **[ Conferir Oferta ↗ ]** (Demais lojas parceiras)
- **Estrutura Visual da Linha de Compra**:
  - **Esquerda**: Miniatura fotográfica do produto (`purchase-item-thumb`).
  - **Centro**: Nome do produto e benefícios (ex: Envio Full / Frete Grátis / Cupons).
  - **Direita**: Botão de compra informando o destino.
- Aplicado com harmonia nos guias de compras editoriais e nas páginas de Pedidos da Comunidade.

---

# Log de Rastreamento - Correção de Sobreposição de Badge e Auditoria de Preços dos Pedidos

## Data: 2026-10-03

### Ação Realizada
1. **Correção de Sobreposição Visual do Badge de Pedido da Comunidade**:
   - Adicionado `z-index: 10` com `box-shadow` e fundo sólido `#FFFFFF` em `.article-badge`.
   - Ajustado o espaçamento superior de `.article-card-thumb` para `padding: 40px 20px 16px` e `height: 230px`, garantindo que produtos altos (como geladeira e air fryer) não disputem espaço ou fiquem por cima da etiqueta.
   - Definido `z-index: 1` e `max-width: 100%` nas imagens dos cards para assegurar ordem de empilhamento perfeita.

2. **Auditoria de Existência e Atualização de Preços na Amazon**:
   - Verificados todos os 16 produtos cadastrados em `pedidos.js` diretamente na Amazon Brasil.
   - Todos os 16 itens continuam ativos e disponíveis (HTTP 200). Nenhum produto descontinuado.
   - Valores atualizados com base nos preços vigentes em tempo real:
     - `B0FVP6KRP4` (Geladeira Electrolux 320L): R$ 2.949,00 (anteriormente `null`).
     - `B0GYGFRXSY` (Air Fryer Octo Fry Elgin 8L): R$ 338,00 (era R$ 279,91).
     - `B0FJMHMCBZ` (Headphone Bluetooth Philips TAH2300BK): R$ 129,00 (era R$ 125,90).
     - `B0FPT7HB8G` (Carrinho Organizador 3 Prateleiras): R$ 113,90 (era R$ 96,79).
     - `B0DVMQVVDY` (Fone TWS Philips TAT1109BK): R$ 129,00 (era R$ 99,99).
     - `B0FQFH5PJS` (Apple Watch SE 3): R$ 2.399,00 (confirmado).
     - `B0755PV4H7` (Repetidor Wi-Fi TP-Link RE200): R$ 173,53 (era R$ 170,91).
     - `B0FRJV1B75` (Smart TV 43 LG 4K): R$ 1.690,05 (era R$ 1.604,55).
     - `B0BL5CSRBM` (Creatina Soldiers Nutrition 1kg): R$ 68,90 (era R$ 68,89).
     - `B0DCM31SDG` (Fogão Elétrico Elgin Double Cook): R$ 79,00 (anteriormente `null`).
     - `B0GLTJ4MYM` (Smartphone Motorola Edge 70 5G): R$ 2.249,10 (confirmado).
     - `B0CVSJFMFN` (Paçoca Rolha Ricco 1,5kg): R$ 26,50 (confirmado).
     - `B0GS79683R` (Kit Doces Aniversário 25 Crianças): R$ 85,49 (era R$ 89,99).
     - `B0H7FLPHPQ` (Kit Elástico Cabelo Infantil 875 peças): R$ 37,90 (confirmado).
     - `B096YGN1QF` (Jogo Totó Super Craque DM Toys): R$ 98,70 (era R$ 93,90).
     - `B0GX57BFD1` (Garrafa Térmica 750ml): R$ 41,70 (era R$ 39,90).

---

# Log de Rastreamento - Padronização Rigorosa de Largura (280px) para Botões Shopee e Mercado Livre

## Data: 2026-10-03

### Ação Realizada
- **Ajuste Milimétrico de Largura Idêntica**:
  - Como o texto do botão do Mercado Livre ("Conferir no Mercado Livre") possui 25 caracteres e demanda ~275px somando padding e ícone, a largura padrão de 250px estava permitindo que o botão do Mercado Livre ficasse ligeiramente maior que o da Shopee.
  - A largura de ambos os botões foi fixada com precisão absoluta em **`280px`** tanto nas regras de CSS (`width: 280px; min-width: 280px; max-width: 280px;`) quanto inline (`style="width: 280px;"`) e no contêiner `.purchase-item-right` (`flex: 0 0 280px; width: 280px;`).
  - O botão da Shopee e o botão do Mercado Livre agora possuem rigorosamente o mesmo tamanho e proporção.
  - Em telas menores que 680px (`@media (max-width: 680px)`), ambos ocupam `width: 100% !important` com centralização automática.

---

# Log de Rastreamento - Inclusão Editorial: Creatina Dark Lab 1kg e Lavadora WAP Ousada Plus 2200

## Data: 2026-10-03

### Ação Realizada
1. **Cadastro da Creatina Monohidratada 100% Pura 1Kg - Dark Lab**:
   - Slug: `creatina-dark-lab-1kg`
   - Categoria: *Saúde & Nutrição*
   - Links afiliados vinculados:
     - **Mercado Livre**: `https://meli.la/2nMQg1S` (Destaque: Envio Rápido / Frete Grátis com Full)
     - **Shopee**: `https://s.shopee.com.br/9V1y7OkvUe` (Destaque: Loja Oficial / Cupons de Frete e Moedas)
   - Conteúdo: Análise técnica com laudos de pureza acima de 99%, rendimento de 200 doses, ficha técnica e prós/contras.

2. **Cadastro da Lavadora de Alta Pressão WAP Ousada Plus 2200 (1500W - 1750 PSI)**:
   - Slug: `lavadora-alta-pressao-wap-ousada-plus-2200`
   - Categoria: *Casa & Eletro*
   - Links afiliados vinculados:
     - **Amazon**: `https://www.amazon.com.br/dp/B077PT41YL?tag=mdm0c7-20` (Garantia e Entrega Prime)
     - **Mercado Livre**: `https://meli.la/2UH78j8` (Envio Rápido / Frete Grátis com Full)
     - **Shopee**: `https://s.shopee.com.br/30oUNp9FTs` (Loja Oficial / Cupons de Frete e Moedas)
   - Conteúdo: Ficha técnica completa com motor 1500W, vazão 342 L/h, sistema Stop Total, bomba de cabeçote em alumínio e guia de decisão.

3. **Sitemap Atualizado**:
   - `sitemap.xml` regenerado com as novas páginas editoriais indexáveis.

---

# Log de Rastreamento - Layout de Compra Unificado com Imagem Única Maior

## Data: 2026-10-03

### Ação Realizada
- **Eliminação de Repetições de Miniaturas**:
  - Em produtos com múltiplos marketplaces (como a Lavadora WAP com 3 lojas e as Creatinas com 2 lojas), a imagem pequena não é mais repetida em cada linha.
- **Estrutura Unificada (`.purchase-unified-box`)**:
  - **Lado Esquerdo (`.purchase-unified-media`)**: Uma única imagem fotográfica de destaque, consideravelmente maior (220px de largura e expansão vertical elástica `align-items: stretch` para preencher toda a altura do bloco).
  - **Lado Direito (`.purchase-unified-content`)**:
    - Título oficial do produto exibido de forma limpa uma única vez no topo.
    - Lista de lojas parceiras com seus selos/benefícios de entrega e botões de compra padronizados com exatamente 280px de largura.
- **Responsividade Aperfeiçoada**:
  - Em telas menores que 820px (`@media (max-width: 820px)`), o bloco se reorganiza verticalmente, posicionando a imagem maior com respiro no topo e os botões em largura total abaixo.

---

# Log de Rastreamento - Inclusão Editorial: Ar-Condicionado LG Dual Inverter +AI Voice 9.000 BTUs

## Data: 2026-10-03

### Ação Realizada
- **Cadastro do Ar-Condicionado LG Dual Inverter +AI Voice 9.000 BTUs Frio 127V**:
  - Slug: `ar-condicionado-lg-dual-inverter-voice-9000-btus`
  - Categoria: *Casa & Eletro*
  - Link de afiliado:
    - **Mercado Livre**: `https://meli.la/1b9phq3` (Destaque: Envio Rápido / Frete Grátis com Full)
  - Ficha técnica aprofundada:
    - Economia de até 70% de energia e refrigeração 40% mais rápida com compressor de rotor duplo.
    - Operação ultra silenciosa a partir de 19 dB no modo sono.
    - Conectividade Wi-Fi nativa via aplicativo LG ThinQ com comandos de voz por Alexa e Google Assistente.
    - Serpentina 100% de cobre com aletas anticorrosivas GoldFin e 10 anos de garantia no compressor.
    - Tensão 127V (versão altamente demandada no mercado).
- `sitemap.xml` regenerado com 8 URLs indexáveis.











