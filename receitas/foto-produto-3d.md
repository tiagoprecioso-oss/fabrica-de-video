# Receita: fotos de produto em 3D (v2, 29/10/2026)

## Quando usar
Uma marca (nossa, de cliente ou conceito) precisa de fotos de produto e não temos produto físico, câmera nem estúdio.

## Entradas
- Manual da marca (cores, direção de foto) e a arte da embalagem/rótulo gerada por script.

## Passos
1. **Rótulo/arte** gerado por script em PNG (ex.: `python3 tools/rotulo_ninho.py` → `saida/ninho/rotulo_*.png`).
2. **Cena** em `blender/<marca>_produto.py`, copiando a estrutura de `blender/ninho_produto.py`:
   - argumentos `--cena --lote --res --proporcao --amostras --frames --saida --gpu`;
   - produto modelado por código (bmesh) com UV de projeção frontal para o rótulo;
   - superfície e parede com **texturas CC0 escaneadas da Poly Haven** (`tools/texturas_ninho.sh` → `public/texturas/`, versionadas) e HDRI de estúdio fraco para reflexos; procedural só como reserva;
   - papel: deslocamento Voronoi fraco (vincos) + ruído fino de fibra no relevo e na rugosidade;
   - luz de "janela" (área grande de lado) + rebate fraco + recorte atrás; AgX; denoiser ligado;
   - câmera 50–70 mm, profundidade de campo leve (f/3–4).
3. **Rascunho** rápido: `blender -b -P blender/<cena>.py -- --cena hero --res 800 --amostras 24 --saida saida/<marca>/teste` e olhe. Ajuste luz/escala/câmera (1–3 rodadas).
4. **Final**: um script que roda tudo, como `tools/pecas_ninho.sh` (rótulos → renders → JPG recortados em `portfolio/<marca>/img/`).
   - Nuvem do Claude (2 núcleos): ~8–10 min por imagem final. Rode com `nohup ... &` (processo em segundo plano morre quando o comando do terminal acaba).
   - GitHub: workflow `Renderizar peças 3D` roda sozinho quando a cena muda.
   - **PC do Tiago (melhor caminho):** copiar `blender/`, `public/texturas/`, `portfolio/<marca>/rotulos/` e `tools/render_ninho_pc.bat` (como `RENDERIZAR.bat`) para uma pasta do PC e dar duplo clique. RTX 3060 + Blender 5.2: hero 2400 px/256 amostras ≈ 55 s; pacote ≈ 40 s; as 5 imagens em ~4 min. Os PNG voltam pela ponte e o recorte para o site roda na nuvem.
5. Olhe cada imagem final antes de usar. Imagem fraca não entra.
6. Commit dos scripts e dos JPG em `portfolio/<marca>/img/`; atualizar esta receita.

## Pronto quando
- [ ] Produto parece real (escala certa, sombra de contato, rótulo legível).
- [ ] Cores batem com o manual.
- [ ] Um comando refaz todas as imagens do zero.

## Lições
- 29/10 — Grãos do tamanho errado parecem botões de chocolate: **escala real** (grão ≈ 1 cm para pacote de 15 cm).
- 29/10 — Luz forte demais + AgX deixa tudo branco e lava o rótulo: chave ~280 W, mundo 0,08, parede cinza-quente média.
- 29/10 — Linhas finas no rótulo somem no render: engrossar (2,6 px a 1200 px de largura) e escurecer as cores.
- 29/10 — Macro de grãos ficou "bombom" (liso e brilhante demais). Falta: rugosidade maior (0,55), variação de cor por grão, fenda mais funda, textura de superfície. Ainda não resolvido.
- 29/10 — O `pip install bpy` baixou a 35 KB/s; o Blender oficial (download.blender.org) baixa em 1 min. Usar o oficial: `/opt/blender/blender-4.2.3-linux-x64/blender`.
- 29/10 — Pacote pequeno no quadro: recortar no script de conversão ou aproximar a câmera (lente 85 mm).

- 29/10 — Render na nuvem (CPU, poucas amostras, materiais procedurais) foi achado **fraco** pelo Tiago. Com texturas reais + vincos + GPU a v2 ficou muito melhor. Procedural puro dá cara de "3D de computador".
- 29/10 — Grão: fenda estreita e funda (atributo `fenda` na malha) com a película clara dentro, cor por grão (Object Info › Random), relevo celular. O macro melhorou mas ainda parece CG (cor acinzentada, liso de perto): **não entra no site** até ficar bom. Próximo: fotogrametria/escaneado CC0 de grão, se existir, ou subdivisão + displacement real.
- 29/10 — Rótulo em PNG versionado em `portfolio/<marca>/rotulos/` para o PC não precisar de Python.

## Histórico
- v1 29/10/2026 — Ninho Alto (hero + 3 pacotes aprovados; macro reprovado)
- v2 29/10/2026 — texturas CC0 reais, papel com vincos, grãos novos, render na RTX 3060 do Tiago (hero + 3 pacotes trocados no site; macro ainda fora)
