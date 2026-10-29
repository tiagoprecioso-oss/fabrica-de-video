# Receita: site de marca (v2, 29/10/2026)

## Quando usar
"Faça o site da marca X" — loja, landing page ou portfólio de uma marca (nossa, de cliente ou conceito).

## Entradas
- Manual da marca pronto (`portfolio/<marca>/marca.md`, ver `receitas/marca.md`): conceito, promessa, cores, tipos, voz, produtos.
- Imagens da fábrica (fotos 3D, rótulos) — ver `receitas/foto-produto-3d.md`. **Sem imagem própria, não comece o site.**
- Pesquisa de referências feita (`receitas/pesquisa-de-referencias.md`).

## Passos
1. **Releia o manual e a pesquisa.** Escreva no topo do `<style>` o plano: 1 linha de conceito de layout + tokens de cor e tipo **copiados do manual** (nada inventado na hora). — agente: desenvolvedor-web
2. **Estrutura** (loja de produto; adapte a ordem, não a lógica):
   1. faixa fina de aviso (frete, prazo, safra);
   2. cabeçalho: menu à esquerda, marca no centro, sacola à direita;
   3. **hero = imagem grande do produto** com 1 título curto e 1 botão (no celular a legenda sai de cima da foto e vai para baixo dela);
   4. grade de produtos: foto 4:5, nome, preço, 1 linha de notas, botão;
   5. seção de origem/prova: imagem + texto curto + **tabela com dados reais**;
   6. a assinatura visual da marca em destaque (ex.: os rótulos);
   7. ferramenta útil (ex.: calculadora de assinatura com preço por xícara);
   8. guia/uso do produto;
   9. rodapé com newsletter e o aviso de projeto conceitual quando for fictício.
3. **Regras de visual** (aprendidas na pesquisa):
   - a foto conta a história; tipografia pequena e exata (corpo 16 px, títulos 26–52 px, peso 500);
   - cor só onde o manual manda (embalagem, pontinhos de cada produto); fundo neutro;
   - nada de formas geométricas decorativas, gradientes chamativos, emojis ou cards com sombra em tudo;
   - números em fonte mono com `tabular-nums`;
   - claro e escuro definidos por tokens; margem lateral `max(16px, env(safe-area-inset-*))`.
4. **Escreva** `portfolio/<marca>/site.html` (formato artifact: sem `<html>/<head>/<body>`; começa com `<title>`, fontes do Google Fonts, `<style>`). Imagens em `portfolio/<marca>/img/` com caminho relativo `img/...`.
5. **Confira**: `node tools/conferir_pagina.js portfolio/<marca>/site.html saida/conf/<marca>` → olhe `desktop.png` e `celular.png`; corrija rolagem lateral, erros, texto em cima da foto, contraste. Uma rodada de ajustes.
6. **Publique** como artifact (ferramenta Artifact, `file_path` do site.html e `files` mapeando cada `img/*.jpg`). Republicar o mesmo arquivo mantém o link.
7. **Commit** de `portfolio/<marca>/` (site, img, marca.md) e push.
8. **Atualize esta receita** (Lições/versão) e a lista de entregas no `marca.md`. — agente: receiteiro

## Pronto quando
- [ ] Todas as imagens saíram da fábrica (3D, rótulo, render) e o script que as gera está no repositório.
- [ ] Cores, tipos e textos batem com o manual (inclusive a promessa da marca no título).
- [ ] Desktop e celular sem rolagem lateral nem erros; legível no claro e no escuro.
- [ ] Botões de compra/formulários respondem (em conceito, com aviso "demo").
- [ ] Link publicado e o Tiago sabe que precisa liberar no menu Compartilhar.

## Lições
- 29/10 — v1 do Ninho Alto: sem pesquisa e sem fotos, ficou "com cara de IA". Causa: letra display gigante, azulejos geométricos, nenhuma imagem real. Solução na v2: pesquisa primeiro, fotos 3D do Blender, tipografia contida.
- 29/10 — O título do hero ("Three lots from one mountain") não usou a promessa do manual ("Grown above 1,100 m"). Conferir textos contra o manual no passo 1.
- 29/10 — Legenda sobre a foto no celular cobre o produto: no celular, legenda abaixo da imagem.
- 29/10 — Imagem ruim (macro de grãos parecendo bombom) sai do site até ficar boa; melhor menos imagens do que uma fraca.

## Histórico
- v1 29/10/2026 — Ninho Alto, 1ª versão (reprovada pelo Tiago)
- v2 29/10/2026 — Ninho Alto v2 com pesquisa e 3D (aprovada como "melhorando")
