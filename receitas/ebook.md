# Receita: ebook ilustrado em PDF (v1, 29/10/2026)

## Quando usar
Ebook ou material para vender/entregar (Hotmart, isca de e-mail, bônus de curso): texto com dados, fichas para imprimir, ilustrações próprias.

## Entradas
- Tema, público e sumário (ex.: `docs/plano-funil.md`).
- Estilo do canal em `src/tema.js` (finanças: `grana`).

## Passos
1. **Pesquisa** com fontes oficiais e data de referência — `pesquisa/<produto>.md` — agente: pesquisador. Marque o que mudar rápido (programas do governo, valores em julgamento) para o texto não cravar.
2. **Contas antes do texto**: todo exemplo numérico sai de um script — `produtos/<produto>/contas.py`. O texto copia os números do script, nunca o contrário.
3. **Texto** em `produtos/<produto>/texto.md` (frontmatter + `# ` por seção, `# Fase N · Título` para capítulos, blocos `:::tipo`) — agente: autor-de-ebook. Blocos disponíveis no topo de `tools/ebook.py`.
4. **Checagem** item por item contra a pesquisa, refazendo as contas — `checagem/<produto>.md` — agente: checador (de preferência outra sessão, que não escreveu o texto).
5. **Diagramação** — `python3 tools/ebook.py produtos/<produto>` → `<produto>.pdf` (A4), `<produto>-celular.pdf` (110×196 mm) e `previa.png`. Fontes: Archivo (OFL) em `public/fonts/`. Ilustrações em SVG feitas no próprio script (sem imagem de terceiros).
6. **Conferir as páginas**: renderizar todas as páginas em folhas de contato (pypdfium2) e olhar: linhas órfãs, título sozinho no pé, caixa cortada, página quase vazia.
7. **Compliance e revisor**, depois copywriter (página de venda) — e só o Tiago sobe na Hotmart.

## Pronto quando
- [ ] Todo número do texto aparece em `checagem/` como OK.
- [ ] Contas refeitas por `contas.py` batem com o texto.
- [ ] PDFs A4 e celular gerados por um comando, corpo ≥ 11 pt, sem páginas quebradas.
- [ ] Aviso educativo, data dos dados e lista de fontes no livro.

## Lições
- 29/10/2026 — "Endividamento de 50,1%" é dívida total ÷ renda de 12 meses, não "renda comprometida" (essa é o comprometimento, 29%). Conferir a definição do indicador, não só o número.
- 29/10/2026 — Simulação "só pagando o mínimo" pode não terminar nunca (juros > mínimos): o script precisa tratar isso, e esse resultado é o argumento mais forte do livro.
- 29/10/2026 — `break-after:avoid` nos subtítulos e `orphans/widows` nos parágrafos resolveram as quebras feias do Chromium.
- 29/10/2026 — Rodapé com número de página: Chromium imprime em todas as páginas; a capa sai de um segundo PDF sem rodapé e as duas partes são unidas com pypdf.

## Histórico
- v1 29/10/2026 — primeira versão (ebook "Chefões do cartão", Din no Chão).
