# Radar Pop — painel de pautas

O Radar Pop é o painel onde as pautas do dia aparecem (gancho, roteiro, legenda, hashtags, fontes) e onde os vídeos prontos da fábrica chegam para aprovar e baixar. Ele roda como um *artifact* do claude.ai, com banco de dados próprio.

Cada pessoa monta o seu: as pautas e os vídeos ficam na conta de quem publicou.

## Montar o seu (no claude.ai, ~5 minutos)

1. **Publicar o painel.** Numa conversa do claude.ai, anexe o arquivo `radar-pop.html` desta pasta e peça:
   > Publique este arquivo como um artifact com as capabilities `db`, `downloads` e `assets`. Depois me diga a URL do artifact.

   Guarde a URL (formato `https://claude.ai/artifact/...`).

2. **Criar a tarefa das pautas.** Na mesma conversa, peça:
   > Crie uma tarefa agendada diária às 6h47 (horário de Brasília) com o prompt do arquivo `AGENTE-PAUTAS.md`, trocando `<URL_DO_RADAR_POP>` pela URL do meu artifact.

3. **(Opcional) Criar a tarefa da fábrica.** Para o vídeo diário automático, faça antes o fork do repositório `fabrica-de-video` e conecte seu GitHub ao Claude (Configurações → Conectores) com o app do Claude instalado no seu fork. Depois peça:
   > Crie uma tarefa agendada diária às 8h23 com o prompt de `AGENTE-FABRICA.md`, trocando `<URL_DO_RADAR_POP>` pela URL do meu artifact e `<DONO_DO_REPO>` pelo meu usuário do GitHub.

No dia seguinte, abra o artifact: as pautas aparecem de manhã e, se a fábrica estiver ligada, o vídeo do dia aparece dentro da pauta com player e botão de baixar.

## Como usar o painel
- **Ver roteiro:** abre o roteiro, a legenda, as hashtags e as fontes da pauta, com botão de copiar.
- **Status:** mude para *Em produção*, *Postada* ou *Descartada*. O agente de pautas não repete assuntos postados ou descartados.
- **Gerar vídeo:** abre o estúdio. Você coloca prints ou clipes em cada cena e grava o vídeo vertical direto no navegador.
- **Baixar vídeo:** aparece quando a fábrica já entregou o vídeo daquela pauta.
