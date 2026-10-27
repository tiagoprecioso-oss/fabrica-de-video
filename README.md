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

## Para quem vai rodar no próprio Claude (amigos e colaboradores)

1. **Faça um fork** deste repositório no GitHub (botão *Fork*) e clone o seu fork.
2. Instale: `npm install` e `npx remotion browser ensure` (precisa de Node 18+ e Python 3 com `numpy`).
3. Teste: `./fabricar.sh videos/gta6-preco.json` deve gerar `saida/gta6-preco.mp4`.
4. Abra a pasta no **Claude Code**. Os agentes de `.claude/agents/` (pesquisador, roteirista, diretor, revisor) são carregados sozinhos.
5. Peça um vídeo: *"Faça um vídeo sobre <assunto> usando o fluxo do README"*.
6. Para ver e ajustar o visual ao vivo: `npx remotion studio src/index.jsx`.

Onde mexer para aperfeiçoar:
- **Novo estilo visual:** `src/tema.js` (cores e fontes) + um fundo em `src/componentes/Fundos.jsx`.
- **Novo tipo de bloco/formato:** `src/componentes/Blocos2.jsx` e registrar em `src/DadoMedido.jsx`; documente em `MODELOS.md`.
- **Comportamento dos agentes:** `.claude/agents/*.md`.

Mandou uma melhoria? Abra um *pull request* para este repositório. A automação diária do canal usa a branch `main`, então mudanças só entram depois de revisadas.

O **Radar Pop** (painel de pautas) está em `radar-pop/`: cada pessoa publica o seu no próprio claude.ai e cria as tarefas agendadas com os prompts de lá. Veja `radar-pop/LEIA-ME.md`.

## Estrutura
- `src/` — modelos de vídeo (React/Remotion). `tema.js` = cores e fontes da marca.
- `videos/` — um JSON por vídeo.
- `tools/trilha.py` — trilha sintetizada que fecha no loop.
- `public/` — fontes e trilhas.
- `saida/` — vídeos prontos.

Requer Node 18+ e Python 3 com numpy.
