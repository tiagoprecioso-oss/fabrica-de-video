"""Rótulos da marca conceito Ninho Alto (mapas topográficos por lote). Lê nomes, cores, altitudes e sementes de portfolio/ninho-alto/marca.json.
Uso: python3 tools/rotulo_ninho.py  → saida/ninho/rotulo_<lote>.png (texturas para o Blender e imagens para o site)
"""
import os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, 'public', 'fonts')
SAIDA = os.path.join(RAIZ, 'saida', 'ninho'); os.makedirs(SAIDA, exist_ok=True)

import json
MARCA = json.load(open(os.path.join(RAIZ, 'portfolio', 'ninho-alto', 'marca.json'), encoding='utf-8'))
_COR = {c['token']: c['hex'] for c in MARCA['cores']['neutras'] + MARCA['cores']['lotes']}
rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
PAPEL = rgb(_COR['paper']); TINTA = rgb(_COR['ink'])
LOTES = [dict(id=l['id'], nome=l['nome'], cor=rgb(_COR[l['cor']]), alt=f"{l['alt_m']:,} m", proc=l['processo'],
              var=l['variedade'], notas=l['notas'], semente=l['semente']) for l in MARCA['lotes']]

def fonte(nome, tam, peso=None):
    f = ImageFont.truetype(os.path.join(FONTES, nome), tam)
    if peso:
        try: f.set_variation_by_name(peso)
        except Exception: pass
    return f

def relevo(semente, n=400):
    rng = np.random.default_rng(semente)
    y, x = np.mgrid[0:1:n * 1j, 0:1:n * 1j]
    z = np.zeros_like(x)
    for _ in range(9):
        cx, cy = rng.uniform(.1, .9, 2); s = rng.uniform(.08, .25); h = rng.uniform(.4, 1)
        z += h * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s))
    pico = np.unravel_index(z.argmax(), z.shape)
    return x, y, z, (x[pico], y[pico])

def mapa(lote, w, h):
    x, y, z, (px, py) = relevo(lote['semente'])
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off')
    fig.patch.set_alpha(0)
    c = tuple(v / 255 for v in lote['cor'])
    ax.contour(x, y, z, levels=22, colors=[c], linewidths=2.6)
    ax.plot([px], [py], 'o', ms=9, color=tuple(v / 255 for v in TINTA))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    tmp = os.path.join(SAIDA, '_mapa.png'); fig.savefig(tmp, transparent=True); plt.close(fig)
    return Image.open(tmp).convert('RGBA'), (px, py)

def rotulo(lote, W=1200, H=1600):
    im = Image.new('RGB', (W, H), PAPEL); d = ImageDraw.Draw(im)
    m = 90
    # cabeçalho
    d.text((m, m), 'NINHO ALTO', font=fonte('HankenGrotesk.ttf', 54, 'SemiBold'), fill=TINTA)
    d.text((W - m, m + 14), 'MINAS GERAIS · BRAZIL', font=fonte('IBMPlexMono-Regular.ttf', 26), fill=TINTA, anchor='ra')
    d.line((m, m + 92, W - m, m + 92), fill=TINTA, width=2)
    # mapa topográfico
    mw, mh = W - 2 * m, 760
    mp, (px, py) = mapa(lote, mw, mh)
    im.paste(mp, (m, m + 130), mp)
    ax, ay = m + px * mw, m + 130 + (1 - py) * mh
    f = fonte('IBMPlexMono-Medium.ttf', 26)
    d.text((ax + 22, ay - 16), lote['alt'], font=f, fill=TINTA)
    # nome e ficha
    y0 = m + 130 + mh + 40
    d.text((m, y0), lote['nome'], font=fonte('HankenGrotesk.ttf', 84, 'Medium'), fill=TINTA)
    d.text((m, y0 + 110), lote['notas'], font=fonte('HankenGrotesk.ttf', 34, 'Regular'), fill=TINTA)
    fm = fonte('IBMPlexMono-Regular.ttf', 28)
    linhas = [('PROCESS', lote['proc']), ('VARIETY', lote['var']), ('ALTITUDE', lote['alt'])]
    for i, (k, v) in enumerate(linhas):
        yy = y0 + 190 + i * 46
        d.text((m, yy), k, font=fm, fill=TINTA); d.text((m + 220, yy), v, font=fm, fill=TINTA)
    # rodapé
    d.rectangle((0, H - 110, W, H), fill=lote['cor'])
    d.text((m, H - 72), 'WHOLE BEAN · 340 g / 12 oz', font=fonte('IBMPlexMono-Medium.ttf', 28), fill=PAPEL)
    d.text((W - m, H - 72), 'CONCEPT', font=fonte('IBMPlexMono-Medium.ttf', 28), fill=PAPEL, anchor='ra')
    out = os.path.join(SAIDA, f"rotulo_{lote['id']}.png"); im.save(out)
    rep = os.path.join(RAIZ, 'portfolio', 'ninho-alto', 'rotulos'); os.makedirs(rep, exist_ok=True)
    im.save(os.path.join(rep, f"rotulo_{lote['id']}.png"), optimize=True)  # cópia versionada para o Blender no PC
    return out

if __name__ == '__main__':
    for l in LOTES: print(rotulo(l))
    os.remove(os.path.join(SAIDA, '_mapa.png'))
