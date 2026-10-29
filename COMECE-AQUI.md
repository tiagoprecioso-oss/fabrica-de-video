# Comece aqui (Tiago, Felipe e Lucca)

Este repositório é o estúdio inteiro: a fábrica, os 27 agentes, as receitas, o Radar Pop e os planos. **O estado atual e os próximos passos estão no [README.md](README.md)** (esta página guarda o guia de instalação).

## Abrir no seu computador
1. Instale o Claude Code e o Git. Para renderizar localmente: Node 18+ e Python 3 com `numpy`.
2. `git clone https://github.com/tiagoprecioso-oss/fabrica-de-video` e abra a pasta no Claude Code. Os agentes de `.claude/agents/` e as regras do `CLAUDE.md` carregam sozinhos.
3. Peça, por exemplo: *"Faça o próximo vídeo de finanças seguindo o ESTUDIO.md"* ou *"Escreva o ebook Chefões do cartão com o autor-de-ebook e o diagramador"*.
4. Não precisa renderizar no seu PC: todo JSON novo em `videos/` que chega na `main` é renderizado pelo GitHub Actions e vira uma release com o `.mp4`.

Felipe e Lucca: façam um **fork** (ou peçam ao Tiago acesso de colaborador) e mandem melhorias por *pull request*. A automação diária usa a `main`.

## Continuar de outra conta do Claude (ex.: Felipe, no PC dele)
Tudo o que o Claude precisa está neste repositório. O que **não** vem junto: a memória do Claude do Tiago, os documentos do Project dele e as páginas vivas (são da conta dele). Por isso:
1. **Acesso:** o Tiago adiciona a pessoa como colaboradora (GitHub → Settings → Collaborators) para ela poder dar push na `main`. Sem isso, fork + pull request.
2. **Claude:** abra o clone no Claude Code (ou conecte o repositório numa sessão do Claude na web) e mande:
   > Leia o README, o CLAUDE.md, o COMECE-AQUI.md e as receitas da fábrica e continue de onde paramos: <passo>.
3. **Páginas (site, manual, Radar Pop):** a outra conta não edita as do Tiago. Ela publica a própria cópia a partir dos arquivos daqui (`portfolio/ninho-alto/site.html`, `portfolio/ninho-alto/manual.html` com as imagens de `img/`, `radar-pop/radar-pop.html`).
4. **Blender:** o PC do Felipe não tem placa de vídeo, então lá não se renderiza. Para **fotos**, edite a cena (`blender/ninho_produto.py`) e dê push: o GitHub Actions (**Renderizar peças 3D**) renderiza sozinho e publica na release `pecas-ninho-alto` (pode subir as amostras no workflow, o limite é 6 h). Para **vídeo 3D com física**, só no PC do Tiago (RTX 3060), quando ele voltar a ter limite.
6. **Tarefas automáticas pausadas (29/10):** as das 06:47 (Radar Pop) e 08:23 (vídeo do dia) foram desligadas na conta do Tiago para poupar limite. Para religar, peça ao Claude do Tiago; ou monte as suas pelo `radar-pop/LEIA-ME.md`.
5. **Preferências do Tiago que valem sempre:** todo Short/Reels fecha em loop; legendas menores e corridas, sem som a cada palavra; comparação em reais quando houver dado brasileiro; formatos baseados no que já funciona comprovadamente; nada é postado sem o Tiago.

### Onde paramos (29/10/2026)
- **Ebook "Chefões do cartão" (Felipe, 29/10 à tarde):** v1 em PDF reprovada pelo Felipe (sem pesquisa, visual de relatório). **v2 = página interativa** em desenho animado (`produtos/chefoes-do-cartao/web/index.html`), feita depois de pesquisar referências (`pesquisa/chefoes-design.md`). Publicada na conta do Felipe: https://claude.ai/artifact/KDdJ7H4vUdiWpzFTvENSp2 . Próximo: revisão do Tiago, hospedagem para compradores, PDF no mesmo visual, página de venda.
- **Regras novas do Felipe (29/10), já no CLAUDE.md:** pesquisar antes de todo produto; tudo que puder ser imersivo, interativo e animado, é; Blender só no PC do Tiago (a cena `queda` não foi mexida).
- Feito hoje: manual da Ninho Alto como design system (`portfolio/ninho-alto/marca.json` → `python3 tools/manual_ninho.py`).
- **Feito (29/10, fim da tarde):** fotos 3D v2 renderizadas no PC do Tiago (itens 1–4 abaixo, menos o macro). **Próximo:** vídeo dos grãos caindo (item 5) e macro dos grãos. Plano original:
  1. Texturas CC0 escaneadas da Poly Haven (pedra, papel kraft, cerâmica) no lugar das procedurais.
  2. Pacote com simulação de tecido (dobras e amassados).
  3. Grãos novos: rugosidade ~0,55, fenda funda, cor variando por grão, escala real (≈1 cm).
  4. Render final com mais amostras e 2000 px+; comparar lado a lado com `portfolio/ninho-alto/img/hero.jpg` antes de trocar.
  5. **Em andamento (29/10, 15h40):** cena `--cena queda` em `blender/ninho_produto.py` (Reels 9:16, grãos soltos em camadas caindo na frente do pacote, física de corpo rígido, `--video` grava .mp4). A física já funciona (teste: `NINHO_DEBUG=1 blender -b -P blender/ninho_produto.py -- --cena queda --frames 1-60` imprime a altura dos grãos). Falta: alguns grãos voam para fora da laje (conferir quique/atrito e o espalhamento ao bater no pacote), ajustar o enquadramento (a lente 70 corta o pacote; testar 50 mm e câmera mais longe) e renderizar no PC do Tiago: `--cena queda --proporcao 9:16 --res 1080 --frames 1-240 --amostras 128 --gpu --video`. Depois:
  6. **Pedido do Tiago (29/10):** melhorar o **ambiente** dos renders 3D (cenário mais rico e com cara de estúdio de verdade: mais elementos de cena, luz mais trabalhada, profundidade) e fazer o **site da Ninho Alto bem imersivo, interativo e animado** (ex.: pacote 3D girando com o mouse/scroll, grãos caindo ligados à rolagem, transições entre os lotes). Pesquisar referências de sites imersivos de produto antes do primeiro rascunho (`receitas/pesquisa-de-referencias.md`) e seguir `receitas/site.md`.
  7. Antes era: vídeo dos grãos caindo do pacote com física (`receitas/motion-3d.md`), pacote girando para Reels, café sendo servido; site v3 usando `tokens.css`.

## O que tem aqui
| Arquivo | O que é |
|---|---|
| `ESTUDIO.md` | Organograma: 27 agentes em 7 departamentos e as linhas de produção |
| `receitas/` | Passo a passo de tudo que já deu certo |
| `MODELOS.md` | Formatos de vídeo, estilos, camada gameplay e o formato de finanças (chefão, extrato) |
| `docs/plano-funil.md` | Plano do funil de finanças (ebook "Chefões do cartão" → minicurso → WhatsApp) |
| `docs/pesquisa-monetizacao.md` | Como canais dark ganham dinheiro, aqui e em outros países |
| `docs/analise-canais-dark.md` | O que prende nos canais dark (gameplay, legenda dupla, cortes) |
| `docs/direitos.md` | O que pode e o que não pode usar (música, gameplay, GTA, Fortnite) |
| `docs/gravar-gameplay.md` | Como gravar o Fortnite com o app da NVIDIA |
| `radar-pop/` | O painel de pautas (cópia) e os prompts das tarefas diárias |
| `painel/chao-da-fabrica.html` | O painel lúdico do estúdio (abra no navegador) |
| `videos/` | Um JSON por vídeo; `saida/` guarda os renders locais |

## Páginas vivas (no claude.ai do Tiago)
- Radar Pop: https://claude.ai/artifact/LasVjXDtUwVj9qAkA5KZis
- Chão da Fábrica: https://claude.ai/artifact/RTfocgFhiAuJ45xtALqbfP
- Plano do funil: https://claude.ai/artifact/R2NRFYjELs4opAFzEJJv7G

São privadas: só abrem para quem o Tiago compartilhar (menu Compartilhar de cada página). Para ter as suas próprias, siga `radar-pop/LEIA-ME.md`.

## Tarefas automáticas (na conta do Tiago)
- 06:47: Radar Pop (o que está em alta no Brasil e nos EUA + 5 pautas, pelo menos 1 de finanças).
- 08:23: fábrica (pega a melhor pauta, faz o vídeo, renderiza no GitHub e deixa no Radar Pop para aprovar).
Nada é postado sem aprovação do Tiago.

## Próximos passos (decisões do Tiago)
1. Nome do canal de finanças e voz do narrador (grátis ou paga).
2. Criar as contas: canais (TikTok de finanças como conta comercial; de cultura pop como pessoal), Hotmart, MailerLite.
3. Gravar o Fortnite (`docs/gravar-gameplay.md`) e subir no Drive.
4. Escrever o ebook "Chefões do cartão" (autor-de-ebook → checador → diagramador).
