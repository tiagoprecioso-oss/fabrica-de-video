"""Diagramador de ebooks da fábrica: texto.md → HTML → PDF (A4 e celular) + prévia.
Uso: python3 tools/ebook.py produtos/chefoes-do-cartao
Saída: <pasta>/<nome>.pdf, <pasta>/<nome>-celular.pdf, <pasta>/previa.png, <pasta>/build/*.html

Formato do texto.md: frontmatter (titulo, subtitulo, autor, edicao, dados); '# ' abre uma seção em página nova
('# Fase N · Título' vira abertura de fase); '## ' subtítulo; parágrafos, listas '-' e '1.'; **negrito**;
blocos ':::tipo ... :::' (hud, alerta, dica, missao, ranking, chefao, formula, ficha, regras, tabela,
batalha, roteiro, plano, fichas). Estilo visual: 'grana' (src/tema.js).
"""
import html, os, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / 'public' / 'fonts'
C = dict(papel='#FFFFFF', fundo='#EEF3EE', tinta='#12241B', verde='#0E9F6E', verde2='#0E8A5F', vermelho='#E03E2D',
         ambar='#C77700', azul='#3557D6', apagado='#5C6F64', linha='#D5E0D8', claro='#F6F9F6')

# ---------- texto ----------
def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return s

def paragrafos(linhas):
    """Mini-markdown: parágrafos, listas e subtítulos."""
    out, lista, buf = [], None, []
    def fecha_par():
        if buf: out.append('<p>' + inl(' '.join(buf)) + '</p>'); buf.clear()
    def fecha_lista():
        nonlocal lista
        if lista: out.append(f'<{lista[0]}>' + ''.join(f'<li>{inl(i)}</li>' for i in lista[1]) + f'</{lista[0]}>'); lista = None
    for l in linhas:
        s = l.strip()
        m_ul, m_ol = re.match(r'^- (.*)', s), re.match(r'^\d+\. (.*)', s)
        if not s: fecha_par(); fecha_lista(); continue
        if s.startswith('## '): fecha_par(); fecha_lista(); out.append(f'<h3>{inl(s[3:])}</h3>'); continue
        if m_ul or m_ol:
            fecha_par(); tag = 'ul' if m_ul else 'ol'
            if not lista or lista[0] != tag: fecha_lista(); lista = (tag, [])
            lista[1].append((m_ul or m_ol).group(1)); continue
        fecha_lista(); buf.append(s)
    fecha_par(); fecha_lista()
    return '\n'.join(out)

def campos(linhas):
    return [[c.strip() for c in l.split('|')] for l in linhas if l.strip()]

# ---------- desenhos (SVG próprios) ----------
def barra_vida(pct, cor):
    return f'<div class="vida"><span class="vida-rot">VIDA</span><div class="vida-trilho"><div class="vida-cheia" style="width:{pct}%;background:{cor}"></div></div></div>'

def monstro(tipo, cor, tam=120):
    """Chefões geométricos e chapados, feitos à mão em SVG. tipo: dragao, golem, sombra, cavaleiro, lacaio."""
    t, o = C['tinta'], '#FFFFFF'
    olhos = lambda x1, x2, y, r=7: (f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{o}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{o}"/>'
                                    f'<circle cx="{x1+2}" cy="{y+1}" r="{r*0.45:.1f}" fill="{t}"/><circle cx="{x2+2}" cy="{y+1}" r="{r*0.45:.1f}" fill="{t}"/>')
    sombra_chao = f'<ellipse cx="60" cy="112" rx="38" ry="5" fill="{t}" opacity=".12"/>'
    if tipo == 'dragao':
        corpo = (f'<path d="M18 40 L30 52 L26 30 L42 46 L46 22 L56 44 L66 20 L72 44 L86 26 L84 50 L102 38 L94 60 '
                 f'Q104 90 82 104 L38 104 Q14 90 24 60 Z" fill="{cor}"/>'
                 f'<path d="M36 80 Q60 96 84 80 L80 92 L72 86 L66 94 L60 86 L54 94 L48 86 L40 92 Z" fill="{t}"/>'
                 + olhos(46, 74, 66, 8) +
                 f'<path d="M36 56 L54 62 M84 56 L66 62" stroke="{t}" stroke-width="4" stroke-linecap="round"/>'
                 f'<path d="M30 104 Q24 96 16 100 Q20 108 30 104" fill="{cor}"/>')
    elif tipo == 'golem':
        corpo = (f'<rect x="22" y="30" width="76" height="74" rx="6" fill="{cor}"/>'
                 f'<rect x="34" y="14" width="52" height="24" rx="4" fill="{cor}"/>'
                 f'<path d="M22 58 H98 M22 82 H98 M48 30 V58 M74 58 V82 M44 82 V104" stroke="{t}" stroke-width="2.5" opacity=".35"/>'
                 + olhos(46, 74, 46, 6) +
                 f'<rect x="44" y="64" width="32" height="8" rx="2" fill="{t}"/>')
    elif tipo == 'sombra':
        corpo = (f'<path d="M24 104 L24 56 Q24 18 60 18 Q96 18 96 56 L96 104 L86 94 L76 104 L66 94 L56 104 L46 94 L36 104 Z" fill="{cor}"/>'
                 + olhos(48, 72, 54, 8) +
                 f'<path d="M46 76 Q60 68 74 76" stroke="{t}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    elif tipo == 'cavaleiro':
        corpo = (f'<path d="M26 104 L26 50 Q26 16 60 16 Q94 16 94 50 L94 104 Z" fill="{cor}"/>'
                 f'<rect x="32" y="48" width="56" height="16" rx="4" fill="{t}"/>'
                 f'<path d="M40 56 H80" stroke="{o}" stroke-width="4" stroke-dasharray="6 5"/>'
                 f'<path d="M60 16 V8 M60 8 Q74 4 78 14" stroke="{C["vermelho"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M60 70 V100" stroke="{t}" stroke-width="3" opacity=".3"/>')
    else:  # lacaio
        corpo = (f'<path d="M30 104 Q22 104 24 86 Q26 54 60 52 Q94 54 96 86 Q98 104 90 104 Z" fill="{cor}"/>'
                 + olhos(48, 72, 78, 7) +
                 f'<path d="M52 94 Q60 99 68 94" stroke="{t}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                 f'<path d="M60 52 Q58 40 66 36" stroke="{cor}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                 f'<circle cx="67" cy="35" r="4" fill="{cor}"/>')
    return f'<svg class="monstro" viewBox="0 0 120 120" width="{tam}" height="{tam}" aria-hidden="true">{sombra_chao}{corpo}</svg>'

def tipo_monstro(nome):
    n = nome.lower()
    for k, t in (('drag', 'dragao'), ('golem', 'golem'), ('sombra', 'sombra'), ('cavaleiro', 'cavaleiro')):
        if k in n: return t
    return 'lacaio'

COR_NIVEL = {5: C['vermelho'], 4: '#E8692A', 3: C['ambar'], 2: C['azul'], 1: C['verde']}

def icone(tipo):
    t = C['tinta']
    d = {
        'vida': f'<path d="M12 21 L4 13 Q0 8 4 4 Q8 1 12 6 Q16 1 20 4 Q24 8 20 13 Z" fill="{C["vermelho"]}"/>',
        'ataque': f'<path d="M4 20 L16 8 M14 4 L20 4 L20 10 M6 14 L10 18" stroke="{t}" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
        'dano': f'<circle cx="12" cy="12" r="9" fill="none" stroke="{C["verde"]}" stroke-width="2.6"/><circle cx="12" cy="12" r="3.5" fill="{C["verde"]}"/>',
        'fase': f'<path d="M5 12 L10 17 L19 7" stroke="{C["verde"]}" stroke-width="3" fill="none" stroke-linecap="round"/>',
    }
    return f'<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">{d[tipo]}</svg>'

# ---------- blocos ----------
def bloco(tipo, linhas):
    if tipo in ('alerta', 'dica', 'missao'):
        rot = {'alerta': 'ATENÇÃO', 'dica': 'DICA', 'missao': 'MISSÃO'}[tipo]
        return f'<aside class="caixa {tipo}"><div class="caixa-rot">{rot}</div>{paragrafos(linhas)}</aside>'
    if tipo == 'hud':
        ics = ['vida', 'ataque', 'dano', 'fase']
        cel = ''.join(f'<div class="hud-cel">{icone(ics[i % 4])}<b>{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas)))
        return f'<div class="hud">{cel}</div>'
    if tipo == 'ranking':
        rows = campos(linhas); mx = max(float(r[1].replace(',', '.')) for r in rows); out = []
        for nome, anual, mensal in rows:
            v = float(anual.replace(',', '.')); cor = C['vermelho'] if v > 300 else '#E8692A' if v > 150 else C['ambar'] if v > 60 else C['verde']
            out.append(f'<div class="rk"><div class="rk-nome">{inl(nome)}</div><div class="rk-trilho"><div class="rk-barra" style="width:{max(4, v / mx * 100):.1f}%;background:{cor}"></div></div>'
                       f'<div class="rk-num"><b>{anual}%</b> ao ano<br><span>{mensal}% ao mês</span></div></div>')
        return '<figure class="ranking"><figcaption>Força de ataque · juros médios, Banco Central, set/2026</figcaption>' + ''.join(out) + '</figure>'
    if tipo == 'chefao':
        d = {}
        for l in linhas:
            if ':' in l: k, v = l.split(':', 1); d[k.strip()] = v.strip()
        nv = int(d.get('nivel', 3)); cor = COR_NIVEL.get(nv, C['ambar'])
        pips = ''.join(f'<i class="{"on" if i < nv else ""}" style="{"background:" + cor if i < nv else ""}"></i>' for i in range(5))
        return (f'<section class="chefao" style="--cor:{cor}"><div class="ch-arte">{monstro(tipo_monstro(d["nome"]), cor, 132)}'
                f'<div class="ch-nivel">PERIGO<div class="pips">{pips}</div></div></div>'
                f'<div class="ch-info"><div class="ch-rot">CHEFÃO · {inl(d.get("dívida", ""))}</div><h3 class="ch-nome">{inl(d["nome"])}</h3>'
                f'{barra_vida(100, cor)}<div class="ch-atk"><span>ATAQUE</span> {inl(d.get("ataque", ""))}</div>'
                f'<dl><dt>Como aparece</dt><dd>{inl(d.get("como_aparece", ""))}</dd><dt>Ponto fraco</dt><dd>{inl(d.get("ponto_fraco", ""))}</dd></dl></div></section>')
    if tipo == 'formula':
        return f'<div class="formula">{inl(" ".join(linhas))}</div>'
    if tipo == 'ficha':
        return ficha_html(campos(linhas))
    if tipo == 'regras':
        return '<div class="regras">' + ''.join(f'<div class="regra"><b>{inl(a)}</b><span>{inl(b)}</span></div>' for a, b in campos(linhas)) + '</div>'
    if tipo == 'tabela':
        rows = campos(linhas)
        head = ''.join(f'<th>{inl(c)}</th>' for c in rows[0])
        body = ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
        return f'<table class="tab"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'
    if tipo == 'batalha':
        rows = campos(linhas); out = []
        for i, (a, b) in enumerate(rows):
            perde = i == 0 and len(rows) > 2 or 'sem troca' in a.lower()
            ganha = i == len(rows) - 1
            cls = 'perde' if perde else 'ganha' if ganha else 'meio'
            out.append(f'<div class="bt {cls}"><b>{inl(a)}</b><span>{inl(b)}</span></div>')
        return '<div class="batalha">' + ''.join(out) + '</div>'
    if tipo == 'roteiro':
        return '<ol class="roteiro">' + ''.join(f'<li><b>{inl(a)}</b><span>{inl(b)}</span></li>' for a, b in campos(linhas)) + '</ol>'
    if tipo == 'plano':
        out = []
        for sem, tit, txt in campos(linhas):
            out.append(f'<div class="pl"><div class="pl-box"></div><div class="pl-sem">{inl(sem)}</div><div><b>{inl(tit)}</b><span>{inl(txt)}</span></div></div>')
        return '<div class="plano">' + ''.join(out) + '</div>'
    if tipo == 'fichas':
        n = int(linhas[0].strip()); campos_f = [[x, ''] for x in ('Nome do chefão', 'Onde está (banco, loja)')] + [['Vida (saldo devedor hoje)', 'R$'], ['Ataque (taxa ao mês)', '%'], ['Ataque do mês (saldo × taxa)', 'R$'], ['Parcela ou mínimo', 'R$'], ['Parcelas que faltam', ''], ['Atrasada? Há quanto tempo?', ''], ['Estratégia e ataque especial', '']]
        return '<div class="fichas">' + ''.join(ficha_html(campos_f, f'Ficha {i + 1}') for i in range(n)) + '</div>'
    raise ValueError('bloco desconhecido: ' + tipo)

def ficha_html(rows, titulo='Ficha do chefão'):
    linhas = ''.join(f'<div class="fi-l"><span>{inl(a)}</span><em>{inl(b) if len(rows[0]) > 1 and b else ""}</em></div>' for a, *bs in rows for b in [bs[0] if bs else ''])
    return f'<div class="ficha"><div class="fi-top">{monstro("lacaio", C["apagado"], 34)}<b>{titulo}</b></div>{linhas}</div>'

# ---------- montagem ----------
def ler(pasta):
    t = (pasta / 'texto.md').read_text(encoding='utf-8')
    meta = {}
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if m:
        for l in m.group(1).splitlines():
            k, v = l.split(':', 1); meta[k.strip()] = v.strip()
        t = t[m.end():]
    secoes, atual = [], None
    for l in t.splitlines():
        if l.startswith('# '):
            atual = {'titulo': l[2:].strip(), 'linhas': []}; secoes.append(atual)
        elif atual is not None: atual['linhas'].append(l)
    return meta, secoes

def corpo_secao(linhas):
    out, buf, i = [], [], 0
    while i < len(linhas):
        s = linhas[i].strip()
        if s.startswith(':::') and len(s) > 3:
            out.append(paragrafos(buf)); buf = []
            tipo = s[3:].strip(); j = i + 1; dentro = []
            while linhas[j].strip() != ':::': dentro.append(linhas[j]); j += 1
            out.append(bloco(tipo, dentro)); i = j + 1; continue
        buf.append(linhas[i]); i += 1
    out.append(paragrafos(buf))
    return '\n'.join(out)

def secao_html(sec):
    m = re.match(r'Fase (\d+) · (.*)', sec['titulo'])
    if m:
        n = int(m.group(1)); pct = max(8, 100 - (n - 1) * 18)
        abre = (f'<header class="fase"><div class="fase-n">FASE {n}<span>/6</span></div><h1>{inl(m.group(2))}</h1>'
                f'<div class="fase-vida">{barra_vida(pct, C["vermelho"])}<small>barra de vida dos chefões</small></div></header>')
    else:
        abre = f'<header class="extra"><h1>{inl(sec["titulo"])}</h1></header>'
    cls = 'junto' if sec['titulo'] == 'Fontes' else 'secao' + (' fichas-sec' if 'Fichas' in sec['titulo'] else '')
    return f'<section class="{cls}">{abre}{corpo_secao(sec["linhas"])}</section>'

def capa_html(meta):
    return f'''<section class="capa">
  <div class="capa-top"><span class="selo">{inl(meta.get("autor", ""))}</span><span class="ed">{inl(meta.get("edicao", ""))}</span></div>
  <div class="capa-arena">
    <div class="capa-chefes">{monstro("sombra", C["ambar"], 120)}{monstro("dragao", C["vermelho"], 230)}{monstro("golem", "#E8692A", 130)}</div>
    {barra_vida(72, C["vermelho"])}
  </div>
  <h1 class="capa-tit">{inl(meta.get("titulo", ""))}</h1>
  <p class="capa-sub">{inl(meta.get("subtitulo", ""))}</p>
  <div class="capa-pe"><span>6 fases</span><span>5 chefões</span><span>plano de 90 dias</span><span>fichas para imprimir</span></div>
  <p class="capa-dados">Dados: {inl(meta.get("dados", ""))} · conteúdo educativo</p>
</section>'''

def css(celular):
    pag = '110mm 196mm' if celular else 'A4'
    mg = '10mm 8mm 13mm' if celular else '17mm 18mm 19mm'
    base = '11pt' if celular else '11.5pt'
    f = lambda nome, arq, peso, estilo='normal': f"@font-face{{font-family:'{nome}';src:url('{(FONTES / arq).as_uri()}');font-weight:{peso};font-style:{estilo}}}"
    return f'''
{f("Archivo", "Archivo400.woff2", 400)}{f("Archivo", "Archivo400i.woff2", 400, "italic")}{f("Archivo", "Archivo600.woff", 600)}
{f("Archivo", "Archivo700.woff2", 700)}{f("Archivo", "Archivo800.woff", 800)}{f("Archivo Black", "ArchivoBlack.woff", 400)}
@page{{size:{pag};margin:{mg}}}
@page capa{{margin:0}}
*{{box-sizing:border-box}}
html{{font-family:Archivo,sans-serif;font-size:{base};line-height:1.5;color:{C["tinta"]};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0}}
h1,h3,.fase-n,.capa-tit,.ch-nome{{font-family:'Archivo Black',Archivo,sans-serif;font-weight:400;letter-spacing:-.01em;line-height:1.08}}
p{{margin:0 0 .7em;orphans:3;widows:3}} strong{{font-weight:700}}
ul,ol{{margin:0 0 .8em;padding-left:1.3em}} li{{margin:.2em 0}}
h3{{font-size:1.25em;margin:1.3em 0 .45em;color:{C["verde2"]};break-after:avoid}}
li{{break-inside:avoid}}
.junto{{margin-top:12mm}}
.secao{{break-before:page}}
/* capa */
.capa{{page:capa;height:{'196mm' if celular else '297mm'};background:{C["fundo"]};padding:{'12mm 9mm' if celular else '22mm 20mm'};display:flex;flex-direction:column;position:relative;overflow:hidden}}
.capa::before{{content:'';position:absolute;inset:0;background-image:linear-gradient({C["linha"]} 1px,transparent 1px),linear-gradient(90deg,{C["linha"]} 1px,transparent 1px);background-size:{'6mm 6mm' if celular else '9mm 9mm'};opacity:.55}}
.capa>*{{position:relative}}
.capa-top{{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:.85em}}
.selo{{background:{C["tinta"]};color:#fff;padding:.35em .8em;border-radius:3px;letter-spacing:.06em;text-transform:uppercase}}
.ed{{color:{C["apagado"]}}}
.capa-arena{{margin:auto 0 0;padding-top:{'4mm' if celular else '18mm'}}}
.capa-chefes{{display:flex;align-items:flex-end;justify-content:center;gap:0}}
.capa-chefes svg:nth-child(2){{width:{'52%' if celular else '230px'};height:auto}}
.capa-chefes svg:not(:nth-child(2)){{width:{'26%' if celular else '125px'};height:auto}}
.capa .vida{{max-width:{'100%' if celular else '70%'};margin:.6em auto 0}}
.capa-tit{{font-size:{'2.9em' if celular else '4.6em'};margin:{'5mm' if celular else '12mm'} 0 .15em;text-transform:uppercase;color:{C["tinta"]}}}
.capa-sub{{font-size:{'1.15em' if celular else '1.55em'};font-weight:600;color:{C["verde2"]};margin:0 0 1.2em}}
.capa-pe{{display:flex;flex-wrap:wrap;gap:.45em}}
.capa-pe span{{border:1.5px solid {C["tinta"]};border-radius:99px;padding:.2em .75em;font-weight:700;font-size:.82em;background:#fff}}
.capa-dados{{margin:1.4em 0 0;font-size:.78em;color:{C["apagado"]}}}
/* barra de vida */
.vida{{display:flex;align-items:center;gap:.5em}}
.vida-rot{{font-family:'Archivo Black';font-size:.72em;letter-spacing:.08em}}
.vida-trilho{{flex:1;height:.85em;border:2px solid {C["tinta"]};border-radius:3px;background:#fff;padding:1.5px}}
.vida-cheia{{height:100%;border-radius:1px}}
/* aberturas */
.fase{{background:{C["fundo"]};border-radius:6px;padding:{'6mm 6mm 5mm' if celular else '10mm 10mm 8mm'};margin-bottom:{'6mm' if celular else '9mm'};position:relative;overflow:hidden}}
.fase-n{{font-size:{'.9em' if celular else '1em'};color:{C["vermelho"]};letter-spacing:.08em}}
.fase-n span{{color:{C["apagado"]}}}
.fase h1{{font-size:{'2em' if celular else '2.7em'};margin:.25em 0 .5em}}
.fase-vida small{{display:block;font-size:.72em;color:{C["apagado"]};margin-top:.3em}}
.extra h1{{font-size:{'1.8em' if celular else '2.3em'};margin:0 0 .6em;padding-bottom:.3em;border-bottom:3px solid {C["tinta"]}}}
/* caixas */
.caixa{{border-radius:5px;padding:.85em 1em .3em;margin:1em 0 1.1em;break-inside:avoid;border:2px solid}}
.caixa-rot{{font-family:'Archivo Black';font-size:.72em;letter-spacing:.1em;margin-bottom:.35em}}
.dica{{background:#EAF6F0;border-color:{C["verde"]}}} .dica .caixa-rot{{color:{C["verde2"]}}}
.alerta{{background:#FDEDEB;border-color:{C["vermelho"]}}} .alerta .caixa-rot{{color:{C["vermelho"]}}}
.missao{{background:{C["tinta"]};color:#fff;border-color:{C["tinta"]}}} .missao .caixa-rot{{color:#7FE0B8}} .missao strong{{color:#FFD27A}}
/* hud */
.hud{{display:grid;grid-template-columns:{'1fr 1fr' if celular else 'repeat(4,1fr)'};gap:.5em;margin:1em 0 1.2em}}
.hud-cel{{background:{C["claro"]};border:1.5px solid {C["linha"]};border-radius:5px;padding:.6em .7em}}
.hud-cel b{{display:block;font-size:.95em;margin:.25em 0 .1em}} .hud-cel span{{font-size:.85em;color:{C["apagado"]};line-height:1.3;display:block}}
/* ranking */
.ranking{{margin:1em 0 1.3em;break-inside:avoid}}
.ranking figcaption{{font-size:.78em;color:{C["apagado"]};font-weight:600;margin-bottom:.5em;text-transform:uppercase;letter-spacing:.05em}}
.rk{{display:grid;grid-template-columns:{'1fr' if celular else '9.5em 1fr 7.5em'};gap:{'.15em' if celular else '.7em'};align-items:center;margin:.45em 0}}
.rk-nome{{font-weight:700;font-size:.92em}}
.rk-trilho{{height:1.1em;background:{C["claro"]};border-radius:2px}} .rk-barra{{height:100%;border-radius:2px}}
.rk-num{{font-size:.8em;line-height:1.25}} .rk-num span{{color:{C["apagado"]}}}
/* chefão */
.chefao{{display:grid;grid-template-columns:{'1fr' if celular else '150px 1fr'};gap:{'.4em' if celular else '1.1em'};border:2.5px solid {C["tinta"]};border-radius:7px;padding:1em;margin:1.3em 0;break-inside:avoid;background:#fff;box-shadow:4px 4px 0 var(--cor)}}
.ch-arte{{background:{C["fundo"]};border-radius:5px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.5em}}
.ch-arte svg{{{'width:96px;height:96px' if celular else ''}}}
.ch-nivel{{font-family:'Archivo Black';font-size:.62em;letter-spacing:.1em;text-align:center;margin-top:.2em}}
.pips{{display:flex;gap:3px;justify-content:center;margin-top:3px}} .pips i{{width:13px;height:7px;border:1.5px solid {C["tinta"]};border-radius:1px;background:#fff}}
.ch-rot{{font-size:.7em;font-weight:800;letter-spacing:.06em;color:{C["apagado"]};text-transform:uppercase}}
.ch-nome{{font-size:1.55em;margin:.15em 0 .4em;color:{C["tinta"]}}}
.ch-atk{{margin:.55em 0 .4em;font-weight:700;color:var(--cor)}} .ch-atk span{{font-family:'Archivo Black';font-size:.75em;letter-spacing:.08em;color:{C["tinta"]};margin-right:.3em}}
.chefao dl{{margin:0}} .chefao dt{{font-weight:800;font-size:.8em;text-transform:uppercase;letter-spacing:.04em;margin-top:.45em}} .chefao dd{{margin:0;font-size:.95em}}
/* fórmula, regras, tabela, batalha, roteiro */
.formula{{font-family:'Archivo Black';font-size:{'1.15em' if celular else '1.45em'};text-align:center;padding:.7em;border:2.5px dashed {C["verde"]};border-radius:6px;margin:.9em 0 1em;background:#fff}}
.regras{{display:grid;gap:.45em;margin:.9em 0 1.2em}}
.regra{{display:grid;grid-template-columns:{'4.6em' if celular else '5.6em'} 1fr;gap:.6em;align-items:start;background:{C["claro"]};border-left:4px solid {C["verde"]};padding:.55em .7em;border-radius:3px;break-inside:avoid}}
.regra b{{font-family:'Archivo Black';font-weight:400;font-size:.82em;color:{C["verde2"]};padding-top:.15em}}
.tab{{width:100%;border-collapse:collapse;margin:.8em 0 1.1em;font-size:{'.8em' if celular else '.92em'};break-inside:avoid}}
.tab th{{background:{C["tinta"]};color:#fff;text-align:left;padding:.45em .55em;font-weight:700}}
.tab td{{padding:.45em .55em;border-bottom:1.5px solid {C["linha"]}}}
.batalha{{display:grid;gap:.5em;margin:.9em 0 1.2em}}
.bt{{border-radius:5px;padding:.7em .85em;break-inside:avoid;border:2px solid}}
.bt b{{display:block;font-family:'Archivo Black';font-weight:400;font-size:.9em;margin-bottom:.15em}} .bt span{{font-size:.95em}}
.bt.perde{{background:#FDEDEB;border-color:{C["vermelho"]}}} .bt.perde b{{color:{C["vermelho"]}}}
.bt.meio{{background:#FFF6E5;border-color:{C["ambar"]}}} .bt.meio b{{color:{C["ambar"]}}}
.bt.ganha{{background:#EAF6F0;border-color:{C["verde"]}}} .bt.ganha b{{color:{C["verde2"]}}}
.roteiro{{list-style:none;padding:0;counter-reset:r;margin:.9em 0 1.2em}}
.roteiro li{{counter-increment:r;position:relative;padding:0 0 .8em 2.6em;break-inside:avoid}}
.roteiro li::before{{content:counter(r);position:absolute;left:0;top:0;width:1.8em;height:1.8em;border-radius:50%;background:{C["verde"]};color:#fff;font-family:'Archivo Black';display:flex;align-items:center;justify-content:center;font-size:.85em}}
.roteiro b{{display:block}}
/* plano */
.plano{{display:grid;gap:.4em;margin:.9em 0 1.2em}}
.pl{{display:grid;grid-template-columns:1.3em {'4.4em' if celular else '5.4em'} 1fr;gap:.6em;align-items:start;border-bottom:1.5px solid {C["linha"]};padding:.45em 0 .55em;break-inside:avoid}}
.pl-box{{width:1.05em;height:1.05em;border:2px solid {C["tinta"]};border-radius:2px;margin-top:.2em}}
.pl-sem{{font-family:'Archivo Black';font-size:.8em;color:{C["verde2"]};padding-top:.2em}}
.pl b{{display:block}} .pl span{{font-size:.93em}}
/* fichas */
.ficha{{border:2px solid {C["tinta"]};border-radius:6px;padding:.7em .9em .4em;margin:.8em 0 1em;break-inside:avoid;background:#fff}}
.fi-top{{display:flex;align-items:center;gap:.4em;font-family:'Archivo Black';margin-bottom:.3em}} .fi-top b{{font-weight:400}}
.fi-l{{display:flex;align-items:flex-end;gap:.5em;border-bottom:1.5px dotted {C["apagado"]};padding:.62em 0 .2em;font-size:.88em}}
.fi-l span{{font-weight:700;white-space:nowrap}} .fi-l em{{font-style:normal;color:{C["apagado"]};margin-left:auto;padding-right:{'3em' if celular else '8em'}}}
.fichas .ficha{{{'' if celular else 'margin:0 0 7mm'}}}
.fichas .ficha:nth-child(2n){{{'' if celular else 'break-after:page'}}}
'''

def montar(pasta, celular):
    meta, secoes = ler(pasta)
    corpo = capa_html(meta) + ''.join(secao_html(s) for s in secoes)
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{inl(meta.get("titulo", ""))}</title><style>{css(celular)}</style></head><body>{corpo}</body></html>', meta

def pdf(pasta, celular):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    doc, meta = montar(pasta, celular)
    build = pasta / 'build'; build.mkdir(exist_ok=True)
    nome = pasta.name + ('-celular' if celular else '')
    arq_html = build / f'{nome}.html'; arq_html.write_text(doc, encoding='utf-8')
    rodape = (f'<div style="width:100%;font-family:Arial;font-size:7.5px;color:{C["apagado"]};padding:0 {"8mm" if celular else "18mm"};display:flex;justify-content:space-between">'
              f'<span>{html.escape(meta.get("titulo", ""))} · {html.escape(meta.get("autor", ""))}</span><span class="pageNumber"></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(arq_html.as_uri()); pg.wait_for_timeout(400)
        com = build / f'{nome}-rodape.pdf'; sem = build / f'{nome}-capa.pdf'
        pg.pdf(path=str(com), prefer_css_page_size=True, display_header_footer=True, header_template='<span></span>', footer_template=rodape)
        pg.pdf(path=str(sem), prefer_css_page_size=True)
        b.close()
    w = PdfWriter(); capa, resto = PdfReader(str(sem)), PdfReader(str(com))
    w.add_page(capa.pages[0])
    for pgn in resto.pages[1:]: w.add_page(pgn)
    w.add_metadata({'/Title': meta.get('titulo', ''), '/Author': meta.get('autor', ''), '/Subject': meta.get('subtitulo', '')})
    saida = pasta / f'{nome}.pdf'
    with open(saida, 'wb') as fh: w.write(fh)
    com.unlink(); sem.unlink()
    return saida, len(w.pages)

def previa(arq_pdf, saida, paginas):
    import pypdfium2 as pdfium
    from PIL import Image
    d = pdfium.PdfDocument(str(arq_pdf)); ims = []
    for i in paginas:
        if i < len(d): ims.append(d[i].render(scale=1.1).to_pil())
    h = max(i.height for i in ims); gap = 24
    tela = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) + 1), h + gap * 2), (214, 224, 216))
    x = gap
    for im in ims: tela.paste(im, (x, gap)); x += im.width + gap
    tela.save(saida)

if __name__ == '__main__':
    pasta = (RAIZ / sys.argv[1]).resolve() if len(sys.argv) > 1 else sys.exit(__doc__)
    a4, n = pdf(pasta, False); print(a4.relative_to(RAIZ), n, 'páginas')
    cel, n2 = pdf(pasta, True); print(cel.relative_to(RAIZ), n2, 'páginas')
    previa(a4, pasta / 'previa.png', [0, 2, 3]); print((pasta / 'previa.png').relative_to(RAIZ))
