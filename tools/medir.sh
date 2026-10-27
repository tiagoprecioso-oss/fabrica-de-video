#!/usr/bin/env bash
# Mede o ritmo de um vídeo com o Sharingan (cortes, câmera, áudio) e,
# se houver referência, compara com ela.
# Uso: tools/medir.sh saida/<id>.mp4 [referencias/<nome>.json]
# Gera saida/<id>-medidas.md (e a análise completa em saida/<id>-sharingan/).
set -uo pipefail
VID="$1"; REF="${2:-}"
ID=$(basename "$VID" .mp4)
DIR="$(dirname "$VID")/$ID-sharingan"
AQUI="$(cd "$(dirname "$0")" && pwd)"
python3 -I "$AQUI/sharingan/scripts/sharingan.py" analyze "$VID" -o "$DIR" --title "$ID" > "$DIR.log" 2>&1 || { tail -20 "$DIR.log"; exit 1; }
python3 - "$DIR/analysis.json" "$ID" > "$(dirname "$VID")/$ID-medidas.md" <<'EOF'
import json, sys
a = json.load(open(sys.argv[1])); e = a["edit"]["stats"]; au = a.get("audio", {})
moves = {}
for s in a.get("camera", {}).get("shots", []):
    moves[s.get("move", "?")] = moves.get(s.get("move", "?"), 0) + 1
print(f"# Medidas: {sys.argv[2]}\n")
print(f"- Duração: {a['source']['duration_s']:.1f} s")
print(f"- Cenas: {e['shot_count']} · duração média {e['asl_s']} s · {e['cuts_per_min']} cortes/min")
print(f"- Câmera: " + ", ".join(f"{k} ×{v}" for k, v in moves.items()))
print(f"- Áudio: {au.get('class')} · {au.get('tempo_bpm')} BPM · cortes na batida: {au.get('cuts', {}).get('verdict', 'n/a')}")
print("\nMeta da fábrica (virais de games, out/2026): troca de cena a cada 1–3 s.")
EOF
if [ -n "$REF" ]; then
  echo -e "\n## Comparação com $(basename "$REF" .json)\n" >> "$(dirname "$VID")/$ID-medidas.md"
  python3 -I "$AQUI/sharingan/scripts/sharingan.py" compare "$REF" "$DIR/analysis.json" >> "$(dirname "$VID")/$ID-medidas.md" 2>&1 || true
fi
cat "$(dirname "$VID")/$ID-medidas.md"
