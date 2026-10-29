# Receita: motion 3D com física (v0 — rascunho, ainda não testada)

## Quando usar
Vídeos curtos de produto que impressionam: grãos saindo do pacote e rolando na mesa, café caindo no copo, produto girando. Servem de hero do site (loop de 6–8 s), Reels e anúncios.

## Entradas
- Manual da marca (seção motion: velocidade, câmera, duração) e a cena de foto do produto pronta (`receitas/foto-produto-3d.md`), para reaproveitar modelos, luz e materiais.

## Passos (plano)
1. Reaproveite a cena de foto (`blender/<marca>_produto.py`) e crie a cena de motion `blender/<marca>_motion.py` com os mesmos argumentos + `--frames`.
2. **Grãos rolando** (corpo rígido): pacote tombado como colisor "passivo"; 150–300 grãos "ativos" nascendo dentro da boca do pacote; atrito 0,6, quique 0,2; `bpy.ops.ptcache.bake_all()` antes de renderizar.
3. **Café caindo** (líquido falso, leve): fio = curva com espessura animada + ruído; superfície do café = disco que sobe dentro do copo com material de líquido escuro (IOR 1,33, rugosidade baixa) e espuma (crema) de ruído. Mantaflow só se o PC aguentar.
4. Câmera: movimento lento e único por plano (travelling 5–10 cm ou órbita de 10–15°), lente 50–85 mm, foco no ponto de ação.
5. Prévia na nuvem: `--res 540 --amostras 16 --frames 1-48` só para ver o movimento.
6. Final no PC do Tiago com GPU (`--gpu`), 1080×1920 (Reels) e 1920×1080 (site), 30 fps; juntar com ffmpeg:
   `ffmpeg -framerate 30 -i saida/<marca>/motion_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 portfolio/<marca>/video/<nome>.mp4`
7. Para o site: versão leve (`-crf 26`, sem áudio, `<video autoplay muted loop playsinline>`).
8. Para Reels: vira `midia` num JSON da fábrica (`videos/<id>.json`) com trilha do compositor.

## Pronto quando
- [ ] Física convincente (nada atravessa nada, os grãos param de verdade).
- [ ] Loop sem salto quando for hero do site.
- [ ] Um comando refaz o vídeo.

## Lições
- (preencher no primeiro teste)

## Histórico
- v0 29/10/2026 — plano escrito, ainda não testado
