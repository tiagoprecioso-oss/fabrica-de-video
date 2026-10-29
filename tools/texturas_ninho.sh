#!/usr/bin/env bash
# Baixa as texturas e o HDRI CC0 da Poly Haven usados nas cenas da Ninho Alto → public/texturas/
# Uso: tools/texturas_ninho.sh   (as texturas já ficam no repositório; rode só para trocar ou atualizar)
set -euo pipefail
cd "$(dirname "$0")/.."
D=public/texturas; mkdir -p $D
python3 - "$D" <<'PY'
import json, sys, subprocess, os
get = lambda u: subprocess.run(['curl', '-sSL', '-A', 'fabrica-precioso', u], check=True, capture_output=True).stdout
D = sys.argv[1]
TEX = {'concrete_floor_01': '2k', 'grey_plaster': '1k'}   # laje e parede
MAPAS = {'Diffuse': 'diff', 'Rough': 'rough', 'nor_gl': 'nor'}
def baixa(url, dest):
    if not os.path.exists(dest): open(dest, 'wb').write(get(url))
    print(dest, os.path.getsize(dest) // 1024, 'KB')
for a, res in TEX.items():
    f = json.loads(get(f'https://api.polyhaven.com/files/{a}'))
    for k, nome in MAPAS.items():
        baixa(f[k][res]['jpg']['url'], f'{D}/{a}_{nome}.jpg')
h = json.loads(get('https://api.polyhaven.com/files/art_studio'))
baixa(h['hdri']['1k']['hdr']['url'], f'{D}/art_studio_1k.hdr')
PY
cat > $D/CREDITOS.md <<'MD'
# Texturas
Todas da [Poly Haven](https://polyhaven.com), licença **CC0** (domínio público, uso comercial livre, sem crédito obrigatório):
- `concrete_floor_01` (laje), `grey_plaster` (parede), HDRI `art_studio` (reflexos).
MD
