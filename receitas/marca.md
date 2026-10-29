# Receita: criar uma marca (v1, 29/10/2026)

## Quando usar
"Crie uma marca para X" — marca conceito para o portfólio, marca de cliente ou marca de um produto nosso.

## Entradas
- Segmento, público, país e idioma, faixa de preço. Para cliente: briefing respondido.

## Passos
1. **Pesquisa de referências** (`receitas/pesquisa-de-referencias.md`): 6–10 marcas líderes do segmento.
2. **Nome**: 5 opções; busque cada uma ("<nome> <segmento>") e descarte as que já existem no segmento. Para marca fictícia, prefira palavra inventada ou combinação rara.
3. **Conceito** em 3 linhas: o que vende, para quem, a promessa (1 frase com um dado concreto).
4. **Assinatura visual**: **uma** ideia gráfica que só essa marca teria, tirada do mundo do produto (Ninho Alto: mapa topográfico da encosta de cada lote). Ela tem que ser gerável por código.
5. **Manual** em `portfolio/<marca>/marca.md`:
   - conceito, promessa, voz (com 2 exemplos de frase);
   - wordmark/logo e regras de uso (tamanho mínimo, área de respiro, fundos permitidos);
   - cores com hex (neutros + 1 cor por produto/linha), tipos (no máximo 2 famílias, com arquivo em `public/fonts/`);
   - direção de foto (luz, superfície, enquadramento) e de motion (velocidade, câmera, duração);
   - produtos com dados; lista de entregas com checkbox.
6. **Gerador da assinatura visual** em `tools/<algo>_<marca>.py` (ex.: `tools/rotulo_ninho.py`), lendo cores e textos de um só lugar.
7. **Fotos 3D** (`receitas/foto-produto-3d.md`) e **site** (`receitas/site.md`).
8. Se for fictícia: toda peça leva "Concept project — fictional brand by Precioso Productions". Nunca imitar marca real.
9. Commit e atualizar esta receita.

## Pronto quando
- [ ] Nome checado, conceito e promessa escritos, assinatura visual gerada por script.
- [ ] Manual com cores, tipos, logo, foto, motion e voz.
- [ ] Toda peça seguinte cita o manual como fonte (nenhum valor inventado na hora).

## Lições
- 29/10 — A 1ª identidade da Ninho Alto (azulejos, Syne, grão sorrindo) foi feita antes da pesquisa e caiu no genérico. O manual precisa existir **antes** do site e dos vídeos.
- 29/10 — O manual v1 era curto demais (sem regras de logo, foto e motion) e o site saiu com inconsistências. Seguir a lista do passo 5 inteira.

## Histórico
- v1 29/10/2026 — Ninho Alto Coffee
