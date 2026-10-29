"""Diagramador de ebooks da fábrica (v2, visual "desenho animado"): texto.md → HTML → PDF (A4 e celular) + prévia.
Uso: python3 tools/ebook.py produtos/chefoes-do-cartao
Saída: <pasta>/<nome>.pdf, <pasta>/<nome>-celular.pdf, <pasta>/previa.png, <pasta>/build/*.html

Antes: python3 tools/extrair_arte.py <pasta>/web/index.html <pasta>/arte   (desenhos vêm da página interativa)
Formato do texto.md: frontmatter (titulo, subtitulo, autor, edicao, dados); '# ' abre uma seção em página nova;
'# Fase N · Título' é uma fase (o bloco :::abertura vira a página de abertura colorida); '## ' subtítulo;
parágrafos, listas '-' e '1.', **negrito'; blocos ':::tipo ... :::':
  hud, din, alerta, missao, numeros, ranking, chefao (cartas, agrupadas), grafico (teto|ana), formula, ficha, regras,
  tabela, aposta, extrato, batalha, golpe (agrupados), escudos, plano, mundo2, fichas, abertura.
Estilo: o da página interativa (Baloo 2 + Nunito, paleta "grana" em versão vibrante).
"""
import html, re, sys, importlib.util
from pypdf.generic import NameObject
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / 'public' / 'fonts'
C = dict(bg='#F5FAF3', papel='#E7EFE3', cartao='#F1F6EE', tinta='#17302A', apagado='#5B7067', linha='#CAD8C8',
         grana='#1FBF6A', grana_esc='#139256', grana_cl='#DDF7E8', fogo='#FF5146', fogo_esc='#D3352B', fogo_cl='#FFE3DF',
         laranja='#FF9A22', laranja_esc='#D9780A', amarelo='#FFCB2D', amarelo_esc='#E0A400', amarelo_cl='#FFF4CC',
         azul='#279FEA', azul_esc='#1679BF', roxo='#9466F5', roxo_esc='#7044D6', roxo_cl='#EEE6FF',
         ciano='#17C1C3', ciano_esc='#0B9496', rosa='#FF6FA8', noite='#4B3A78', noite_esc='#2F2350')
COR_NIVEL = {5: 'fogo', 4: 'laranja', 3: 'roxo', 2: 'azul', 1: 'grana'}
COR_ARTE = {'rotativo': 'fogo', 'parcelado': 'laranja', 'cheque': 'roxo', 'pessoal': 'azul', 'consclt': 'rosa',
            'fgts': 'noite', 'contas': 'amarelo', 'veiculos': 'ciano', 'consignado': 'grana'}

def cor(n, sufixo=''):
    return C.get((n + sufixo).replace('-', '_'), C.get(n, n))

# ---------- texto ----------
def inl(s):
    s = html.escape(s, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)

def paragrafos(linhas):
    out, lista, buf = [], None, []
    def fp():
        if buf: out.append('<p>' + inl(' '.join(buf)) + '</p>'); buf.clear()
    def fl():
        nonlocal lista
        if lista: out.append(f'<{lista[0]}>' + ''.join(f'<li>{inl(i)}</li>' for i in lista[1]) + f'</{lista[0]}>'); lista = None
    for l in linhas:
        s = l.strip(); mu, mo = re.match(r'^- (.*)', s), re.match(r'^\d+\. (.*)', s)
        if not s: fp(); fl(); continue
        if s.startswith('## '): fp(); fl(); out.append(f'<h3>{inl(s[3:])}</h3>'); continue
        if mu or mo:
            fp(); tag = 'ul' if mu else 'ol'
            if not lista or lista[0] != tag: fl(); lista = (tag, [])
            lista[1].append((mu or mo).group(1)); continue
        fl(); buf.append(s)
    fp(); fl()
    return '\n'.join(out)

def campos(linhas):
    return [[c.strip() for c in l.split('|')] for l in linhas if l.strip()]

def chaves(linhas):
    d, resto = {}, []
    for l in linhas:
        m = re.match(r'^([a-zçãíúéêó_]+):\s*(.*)$', l.strip())
        if m: d[m.group(1)] = m.group(2)
        elif l.strip(): resto.append(l)
    return d, resto

# ---------- campos do PDF (marcadores lidos por tools/pdf_campos.py) ----------
NCAMPO = [0]
def mk(nome):
    return f'<span class="mk">QZ{nome}ZQ</span>'
def campo_linha(rotulo, prefixo=''):
    NCAMPO[0] += 1; n = NCAMPO[0]
    return f'<div class="fi-l"><span>{inl(rotulo)}</span><em>{inl(prefixo)}</em>{mk(f"t{n}a")}<i class="esp"></i>{mk(f"t{n}b")}</div>'

# ---------- arte ----------
ARTE = {}
def arte(nome, w=120, extra=''):
    svg = ARTE.get(nome)
    if not svg: return ''
    return re.sub(r'<svg ', f'<svg width="{w}" height="{w}" class="arte {extra}" ', svg, count=1)

def barra_vida(pct, c):
    return f'<div class="vida"><span>VIDA</span><div class="vida-t"><div class="vida-c" style="width:{pct}%;background:{c}"></div></div></div>'

def icone(nome, c):
    p = {'vida': '<path d="M12 21 L4 13 Q0 8 4 4 Q8 1 12 6 Q16 1 20 4 Q24 8 20 13 Z" fill="%s"/>' % C['fogo'],
         'ataque': '<path d="M4 20 L16 8 M14 4 L20 4 L20 10 M6 14 L10 18" stroke="%s" stroke-width="2.8" fill="none" stroke-linecap="round"/>' % C['tinta'],
         'dano': '<circle cx="12" cy="12" r="9" fill="none" stroke="%s" stroke-width="2.8"/><circle cx="12" cy="12" r="3.5" fill="%s"/>' % (C['grana'], C['grana']),
         'fase': '<path d="M5 12 L10 17 L19 7" stroke="%s" stroke-width="3.2" fill="none" stroke-linecap="round"/>' % C['grana'],
         'alvo': '<circle cx="12" cy="12" r="9" fill="none" stroke="%s" stroke-width="2.6"/><circle cx="12" cy="12" r="5" fill="none" stroke="%s" stroke-width="2.6"/><circle cx="12" cy="12" r="1.8" fill="%s"/>' % (c, c, c),
         'escudo': '<path d="M12 2 L21 5 V11 Q21 18 12 22 Q3 18 3 11 V5Z" fill="%s" stroke="%s" stroke-width="1.8" stroke-linejoin="round"/>' % (c, C['tinta']),
         'cadeado': '<rect x="4" y="10" width="16" height="12" rx="3" fill="%s" stroke="%s" stroke-width="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="%s" stroke-width="3" fill="none"/>' % (C['amarelo'], C['tinta'], C['amarelo'])}[nome]
    return f'<svg viewBox="0 0 24 24" width="22" height="22">{p}</svg>'

ICONES_GOLPE = {
    'Renegociar': '<path d="M5 4h11l3 3v13H5z" fill="#FFCB2D" stroke="#17302A" stroke-width="2" stroke-linejoin="round"/><path d="M8 10h8M8 14h8M8 18h5" stroke="#17302A" stroke-width="2" stroke-linecap="round"/>',
    'Portabilidade': '<rect x="2" y="6" width="9" height="12" rx="2" fill="#279FEA" stroke="#17302A" stroke-width="2"/><rect x="13" y="6" width="9" height="12" rx="2" fill="#fff" stroke="#17302A" stroke-width="2"/><path d="M8 3c5 0 9 0 9 3M17 6l-2-2M17 6l2-2" stroke="#17302A" stroke-width="2" fill="none" stroke-linecap="round"/>',
    'Trocar dívida cara por barata': '<path d="M4 8h13l-3-3M20 16H7l3 3" stroke="#139256" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    'Dinheiro extra': '<path d="M13 2 L5 13 h6 l-2 9 l9 -12 h-6z" fill="#FFCB2D" stroke="#17302A" stroke-width="2" stroke-linejoin="round"/>',
    'Antecipar parcelas': '<circle cx="12" cy="13" r="8" fill="#fff" stroke="#17302A" stroke-width="2"/><path d="M12 9v4l3 2M9 2h6" stroke="#17302A" stroke-width="2" fill="none" stroke-linecap="round"/>',
    'Pedir socorro': '<circle cx="12" cy="12" r="9" fill="#9466F5" stroke="#17302A" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="#fff" stroke="#17302A" stroke-width="2"/><path d="M5.6 5.6l3.6 3.6M18.4 5.6l-3.6 3.6M5.6 18.4l3.6-3.6M18.4 18.4l-3.6-3.6" stroke="#fff" stroke-width="2"/>'}

# ---------- gráficos (números do contas.py) ----------
CONTAS = None
def brl0(v): return 'R$ ' + f'{v:,.0f}'.replace(',', '.')
def grafico(tipo):
    W, H, m = 640, 270, dict(l=74, r=24, t=16, b=36)
    if tipo == 'teto':
        t = CONTAS.M['rotativo']
        series = [([1000 * (1 + t) ** i for i in range(13)], C['fogo'], 'Sem a lei'), ([min(2000, 1000 * (1 + t) ** i) for i in range(13)], C['grana'], 'Com o teto de 100%')]
        passo = 1500
    else:
        a = CONTAS.historico(CONTAS.exemplo(), 600, lambda d: -d['taxa'])
        b = CONTAS.historico(CONTAS.exemplo(), 600, lambda d: d['saldo'])
        mn = CONTAS.historico(CONTAS.exemplo(), 300, None, max(len(a), len(b)) - 1)
        series = [(mn, C['fogo'], 'Só o mínimo'), (b, C['amarelo_esc'], 'Bola de Neve'), (a, C['grana'], 'Avalanche')]
        passo = 2000
    n = max(len(s[0]) for s in series) - 1; mx = max(max(s[0]) for s in series); topo = -(-mx // passo) * passo
    X = lambda i: m['l'] + (W - m['l'] - m['r']) * i / n
    Y = lambda v: H - m['b'] - (H - m['t'] - m['b']) * v / topo
    g = ''
    for k in range(int(topo // passo) + 1):
        v = k * passo; g += f'<line x1="{m["l"]}" x2="{W - m["r"]}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{C["linha"]}" stroke-width="1.5"/><text x="{m["l"] - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{brl0(v)}</text>'
    pas = 1 if n <= 12 else 3
    for i in range(0, n + 1, pas): g += f'<text x="{X(i):.1f}" y="{H - 14}" text-anchor="middle">{i}</text>'
    for vals, c, _ in series:
        d = ' '.join(f'{"L" if i else "M"}{X(i):.1f} {Y(v):.1f}' for i, v in enumerate(vals))
        g += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{X(len(vals) - 1):.1f}" cy="{Y(vals[-1]):.1f}" r="7" fill="{c}" stroke="#fff" stroke-width="2.5"/>'
    leg = ''.join(f'<span><i style="background:{c}"></i>{t}</span>' for _, c, t in series)
    tit = 'R$ 1.000 no rotativo, mês a mês' if tipo == 'teto' else 'Vida total dos chefões da Ana, mês a mês'
    return f'<figure class="graf"><figcaption>{tit}</figcaption><svg viewBox="0 0 {W} {H}" width="100%">{g}</svg><div class="leg">{leg}<span class="eixo">eixo de baixo: meses</span></div></figure>'

# ---------- blocos ----------
def din(texto, tom=''):
    return f'<div class="din {tom}">{arte("din", 66)}<div class="balao">{paragrafos(texto)}</div></div>'

def bloco(tipo, linhas):
    if tipo == 'din': return din(linhas)
    if tipo == 'alerta': return f'<aside class="alerta"><span class="pilula">ATENÇÃO</span>{paragrafos(linhas)}</aside>'
    if tipo == 'missao': return f'<aside class="missao"><span class="m-ic">{icone("alvo", C["amarelo"])}</span><div><span class="pilula am">MISSÃO</span>{paragrafos(linhas)}</div></aside>'
    if tipo == 'hud':
        ics = ['vida', 'ataque', 'dano', 'fase']
        return '<div class="hud">' + ''.join(f'<div>{icone(ics[i], "")}<b>{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'numeros':
        cs = ['fogo', 'azul', 'grana', 'roxo']
        return '<div class="numeros">' + ''.join(f'<div><b style="color:{cor(cs[i])}">{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'ranking':
        rows = campos(linhas); mx = max(float(r[3].replace(',', '.')) for r in rows); out = []
        for nome, anual, mens, rs in rows:
            v = float(rs.replace(',', '.')); c = C['fogo'] if v > 120 else C['laranja'] if v > 80 else C['roxo'] if v > 60 else C['azul'] if v > 30 else C['grana']
            sub = f'{mens}% ao mês · {anual}' + ('% ao ano' if anual[0].isdigit() else '')
            out.append(f'<div class="rk"><div class="rk-n">{inl(nome)}<span>{sub}</span></div><div class="rk-t"><div style="width:{max(3, v / mx * 100):.1f}%;background:{c}"></div></div><b>R$ {rs}</b></div>')
        return '<figure class="ranking"><figcaption>Juros de um mês sobre R$ 1.000 · médias do Banco Central</figcaption>' + ''.join(out) + '</figure>'
    if tipo == 'chefao':
        d, _ = chaves(linhas); nv = int(d.get('nivel', 3)); a = d.get('arte', 'rotativo'); c = cor(COR_ARTE.get(a, COR_NIVEL[nv]))
        pips = ''.join(f'<i style="{"background:" + c if i < nv else ""}"></i>' for i in range(5))
        return (f'<article class="carta" style="--c:{c}"><div class="carta-arte" style="background:{c}22">{arte(a, 150)}</div>'
                f'<span class="carta-tipo">{inl(d.get("dívida", ""))}</span><h4>{inl(d["nome"])}</h4>'
                f'<div class="carta-atk" style="color:{c}">{inl(d.get("ataque", ""))}</div><div class="pips">PERIGO {pips}</div>'
                f'<dl><dt>Como aparece</dt><dd>{inl(d.get("como_aparece", ""))}</dd><dt>Ponto fraco</dt><dd>{inl(d.get("ponto_fraco", ""))}</dd></dl></article>')
    if tipo == 'grafico': return grafico(linhas[0].strip())
    if tipo == 'formula': return f'<div class="formula">{inl(" ".join(linhas))}</div>'
    if tipo == 'ficha': return ficha_html(campos(linhas))
    if tipo == 'regras':
        cs = ['azul', 'roxo', 'grana']
        return '<div class="regras">' + ''.join(f'<div><b style="background:{cor(cs[i])}">{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'tabela':
        rows = campos(linhas)
        return ('<table class="tab"><thead><tr>' + ''.join(f'<th>{inl(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>'
                + ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table>')
    if tipo == 'aposta': return f'<aside class="aposta"><span class="q">?</span><div><span class="pilula az">APOSTE</span>{paragrafos(linhas)}<div class="campo-l">{campo_linha("Minha aposta:")}</div></div>{arte("din", 70)}</aside>'
    if tipo == 'campo':
        ajuda = ' '.join(l.strip() for l in linhas[1:] if l.strip())
        return f'<div class="campo-l solto">{campo_linha(linhas[0].strip())}' + (f'<p class="campo-ajuda">{inl(ajuda)}</p>' if ajuda else '') + '</div>'
    if tipo == 'extrato':
        d, _ = chaves(linhas)
        chips = ''.join(f'<span>{inl(x.strip())}</span>' for x in d.get('juros', '').split('|'))
        vit = f'<div class="ex-vit">{inl(d["vitoria"])}</div>' if d.get('vitoria') else ''
        return (f'<section class="extrato"><div class="ex-cab"><b>Extrato do mês {d["mes"]}</b><span class="pilula">AVALANCHE</span></div>'
                f'<div class="ex-p"><i style="background:{C["fogo"]}">1</i><p>Os chefões atacam: <strong>+{inl(d["total_juros"])}</strong> de juros.<span class="chips">{chips}</span></p></div>'
                f'<div class="ex-p"><i style="background:{C["azul"]}">2</i><p>Você paga o mínimo de cada um: <strong>−{inl(d["minimos"])}</strong>.</p></div>'
                f'<div class="ex-p"><i style="background:{C["grana"]}">3</i><p>{inl(d["terceiro"])}</p></div>'
                f'<div class="ex-s">{inl(d["saldo"])}</div>{vit}</section>')
    if tipo == 'batalha':
        cls = ['perde', 'meio', 'ganha']
        return '<div class="batalha">' + ''.join(f'<div class="bt {cls[min(i, 2)]}"><b>{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'golpe':
        d, resto = chaves(linhas); c = cor(d.get('cor', 'azul'))
        ic = ICONES_GOLPE.get(d['titulo'], '')
        return f'<article class="golpe" style="--c:{c}"><div class="g-cab"><span class="g-ic" style="background:{c}26"><svg viewBox="0 0 24 24" width="30" height="30">{ic}</svg></span><h4>{inl(d["titulo"])}</h4></div>{paragrafos(sum(([r, ""] for r in resto), []))}</article>'
    if tipo == 'escudos':
        cs = ['grana', 'azul', 'roxo', 'laranja']
        return '<div class="escudos">' + ''.join(f'<div><svg viewBox="0 0 24 24" width="54" height="54"><path d="M12 2 L21 5 V11 Q21 18 12 22 Q3 18 3 11 V5Z" fill="{cor(cs[i])}" stroke="{C["tinta"]}" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg><b>{inl(a)}</b><span>{inl(b)}</span></div>' for i, (a, b) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'plano':
        NCAMPO[0] += 1; base = NCAMPO[0]
        return '<div class="plano">' + ''.join(f'<div class="pl"><i>{mk(f"c{base}x{k}")}</i><div><small>{inl(s)}</small><b>{inl(t)}</b><span>{inl(x)}</span></div></div>' for k, (s, t, x) in enumerate(campos(linhas))) + '</div>'
    if tipo == 'fichas':
        n = int(linhas[0].strip())
        cf = [['Nome do chefão', ''], ['Onde está (banco, loja)', ''], ['Vida (saldo devedor hoje)', 'R$'], ['Ataque (taxa ao mês)', '%'], ['Ataque do mês (vida × taxa)', 'R$'], ['Parcela ou mínimo', 'R$'], ['Parcelas que faltam', ''], ['Atrasada? Há quanto tempo?', ''], ['Estratégia e ataque especial', '']]
        return '<div class="fichas">' + ''.join(ficha_html(cf, f'Ficha {i + 1}') for i in range(n)) + '</div>'
    raise ValueError('bloco desconhecido: ' + tipo)

def ficha_html(rows, titulo='Ficha do chefão'):
    ls = ''.join(campo_linha(a, b[0] if b and b[0] else '') for a, *b in rows)
    return f'<div class="ficha"><div class="fi-top">{arte("din", 34)}<b>{titulo}</b></div>{ls}</div>'

# ---------- seções ----------
def ler(pasta):
    t = (pasta / 'texto.md').read_text(encoding='utf-8'); meta = {}
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if m:
        for l in m.group(1).splitlines(): k, v = l.split(':', 1); meta[k.strip()] = v.strip()
        t = t[m.end():]
    secs, at = [], None
    for l in t.splitlines():
        if l.startswith('# '): at = {'titulo': l[2:].strip(), 'linhas': []}; secs.append(at)
        elif at is not None: at['linhas'].append(l)
    return meta, secs

def corpo(linhas):
    """Separa blocos; cartas de chefão e golpes seguidos viram uma grade."""
    itens, buf, i = [], [], 0
    while i < len(linhas):
        s = linhas[i].strip()
        if s.startswith(':::') and len(s) > 3:
            if any(x.strip() for x in buf): itens.append(('p', paragrafos(buf)))
            buf = []
            tipo = s[3:].strip(); j = i + 1; dentro = []
            while linhas[j].strip() != ':::': dentro.append(linhas[j]); j += 1
            itens.append((tipo, dentro)); i = j + 1; continue
        buf.append(linhas[i]); i += 1
    if any(x.strip() for x in buf): itens.append(('p', paragrafos(buf)))
    out, grupo, gtipo = [], [], None
    def fecha():
        nonlocal grupo, gtipo
        if grupo: out.append(f'<div class="grade-{gtipo}">' + ''.join(grupo) + '</div>'); grupo = []; gtipo = None
    for tipo, cont in itens:
        if tipo in ('chefao', 'golpe'):
            if gtipo != tipo: fecha(); gtipo = tipo
            grupo.append(bloco(tipo, cont)); continue
        fecha()
        if tipo == 'p': out.append(cont)
        elif tipo in ('abertura', 'mundo2'): continue
        else: out.append(bloco(tipo, cont))
    fecha()
    return '\n'.join(out)

def abertura_html(n, titulo, d):
    c = cor(d.get('cor', 'azul')); a = d.get('arte', 'rotativo')
    escuro = d.get('cor') in ('amarelo', 'grana', 'ciano')
    return (f'<section class="abertura" id="fase-{n}" style="background:{c};color:{C["tinta"] if escuro else "#fff"}"><a class="ab-mapa" href="#mapa">← mapa do jogo</a><div class="ab-num">{n}</div>'
            f'<div class="ab-txt"><span class="ab-rot" style="background:{C["tinta"] if escuro else "#ffffff2e"};color:#fff">FASE {n} DE 6</span><h1>{inl(titulo)}</h1><p>{inl(d.get("promessa", ""))}</p></div>'
            f'<div class="ab-arte">{arte(a, 420)}</div><div class="ab-chao"></div></section>')

def mundo2_html(titulo, linhas):
    d = [l for l in linhas if l.strip()]
    txt = [l for l in d if '|' not in l]; mundos = campos([l for l in d if '|' in l])
    cards = ''.join(f'<div class="mundo {"feito" if i == 0 else ""}">{"" if i == 0 else icone("cadeado", "")}<small>{inl(a)}</small><b>{inl(b)}</b><span>{inl(c)}</span></div>' for i, (a, b, c) in enumerate(mundos))
    cofre = (f'<svg viewBox="0 0 150 140" width="220" height="205"><ellipse cx="75" cy="132" rx="52" ry="6" fill="#000" opacity=".25"/><rect x="18" y="22" width="114" height="104" rx="20" fill="{C["amarelo"]}" stroke="{C["tinta"]}" stroke-width="4"/>'
             f'<rect x="30" y="34" width="90" height="80" rx="12" fill="{C["amarelo_esc"]}" stroke="{C["tinta"]}" stroke-width="3"/><circle cx="75" cy="74" r="22" fill="#fff" stroke="{C["tinta"]}" stroke-width="4"/>'
             f'<path d="M75 58v32M59 74h32" stroke="{C["tinta"]}" stroke-width="4" stroke-linecap="round"/><rect x="120" y="54" width="8" height="40" rx="4" fill="{C["tinta"]}"/></svg>')
    return (f'<section class="mundo2" id="mundo-2"><a class="ab-mapa" href="#mapa">← mapa do jogo</a><span class="ab-rot" style="background:{C["amarelo"]};color:{C["tinta"]}">FIM DE JOGO? AINDA NÃO</span><h1>{inl(titulo.replace(" · ", ": "))}</h1>'
            f'<div class="m2-topo"><div>{"".join("<p>" + inl(t) + "</p>" for t in txt)}</div>{cofre}</div><div class="mundos">{cards}</div>'
            f'<p class="m2-pe">O minicurso continua daqui. Fique de olho na área de membros.</p></section>')

def mapa_html(secs):
    fases = [re.match(r'Fase (\d+) · (.*)', s['titulo']) for s in secs]; fases = [f for f in fases if f]
    cores = ['fogo', 'laranja', 'azul', 'roxo', 'amarelo', 'grana']
    nos = ''
    for i, f in enumerate(fases):
        lado = 'esq' if i % 2 == 0 else 'dir'
        nos += f'<a class="no {lado}" href="#fase-{f.group(1)}"><span class="bola" style="background:{cor(cores[i])}">{f.group(1)}</span><div><small>FASE {f.group(1)}</small><b>{inl(f.group(2))}</b></div></a>'
    nos += f'<a class="no esq trancado" href="#mundo-2"><span class="bola" style="background:{C["noite"]}">{icone("cadeado", "")}</span><div><small>MUNDO 2</small><b>O Cofre</b></div></a>'
    return f'<section class="mapa" id="mapa"><h2>O mapa do jogo</h2><p>Seis fases para derrotar os chefões. No fim, o próximo mundo. <strong>Toque em uma fase para ir até ela.</strong></p><div class="trilha"><svg class="caminho" viewBox="0 0 100 700" preserveAspectRatio="none"><path d="M30 30 C 90 80, 90 120, 70 130 S 10 210, 30 230 S 90 320, 70 330 S 10 410, 30 430 S 90 520, 70 530 S 10 610, 30 640" fill="none" stroke="{C["linha"]}" stroke-width="7" stroke-dasharray="2 14" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>{nos}</div></section>'

def secao_html(sec):
    m = re.match(r'(Fase (\d+)|Mundo (\d+)) · (.*)', sec['titulo'])
    if m and m.group(3):
        return mundo2_html(sec['titulo'], bloco_conteudo(sec['linhas'], 'mundo2') or [])
    if m:
        ab, _ = chaves(bloco_conteudo(sec['linhas'], 'abertura') or [])
        return abertura_html(m.group(2), m.group(4), ab) + f'<section class="pag">{corpo(sec["linhas"])}</section>'
    cls = 'junto' if sec['titulo'] == 'Fontes' else 'pag' + (' fichas-sec' if 'Fichas' in sec['titulo'] else '')
    return f'<section class="{cls}"><h2>{inl(sec["titulo"])}</h2>{corpo(sec["linhas"])}</section>'

def bloco_conteudo(linhas, tipo):
    for i, l in enumerate(linhas):
        if l.strip() == ':::' + tipo:
            j = i + 1; out = []
            while linhas[j].strip() != ':::': out.append(linhas[j]); j += 1
            return out
    return None

def capa_html(meta):
    desfile = ''.join(arte(a, w) for a, w in [('cheque', 120), ('parcelado', 130), ('rotativo', 230), ('pessoal', 130), ('consignado', 115)])
    return f'''<section class="capa">
  <div class="capa-top"><span class="selo">{arte("din", 30)}{inl(meta.get("autor", ""))} · ebook + simulador</span><span>{inl(meta.get("edicao", ""))}</span></div>
  <h1 class="capa-tit">Chefões<span>do cartão</span></h1>
  <p class="capa-sub">{inl(meta.get("subtitulo", ""))}</p>
  <div class="desfile">{desfile}</div><div class="capa-chao"></div>
  <div class="chips"><span>9 chefões</span><span>6 ataques especiais</span><span>simulador da batalha</span><span>plano de 90 dias</span></div>
  <p class="capa-pe">Juros médios do Banco Central ({inl(meta.get("dados", ""))}). Conteúdo educativo: não é recomendação de investimento.</p>
</section>'''

def css(cel):
    f = lambda nome, arq, peso: f"@font-face{{font-family:'{nome}';src:url('{(FONTES / arq).as_uri()}');font-weight:{peso}}}"
    fontes = ''.join([f('Baloo 2', 'Baloo2-800.woff2', 800), f('Baloo 2', 'Baloo2-700.woff2', 700)] + [f('Nunito', f'Nunito-{w}.woff2', w) for w in (400, 600, 700, 800, 900)])
    pag = '110mm 196mm' if cel else 'A4'
    mg = '9mm 8mm 12mm' if cel else '16mm 17mm 18mm'
    k = lambda a, b: b if cel else a   # a = A4, b = celular
    T = C['tinta']
    return f'''{fontes}
@page{{size:{pag};margin:{mg}}}
@page cheia{{margin:0}}
*{{box-sizing:border-box}}
html{{font-family:Nunito,sans-serif;font-size:{k("11.6pt","10.6pt")};line-height:1.55;color:{T};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{margin:0;background:{C["papel"]}}}
h1,h2,h3,h4,.disp{{font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;line-height:1.02;letter-spacing:-.01em;margin:0}}
p{{margin:0 0 .75em;orphans:3;widows:3}} strong{{font-weight:800}}
ul,ol{{margin:0 0 .9em;padding-left:1.3em}} li{{margin:.25em 0;break-inside:avoid}}
h2{{font-size:{k("2.5em","2em")};margin:0 0 .5em}}
h3{{font-size:{k("1.55em","1.35em")};margin:1.2em 0 .45em;break-after:avoid}}
.pag{{break-before:page}} .junto{{margin-top:12mm}}
.pilula{{display:inline-block;font-weight:900;font-size:.7em;letter-spacing:.14em;border-radius:99px;padding:.25em .8em;background:{C["fogo"]};color:#fff;margin-bottom:.5em}}
.pilula.am{{background:{C["amarelo"]};color:{T}}} .pilula.az{{background:{C["azul"]}}}
.arte{{display:block;overflow:visible}}
/* capa */
.capa{{page:cheia;height:{k("297mm","196mm")};background:{T};color:#fff;padding:{k("20mm 18mm","11mm 9mm")};display:flex;flex-direction:column;gap:{k("7mm","4mm")};overflow:hidden}}
.capa-top{{display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:.85em;color:#9DB8AC;gap:8px}}
.selo{{display:inline-flex;align-items:center;gap:8px;background:#244038;border-radius:99px;padding:5px 14px 5px 6px;color:#fff}}
.capa-tit{{font-size:{k("6.4em","3.6em")};line-height:.86;text-transform:uppercase;margin-top:{k("14mm","6mm")}}}
.capa-tit span{{display:block;color:{C["amarelo"]}}}
.capa-sub{{font-size:{k("1.55em","1.2em")};font-weight:800;color:#BFE9D2;max-width:22em}}
.desfile{{display:flex;align-items:flex-end;justify-content:center;margin-top:auto}}
.desfile svg{{height:auto}} .desfile svg:nth-child(1),.desfile svg:nth-child(5){{width:{k("18%","17%")}}} .desfile svg:nth-child(2),.desfile svg:nth-child(4){{width:{k("20%","19%")}}} .desfile svg:nth-child(3){{width:{k("33%","32%")}}}
.capa-chao{{height:14px;border-radius:99px;background:#244038;margin-top:-12px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}} .chips span{{border:2px solid #3B5C51;border-radius:99px;padding:3px 13px;font-weight:800;font-size:.86em;color:#D6F1E3}}
.capa-pe{{font-size:.78em;color:#9DB8AC;margin:0}}
/* mapa */
.mapa{{break-before:page}} .mapa h2{{margin-bottom:.2em}} .mapa>p{{color:{C["apagado"]};font-size:1.1em}}
.trilha{{position:relative;height:{k("205mm","140mm")};margin-top:6mm}}
.caminho{{position:absolute;inset:0 {k("20%","10%")};width:{k("60%","80%")};height:100%}}
.no{{position:absolute;display:flex;align-items:center;gap:14px;width:{k("62%","80%")}}}
.no.esq{{left:{k("6%","0")}}} .no.dir{{right:{k("6%","0")};flex-direction:row-reverse;text-align:right}}
.no .bola{{width:{k("74px","52px")};height:{k("74px","52px")};border-radius:50%;display:grid;place-items:center;color:#fff;font-family:'Baloo 2';font-weight:800;font-size:{k("2.2em","1.6em")};border:4px solid {T};box-shadow:0 6px 0 {T};flex:none}}
.no small{{display:block;font-weight:900;letter-spacing:.14em;font-size:.72em;color:{C["apagado"]}}} .no b{{font-family:'Baloo 2';font-size:{k("1.45em","1.15em")};line-height:1.05}}
{''.join(f'.no:nth-of-type({i + 1}){{top:{i * (100 / 7):.1f}%}}' for i in range(7))}
.no.trancado .bola{{border-color:{C["noite_esc"]};box-shadow:0 6px 0 {C["noite_esc"]}}}
/* abertura de fase */
.abertura{{page:cheia;break-before:page;height:{k("297mm","196mm")};padding:{k("22mm 18mm","12mm 9mm")};position:relative;overflow:hidden;display:flex;flex-direction:column}}
.ab-num{{position:absolute;right:{k("-6mm","-3mm")};top:{k("-22mm","-12mm")};font-family:'Baloo 2';font-weight:800;font-size:{k("150mm","95mm")};line-height:1;opacity:.16}}
.ab-rot{{display:inline-block;font-weight:900;letter-spacing:.16em;font-size:.8em;border-radius:99px;padding:.35em 1em}}
.ab-txt h1{{font-size:{k("4.2em","2.7em")};margin:.25em 0 .3em;max-width:9em}}
.ab-txt p{{font-size:{k("1.35em","1.1em")};font-weight:700;max-width:24em;opacity:.95}}
.ab-arte{{margin-top:auto;display:flex;justify-content:center}} .ab-arte svg{{width:{k("118mm","70mm")};height:auto}}
.ab-chao{{height:16px;border-radius:99px;background:#0000001f;margin:-14px {k("30mm","16mm")} 0}}
/* blocos */
.din{{display:grid;grid-template-columns:66px 1fr;gap:12px;align-items:start;margin:1.1em 0;break-inside:avoid}}
.balao{{background:{C["amarelo_cl"]};border:2.5px solid {C["amarelo"]};border-radius:4px 20px 20px 20px;padding:.8em 1em .1em;font-weight:600}}
.balao strong{{color:#8A5A00}}
.alerta{{border:2.5px solid {C["fogo"]};background:{C["fogo_cl"]};border-radius:18px;padding:.9em 1.1em .2em;margin:1.1em 0;break-inside:avoid}}
.missao{{background:{T};color:#fff;border-radius:20px;padding:1em 1.2em .3em;margin:1.3em 0;display:grid;grid-template-columns:44px 1fr;gap:12px;break-inside:avoid;box-shadow:0 6px 0 {C["grana"]}}}
.missao strong{{color:{C["amarelo"]}}} .m-ic svg{{width:40px;height:40px}}
.hud{{display:grid;grid-template-columns:{k("repeat(4,1fr)","1fr 1fr")};gap:10px;margin:1em 0 1.3em}}
.hud div{{background:{C["cartao"]};border:2.5px solid {C["linha"]};border-radius:16px;padding:.7em .8em;box-shadow:0 5px 0 {C["linha"]}}}
.hud b{{display:block;font-family:'Baloo 2';font-size:1.25em;margin-top:.2em}} .hud span{{font-size:.86em;color:{C["apagado"]};line-height:1.3;display:block}}
.numeros{{display:grid;grid-template-columns:1fr 1fr;gap:{k("8mm","4mm")};margin:1.2em 0;break-inside:avoid}}
.numeros b{{display:block;font-family:'Baloo 2';font-weight:800;font-size:{k("4.2em","3em")};line-height:.95}} .numeros span{{font-weight:700;color:{C["apagado"]};font-size:.95em}}
.ranking{{margin:1.2em 0;break-inside:avoid}} figcaption{{font-weight:900;font-size:.72em;letter-spacing:.12em;text-transform:uppercase;color:{C["apagado"]};margin-bottom:.7em}}
.rk{{display:grid;grid-template-columns:{k("12.5em 1fr 5.6em","9.5em 1fr 5em")};gap:10px;align-items:center;margin:.45em 0}}
.rk-n{{font-weight:800;line-height:1.15}} .rk-n span{{display:block;font-size:.75em;color:{C["apagado"]};font-weight:700}}
.rk-t{{height:{k("24px","18px")};background:#EDF3EE;border-radius:9px;overflow:hidden}} .rk-t div{{height:100%;border-radius:9px}}
.rk b{{font-family:'Baloo 2';font-size:1.15em;text-align:right}}
.grade-chefao{{display:grid;grid-template-columns:{k("1fr 1fr","1fr")};gap:{k("7mm","5mm")};margin:1em 0}}
.carta{{border:3px solid {T};border-radius:22px;padding:12px;background:{C["cartao"]};box-shadow:0 7px 0 var(--c);break-inside:avoid;display:grid;gap:5px;align-content:start}}
.carta-arte{{border-radius:15px;display:flex;justify-content:center;padding:8px 0 2px}} .carta-arte svg{{width:{k("118px","96px")};height:auto}}
.carta-tipo{{font-size:.72em;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:{C["apagado"]};margin-top:4px}}
.carta h4{{font-size:1.4em}} .carta-atk{{font-family:'Baloo 2';font-weight:800;font-size:1.35em;line-height:1.1}}
.pips{{display:flex;gap:4px;align-items:center;font-size:.66em;font-weight:900;letter-spacing:.1em;color:{C["apagado"]}}} .pips i{{width:17px;height:9px;border-radius:3px;background:#E3EAE4}}
.carta dl{{margin:.3em 0 0;border-top:2px dashed {C["linha"]};padding-top:.4em}} .carta dt{{font-weight:900;font-size:.68em;letter-spacing:.1em;text-transform:uppercase;margin-top:.35em}} .carta dd{{margin:0;font-size:.88em;line-height:1.4}}
.graf{{margin:1.2em 0;background:{C["cartao"]};border:2.5px solid {C["linha"]};border-radius:20px;padding:14px 14px 10px;break-inside:avoid}}
.graf text{{font-family:Nunito;font-size:12px;font-weight:700;fill:{C["apagado"]}}}
.leg{{display:flex;flex-wrap:wrap;gap:14px;font-weight:800;font-size:.85em;margin-top:6px}} .leg span{{display:inline-flex;align-items:center;gap:6px}} .leg i{{width:18px;height:6px;border-radius:9px;display:inline-block}} .leg .eixo{{color:{C["apagado"]};margin-left:auto}}
.formula{{font-family:'Baloo 2';font-weight:800;font-size:{k("1.7em","1.3em")};text-align:center;padding:.6em;border:3px dashed {C["grana"]};border-radius:20px;margin:1em 0;background:{C["grana_cl"]}}}
.regras{{display:grid;grid-template-columns:{k("repeat(3,1fr)","1fr")};gap:10px;margin:1.2em 0;break-inside:avoid}}
.regras div{{background:{C["cartao"]};border:2.5px solid {C["linha"]};border-radius:18px;padding:.8em .9em;font-weight:700;line-height:1.35}}
.regras b{{display:grid;place-items:center;width:36px;height:36px;border-radius:12px;color:#fff;font-family:'Baloo 2';font-size:1.3em;margin-bottom:.4em}}
.tab{{width:100%;border-collapse:separate;border-spacing:0;margin:1em 0 1.2em;font-size:.92em;break-inside:avoid}}
.tab th{{background:{T};color:#fff;text-align:left;padding:.5em .7em;font-weight:800}} .tab th:first-child{{border-radius:12px 0 0 0}} .tab th:last-child{{border-radius:0 12px 0 0}}
.tab td{{padding:.5em .7em;border-bottom:2px solid {C["linha"]};font-weight:700}}
.aposta{{display:grid;grid-template-columns:62px 1fr 70px;gap:14px;align-items:center;background:#EAF6FE;border:3px solid {C["azul"]};border-radius:22px;padding:1em 1.1em .5em;margin:1.3em 0;break-inside:avoid;box-shadow:0 6px 0 {C["azul"]}}}
.aposta .q{{width:58px;height:58px;border-radius:18px;background:{C["azul"]};color:#fff;display:grid;place-items:center;font-family:'Baloo 2';font-weight:800;font-size:2.4em}}
.extrato{{border:3px dashed {C["linha"]};border-radius:22px;padding:14px 16px;margin:1.1em 0;display:grid;gap:9px;break-inside:avoid;background:{C["cartao"]}}}
.ex-cab{{display:flex;justify-content:space-between;align-items:center}} .ex-cab b{{font-family:'Baloo 2';font-size:1.45em}} .ex-cab .pilula{{background:{C["linha"]};color:{C["apagado"]};margin:0}}
.ex-p{{display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:start}} .ex-p i{{font-style:normal;width:34px;height:34px;border-radius:11px;display:grid;place-items:center;color:#fff;font-weight:900}} .ex-p p{{margin:.2em 0 0}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin-top:5px}} .ex-p .chips span{{font-size:.8em;font-weight:800;border-radius:99px;padding:2px 10px;background:{C["bg"]};border:1.5px solid {C["linha"]};color:{T}}}
.ex-s{{background:{C["grana_cl"]};color:{C["grana_esc"]};border-radius:14px;padding:.6em .9em;font-weight:800}}
.ex-vit{{background:{C["amarelo_cl"]};border:2.5px solid {C["amarelo"]};border-radius:14px;padding:.6em .9em;font-weight:800}}
.batalha{{display:grid;grid-template-columns:{k("repeat(3,1fr)","1fr")};gap:10px;margin:1.1em 0;break-inside:avoid}}
.bt{{border-radius:20px;padding:.9em 1em;border:3px solid;display:grid;gap:4px;align-content:start}} .bt b{{font-family:'Baloo 2';font-size:1.15em;line-height:1.1}} .bt span{{font-size:.92em;font-weight:700}}
.bt.perde{{background:{C["fogo_cl"]};border-color:{C["fogo"]}}} .bt.meio{{background:{C["amarelo_cl"]};border-color:{C["amarelo_esc"]}}} .bt.ganha{{background:{C["grana_cl"]};border-color:{C["grana"]};box-shadow:0 0 0 4px {C["azul"]}}}
.grade-golpe{{display:grid;grid-template-columns:{k("1fr 1fr","1fr")};gap:{k("6mm","4mm")};margin:1em 0}}
.golpe{{border:3px solid {T};border-radius:22px;padding:14px 16px 4px;background:{C["cartao"]};box-shadow:0 6px 0 var(--c);break-inside:avoid}}
.g-cab{{display:flex;align-items:center;gap:10px;margin-bottom:.5em}} .g-ic{{width:48px;height:48px;border-radius:15px;display:grid;place-items:center;flex:none}} .golpe h4{{font-size:1.35em}} .golpe p{{font-size:.93em}}
.escudos{{display:grid;grid-template-columns:{k("1fr 1fr","1fr")};gap:10px;margin:1.1em 0}}
.escudos div{{display:grid;grid-template-columns:58px 1fr;gap:4px 12px;align-items:center;background:{C["cartao"]};border:2.5px solid {C["linha"]};border-radius:18px;padding:.8em;break-inside:avoid}}
.escudos svg{{grid-row:span 2}} .escudos b{{font-family:'Baloo 2';font-size:1.2em;line-height:1.1}} .escudos span{{font-size:.88em;color:#3A564D;line-height:1.35}}
.plano{{display:grid;grid-template-columns:{k("1fr 1fr","1fr")};gap:8px 14px;margin:1em 0}}
.pl{{display:grid;grid-template-columns:28px 1fr;gap:10px;border-bottom:2px solid {C["linha"]};padding:.3em 0 .6em;break-inside:avoid}}
.pl i{{width:26px;height:26px;border:3px solid {T};border-radius:8px;margin-top:3px}} .pl small{{font-weight:900;font-size:.68em;letter-spacing:.12em;text-transform:uppercase;color:{C["grana_esc"]}}} .pl b{{display:block;font-family:'Baloo 2';font-size:1.15em;line-height:1.1}} .pl span{{font-size:.88em;color:#3A564D}}
.ficha{{border:3px solid {T};border-radius:20px;padding:.8em 1em .5em;margin:0 0 7mm;break-inside:avoid;background:{C["cartao"]}}}
.fi-top{{display:flex;align-items:center;gap:8px;font-family:'Baloo 2';font-size:1.2em;margin-bottom:.2em}} .fi-top b{{font-weight:800}}
.fi-l{{display:flex;align-items:flex-end;gap:8px;border-bottom:2px dotted {C["apagado"]};padding:{k(".75em",".6em")} 0 .2em;font-size:.9em}}
.fi-l span{{font-weight:800;white-space:nowrap}} .fi-l em{{font-style:normal;color:{C["apagado"]};margin-left:auto;padding-right:{k("7em","2.5em")}}}
.fichas .ficha:nth-child(2n){{{"" if cel else "break-after:page"}}}
/* interatividade */
a{{color:inherit;text-decoration:none}}
.mk,.pl .mk,.fi-l .mk{{font-size:2px!important;line-height:0!important;color:rgba(255,255,255,0)!important;letter-spacing:0!important;white-space:nowrap;font-weight:400!important}}
.fi-l .esp{{flex:1;min-width:30px}} .fi-l em{{margin-left:.4em;padding-right:0}}
.pl i{{display:grid;place-items:center}} .pl i .mk{{position:relative;top:9px}}
.campo-l .fi-l{{border-bottom:2px dotted currentColor;margin-top:.4em;padding-top:.3em}}
.campo-l.solto{{background:{C["cartao"]};border:2.5px solid {C["linha"]};border-radius:16px;padding:.2em 1em .6em;margin:1em 0}}
.campo-ajuda{{font-size:.78em;line-height:1.35;color:{C["apagado"]};margin:.45em 0 0;font-weight:600}}
.ab-mapa{{position:absolute;top:{k("9mm","5mm")};right:{k("18mm","9mm")};font-weight:900;font-size:.8em;letter-spacing:.06em;border:2px solid currentColor;border-radius:99px;padding:.25em .9em;z-index:2;opacity:.9}}
.mundo2{{position:relative;overflow:hidden}}
/* mundo 2 */
.mundo2{{page:cheia;break-before:page;height:{k("297mm","196mm")};background:{C["noite_esc"]};color:#fff;padding:{k("22mm 18mm","12mm 9mm")};display:flex;flex-direction:column;gap:{k("7mm","4mm")}}}
.mundo2 .ab-rot{{align-self:flex-start}}
.mundo2 h1{{font-size:{k("4em","2.6em")};margin-top:.2em}}
{'.mundo2 h1{font-size:2.2em}.m2-topo p{font-size:.92em;margin-bottom:.5em}.mundo{padding:.6em .8em}.mundo b{font-size:1.1em}.mundo span{font-size:.8em}.m2-topo svg{display:none}' if cel else ''}
.m2-topo{{display:grid;grid-template-columns:{k("1fr 220px","1fr")};gap:8mm;align-items:center}} .m2-topo p{{font-size:{k("1.2em","1em")};color:#E3DCF8}} .m2-topo strong{{color:{C["amarelo"]}}}
{"" if not cel else ".m2-topo svg{width:120px;height:auto}"}
.mundos{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:auto}}
.mundo{{border-radius:18px;padding:.9em 1em;border:2px solid #ffffff38;background:#ffffff10;position:relative}}
.mundo small{{display:block;font-weight:900;letter-spacing:.14em;font-size:.7em;color:{C["amarelo"]}}} .mundo b{{font-family:'Baloo 2';font-size:1.35em;display:block}} .mundo span{{font-size:.88em;color:#D5CCF0}}
.mundo.feito{{background:{C["grana"]};border-color:{C["grana"]}}} .mundo.feito small,.mundo.feito span{{color:#fff}}
.mundo svg{{position:absolute;top:12px;right:12px}}
.m2-pe{{color:#CFC5EE;font-weight:700;margin:0}}
'''

def montar(pasta, cel):
    meta, secs = ler(pasta)
    corpo_html = capa_html(meta) + mapa_html(secs) + ''.join(secao_html(s) for s in secs)
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{inl(meta.get("titulo", ""))}</title><style>{css(cel)}</style></head><body>{corpo_html}</body></html>', meta

def pdf(pasta, cel):
    from playwright.sync_api import sync_playwright
    doc, meta = montar(pasta, cel)
    build = pasta / 'build'; build.mkdir(exist_ok=True)
    nome = pasta.name + ('-celular' if cel else '')
    a = build / f'{nome}.html'; a.write_text(doc, encoding='utf-8')
    rodape = (f'<div style="width:100%;font-family:Arial;font-size:7.5px;color:{C["apagado"]};padding:0 {"8mm" if cel else "17mm"};display:flex;justify-content:space-between">'
              f'<span>{html.escape(meta.get("titulo", ""))} · {html.escape(meta.get("autor", ""))}</span><span class="pageNumber"></span></div>')
    saida = pasta / f'{nome}.pdf'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(a.as_uri()); pg.wait_for_timeout(500)
        pg.pdf(path=str(saida), prefer_css_page_size=True, display_header_footer=True, header_template='<span></span>', footer_template=rodape)
        b.close()
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(str(saida)); w = PdfWriter()
    from pypdf.generic import StreamObject, ArrayObject
    rgb = ' '.join(f'{int(C["papel"][i:i + 2], 16) / 255:.3f}' for i in (1, 3, 5))
    for pgn in r.pages:
        pg2 = w.add_page(pgn); W_, H_ = float(pg2.mediabox.width), float(pg2.mediabox.height)
        fundo = StreamObject(); fundo.set_data(f'q {rgb} rg 0 0 {W_:.2f} {H_:.2f} re f Q\n'.encode())
        bruto = pg2.raw_get('/Contents'); conteudo = bruto.get_object()
        lista = [conteudo.raw_get(i) for i in range(len(conteudo))] if isinstance(conteudo, ArrayObject) else [bruto]
        pg2[NameObject('/Contents')] = ArrayObject([w._add_object(fundo)] + lista)
    w.add_metadata({'/Title': meta.get('titulo', ''), '/Author': meta.get('autor', ''), '/Subject': meta.get('subtitulo', '')})
    with open(saida, 'wb') as fh: w.write(fh)
    sys.path.insert(0, str(Path(__file__).parent)); from pdf_campos import main as campos
    campos(str(saida))   # marcadores invisíveis → campos preenchíveis e caixas de marcar
    return saida, len(r.pages)

def previa(arq_pdf, saida, paginas):
    import pypdfium2 as pdfium
    from PIL import Image
    d = pdfium.PdfDocument(str(arq_pdf)); ims = [d[i].render(scale=1.1).to_pil() for i in paginas if i < len(d)]
    h = max(i.height for i in ims); gap = 24
    tela = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) + 1), h + gap * 2), (214, 224, 216)); x = gap
    for im in ims: tela.paste(im, (x, gap)); x += im.width + gap
    tela.save(saida)

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    pasta = (RAIZ / sys.argv[1]).resolve()
    for svg in (pasta / 'arte').glob('*.svg'): ARTE[svg.stem] = svg.read_text(encoding='utf-8')
    if (pasta / 'contas.py').exists():
        spec = importlib.util.spec_from_file_location('contas', pasta / 'contas.py'); CONTAS = importlib.util.module_from_spec(spec); spec.loader.exec_module(CONTAS)
    a4, n = pdf(pasta, False); print(a4.relative_to(RAIZ), n, 'páginas')
    cel, n2 = pdf(pasta, True); print(cel.relative_to(RAIZ), n2, 'páginas')
    previa(a4, pasta / 'previa.png', [0, 2, 3]); print((pasta / 'previa.png').relative_to(RAIZ))
