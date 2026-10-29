"""Capa e mockups de um ebook da fábrica, por código (HTML + CSS 3D → PNG com o Chromium do Playwright).
Uso: python3 tools/capa.py produtos/chefoes-do-cartao
Saída em <pasta>/divulgacao/: capa-vertical.png (1600×2400), produto-quadrado.png (1200×1200), mockup-16x9.png (1920×1080),
mockup-quadrado.png (1080×1080), mockup-story.png (1080×1920), teste-miniatura.png e telas/ (capturas do produto).
Precisa de: <pasta>/arte/*.svg (tools/extrair_arte.py), <pasta>/<nome>.pdf (tools/ebook.py) e <pasta>/web/index.html.
"""
import base64, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
F = RAIZ / 'public' / 'fonts'
C = dict(tinta='#17302A', tinta2='#244038', amarelo='#FFCB2D', amarelo_esc='#E0A400', fogo='#FF5146', grana='#1FBF6A', grana_esc='#139256',
         azul='#279FEA', roxo='#9466F5', laranja='#FF9A22', papel='#E7EFE3', cartao='#F1F6EE', linha='#CAD8C8', apagado='#5B7067', menta='#BFE9D2')

def uri(p):
    return 'data:image/png;base64,' + base64.b64encode(Path(p).read_bytes()).decode()

def svg(pasta, nome):
    return 'data:image/svg+xml;base64,' + base64.b64encode((pasta / 'arte' / f'{nome}.svg').read_bytes()).decode()

def fontes():
    f = lambda n, a, w: f"@font-face{{font-family:'{n}';src:url('{(F / a).as_uri()}');font-weight:{w}}}"
    return f('Baloo 2', 'Baloo2-800.woff2', 800) + ''.join(f('Nunito', f'Nunito-{w}.woff2', w) for w in (600, 700, 800, 900))

BASE = f'''*{{box-sizing:border-box;margin:0}} body{{font-family:Nunito,sans-serif;color:{C["tinta"]};overflow:hidden}}
.disp{{font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;line-height:.88;letter-spacing:-.01em}}'''

# ---------- capturas do produto ----------
def telas(pasta, dest):
    dest.mkdir(parents=True, exist_ok=True)
    src = (pasta / 'web' / 'index.html').read_text(encoding='utf-8')
    tmp = dest / '_pagina.html'
    tmp.write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + src + '</body></html>', encoding='utf-8')
    import pypdfium2 as pdfium
    with sync_playwright() as p:
        b = p.chromium.launch()
        cel = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, accept_downloads=True)
        cel.goto(tmp.as_uri()); cel.wait_for_timeout(1800)
        cel.screenshot(path=str(dest / 'cel-capa.png'))
        for _ in range(8): cel.click('#proximo'); cel.wait_for_timeout(120)
        cel.wait_for_timeout(1600)
        cel.evaluate("document.querySelector('#palco').scrollIntoView({block:'start'}); window.scrollBy(0,-70)"); cel.wait_for_timeout(700)
        cel.screenshot(path=str(dest / 'cel-batalha.png'))
        cel.fill('#nome-plano', 'Ana')
        with cel.expect_download(timeout=90000) as dl: cel.click('#baixar-pdf')
        dl.value.save_as(str(dest / 'plano-exemplo.pdf'))
        b.close()
    tmp.unlink()
    d = pdfium.PdfDocument(str(dest / 'plano-exemplo.pdf'))
    for i in range(min(2, len(d))): d[i].render(scale=1.4).to_pil().save(dest / f'plano-{i}.png')
    ebook = pdfium.PdfDocument(str(pasta / f'{pasta.name}.pdf'))
    for i, nome in [(0, 'ebook-capa'), (5, 'ebook-bestiario'), (3, 'ebook-abertura'), (14, 'ebook-extrato')]:
        if i < len(ebook): ebook[i].render(scale=1.6).to_pil().save(dest / f'{nome}.png')

# ---------- peças ----------
def capa_vertical(pasta):
    desfile = ''.join(f'<img src="{svg(pasta, n)}" style="width:{w}px">' for n, w in [('cheque', 210), ('parcelado', 250), ('rotativo', 520), ('pessoal', 250), ('consignado', 200)])
    return f'''<style>{fontes()}{BASE}
body{{width:1600px;height:2400px;background:radial-gradient(120% 70% at 50% 72%, {C["tinta2"]} 0%, {C["tinta"]} 60%);color:#fff;padding:120px 110px 110px;display:flex;flex-direction:column}}
.selo{{display:inline-flex;align-items:center;gap:18px;background:{C["tinta2"]};border-radius:99px;padding:14px 36px 14px 14px;font-weight:900;font-size:40px;align-self:flex-start}}
.selo img{{width:70px}}
h1{{font-size:330px;text-transform:uppercase;margin-top:110px}} h1 span{{display:block;color:{C["amarelo"]}}}
.sub{{font-size:74px;font-weight:800;color:{C["menta"]};margin-top:40px;line-height:1.15;max-width:1250px}}
.desfile{{display:flex;align-items:flex-end;justify-content:center;margin-top:auto}}
.chao{{height:34px;border-radius:99px;background:{C["tinta2"]};margin-top:-30px}}
.pe{{display:flex;gap:20px;justify-content:center;margin-top:60px}} .pe span{{border:4px solid #3B5C51;border-radius:99px;padding:10px 34px;font-weight:900;font-size:40px;color:#D6F1E3}}
</style><div class="selo"><img src="{svg(pasta, "din")}">Din no Chão · ebook + simulador</div>
<h1 class="disp">Chefões<span>do cartão</span></h1><p class="sub">Como derrotar as dívidas sem passar aperto</p>
<div class="desfile">{desfile}</div><div class="chao"></div><div class="pe"><span>9 chefões</span><span>simulador</span><span>plano em PDF</span></div>'''

def produto_quadrado(pasta):
    return f'''<style>{fontes()}{BASE}
body{{width:1200px;height:1200px;background:radial-gradient(90% 80% at 72% 70%, {C["tinta2"]} 0%, {C["tinta"]} 62%);color:#fff;padding:80px;position:relative}}
h1{{font-size:208px;text-transform:uppercase;position:relative;z-index:2}} h1 span{{display:block;color:{C["amarelo"]}}}
.sub{{font-size:52px;font-weight:800;color:{C["menta"]};margin-top:28px;line-height:1.1;width:560px;position:relative;z-index:2}}
.drag{{position:absolute;right:40px;bottom:46px;width:520px}}
.mini{{position:absolute;left:80px;bottom:84px;display:flex;gap:6px;align-items:flex-end}} .mini img{{width:150px}}
.chao{{position:absolute;left:60px;right:60px;bottom:70px;height:24px;border-radius:99px;background:{C["tinta2"]}}}
.tag{{position:absolute;right:90px;top:300px;background:{C["amarelo"]};color:{C["tinta"]};font-weight:900;font-size:40px;border-radius:24px;padding:16px 26px;transform:rotate(6deg);box-shadow:0 10px 0 {C["amarelo_esc"]};z-index:3;text-align:center;line-height:1.05}}
</style><div class="chao"></div><h1 class="disp">Chefões<span>do cartão</span></h1><p class="sub">Derrote as dívidas sem passar aperto</p>
<img class="drag" src="{svg(pasta, "rotativo")}"><div class="mini"><img src="{svg(pasta, "cheque")}"><img src="{svg(pasta, "parcelado")}"></div>
<div class="tag">EBOOK<br>+ SIMULADOR</div>'''

def livro(capa_png, w):
    h = int(w * 1.414)
    return f'''<div class="livro" style="width:{w}px;height:{h}px"><div class="miolo"></div><img class="frente" src="{uri(capa_png)}"><div class="lombada"></div></div>'''

def celular(tela_png, w):
    return f'<div class="cel" style="width:{w}px;height:{int(w * 2.08)}px"><div class="tela"><img src="{uri(tela_png)}"></div><i class="notch"></i></div>'

def cartao_bonus(tipo, s=1.0):
    if tipo == 'planilha':
        grade = ''.join(f'<i style="background:{c}"></i>' for c in [C["tinta"]] * 4 + ['#fff', '#fff', C["grana"], '#fff'] * 3)
        return f'<div class="bonus" style="--s:{s}"><span class="b-rot">BÔNUS 1</span><div class="b-grade">{grade}</div><b>Planilha Placar dos Chefões</b><small>Excel e Google Planilhas</small></div>'
    return (f'<div class="bonus" style="--s:{s}"><span class="b-rot">BÔNUS 2</span><div class="b-chat"><p class="u">Me ajude a montar o roteiro para renegociar meu cartão</p>'
            f'<p class="c">Claro! Primeiro, me diga a taxa e o saldo…</p></div><b>Kit de prompts do Din</b><small>para usar com o Claude</small></div>')

MOCK_CSS = f'''
.livro{{position:relative;transform:perspective(2200px) rotateY(-26deg) rotateX(5deg);transform-style:preserve-3d;filter:drop-shadow(30px 40px 30px rgba(23,48,42,.35))}}
.livro .frente{{position:absolute;inset:0;width:100%;height:100%;border-radius:6px 14px 14px 6px;object-fit:cover}}
.livro .lombada{{position:absolute;left:0;top:0;bottom:0;width:7%;background:linear-gradient(90deg,#0d1f1a,#2b4a40 60%,#0d1f1a);transform-origin:left;transform:rotateY(80deg);border-radius:6px 0 0 6px}}
.livro .miolo{{position:absolute;right:-14px;top:10px;bottom:10px;width:30px;background:repeating-linear-gradient(90deg,#f3f6ef 0 2px,#d9e2d4 2px 4px);transform:translateZ(-20px);border-radius:0 6px 6px 0}}
.cel{{position:relative;background:#101614;border-radius:54px;padding:16px;box-shadow:0 30px 60px rgba(23,48,42,.35),inset 0 0 0 3px #2a3a35}}
.cel .tela{{width:100%;height:100%;border-radius:40px;overflow:hidden;background:#000}} .cel .tela img{{width:100%;display:block}}
.cel .notch{{position:absolute;top:26px;left:50%;transform:translateX(-50%);width:28%;height:26px;border-radius:99px;background:#101614}}
.folha{{position:absolute;border-radius:10px;box-shadow:0 18px 40px rgba(23,48,42,.3);overflow:hidden}} .folha img{{width:100%;display:block}}
.bonus{{background:{C["cartao"]};border:5px solid {C["tinta"]};border-radius:calc(30px*var(--s));padding:calc(24px*var(--s));width:calc(360px*var(--s));box-shadow:0 calc(12px*var(--s)) 0 {C["grana"]};display:grid;gap:calc(10px*var(--s))}}
.bonus b{{font-family:'Baloo 2';font-weight:800;font-size:calc(36px*var(--s));line-height:1}} .bonus small{{font-weight:800;font-size:calc(22px*var(--s));color:{C["apagado"]}}}
.b-rot{{justify-self:start;background:{C["fogo"]};color:#fff;font-weight:900;font-size:calc(20px*var(--s));letter-spacing:.12em;border-radius:99px;padding:calc(5px*var(--s)) calc(16px*var(--s))}}
.b-grade{{display:grid;grid-template-columns:repeat(4,1fr);gap:calc(5px*var(--s));background:{C["linha"]};padding:calc(6px*var(--s));border-radius:calc(12px*var(--s))}} .b-grade i{{height:calc(26px*var(--s));border-radius:calc(5px*var(--s))}}
.b-chat{{display:grid;gap:calc(8px*var(--s))}} .b-chat p{{font-size:calc(19px*var(--s));font-weight:700;border-radius:calc(16px*var(--s));padding:calc(10px*var(--s)) calc(14px*var(--s));line-height:1.25}}
.b-chat .u{{background:{C["tinta"]};color:#fff;margin-left:15%}} .b-chat .c{{background:{C["amarelo"]};margin-right:15%}}
.selo-p{{display:inline-flex;align-items:center;gap:14px;font-weight:900;color:{C["grana_esc"]};letter-spacing:.12em}}
'''

def mockup(pasta, t, w, h):
    ebook, bat, plano0, plano1 = t / 'ebook-capa.png', t / 'cel-batalha.png', t / 'plano-0.png', t / 'plano-1.png'
    fundo = f'background:radial-gradient(80% 90% at 60% 55%, {C["cartao"]} 0%, {C["papel"]} 70%)'
    if w > h:  # 16:9
        corpo = f'''<div style="position:absolute;left:90px;top:96px;width:660px">
            <span class="selo-p" style="font-size:24px"><img src="{svg(pasta, "din")}" width="54">DIN NO CHÃO</span>
            <h1 class="disp" style="font-size:118px;text-transform:uppercase;margin-top:22px">Chefões<span style="display:block;color:{C["fogo"]}">do cartão</span></h1>
            <p style="font-size:34px;font-weight:800;margin-top:20px;line-height:1.2;width:560px">Ebook + simulador da batalha + plano pessoal em PDF + 2 bônus</p></div>
          <div class="folha" style="left:760px;top:470px;width:300px;transform:rotate(-8deg)"><img src="{uri(plano1)}"></div>
          <div class="folha" style="left:860px;top:440px;width:300px;transform:rotate(-2deg)"><img src="{uri(plano0)}"></div>
          <div style="position:absolute;left:1040px;top:150px">{livro(ebook, 470)}</div>
          <div style="position:absolute;left:1440px;top:250px">{celular(bat, 340)}</div>
          <div style="position:absolute;left:90px;bottom:80px;display:flex;gap:26px">{cartao_bonus("planilha", .95)}{cartao_bonus("prompts", .95)}</div>'''
    elif w == h:  # quadrado
        corpo = f'''<div style="position:absolute;left:70px;top:64px;width:900px">
            <span class="selo-p" style="font-size:22px"><img src="{svg(pasta, "din")}" width="48">DIN NO CHÃO</span>
            <h1 class="disp" style="font-size:96px;text-transform:uppercase;margin-top:14px">Chefões <span style="color:{C["fogo"]}">do cartão</span></h1></div>
          <div class="folha" style="left:80px;top:250px;width:250px;transform:rotate(-7deg)"><img src="{uri(plano0)}"></div>
          <div style="position:absolute;left:310px;top:200px">{livro(ebook, 360)}</div>
          <div style="position:absolute;left:740px;top:220px">{celular(bat, 240)}</div>
          <div style="position:absolute;left:70px;bottom:56px;right:70px;display:flex;gap:20px;justify-content:space-between;align-items:flex-end">{cartao_bonus("planilha", .7)}<p style="font-size:30px;font-weight:900;text-align:center;line-height:1.15;padding-bottom:20px">Ebook + simulador<br>+ plano em PDF</p>{cartao_bonus("prompts", .7)}</div>'''
    else:  # story
        corpo = f'''<div style="position:absolute;left:80px;top:150px;right:80px">
            <span class="selo-p" style="font-size:28px"><img src="{svg(pasta, "din")}" width="60">DIN NO CHÃO</span>
            <h1 class="disp" style="font-size:150px;text-transform:uppercase;margin-top:24px">Chefões<span style="display:block;color:{C["fogo"]}">do cartão</span></h1>
            <p style="font-size:44px;font-weight:800;margin-top:24px;line-height:1.2">Derrote as dívidas sem passar aperto</p></div>
          <div style="position:absolute;left:60px;top:690px">{livro(ebook, 500)}</div>
          <div style="position:absolute;left:600px;top:720px">{celular(bat, 370)}</div>
          <div style="position:absolute;left:80px;right:80px;bottom:110px;display:flex;gap:24px;justify-content:center">{cartao_bonus("planilha", 1)}{cartao_bonus("prompts", 1)}</div>'''
    return f'<style>{fontes()}{BASE}{MOCK_CSS} body{{width:{w}px;height:{h}px;{fundo};position:relative}}</style>{corpo}'

def render(html, saida, w, h):
    tmp = saida.with_suffix('.html'); tmp.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>' + html + '</body></html>', encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(800); pg.screenshot(path=str(saida)); b.close()
    tmp.unlink()

def miniatura(div):
    from PIL import Image
    v = Image.open(div / 'capa-vertical.png').resize((200, 300), Image.LANCZOS)
    q = Image.open(div / 'produto-quadrado.png').resize((150, 150), Image.LANCZOS)
    t = Image.new('RGB', (420, 340), C['papel']); t.paste(v, (20, 20)); t.paste(q, (250, 20)); t.save(div / 'teste-miniatura.png')

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    pasta = (RAIZ / sys.argv[1]).resolve(); div = pasta / 'divulgacao'; t = div / 'telas'
    telas(pasta, t)
    render(capa_vertical(pasta), div / 'capa-vertical.png', 1600, 2400)
    render(produto_quadrado(pasta), div / 'produto-quadrado.png', 1200, 1200)
    for nome, w, h in [('mockup-16x9', 1920, 1080), ('mockup-quadrado', 1080, 1080), ('mockup-story', 1080, 1920)]:
        render(mockup(pasta, t, w, h), div / f'{nome}.png', w, h)
    miniatura(div)
    print('ok:', ', '.join(sorted(x.name for x in div.glob('*.png'))))
