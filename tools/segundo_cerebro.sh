#!/usr/bin/env bash
# Monta a pasta do "segundo cérebro" do Tiago (notas em Markdown, estilo Obsidian) a partir do repositório.
# Uso: tools/segundo_cerebro.sh [destino]   (padrão: saida/segundo-cerebro) → pasta + .zip
# Notas próprias (índice, decisões, diário) ficam em segundo-cerebro/; o resto é copiado dos docs e receitas.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="${1:-saida/segundo-cerebro}"; D="$DEST/Fabrica - Precioso Productions"
rm -rf "$D"; mkdir -p "$D/Receitas" "$D/Marcas"
cp -r segundo-cerebro/. "$D/"
for f in receitas/*.md; do [ "$(basename "$f")" = "_modelo.md" ] || cp "$f" "$D/Receitas/"; done
mv "$D/Receitas/README.md" "$D/Receitas/00 Indice das receitas.md"
cp portfolio/ninho-alto/marca.md "$D/Marcas/Ninho Alto Coffee.md"
cp docs/plano-precioso.md "$D/Plano Precioso Productions.md"
cp docs/plano-funil.md "$D/Plano do funil (ebook e minicurso).md"
cp docs/direitos.md "$D/Direitos - o que podemos usar.md"
cp docs/pesquisa-monetizacao.md "$D/Pesquisa de monetizacao.md"
cp README.md "$D/Estado da fabrica (README).md"
cp CLAUDE.md "$D/Regras para o Claude (CLAUDE.md).md"
(cd "$DEST" && rm -f segundo-cerebro.zip && zip -qr segundo-cerebro.zip "Fabrica - Precioso Productions")
echo "pronto: $DEST/segundo-cerebro.zip"
