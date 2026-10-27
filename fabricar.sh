#!/usr/bin/env bash
# Renderiza um vídeo da fábrica a partir do JSON.
# Uso: ./fabricar.sh videos/gta6-preco.json
set -euo pipefail
JSON="$1"
ID=$(python3 -c "import json,sys;print(json.load(open('$JSON'))['id'])")
MODELO=$(python3 -c "import json,sys;print(json.load(open('$JSON')).get('modelo','DadoMedido'))")
python3 tools/trilha.py "$JSON"
python3 -c "import json;print(json.dumps({'video':json.load(open('$JSON'))}))" > "saida/$ID.props.json"
npx remotion render src/index.jsx "$MODELO" "saida/$ID.mp4" --props="saida/$ID.props.json" --concurrency=2 --log=error
echo "pronto: saida/$ID.mp4"
