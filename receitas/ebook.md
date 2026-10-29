# Receita: ebook interativo + PDF (v2, 29/10/2026)

## Quando usar
Ebook ou material para vender/entregar (Hotmart, isca de e-mail, bônus de curso). **O produto principal é uma página interativa** (o leitor coloca os próprios números, simula, marca progresso); o PDF é a versão para imprimir.

## Entradas
- Tema, público e sumário (ex.: `docs/plano-funil.md`).
- Estilo do canal em `src/tema.js` (finanças: `grana`).

## Passos
0. **Pesquisa de produto e de referências ANTES de tudo** (regra 4 do CLAUDE.md): o que vende no nicho (Hotmart) e as melhores experiências interativas do tema. `python3 tools/referencias.py saida/ref/<produto> <urls>` → olhar as folhas → `pesquisa/<produto>-design.md` com padrões, o que evitar e a direção. Mostrar a direção e deixar o Felipe/Tiago escolher o estilo visual antes de construir.
1. **Pesquisa de dados** com fontes oficiais e data de referência — `pesquisa/<produto>.md` — agente: pesquisador. Marque o que mudar rápido (programas do governo, valores em julgamento) para o texto não cravar.
2. **Contas antes do texto**: todo exemplo numérico sai de um script — `produtos/<produto>/contas.py`. O texto copia os números do script, nunca o contrário.
3. **Texto** em `produtos/<produto>/texto.md` (frontmatter + `# ` por seção, `# Fase N · Título` para capítulos, blocos `:::tipo`) — agente: autor-de-ebook. Blocos disponíveis no topo de `tools/ebook.py`.
4. **Checagem** item por item contra a pesquisa, refazendo as contas — `checagem/<produto>.md` — agente: checador (de preferência outra sessão, que não escreveu o texto).
5. **Página interativa** em `produtos/<produto>/web/index.html` (um arquivo, sem `<html>/<head>`; carregar o skill `artifact-design` antes). A lógica de contas da página tem que ser a mesma do `contas.py`: rodar a página no Playwright e comparar os números com o script. Publicar com a ferramenta Artifact para revisão.
6. **PDF oficial** (vai para a Hotmart com Social DRM) — `python3 tools/extrair_arte.py produtos/<produto>/web/index.html produtos/<produto>/arte` e depois `python3 tools/ebook.py produtos/<produto>` → `<produto>.pdf` (A4), `<produto>-celular.pdf` (110×196 mm) e `previa.png`. Fontes: Archivo (OFL) em `public/fonts/`. Ilustrações em SVG feitas no próprio script (sem imagem de terceiros).
7. **Conferir as páginas**: renderizar todas as páginas em folhas de contato (pypdfium2) e olhar: linhas órfãs, título sozinho no pé, caixa cortada, página quase vazia.
8. **Compliance e revisor**, depois copywriter (página de venda) — e só o Tiago sobe na Hotmart.

## Pronto quando
- [ ] Todo número do texto aparece em `checagem/` como OK.
- [ ] Contas refeitas por `contas.py` batem com o texto.
- [ ] PDFs A4 e celular gerados por um comando, corpo ≥ 11 pt, sem páginas quebradas.
- [ ] Aviso educativo, data dos dados e lista de fontes no livro.

## Lições
- 29/10/2026 — **Sem fundo branco** (pedido do Felipe: cansa a vista). Fundo verde-sálvia #E7EFE3 e cartões #F1F6EE, na página e no PDF. No PDF, o fundo é pintado em cada página inteira (inclusive margens) pelo tools/ebook.py, antes de criar os campos. Campos de resposta levam uma linha de explicação em letra menor embaixo.
- 29/10/2026 — PDF "interativo" tem limite: links, campos e caixas funcionam nos leitores comuns; animação e contas automáticas não (JavaScript de PDF só no Adobe). Interatividade de verdade fica na página. Campos: o ebook.py escreve marcadores de texto invisíveis (QZ…ZQ) e o pdf_campos.py cria os campos onde eles estão. Cuidados: o marcador não pode ficar na mesma linha de outro texto (as letras se misturam na extração) e nenhuma regra de estilo pode aumentar a letra dele. Conferir preenchendo uma cópia de teste e renderizando com formulários (pypdfium2 init_forms).
- Testar se a marca d'água da Hotmart (Social DRM) mantém os campos preenchíveis antes de lançar.
- 29/10/2026 — PDF v2: linhas em branco entre blocos quebravam a grade das cartas (cada carta ia para uma coluna só). Agrupar blocos iguais seguidos ignorando parágrafos vazios. Páginas de cor de ponta a ponta usam `@page cheia{margin:0}`.
- 29/10/2026 — Referência que funcionou para o PDF: manual de jogo (página de personagens, mapa do jogo como sumário) + ebooks ilustrados do Dribbble (páginas de cor alternadas, número gigante como destaque).
- 29/10/2026 — Plano pessoal em PDF gerado no navegador: jsPDF 2.5.1 + html2canvas 1.4.1 (cdnjs, carregados só no clique) desenham folhas A4 escondidas com o visual da página. SVG com `var(--x)` não pinta como imagem: trocar pelas cores calculadas antes. No claude.ai o download só sai pela permissão `downloads`; fora dele, link de download normal.
- 29/10/2026 — Para o simulador ser didático: o leitor aposta antes de ver o placar, e cada mês é contado em 3 passos (juros, mínimos, sobra no alvo e o porquê). Nomes dos chefões têm gênero: guardar no dado (`fem`) para o texto não sair "o Sombra".
- 29/10/2026 — Fim do produto = começo do próximo: mostrar o mundo seguinte trancado e calcular com os números do leitor o que ele ganha lá (sem rendimento, para não virar recomendação de investimento).
- 29/10/2026 — **v1 reprovada pelo Felipe ("horrível")**: saiu sem pesquisa de referências e parecia relatório de banco (caixas empilhadas, tabelas, verde-planilha, chefões parados). A v2 foi feita depois de olhar Nicky Case, Spent, Habitica, Duolingo, undebt.it e os concorrentes da Hotmart (todos PDFs genéricos) → página interativa em desenho animado vibrante, em que o leitor joga antes de ler.
- 29/10/2026 — Simulador da página conferido contra `contas.py`: bateu centavo por centavo (17 meses / R$ 4.323,76 na Avalanche).
- 29/10/2026 — "Endividamento de 50,1%" é dívida total ÷ renda de 12 meses, não "renda comprometida" (essa é o comprometimento, 29%). Conferir a definição do indicador, não só o número.
- 29/10/2026 — Simulação "só pagando o mínimo" pode não terminar nunca (juros > mínimos): o script precisa tratar isso, e esse resultado é o argumento mais forte do livro.
- 29/10/2026 — `break-after:avoid` nos subtítulos e `orphans/widows` nos parágrafos resolveram as quebras feias do Chromium.
- 29/10/2026 — Rodapé com número de página: Chromium imprime em todas as páginas; a capa sai de um segundo PDF sem rodapé e as duas partes são unidas com pypdf.

## Histórico
- v5 29/10/2026 — PDF oficial interativo: mapa clicável (links para cada fase e "voltar ao mapa"), fichas e respostas preenchíveis, checklist de 90 dias com caixas de marcar (tools/pdf_campos.py roda sozinho no fim do tools/ebook.py).
- v4 29/10/2026 — PDF oficial redesenhado no visual da página (tools/ebook.py v2): arte extraída da página (tools/extrair_arte.py), Baloo 2 + Nunito, capa, mapa do jogo, aberturas de fase em página inteira de cor, cartas, extratos, Mundo 2.
- v3 29/10/2026 — simulador passo a passo com extrato e aposta; gancho para o próximo produto no fim (mundo seguinte trancado + cálculo com os números do leitor).
- v2 29/10/2026 — página interativa como produto principal; pesquisa de referências obrigatória antes do rascunho.
- v1 29/10/2026 — primeira versão (ebook "Chefões do cartão", Din no Chão).
