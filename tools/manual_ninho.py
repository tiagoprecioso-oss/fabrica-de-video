"""Manual da marca Ninho Alto como design system, gerado da fonte única portfolio/ninho-alto/marca.json.

Uso: python3 tools/manual_ninho.py
Gera em portfolio/ninho-alto/:
  - logo/ninho-alto-wordmark-ink.svg, -stone.svg   (wordmark em curvas, Hanken Grotesk 600, tracking do manual)
  - logo/ninho-alto-mark-ink.svg, -stone.svg        (marca de altitude: curvas de nível + ponto, para avatar e favicon)
  - tokens.css                                      (cores claro/escuro, tipos, escala, espaço)
  - manual.html                                     (o manual; formato artifact, imagens em img/)
"""
import html, json, math, os
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, 'portfolio', 'ninho-alto')
M = json.load(open(os.path.join(PASTA, 'marca.json'), encoding='utf-8'))
e = html.escape

CORES = {c['token']: c for c in M['cores']['neutras'] + M['cores']['lotes']}
def hexd(t, escuro=False): return CORES[t]['escuro' if escuro else 'hex']


# ---------- contraste (WCAG 2.1) ----------
def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)
def nota(c): return 'AAA' if c >= 7 else 'AA' if c >= 4.5 else 'AA large' if c >= 3 else 'Fails'


# ---------- wordmark em curvas ----------
def wordmark():
    f = TTFont(os.path.join(RAIZ, M['tipos']['sans']['arquivo']))
    f = instantiateVariableFont(f, {'wght': 600})
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f['hmtx']
    upm = f['head'].unitsPerEm; cap = f['OS/2'].sCapHeight
    track = float(M['logo']['tracking'].replace('em', '')) * upm
    x, partes = 0.0, []
    for ch in M['wordmark']:
        g = cmap[ord(ch)]
        if ch != ' ':
            pen = SVGPathPen(gs, ntos=lambda v: f'{v:.1f}'.rstrip('0').rstrip('.'))
            gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
            partes.append(pen.getCommands())
        x += hmtx[g][0] + track
    x -= track
    return ' '.join(partes), round(x), cap
WM, WM_W, WM_CAP = wordmark()

def svg_wordmark(cor, pad=0, titulo=True):
    vb = f'{-pad} {-WM_CAP - pad} {WM_W + 2 * pad} {WM_CAP + 2 * pad}'
    t = f'<title>{e(M["nome"])}</title>' if titulo else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{e(M["nome"])}">{t}<path fill="{cor}" d="{WM}"/></svg>'


# ---------- marca de altitude (curvas de nível + ponto) ----------
def marca(cor, fundo=None):
    rng = np.random.default_rng(1400)
    harm = [(i, rng.uniform(.05, .10) / i ** .3, rng.uniform(0, 2 * math.pi)) for i in (2, 3, 4)]
    th = np.linspace(0, 2 * math.pi, 121)
    # encosta: as curvas se apertam no lado de cima/direita, como num mapa de relevo íngreme
    cx, cy, n, linhas = 45.0, 57.0, 4, []
    for k in range(n):
        r = 38 * (1 - k / (n + .4))
        amp = 1 - k * .15
        rr = r * (1 + sum(a * amp * np.sin(i * th + p + k * .35) for i, a, p in harm))
        ox, oy = cx + k * 4.2, cy - k * 4.8
        pts = ' '.join(f'{ox + q * math.cos(t):.1f},{oy + q * math.sin(t):.1f}' for q, t in zip(rr, th))
        linhas.append(f'<polygon points="{pts}"/>')
    dx, dy = cx + n * 4.2, cy - n * 4.8
    bg = f'<rect width="100" height="100" fill="{fundo}"/>' if fundo else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Ninho Alto altitude mark">{bg}'
            f'<g fill="none" stroke="{cor}" stroke-width="2.4" stroke-linejoin="round">{"".join(linhas)}</g>'
            f'<circle cx="{dx:.2f}" cy="{dy:.2f}" r="4.6" fill="{cor}"/></svg>')


# ---------- tokens.css ----------
def tokens_css():
    t = M['tipos']
    claro = ''.join(f'  --{c}: {hexd(c)};\n' for c in CORES)
    escuro = ' '.join(f'--{c}: {hexd(c, True)};' for c in CORES)
    esc = ''.join(f'  --t-{s["nome"].lower()}: {s["peso"]} {s["px"]}px/{s["entrelinha"]} var(--f-{s["familia"]});\n' for s in t['escala'])
    sp = ''.join(f'  --s-{i + 1}: {v}px;\n' for i, v in enumerate(M['espaco']['passos']))
    return (f'/* Ninho Alto tokens v{M["versao"]} — gerado por tools/manual_ninho.py a partir de marca.json. Não editar à mão. */\n'
            f':root {{\n{claro}  --f-sans: "{t["sans"]["familia"]}", {t["sans"]["fallback"]};\n  --f-mono: "{t["mono"]["familia"]}", {t["mono"]["fallback"]};\n'
            f'{esc}{sp}  --max: {M["espaco"]["largura_max"]}px;\n  --radius: 0;\n}}\n'
            f'@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ {escuro} color-scheme: dark; }} }}\n'
            f':root[data-theme="dark"] {{ {escuro} color-scheme: dark; }}\n'), claro, escuro


# ---------- página ----------
CSS = r"""
/* Layout: a reference manual laid out like a lot sheet: sticky section index left, specimens at real size right; photography and labels carry the colour, the page stays stone and ink */
:root {
__CLARO__  --f-sans: "Hanken Grotesk", "Helvetica Neue", Arial, sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --invert-bg: var(--ink); --invert-fg: var(--stone);
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { __ESCURO__ color-scheme: dark; } }
:root[data-theme="dark"] { __ESCURO__ color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--stone); color: var(--ink); font-family: var(--f-sans); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--stone); }
img { display: block; max-width: 100%; height: auto; }
h1, h2, h3, p, ul, figure { margin: 0; }
ul { padding: 0; list-style: none; }
h1, h2, h3 { font-weight: 500; letter-spacing: -0.02em; line-height: 1.08; text-wrap: balance; }
a { color: inherit; }
:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px; }
.gutter { padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.wrap { max-width: 1320px; margin: 0 auto; }
.mono { font-family: var(--f-mono); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; font-variant-numeric: tabular-nums; }
.num { font-family: var(--f-mono); font-variant-numeric: tabular-nums; }
.muted { color: var(--muted); }

.notice { background: var(--invert-bg); color: var(--invert-fg); text-align: center; padding-block: 8px; }
header.top { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--stone); border-bottom: 1px solid var(--line); }
.bar { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding-block: 16px; }
.bar svg { height: 11px; width: auto; display: block; }
.bar svg path { fill: var(--ink); }

.hero { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 48px; align-items: end; padding-block: 56px 72px; }
.hero h1 { font-size: clamp(34px, 4.4vw, 60px); max-width: 13ch; margin-block: 14px 20px; }
.hero .lead { font-size: 20px; line-height: 1.45; max-width: 40ch; }
.hero .facts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px 24px; margin-top: 32px; border-top: 1px solid var(--line); padding-top: 16px; }
.hero .facts dt { margin-bottom: 2px; }
.hero .facts dd { margin: 0; }
.hero figure { background: var(--surface); }
.hero figure img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; }
@media (max-width: 860px) { .hero { grid-template-columns: 1fr; gap: 28px; padding-block: 32px 48px; } }

.layout { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 56px; padding-bottom: 96px; }
nav.index { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 72px); align-self: start; border-top: 1px solid var(--ink); padding-top: 12px; }
nav.index ol { list-style: none; margin: 10px 0 0; padding: 0; display: grid; gap: 6px; font-size: 14px; }
nav.index a { text-decoration: none; display: grid; grid-template-columns: 26px 1fr; }
nav.index a:hover { color: var(--muted); }
@media (max-width: 900px) {
  .layout { grid-template-columns: minmax(0, 1fr); gap: 32px; }
  nav.index { position: static; }
  nav.index ol { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
}

section.s { border-top: 1px solid var(--ink); padding-top: 14px; display: grid; gap: 28px; scroll-margin-top: 80px; }
section.s + section.s { margin-top: 88px; }
.shead { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 0 16px; align-items: baseline; }
.shead h2 { font-size: clamp(26px, 2.8vw, 38px); }
.shead p { grid-column: 2; margin-top: 12px; max-width: 62ch; color: var(--muted); }
@media (max-width: 560px) { .shead { grid-template-columns: 1fr; } .shead p { grid-column: 1; } }
h3 { font-size: 20px; letter-spacing: -0.01em; }
.sub { display: grid; gap: 14px; align-content: start; }
.cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px 32px; }
.cols3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }
@media (max-width: 700px) { .cols, .cols3 { grid-template-columns: minmax(0, 1fr); } }

table { width: 100%; border-collapse: collapse; font-size: 15px; }
th, td { text-align: left; vertical-align: top; padding: 10px 12px 10px 0; border-bottom: 1px solid var(--line); }
th { font-weight: 400; }
.tscroll { overflow-x: auto; }

.say { display: grid; gap: 10px; }
.say li { font-size: 20px; line-height: 1.4; padding-bottom: 10px; border-bottom: 1px solid var(--line); }
.say.no li { color: var(--muted); text-decoration: line-through; text-decoration-thickness: 1px; }

.stage { background: var(--paper); border: 1px solid var(--line); display: grid; place-items: center; padding: clamp(32px, 7vw, 88px) 24px; }
.stage svg { width: min(100%, 560px); height: auto; }
.stage svg path { fill: #1C1B19; }
.stage .mono { color: #69645C; }
.space svg { width: min(100%, 620px); }
.bgs { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }
.bgs figure { aspect-ratio: 3 / 2; display: grid; place-items: center; padding: 16px; border: 1px solid var(--line); }
.bgs figure svg { width: 100%; height: auto; }
.bgs figcaption { margin-top: 6px; }
.markrow { display: flex; gap: 20px; align-items: end; flex-wrap: wrap; }
.markrow svg { display: block; }
.avatar { border-radius: 50%; overflow: hidden; }
.donts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 32px; }
.donts li { padding: 8px 0; border-bottom: 1px solid var(--line); }
@media (max-width: 700px) { .donts { grid-template-columns: 1fr; } }

.sw { display: grid; grid-template-columns: 72px minmax(0, 1fr) auto; gap: 16px; align-items: center; padding-block: 12px; border-bottom: 1px solid var(--line); }
.chip { width: 72px; height: 48px; border: 1px solid var(--line); }
.sw .who { display: grid; gap: 2px; min-width: 0; }
.copy { font: inherit; font-family: var(--f-mono); font-size: 13px; background: none; border: 1px solid var(--line); color: var(--ink); padding: 6px 10px; cursor: pointer; font-variant-numeric: tabular-nums; }
.copy:hover { border-color: var(--ink); }
.lots { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.lot { color: #F4F2EC; padding: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; gap: 16px; }
.lot b { font-weight: 500; font-size: 22px; letter-spacing: -0.01em; }
.lot .copy { color: #F4F2EC; border-color: rgba(244, 242, 236, .5); align-self: start; }
@media (max-width: 700px) { .lots { grid-template-columns: 1fr; } .lot { min-height: 120px; } }

.spec { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); gap: 24px; padding: 24px 0; border-bottom: 1px solid var(--line); align-items: end; }
.spec .big { font-size: clamp(64px, 10vw, 120px); line-height: .9; letter-spacing: -0.03em; }
.spec .glyphs { font-size: 20px; line-height: 1.5; overflow-wrap: anywhere; }
@media (max-width: 700px) { .spec { grid-template-columns: 1fr; } }
.scale { display: grid; }
.scale .row { display: grid; grid-template-columns: 140px minmax(0, 1fr); gap: 16px; padding: 18px 0; border-bottom: 1px solid var(--line); align-items: baseline; }
.scale .sample { min-width: 0; overflow-wrap: anywhere; }
@media (max-width: 560px) { .scale .row { grid-template-columns: 1fr; gap: 6px; } }

.labels img { width: 100%; aspect-ratio: 3 / 4; object-fit: cover; border: 1px solid var(--line); }
.labels figcaption, .photos figcaption { margin-top: 8px; }
.photos img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; background: var(--surface); }
.rules { display: grid; }
.rules div { display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--line); }
@media (max-width: 560px) { .rules div { grid-template-columns: 1fr; gap: 2px; } }
.ease { height: 40px; position: relative; border-bottom: 1px solid var(--line); }
.ease span { position: absolute; left: 0; bottom: 0; width: 12px; height: 12px; border-radius: 50%; background: var(--ink); animation: dolly 6s cubic-bezier(.65, 0, .35, 1) infinite alternate; }
@keyframes dolly { to { left: calc(100% - 12px); } }
@media (prefers-reduced-motion: reduce) { .ease span { animation: none; left: 50%; } }

.demo { border: 1px solid var(--line); background: var(--stone); padding: 24px; display: grid; gap: 24px; }
.btn { display: inline-block; font: inherit; font-size: 14px; letter-spacing: .02em; padding: 12px 22px; border: 1px solid var(--ink); background: transparent; color: var(--ink); cursor: pointer; text-decoration: none; }
.btn.solid { background: var(--ink); color: var(--stone); }
.btn:hover { opacity: .85; }
.btnrow { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.card { display: grid; gap: 10px; max-width: 320px; }
.card .ph { background: var(--surface); }
.card .ph img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; }
.card .row { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.card h4 { margin: 0; font-weight: 500; font-size: 18px; display: flex; align-items: center; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.sheet { font-family: var(--f-mono); font-size: 13px; font-variant-numeric: tabular-nums; max-width: 420px; }
.sheet td, .sheet th { padding: 8px 12px 8px 0; }
.field { display: grid; gap: 6px; max-width: 420px; }
.field .in { display: flex; border: 1px solid var(--ink); }
.field input { flex: 1; min-width: 0; font: inherit; border: 0; padding: 12px; background: transparent; color: var(--ink); }
.field input::placeholder { color: var(--muted); }
.field button { border: 0; border-left: 1px solid var(--ink); }
.field .msg { min-height: 1.5em; font-size: 14px; }
.steps { display: grid; gap: 8px; }
.steps div { display: grid; grid-template-columns: 60px minmax(0, 1fr); gap: 16px; align-items: center; }
.steps i { display: block; height: 12px; background: var(--ink); }
footer { border-top: 1px solid var(--line); padding-block: 28px 40px; display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
"""

JS = r"""
document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', () => {
  const v = b.dataset.v, old = b.textContent;
  const done = () => { b.textContent = 'Copied'; setTimeout(() => b.textContent = old, 1200); };
  try {
    navigator.clipboard.writeText(v).then(done, () => sel(b));
  } catch (err) { sel(b); }
}));
function sel(b) { const r = document.createRange(); r.selectNodeContents(b); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
const f = document.getElementById('news');
f.addEventListener('submit', ev => {
  ev.preventDefault();
  const v = document.getElementById('email').value.trim(), m = document.getElementById('newsMsg');
  m.textContent = /.+@.+\..+/.test(v) ? 'Demo only: nothing was sent. In the store this subscribes you to harvest notes.' : 'Enter an email address like name@example.com.';
});
"""

def pagina(claro, escuro):
    L = {l['id']: l for l in M['lotes']}
    secs = [('concept', 'Concept'), ('voice', 'Voice'), ('logo', 'Logo'), ('color', 'Colour'), ('type', 'Type'),
            ('signature', 'Contour labels'), ('photo', 'Photography'), ('motion', 'Motion'), ('components', 'Components'),
            ('space', 'Space and grid'), ('files', 'Source files')]
    num = {k: f'{i + 1:02d}' for i, (k, _) in enumerate(secs)}
    def head(k, titulo, texto):
        return f'<div class="shead"><span class="mono">§ {num[k]}</span><h2>{e(titulo)}</h2><p>{texto}</p></div>'

    # contraste
    pares = [('ink', 'stone', 'Body text on page'), ('muted', 'stone', 'Captions on page'), ('ink', 'paper', 'Text on labels'),
             ('stone', 'ink', 'Notice bar'), ('paper', 'ochre', 'Band text, Sunrise'), ('paper', 'navy', 'Band text, Night'),
             ('paper', 'oxblood', 'Band text, Reserve'), ('ochre', 'stone', 'Ochre dot on page (non-text, needs 3:1)')]
    linhas_c = ''.join(f'<tr><td>{u}</td><td class="num">{hexd(a)} on {hexd(b)}</td><td class="num">{contraste(hexd(a), hexd(b)):.1f}:1</td><td>{'Passes' if 'non-text' in u and contraste(hexd(a), hexd(b)) >= 3 else nota(contraste(hexd(a), hexd(b)))}</td></tr>' for a, b, u in pares)

    sw = ''.join(f'<div class="sw"><span class="chip" style="background:var(--{c["token"]})"></span><span class="who"><span>{e(c["nome"])} <span class="mono muted">--{c["token"]}</span></span><span class="muted" style="font-size:14px">{e(c["uso"])} Dark: <span class="num">{c["escuro"]}</span></span></span><button class="copy" type="button" data-v="{c["hex"]}">{c["hex"]}</button></div>' for c in M['cores']['neutras'])
    lots = ''.join(f'<div class="lot" style="background:{c["hex"]}"><span class="mono">Lot colour · --{c["token"]}</span><span><b>{e(L[c["lote"]]["nome"])}</b><br><span class="num" style="font-size:14px">{L[c["lote"]]["alt_m"]:,} m · dark UI {c["escuro"]}</span></span><button class="copy" type="button" data-v="{c["hex"]}">{c["hex"]}</button></div>' for c in M['cores']['lotes'])

    t = M['tipos']
    escala = ''.join(f'<div class="row"><span class="mono muted">{s["nome"]} · <span class="num">{s["px"]}/{round(s["px"] * s["entrelinha"])}</span> · {s["peso"]}</span><span class="sample" style="font:{s["peso"]} {s["px"]}px/{s["entrelinha"]} var(--f-{s["familia"]});letter-spacing:{s["tracking"]};{"text-transform:uppercase;" if s.get("caixa_alta") else ""}">{e(s["exemplo"])}</span></div>' for s in t['escala'])

    fundos = ''
    for k in M['logo']['fundos_ok']:
        claro_fundo = lum(hexd(k)) > .3
        cor = hexd('ink') if claro_fundo else hexd('paper')
        fundos += f'<div><figure style="background:{hexd(k)}">{svg_wordmark(cor, titulo=False)}</figure><figcaption class="mono muted">{e(CORES[k]["nome"])} · {"Ink" if claro_fundo else "Paper"} wordmark</figcaption></div>'

    # diagrama de respiro: caixa H em volta do wordmark
    H = WM_CAP
    respiro = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-H - 40} {-2 * H - 40} {WM_W + 2 * H + 80} {3 * H + 80}" role="img" aria-label="Clear space equals cap height H on every side">'
               f'<rect x="{-H}" y="{-2 * H}" width="{WM_W + 2 * H}" height="{3 * H}" fill="none" stroke="#8C2622" stroke-width="22" stroke-dasharray="70 50"/>'
               f'<rect x="{-H}" y="{-H}" width="{H}" height="{H}" fill="#8C2622" fill-opacity=".14"/>'
               f'<text x="{-H / 2}" y="{-H / 2 + 105}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="300" fill="#8C2622">H</text>'
               f'<path fill="#1C1B19" d="{WM}"/></svg>')

    rules = lambda rs: ''.join(f'<div><span class="mono">{e(a)}</span><span>{e(b)}</span></div>' for a, b in rs)
    fatos = [('Origin', 'Mantiqueira, Minas Gerais'), ('Altitude', '1,150–1,400 m'), ('Roast', 'Mondays, on demand'), ('Ships', 'Within 72 hours')]
    fat = ''.join(f'<div><dt class="mono muted">{a}</dt><dd>{b}</dd></div>' for a, b in fatos)
    idx = ''.join(f'<li><a href="#{k}"><span class="num muted">{num[k]}</span>{n}</a></li>' for k, n in secs)
    sheet = ''.join(f'<tr><th class="muted">{a}</th><td>{b}</td></tr>' for a, b in [('PROCESS', L['night']['processo']), ('VARIETY', L['night']['variedade']), ('ALTITUDE', f'{L["night"]["alt_m"]:,} m'), ('ROAST', L['night']['torra']), ('PRICE', f'US$ {L["night"]["preco_usd"]} / 12 oz')])
    passos = ''.join(f'<div><span class="num muted">{v} px</span><i style="width:{v * 4}px;max-width:100%"></i></div>' for v in M['espaco']['passos'])
    arquivos = ''.join(f'<tr><td>{e(a)}</td><td class="num">{e(b)}</td><td class="num">{e(c)}</td></tr>' for a, b, c in M['pecas'])
    rot = ''.join(f'<figure><img src="img/rotulo_{l["id"]}.jpg" alt="{e(l["nome"])} label: contour map in {CORES[l["cor"]]["nome"].lower()} with the altitude dot at {l["alt_m"]:,} m" width="1200" height="1600"><figcaption class="mono muted">{e(l["nome"])} · seed {l["semente"]} · {l["alt_m"]:,} m</figcaption></figure>' for l in M['lotes'])
    fotos = ''.join(f'<figure><img src="img/pacote_{i}.jpg" alt="{e(L[i]["nome"])} bag on the stone slab, window light from the left" width="1000" height="1250"><figcaption class="mono muted">{e(L[i]["nome"])} · Blender render</figcaption></figure>' for i in ('reserve', 'sunrise', 'night'))

    return f"""<title>Ninho Alto Brand Manual</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS.replace('__CLARO__', claro).replace('__ESCURO__', escuro)}</style>

<p class="notice mono gutter">{e(M['aviso_conceito'])}</p>
<header class="top"><div class="wrap gutter bar">{svg_wordmark('#1C1B19')}<span class="mono muted">Brand manual · v{M['versao']} · Oct 2026</span></div></header>

<main>
<div class="wrap gutter hero">
  <div>
    <p class="mono muted">Brand manual and design system</p>
    <h1>{e(M['promessa'])}</h1>
    <p class="lead">{e(M['conceito'])}</p>
    <dl class="facts">{fat}</dl>
  </div>
  <figure><img src="img/hero.jpg" alt="Three Ninho Alto bags on a stone slab with coffee beans, lit from a window on the left" width="1600" height="900"></figure>
</div>

<div class="wrap gutter layout">
<nav class="index" aria-label="Sections"><span class="mono">Contents</span><ol>{idx}</ol></nav>
<div>

<section class="s" id="concept">{head('concept', 'Concept', 'What we sell, to whom, and the one promise every piece has to keep.')}
  <div class="cols">
    <div class="sub"><span class="mono muted">Promise</span><p style="font-size:26px;line-height:1.2;letter-spacing:-0.01em">{e(M['promessa'])}</p></div>
    <div class="sub"><span class="mono muted">Audience</span><p>{e(M['publico'])}</p><span class="mono muted">Rule</span><p>Lead with the product and a real number. If a sentence or an image could belong to any coffee brand, cut it.</p></div>
  </div>
</section>

<section class="s" id="voice">{head('voice', 'Voice', e(M['voz']['resumo']))}
  <div class="cols">
    <div class="sub"><span class="mono">Write like this</span><ul class="say">{''.join(f'<li>{e(x)}</li>' for x in M['voz']['faca'])}</ul></div>
    <div class="sub"><span class="mono">Never like this</span><ul class="say no">{''.join(f'<li>{e(x)}</li>' for x in M['voz']['evite'])}</ul></div>
  </div>
</section>

<section class="s" id="logo">{head('logo', 'Logo', 'The wordmark is the logo: NINHO ALTO in Hanken Grotesk SemiBold, capitals, tracked 0.32 em. It ships as outlined vector files, so it never depends on an installed font.')}
  <div class="stage">{svg_wordmark('#1C1B19')}</div>
  <div class="cols">
    <div class="sub"><h3>Clear space</h3><p class="muted">{e(M['logo']['respiro'])}</p><div class="stage space" style="padding:24px">{respiro}</div></div>
    <div class="sub"><h3>Minimum size</h3><p class="muted">Screen: <span class="num">{M['logo']['minimo_px']}</span> px wide. Print: <span class="num">{M['logo']['minimo_mm']}</span> mm wide. Below that, use the altitude mark.</p>
      <div class="stage" style="padding:32px 24px;justify-items:start"><div style="width:{M['logo']['minimo_px']}px">{svg_wordmark('#1C1B19', titulo=False)}</div><span class="mono muted" style="margin-top:10px">{M['logo']['minimo_px']} px</span></div></div>
  </div>
  <div class="sub"><h3>Backgrounds</h3><p class="muted">Ink wordmark on light grounds, Paper wordmark on dark grounds and lot colours. Over photos, only on a calm area of the slab or wall.</p><div class="bgs">{fundos}</div></div>
  <div class="sub"><h3>Altitude mark</h3><p class="muted">For small square spaces only: avatar, favicon, stamp on the bag gusset. Four contour lines tightening up a slope, and the altitude dot, drawn by the same idea as the labels. It never replaces the wordmark on a page or a pack front.</p>
    <div class="markrow"><div style="width:120px">{marca('currentColor')}</div><div class="avatar" style="width:88px">{marca(hexd('paper'), hexd('ink'))}</div><div class="avatar" style="width:56px">{marca(hexd('paper'), hexd('oxblood'))}</div><div style="width:32px">{marca('currentColor')}</div></div></div>
  <div class="sub"><h3>Don’t</h3><ul class="donts">{''.join(f'<li>{e(x)}</li>' for x in M['logo']['nao'])}</ul></div>
</section>

<section class="s" id="color">{head('color', 'Colour', e(M['cores']['regra']))}
  <div class="sub"><h3>Lot colours</h3><div class="lots">{lots}</div></div>
  <div class="sub"><h3>Neutrals</h3><div>{sw}</div></div>
  <div class="sub"><h3>Contrast</h3><p class="muted">WCAG 2.1 ratios, computed from the tokens when this manual is generated. Lot bands carry only short, large text.</p>
    <div class="tscroll"><table><thead><tr><th class="mono muted">Use</th><th class="mono muted">Pair</th><th class="mono muted">Ratio</th><th class="mono muted">Level</th></tr></thead><tbody>{linhas_c}</tbody></table></div></div>
</section>

<section class="s" id="type">{head('type', 'Type', 'Two families. Hanken Grotesk for every word people read; IBM Plex Mono for every number they compare. Weight 500 for headlines, 600 only in the wordmark.')}
  <div class="spec"><span class="big">Aa</span><div><p class="mono muted">{e(t['sans']['familia'])} · 400 500 600</p><p class="glyphs">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz 0123456789</p><p class="muted" style="font-size:14px">{e(t['sans']['uso'])}</p></div></div>
  <div class="spec"><span class="big" style="font-family:var(--f-mono);letter-spacing:-0.04em">09</span><div><p class="mono muted">{e(t['mono']['familia'])} · 400 500</p><p class="glyphs" style="font-family:var(--f-mono)">1,150 m · 72 h · US$ 26 · 93 °C</p><p class="muted" style="font-size:14px">{e(t['mono']['uso'])}</p></div></div>
  <div class="sub"><h3>Scale</h3><div class="scale">{escala}</div></div>
</section>

<section class="s" id="signature">{head('signature', 'Contour labels', 'The one idea only this brand has: every label is a contour map of the slope where the lot was picked, with a dot on the peak and its altitude beside it. The maps are generated, so a new lot gets a new map from a new seed.')}
  <div class="cols3 labels">{rot}</div>
  <div class="rules">{rules([('Lines', '22 contour levels, 2.6 px at label size, in the lot colour only.'), ('Dot', 'Ink, always on the highest point. The altitude sits to its right in Plex Mono.'), ('Band', 'The bottom band is the lot colour with Paper text: weight and the word CONCEPT.'), ('Generator', 'tools/rotulo_ninho.py reads names, colours, altitudes and seeds from marca.json.')])}</div>
</section>

<section class="s" id="photo">{head('photo', 'Photography', 'All product images are 3D renders made in the factory, so the light, the slab and the bags are identical from shot to shot.')}
  <div class="cols3 photos">{fotos}</div>
  <div class="rules">{rules(M['foto']['regras'])}</div>
</section>

<section class="s" id="motion">{head('motion', 'Motion', 'Video follows the same calm as the photos. The dot below moves with the brand’s camera easing over six seconds.')}
  <div class="ease" aria-hidden="true"><span></span></div>
  <div class="rules">{rules(M['motion']['regras'])}</div>
</section>

<section class="s" id="components">{head('components', 'Components', 'Working pieces of the store, built only from the tokens above. Square corners, hairlines, no shadows.')}
  <div class="demo">
    <p class="notice mono" style="margin:-24px -24px 0">Harvest 2026 · roasted on Mondays · ships within 72 hours</p>
    <div class="btnrow"><a class="btn solid" href="#components">Shop the harvest</a><a class="btn" href="#components">Subscribe and save 15%</a><span class="mono muted">Primary · Secondary</span></div>
    <div class="cols">
      <article class="card"><div class="ph"><img src="img/pacote_night.jpg" alt="Mantiqueira Night bag" width="1000" height="1250"></div><div class="row"><h4><span class="dot" style="background:var(--navy)"></span>{e(L['night']['nome'])}</h4><span class="num">$21</span></div><p class="muted" style="font-size:15px">Dark cocoa, molasses, almond. Natural, 1,250 m.</p></article>
      <div class="sub"><span class="mono muted">Lot sheet</span><table class="sheet"><tbody>{sheet}</tbody></table>
        <form class="field" id="news" novalidate><label class="mono muted" for="email">Harvest notes</label><div class="in"><input id="email" type="email" placeholder="you@example.com" autocomplete="email"><button class="btn solid" type="submit">Sign up</button></div><p class="msg muted" id="newsMsg" aria-live="polite"></p></form></div>
    </div>
  </div>
</section>

<section class="s" id="space">{head('space', 'Space and grid', e(M['espaco']['regra']))}
  <div class="cols">
    <div class="sub"><h3>Spacing steps</h3><div class="steps">{passos}</div></div>
    <div class="sub"><h3>Page</h3><div class="rules">{rules([('Max width', f"{M['espaco']['largura_max']} px, centred."), ('Gutter', 'At least 16 px, plus the phone’s safe area.'), ('Products', 'Three columns on desktop, one on phones; photos 4:5.'), ('Corners', '0 px. Only the product dot and avatars are round.')])}</div></div>
  </div>
</section>

<section class="s" id="files">{head('files', 'Source files', 'Everything here is generated in the Precioso Productions factory. Change marca.json, run the generators, and every piece updates together.')}
  <div class="tscroll"><table><thead><tr><th class="mono muted">Piece</th><th class="mono muted">Made by</th><th class="mono muted">Output</th></tr></thead><tbody>{arquivos}</tbody></table></div>
</section>

</div>
</div>
</main>
<footer class="wrap gutter"><span class="mono muted">{e(M['aviso_conceito'])}</span><span class="mono muted">Generated from marca.json · v{M['versao']}</span></footer>
<script>{JS}</script>
"""


if __name__ == '__main__':
    os.makedirs(os.path.join(PASTA, 'logo'), exist_ok=True)
    arq = {
        'logo/ninho-alto-wordmark-ink.svg': svg_wordmark(hexd('ink')),
        'logo/ninho-alto-wordmark-paper.svg': svg_wordmark(hexd('paper')),
        'logo/ninho-alto-mark-ink.svg': marca(hexd('ink')),
        'logo/ninho-alto-avatar.svg': marca(hexd('paper'), hexd('ink')),
    }
    css, claro, escuro = tokens_css()
    arq['tokens.css'] = css
    arq['manual.html'] = pagina(claro, escuro)
    for nome, txt in arq.items():
        with open(os.path.join(PASTA, nome), 'w', encoding='utf-8') as fh: fh.write(txt)
        print('ok', os.path.join('portfolio/ninho-alto', nome))
