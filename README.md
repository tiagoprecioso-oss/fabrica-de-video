# Fábrica de vídeos — Radar Pop

Sistema de agentes do Claude que transforma uma pauta em um Short/Reels pronto (1080×1920, com trilha e final em loop).

## O fluxo

```
Radar Pop (pauta do dia)
   → pesquisador   pesquisa/<id>.md     dados + fontes + contas
   → roteirista    roteiros/<id>.md     roteiro em trechos, com loop
   → diretor       videos/<id>.json     modelo, blocos, câmera, selos
   → fabricar.sh   saida/<id>.mp4       render (Remotion)
   → revisor       revisoes/<id>.md     APROVADO ou CORRIGIR
   → Tiago aprova  → posta (ou agenda no Metricool)
```

Os agentes ficam em `.claude/agents/`. O formato dos vídeos e as regras de qualidade estão em `MODELOS.md`.

## Como usar

```bash
npm install                               # uma vez
npx remotion browser ensure               # uma vez (baixa o navegador de render)
./fabricar.sh videos/gta6-preco.json      # gera saida/gta6-preco.mp4
npx remotion studio src/index.jsx         # abre o editor visual para ajustar ao vivo
```

Pedido completo para o Claude Code, dentro desta pasta:
> Faça o vídeo da pauta "<título>": use o pesquisador, depois o roteirista, o diretor, renderize com ./fabricar.sh e passe pelo revisor. Corrija o que ele apontar e renderize de novo.

## Estrutura
- `src/` — modelos de vídeo (React/Remotion). `tema.js` = cores e fontes da marca.
- `videos/` — um JSON por vídeo.
- `tools/trilha.py` — trilha sintetizada que fecha no loop.
- `public/` — fontes e trilhas.
- `saida/` — vídeos prontos.

Requer Node 18+ e Python 3 com numpy.
