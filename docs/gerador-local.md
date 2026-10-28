# Gerador de imagens e vídeos no PC do Tiago (RTX 3060)

Modelos abertos rodando na placa de vídeo, sem mensalidade. Só funciona no PC (a nuvem e o GitHub não têm placa de vídeo).

## O que a RTX 3060 aguenta
- RTX 3060 de mesa = 12 GB de memória de vídeo (a de notebook costuma ter 6 GB: conferir no app da NVIDIA).
- **Imagens:** FLUX.1 [schnell] em versão compacta (fp8): ~20–60 s por imagem em 12 GB. Licença Apache 2.0 (uso comercial permitido).
- **Vídeo curto:** Wan 2.1 de 1,3 bilhão de parâmetros (texto → vídeo, 480p, poucos segundos): roda em ~8 GB, alguns minutos por clipe. Licença Apache 2.0. Os modelos de vídeo grandes ficam lentos demais em 12 GB.
- Conferir a licença de cada modelo na página dele antes de usar em produto pago.

## Instalar (uma vez, ~30 min)
1. Baixe o **ComfyUI portátil para Windows (NVIDIA)** na página de releases do GitHub: github.com/comfyanonymous/ComfyUI/releases (arquivo `ComfyUI_windows_portable_nvidia.7z`).
2. Extraia com o 7-Zip numa pasta com uns 40 GB livres (ex.: `C:\ComfyUI`).
3. Rode `run_nvidia_gpu.bat`. O navegador abre em `http://127.0.0.1:8188`.
4. No ComfyUI: **Workflow → Browse Templates**. Escolha o modelo de imagem **Flux Schnell** (e, para vídeo, um de **Wan 2.1 1.3B**). O ComfyUI avisa quais arquivos faltam e baixa os modelos.
5. Teste: escreva o pedido (em inglês funciona melhor) e clique em **Run**. As imagens vão para `ComfyUI\output`.

## Como entra no estúdio
- O agente **ilustrador** escreve os pedidos (prompts) no estilo de cada canal e a lista de imagens que cada produto precisa (`produtos/<produto>/imagens.md`).
- O Tiago roda no ComfyUI e sobe as imagens no Drive (ou no repositório, em `produtos/<produto>/img/`).
- Quando o PC estiver ligado ao Claude (app desktop, "Link to this computer"), o Claude pode rodar o ComfyUI direto pela API local (`127.0.0.1:8188`).

## Regras
- Nada de personagens, logos ou artistas conhecidos no pedido; nada de pessoas reais.
- Imagem realista de pessoa gerada por IA em vídeo do YouTube: marcar "conteúdo alterado ou sintético" ao publicar.
- IA é apoio visual; o conteúdo principal continua sendo dado original e roteiro do estúdio.
