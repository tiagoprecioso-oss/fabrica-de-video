# Instruções para o Claude neste repositório

Este repositório é a **fábrica** do Tiago Precioso: uma indústria de conteúdo, marcas e produtos digitais que deve rodar o mais automática possível. Leia o `README.md` (estado atual e próximos passos) antes de começar.

## Regras
1. **Tudo sai da fábrica.** Toda peça (vídeo, imagem 3D, rótulo, site, ebook) é gerada por um script, JSON ou arquivo-fonte deste repositório, que refaz o mesmo resultado. Nada de trabalho manual solto.
2. **Siga as receitas.** Antes de produzir, abra `receitas/README.md` e a receita do que vai fazer. Ao terminar, atualize a receita (passos, lições, versão) — agente `receiteiro`. Sem receita? Escreva uma a partir de `receitas/_modelo.md`.
3. **Use os agentes** de `.claude/agents/` (organograma em `ESTUDIO.md`). Se faltar uma função, crie o agente novo e registre no `ESTUDIO.md`.
4. **Pesquisa antes do primeiro rascunho** em qualquer coisa visual (`receitas/pesquisa-de-referencias.md`). Fugir do visual genérico de IA.
5. **Números com fonte**; finanças é educativo; direitos conforme `docs/direitos.md`.
6. **Nada é postado, vendido ou enviado** sem aprovação do Tiago.
7. **Antes de encerrar**: commit e push em `main` com tudo o que foi produzido, repositório limpo (`git status` vazio), o `README.md` atualizado se o estado do estúdio mudou, e uma nota do dia em `segundo-cerebro/Diário/<data>.md` (o pacote do segundo cérebro do Tiago sai de `tools/segundo_cerebro.sh`).

## Atalhos
- Vídeo: `videos/<id>.json` → push → GitHub renderiza → `tools/esperar_render.sh <id>`.
- 3D: `tools/instalar_blender.sh` (nuvem) · cenas em `blender/` · fotos da Ninho Alto: `tools/pecas_ninho.sh`.
- Conferir página: `node tools/conferir_pagina.js <arquivo.html> <pasta>` · Referências: `node tools/referencias.js <pasta> <urls>`.
- Commits: `git config user.name "Claude"` e `user.email "noreply@anthropic.com"`.
