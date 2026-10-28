# Comece aqui (Tiago, Felipe e Lucca)

Este repositório é o estúdio inteiro: a fábrica de vídeos, os 22 agentes, o Radar Pop, o painel Chão da Fábrica e os planos. Estado em 27/out/2026.

## Abrir no seu computador
1. Instale o Claude Code e o Git. Para renderizar localmente: Node 18+ e Python 3 com `numpy`.
2. `git clone https://github.com/tiagoprecioso-oss/fabrica-de-video` e abra a pasta no Claude Code. Os 22 agentes de `.claude/agents/` carregam sozinhos.
3. Peça, por exemplo: *"Faça o próximo vídeo de finanças seguindo o ESTUDIO.md"* ou *"Escreva o ebook Chefões do cartão com o autor-de-ebook e o diagramador"*.
4. Não precisa renderizar no seu PC: todo JSON novo em `videos/` que chega na `main` é renderizado pelo GitHub Actions e vira uma release com o `.mp4`.

Felipe e Lucca: façam um **fork** (ou peçam ao Tiago acesso de colaborador) e mandem melhorias por *pull request*. A automação diária usa a `main`.

## O que tem aqui
| Arquivo | O que é |
|---|---|
| `ESTUDIO.md` | Organograma: 22 agentes em 6 departamentos e as linhas de produção |
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
