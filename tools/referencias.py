"""Versão em Python do tools/referencias.js (para ambientes onde só o Playwright do Python tem navegador).
Tira prints de sites de referência (topo + duas roladas, desktop e celular) e monta folhas de contato.
Uso: python3 tools/referencias.py <pasta-saida> <url1> <url2> ...
Saída: <pasta>/<site>_*.png e <pasta>/folha_<n>.jpg (4 sites por folha)
"""
import re, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

def nome(u):
    return re.sub(r'_+$', '', re.sub(r'[/.?=&#:]', '_', re.sub(r'https?://(www\.)?', '', u)))[:60]

def main(pasta, sites):
    d = Path(pasta); d.mkdir(parents=True, exist_ok=True); feitos = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for u in sites:
            n = nome(u); arqs = []
            try:
                pg = b.new_page(viewport={'width': 1440, 'height': 900})
                pg.goto(u, wait_until='domcontentloaded', timeout=35000); pg.wait_for_timeout(4500)
                for i, y in enumerate((0, 1100, 2600)):
                    pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(1500)
                    a = d / f'{n}_{i}.png'; pg.screenshot(path=str(a)); arqs.append(a)
                cel = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
                cel.goto(u, wait_until='domcontentloaded', timeout=35000); cel.wait_for_timeout(3500)
                a = d / f'{n}_cel.png'; cel.screenshot(path=str(a)); arqs.append(a)
                feitos.append((u, arqs)); print('ok', u)
            except Exception as e:
                print('falhou', u, str(e)[:120])
        b.close()
    for k in range(0, len(feitos), 4):
        lote = feitos[k:k + 4]; W, H, CW = 480, 300, 140
        tela = Image.new('RGB', (W * 3 + CW + 50, (H + 34) * len(lote) + 10), (235, 235, 235))
        from PIL import ImageDraw
        dr = ImageDraw.Draw(tela)
        for r, (u, arqs) in enumerate(lote):
            y = 10 + r * (H + 34); dr.text((10, y), u[:150], fill=(0, 0, 0))
            for c, a in enumerate(arqs[:3]):
                im = Image.open(a).convert('RGB').resize((W, H)); tela.paste(im, (10 + c * (W + 10), y + 16))
            im = Image.open(arqs[3]).convert('RGB'); im = im.resize((CW, int(CW * im.height / im.width))).crop((0, 0, CW, H))
            tela.paste(im, (10 + 3 * (W + 10), y + 16))
        tela.save(d / f'folha_{k // 4 + 1}.jpg', quality=85); print('folha', d / f'folha_{k // 4 + 1}.jpg')

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
