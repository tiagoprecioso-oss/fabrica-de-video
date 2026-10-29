# Fábrica — Precioso Productions

**Novo por aqui (ou conversa nova com o Claude)? Leia esta página inteira, depois [CLAUDE.md](CLAUDE.md) e [receitas/](receitas/README.md).** O organograma dos 27 agentes está em [ESTUDIO.md](ESTUDIO.md).

A fábrica é uma **indústria de conteúdo, marcas e produtos digitais** o mais automática possível. Regra número 1: **tudo sai da fábrica** — toda peça é gerada por script, JSON ou arquivo deste repositório. Regra número 2: **tudo que dá certo vira receita** em `receitas/`, e a receita melhora a cada uso.

## Estado em 29/10/2026

| Linha | O que é | Estado |
|---|---|---|
| **Precioso Productions** (serviço) | Estúdio de vídeo, marca, site e 3D para clientes no Brasil e no exterior (dólar/euro) | Montando o portfólio. 1ª marca vitrine: **Ninho Alto Coffee** (fictícia, em inglês): manual, rótulos topográficos, fotos 3D no Blender e site v2 publicados. Plano: `docs/plano-precioso.md` |
| **Produtos** | Ebook "Chefões do cartão" → minicurso (Hotmart); depois kit de agentes da fábrica | Funil desenhado (`docs/plano-funil.md`), ebook ainda não escrito |
| **Din no Chão** (finanças) | Canal de Shorts que puxa os produtos | Estilo `grana` pronto, 1º vídeo feito |
| **Canal de cultura pop** | Laboratório de formatos (sem meta de receita) | Vídeo diário automático (tarefa às 08:23), aprovação no Radar Pop |

### Próximos passos
1. **Ninho Alto:** manual completo como design system → vídeo 3D dos grãos rolando do pacote (Blender, física) → site v3 com o vídeo no topo → 3 Reels e 2 anúncios → projeto no Behance.
2. **Precioso Productions:** marca, site e Instagram do estúdio; perfis no Behance, Contra e Upwork.
3. **Produtos:** escrever e diagramar o ebook; página de venda; Hotmart.
4. Pendências do Tiago: liberar os links no menu Compartilhar; contador (exportação de serviço); conectar a pasta da fábrica no app Claude para computador, para o Claude usar o Blender do PC (RTX 3060) em motion.

### Como começar uma conversa nova com o Claude
- **Melhor jeito:** app Claude para computador → conectar a pasta da fábrica (clone deste repositório). Assim o Claude roda o Blender e o render no PC do Tiago.
- Primeira mensagem sugerida: *"Leia o README, o CLAUDE.md e as receitas da fábrica e continue de onde paramos: <próximo passo>."*

### Onde está cada coisa
| Pasta / arquivo | O que tem |
|---|---|
| `receitas/` | Passo a passo de tudo que já deu certo (vídeo curto, marca, site, foto 3D, motion 3D, pesquisa de referências) |
| `portfolio/<marca>/` | Manual (`marca.md`), site (`site.html`), imagens (`img/`) de cada marca |
| `blender/` | Cenas 3D por código (`ninho_produto.py`, `cena_cartao.py`) |
| `tools/` | Ferramentas: render, rótulos, peças 3D, conferir página, referências, instalar Blender |
| `videos/`, `pesquisa/`, `roteiros/`, `revisoes/` | Uma linha por vídeo do canal |
| `docs/` | Planos (Precioso, funil), direitos, monetização, Blender |
| `.claude/agents/` | Os 27 agentes |

### Páginas vivas (claude.ai do Tiago, privadas até compartilhar)
- Radar Pop (pautas e aprovação de vídeos): https://claude.ai/artifact/LasVjXDtUwVj9qAkA5KZis
- Ninho Alto Coffee (site conceito): https://claude.ai/artifact/WhrQ8VnGzQKWuXbuPGEfmt
- Chão da Fábrica: https://claude.ai/artifact/RTfocgFhiAuJ45xtALqbfP
- Plano do funil: https://claude.ai/artifact/R2NRFYjELs4opAFzEJJv7G

## Automações no GitHub
- **Renderizar vídeos:** todo `videos/*.json` novo na `main` vira release com `.mp4` e folha de revisão (~3 min).
- **Renderizar peças 3D:** quando uma cena em `blender/ninho_*.py` ou o gerador de rótulos muda, renderiza as fotos 3D e publica na release `pecas-ninho-alto`.

---

# Fábrica de vídeos (detalhes técnicos)

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

## Render automático no GitHub
Todo JSON novo ou alterado em `videos/` que chega na `main` é renderizado pelo GitHub Actions (`.github/workflows/renderizar.yml`) em ~3 minutos. O resultado vira uma *release* com o nome do vídeo, contendo o `.mp4` e a `-revisao.jpg` (folha com um quadro por legenda). Para baixar daqui: `tools/esperar_render.sh <id>`. Também dá pra disparar à mão na aba **Actions → Renderizar vídeos → Run workflow**.

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

## Gameplay, direitos e medição
- **Gameplay:** camada `"gameplay"` (tela cheia ou dividida) em `MODELOS.md`. Clipes em `public/gameplay/`; como gravar em `docs/gravar-gameplay.md`.
- **Direitos:** o que pode e o que não pode (música e vídeo) em `docs/direitos.md`. Resumo: trilha nossa, Fortnite sim (com aviso da Epic), GTA sem imagens do jogo.
- **Medição:** `tools/medir.sh saida/<id>.mp4` mede cenas, cortes/min, câmera e áudio com o Sharingan (`tools/sharingan`, licença MIT). Precisa de `pip install opencv-python-headless`.
- **Pesquisa de formato:** `docs/analise-canais-dark.md`.

## Estrutura
- `src/` — modelos de vídeo (React/Remotion). `tema.js` = cores e fontes da marca.
- `videos/` — um JSON por vídeo.
- `tools/trilha.py` — trilha sintetizada que fecha no loop.
- `public/` — fontes e trilhas.
- `saida/` — vídeos prontos.
- `docs/` — análise de canais, direitos, como gravar gameplay.

Requer Node 18+ e Python 3 com numpy.
