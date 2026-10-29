# Instruções para o Claude neste repositório

Este repositório é a **fábrica** do Tiago Precioso: uma indústria de conteúdo, marcas e produtos digitais que deve rodar o mais automática possível. Leia o `README.md` (estado atual e próximos passos) antes de começar.

## Regras
1. **Tudo sai da fábrica.** Toda peça (vídeo, imagem 3D, rótulo, site, ebook) é gerada por um script, JSON ou arquivo-fonte deste repositório, que refaz o mesmo resultado. Nada de trabalho manual solto.
2. **Siga as receitas.** Antes de produzir, abra `receitas/README.md` e a receita do que vai fazer. Ao terminar, atualize a receita (passos, lições, versão) — agente `receiteiro`. Sem receita? Escreva uma a partir de `receitas/_modelo.md`.
3. **Use os agentes** de `.claude/agents/` (organograma em `ESTUDIO.md`). Se faltar uma função, crie o agente novo e registre no `ESTUDIO.md`. **Sempre**, em toda etapa (pedido do Felipe, 29/10: é assim que ele testa e aprimora os agentes): a sessão principal coordena e entrega, mas o trabalho de cada função é feito pelo agente dela. Ao fim, anote em `ESTUDIO.md` (seção Desempenho dos agentes) o que cada um fez bem ou mal, para aprimorar.
4. **Pesquisa antes do primeiro rascunho** em qualquer coisa visual (`receitas/pesquisa-de-referencias.md`). Fugir do visual genérico de IA. **Todo produto novo** (ebook, curso, página, ferramenta) começa pela pesquisa do que comprovadamente dá certo no nicho (o que mais vende, o que os melhores fazem), registrada em `pesquisa/` antes de qualquer rascunho. Pedido do Felipe, 29/10: o ebook v1 saiu sem pesquisa e ficou feio.
5. **Imersivo, interativo e animado sempre que der.** Se o produto pode ser uma página viva (rolagem animada, calculadora, fichas que se preenchem, progresso salvo), ele é; o PDF fica como versão secundária para baixar ou imprimir.
6. **Blender é do Tiago.** Qualquer coisa que precise de Blender (render, física, cena 3D) fica para o PC do Tiago (RTX 3060). Em outras contas/sessões, não mexer nas cenas de `blender/`; deixar o pedido anotado no `COMECE-AQUI.md`.
7. **Números com fonte**; finanças é educativo; direitos conforme `docs/direitos.md`.
8. **Nada é postado, vendido ou enviado** sem aprovação do Tiago.
9. **Antes de encerrar**: commit e push em `main` com tudo o que foi produzido, repositório limpo (`git status` vazio), o `README.md` atualizado se o estado do estúdio mudou, e uma nota do dia em `segundo-cerebro/Diário/<data>.md` (o pacote do segundo cérebro do Tiago sai de `tools/segundo_cerebro.sh`).

## Atalhos
- Vídeo: `videos/<id>.json` → push → GitHub renderiza → `tools/esperar_render.sh <id>`.
- 3D: `tools/instalar_blender.sh` (nuvem) · cenas em `blender/` · fotos da Ninho Alto: `tools/pecas_ninho.sh`.
- Conferir página: `node tools/conferir_pagina.js <arquivo.html> <pasta>` · Referências: `node tools/referencias.js <pasta> <urls>`.
- Commits: `git config user.name "Claude"` e `user.email "noreply@anthropic.com"`.
