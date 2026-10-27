# Como gravar gameplay para a fábrica

Jogo atual: **Fortnite** (a Epic permite monetizar; ver `docs/direitos.md`).

## O que gravar
- 3 a 5 minutos no total, em trechos de ~30 s.
- Dirigindo carros, planando/paraquedas, correndo, escalando, construindo. Para pautas de GTA, dirigindo.
- Personagem/carro **no centro da tela** e câmera sem girar muito: o vídeo vertical aproveita só o centro
  (tela cheia ≈ 1/3 central da largura; dividida ≈ 2/3).
- Gravar **ao vivo** (o replay da Carreira redesenha a partida e perde qualidade).
- Interface reduzida: Configurações → Interface do jogo → HUD (desligar feed de eliminações, desafios, mensagens).
- Música do jogo no zero, chat de voz desligado. Sem skins de parceria, sem danças com música licenciada, sem menus.

## NVIDIA app (PC)
- Alt + Z → Configurações → Captura de vídeo: resolução do jogo (1080p/1440p), 60 fps, 25–30 Mbps, formato **H.264**, microfone desligado.
- Alt + F9 grava/para. Alt + F10 salva os últimos minutos (Replay Instantâneo).
- Arquivos em Vídeos\Fortnite.

## Entregar
Subir numa pasta do Google Drive (ex.: "gameplay fortnite") e avisar o Claude. Ele corta os trechos,
converte para `public/gameplay/<jogo>-<cena>.mp4` (1080p, H.264, sem áudio) e usa no campo `"gameplay"` do JSON.
