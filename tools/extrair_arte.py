"""Extrai os desenhos (SVG) de uma página interativa para arquivos, com as cores já resolvidas.
A página é a fonte única da arte: o PDF e as peças de divulgação usam estes arquivos.
Uso: python3 tools/extrair_arte.py produtos/chefoes-do-cartao/web/index.html produtos/chefoes-do-cartao/arte
Saída: <pasta>/<tipo>.svg para cada [data-boss] da página e <pasta>/din.svg
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

JS = r'''() => {
  const cs = getComputedStyle(document.documentElement), out = {};
  const limpa = (svg, corBoss) => {
    let x = svg.outerHTML.replace(/<g class="ko-olhos"[^>]*>[\s\S]*?<\/g>/g, '');
    if (corBoss) x = x.replace(/var\(--boss-cor\)/g, corBoss);
    x = x.replace(/var\((--[\w-]+)\)/g, (m, n) => cs.getPropertyValue(n).trim() || '#999');
    if (!x.includes('xmlns=')) x = x.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    return x.replace(/ aria-hidden="true"/, '');
  };
  document.querySelectorAll('[data-boss]').forEach(el => {
    const t = el.dataset.boss, svg = el.querySelector('svg'); if (!svg || out[t]) return;
    const g = svg.querySelector('[style*="--boss-cor"]');
    const cor = g ? cs.getPropertyValue(g.style.getPropertyValue('--boss-cor').replace(/var\(|\)/g, '').trim()).trim() : null;
    out[t] = limpa(svg, cor);
  });
  const din = document.querySelector('[data-din] svg'); if (din) out.din = limpa(din);
  return out;
}'''

def main(pagina, pasta):
    src = Path(pagina).read_text(encoding='utf-8')
    tmp = Path(pasta) / '_tmp.html'; Path(pasta).mkdir(parents=True, exist_ok=True)
    tmp.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>' + src + '</body></html>', encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(1200)
        arte = pg.evaluate(JS); b.close()
    tmp.unlink()
    for nome, svg in arte.items():
        (Path(pasta) / f'{nome}.svg').write_text(svg, encoding='utf-8')
    print(len(arte), 'desenhos:', ', '.join(sorted(arte)))

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
