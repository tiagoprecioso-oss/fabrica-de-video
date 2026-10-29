# Receita: vídeo curto de dados (v3, 29/10/2026)

## Quando usar
Short/Reels/TikTok de 25–45 s a partir de uma pauta (canal de cultura pop, Din no Chão, ou vídeos para marcas).

## Entradas
- Pauta do Radar Pop (título, gancho, ângulo) ou briefing da marca.

## Passos
1. **Pauta**: no Radar Pop, coleção `pautas`, status "nova", de hoje ou ontem, sem `video`, maior `potencial`. Modelo pela tabela de `MODELOS.md`; varie modelo e estilo em relação aos últimos `videos/`.
2. **Pesquisa** → `pesquisa/<id>.md` (agente pesquisador): tabela com fonte por número, contas em Python, comparação em reais quando houver dado brasileiro, dúvidas.
3. **Roteiro** → `roteiros/<id>.md` (roteirista): 8–10 trechos, gancho no 1º, final que emenda no início (loop), legenda do post e hashtags.
4. **Direção** → `videos/<id>.json` (diretor): modelo, estilo, blocos sem buracos, câmeras alternadas, `batidas = round(duracao/0.577)`. Validar: `python3 -c "import json;json.load(open('videos/<id>.json'))"`.
5. **Commit e push** em `main` (pesquisa, roteiros, videos) → o GitHub renderiza (~3 min).
6. **Baixar**: `tools/esperar_render.sh <id>` → `saida/<id>.mp4` e `saida/<id>-revisao.jpg`.
7. **Revisão** (revisor): olhar a folha, conferir cada número contra a fonte, loop, direitos; `tools/medir.sh saida/<id>.mp4`; escrever `revisoes/<id>.md` e commit. Até 3 rodadas.
8. **Entrega**: subir o mp4 no Radar Pop (Artifact `asset: true`) e atualizar a pauta (video, video_id, modelo, estilo, roteiro, legenda, hashtags, fontes) sem mudar o status.
9. **Limpeza**: `git checkout -- tools/sharingan` (o medir.sh gera cache) e apagar `saida/<id>-medidas.md` e `saida/<id>-sharingan/`.

## Pronto quando
- [ ] Todo número na tela tem fonte e bate; legendas em até 2 linhas; último quadro só fundo; frase final emenda no gancho.
- [ ] Revisão APROVADO commitada e pauta atualizada no Radar Pop.

## Lições
- 29/10 — Número divergente entre fontes: use a formulação que vale para todas ("menos de US$ 15 mi", "mais de 90%").
- 29/10 — O medir.sh suja o repositório (cache .pyc e pastas em saida/): limpar antes de encerrar (passo 9).
- 28/10 — Legenda de abertura longa quebra em 3 linhas: no máximo ~55 caracteres por legenda.

## Histórico
- v1 27/10 — GTA 6 (primeiros vídeos)
- v2 28/10 — render automático no GitHub
- v3 29/10 — Godzilla Minus One; limpeza e regra de números divergentes
