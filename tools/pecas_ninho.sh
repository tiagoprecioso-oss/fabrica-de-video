#!/usr/bin/env bash
# Fábrica da marca Ninho Alto: rótulos → fotos 3D (Blender) → imagens do site em portfolio/ninho-alto/img.
# Uso: tools/pecas_ninho.sh [qualidade]   qualidade: rascunho | final (padrão final)
# BLENDER=/caminho/do/blender  (padrão: blender no PATH). No PC com placa NVIDIA: GPU=1 tools/pecas_ninho.sh
set -euo pipefail
cd "$(dirname "$0")/.."
B="${BLENDER:-blender}"; Q="${1:-final}"; G=""; [ "${GPU:-0}" = "1" ] && G="--gpu"
if [ "$Q" = "rascunho" ]; then R=0.5; A=24; else R=1; A=80; fi
r() { python3 -c "print(int($1*$R))"; }
python3 tools/rotulo_ninho.py
"$B" -b -P blender/ninho_produto.py -- --cena hero --res "$(r 1800)" --amostras $A $G --saida saida/ninho/hero
for l in reserve sunrise night; do
  "$B" -b -P blender/ninho_produto.py -- --cena pacote --lote $l --res "$(r 1000)" --proporcao 4:5 --amostras $A $G --saida saida/ninho/pacote_$l
done
# cena "graos" (macro) ainda em ajuste: não entra no site
mkdir -p portfolio/ninho-alto/img
python3 - <<'PY'
from PIL import Image; import glob, os
for f in glob.glob('saida/ninho/*.png'):
    if os.path.basename(f).startswith('graos'): continue
    n = os.path.basename(f)[:-4]
    if n.startswith('_'): continue
    im = Image.open(f).convert('RGB')
    if n.startswith('rotulo'): im = im.resize((900, 1200), Image.LANCZOS)
    if n.startswith('pacote'):  # enquadra o pacote (4:5) para os cards do site
        w, h = im.size; cw, ch = int(w * .68), int(w * .68 * 1.25); cx, cy = int(w * .51), int(h * .52)
        im = im.crop((cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2))
    im.save(f'portfolio/ninho-alto/img/{n}.jpg', quality=84, optimize=True, progressive=True)
    if n == 'hero':  # recorte do lado direito para a seção de origem
        w, h = im.size; im.crop((int(w * .52), int(h * .08), w, int(h * .92))).save('portfolio/ninho-alto/img/origem.jpg', quality=84, optimize=True)
    print('img', n)
PY
