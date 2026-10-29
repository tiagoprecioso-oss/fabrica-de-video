# Receita: criar uma marca (v2, 29/10/2026)

## Quando usar
"Crie uma marca para X" — marca conceito para o portfólio, marca de cliente ou marca de um produto nosso.

## Entradas
- Segmento, público, país e idioma, faixa de preço. Para cliente: briefing respondido.

## Passos
1. **Pesquisa de referências** (`receitas/pesquisa-de-referencias.md`): 6–10 marcas líderes do segmento.
2. **Nome**: 5 opções; busque cada uma ("<nome> <segmento>") e descarte as que já existem no segmento. Para marca fictícia, prefira palavra inventada ou combinação rara.
3. **Conceito** em 3 linhas: o que vende, para quem, a promessa (1 frase com um dado concreto).
4. **Assinatura visual**: **uma** ideia gráfica que só essa marca teria, tirada do mundo do produto (Ninho Alto: mapa topográfico da encosta de cada lote). Ela tem que ser gerável por código.
5. **Fonte única** em `portfolio/<marca>/marca.json` (cores claro/escuro, tipos e escala, espaço, logo, produtos, foto, motion, voz). Nenhum script ou página guarda cor, nome ou preço próprio: todos leem o JSON.
6. **Manual como design system**, gerado do JSON por `tools/manual_<marca>.py` (modelo: `tools/manual_ninho.py`): `manual.html` (artifact), `tokens.css` e `logo/` com o wordmark **em curvas** (fontTools) e versões clara/escura. Inclui tabela de contraste WCAG calculada dos tokens. Conferir com `node tools/conferir_pagina.js` e publicar com as imagens em `files`.
7. **Resumo** em `portfolio/<marca>/marca.md`:
   - conceito, promessa, voz (com 2 exemplos de frase);
   - wordmark/logo e regras de uso (tamanho mínimo, área de respiro, fundos permitidos);
   - cores com hex (neutros + 1 cor por produto/linha), tipos (no máximo 2 famílias, com arquivo em `public/fonts/`);
   - direção de foto (luz, superfície, enquadramento) e de motion (velocidade, câmera, duração);
   - produtos com dados; lista de entregas com checkbox.
8. **Gerador da assinatura visual** em `tools/<algo>_<marca>.py` (ex.: `tools/rotulo_ninho.py`), lendo cores e textos de um só lugar.
9. **Fotos 3D** (`receitas/foto-produto-3d.md`) e **site** (`receitas/site.md`).
10. Se for fictícia: toda peça leva "Concept project — fictional brand by Precioso Productions". Nunca imitar marca real.
11. Commit e atualizar esta receita.

## Pronto quando
- [ ] Nome checado, conceito e promessa escritos, assinatura visual gerada por script.
- [ ] Manual com cores, tipos, logo, foto, motion e voz.
- [ ] `marca.json` existe e o manual, os tokens, o logo em curvas e a assinatura visual são gerados dele.
- [ ] Contraste conferido nos dois temas; logo testado em todos os fundos permitidos.
- [ ] Toda peça seguinte cita o manual como fonte (nenhum valor inventado na hora).

## Lições
- 29/10 — A 1ª identidade da Ninho Alto (azulejos, Syne, grão sorrindo) foi feita antes da pesquisa e caiu no genérico. O manual precisa existir **antes** do site e dos vídeos.
- 29/10 — O manual v1 era curto demais (sem regras de logo, foto e motion) e o site saiu com inconsistências. Seguir a lista do passo 5 inteira.

- 29/10 — O `logo.svg` da v1 (sol, montanha, Syne) continuava no repositório depois da troca de identidade. Ao refazer a marca, apagar os arquivos antigos e listar o que foi aposentado no manual.
- 29/10 — Cor e lote escritos à mão em cada script divergem (rótulo usava um papel, o site outro). Com o `marca.json` como fonte única isso acabou.
- 29/10 — `tools/referencias.js` não abre todo site (Cloudflare, túnel bloqueado, página que só carrega com rolagem). Pegar 6–8 URLs e aceitar perder algumas.

## Histórico
- v1 29/10/2026 — Ninho Alto Coffee
- v2 29/10/2026 — fonte única `marca.json` e manual como design system gerado por script (Ninho Alto)
