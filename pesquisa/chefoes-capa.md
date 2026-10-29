# Pesquisa: capa e mockups do "Chefões do Cartão" (29/10/2026)

## Onde a capa aparece
- **Hotmart (loja e checkout):** a imagem do produto aparece quadrada e pequena na lista (prints dos concorrentes em `saida/ref/chefoes/`). A ajuda da Hotmart não publica a medida (https://suportehotmart.zendesk.com/hc/en-us/articles/360031150472-How-to-set-up-the-new-product-page): o Tiago confere na tela "Editar informações básicas". Geramos quadrada 1200×1200 (reduz sem perder nitidez).
- **Página de vendas e anúncios:** mockup do pacote (16:9, quadrado e 9:16 para stories).
- **Dentro do produto:** capa vertical 2:3 (a primeira página do PDF).

## Regras de capa que funcionam em miniatura
(https://spa-selfpubagency.lovable.app/publishing-blog/cover-design-at-thumbnail-size)
- Testar em ~200×300 px no celular, ao lado dos concorrentes.
- Gênero reconhecível em 1 segundo: o nosso é "jogo/desenho animado" → ilustração e cor saturada.
- Título é o maior elemento; no máximo dois tamanhos de letra; tirar o resto.
- Alto contraste e letra grossa; traço fino some na miniatura.

## Mockups
- Mockup mostra o produto "em uso" e o que vem no pacote (https://herospark.com/blog/e-book-mockup/). Para nós: livro + celular com o simulador + plano em PDF + bônus, cada peça com o próprio visual.
- Concorrentes na Hotmart: capas de banco de imagem, sem mostrar o que vem dentro. Diferencial: mostrar o simulador funcionando e os chefões.

## Direção
- Fundo escuro (tinta) na capa, sem branco; chefões grandes; título em duas cores (branco + amarelo) com Baloo 2 800.
- Mockup sobre verde-sálvia (sem branco), livro em perspectiva com lombada, celular com o palco da batalha, folhas do plano e os bônus em cartões.
- Tudo por script (`tools/capa.py`), com a arte e as telas tiradas do próprio produto.
