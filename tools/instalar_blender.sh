#!/usr/bin/env bash
# Instala o Blender oficial 4.2 LTS na nuvem do Claude (ou em qualquer Linux) em ~1 min.
# Uso: tools/instalar_blender.sh   → /opt/blender/blender-4.2.3-linux-x64/blender
set -euo pipefail
D=/opt/blender; B=$D/blender-4.2.3-linux-x64/blender
[ -x "$B" ] && { "$B" --version | head -1; exit 0; }
mkdir -p $D && cd $D
curl -sSL -o b.tar.xz https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz
tar xf b.tar.xz && rm b.tar.xz
"$B" --version | head -1
