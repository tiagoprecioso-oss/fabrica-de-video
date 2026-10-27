#!/usr/bin/env bash
# Espera o GitHub Actions renderizar um vídeo e baixa o resultado para saida/.
# Uso: tools/esperar_render.sh <id> [commit]   (commit padrão: HEAD)
# Sai com 0 e os arquivos saida/<id>.mp4 e saida/<id>-revisao.jpg baixados;
# sai com 2 e o fim do log se o render falhar; 3 se passar de 30 min.
set -uo pipefail
ID="$1"; SHA=$(git rev-parse "${2:-HEAD}"); CURTO=${SHA:0:7}
REPO=$(git remote get-url origin | sed -E 's#.*github.com[/:]([^/]+/[^/.]+)(\.git)?$#\1#')
mkdir -p saida
for i in $(seq 1 60); do
  corpo=$(gh api "repos/$REPO/releases/tags/$ID" --jq .body 2>/dev/null || true)
  if [[ "$corpo" == *"$CURTO"* ]]; then
    for a in $(gh api "repos/$REPO/releases/tags/$ID" --jq '.assets[].id'); do
      nome=$(gh api "repos/$REPO/releases/assets/$a" --jq .name)
      gh api -H "Accept: application/octet-stream" "repos/$REPO/releases/assets/$a" > "saida/$nome"
    done
    echo "pronto: saida/$ID.mp4 e saida/$ID-revisao.jpg"; exit 0
  fi
  run=$(gh api "repos/$REPO/actions/runs?head_sha=$SHA" --jq '.workflow_runs[0] | "\(.id) \(.status) \(.conclusion)"' 2>/dev/null || true)
  if [[ "$run" == *"completed failure"* || "$run" == *"completed cancelled"* ]]; then
    rid=${run%% *}
    job=$(gh api "repos/$REPO/actions/runs/$rid/jobs" --jq '.jobs[0].id')
    echo "render falhou (run $rid). Fim do log:"
    gh api "repos/$REPO/actions/jobs/$job/logs" | grep -v '^\s*$' | tail -40
    exit 2
  fi
  sleep 30
done
echo "tempo esgotado esperando o render de $ID"; exit 3
