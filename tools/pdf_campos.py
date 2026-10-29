"""Transforma os marcadores invisíveis de um PDF da fábrica em campos interativos (AcroForm).
O tools/ebook.py escreve marcadores de texto transparente: QZt<n>aZQ ... QZt<n>bZQ (início e fim de um campo de texto)
e QZc<n>x<k>ZQ (centro de uma caixa de marcar). Este script acha cada marcador, cria o campo no lugar e salva o PDF.
Uso: python3 tools/pdf_campos.py <arquivo.pdf> [caixa_px=26]
Funciona nos leitores comuns (Adobe, Chrome, Edge, Preview/iOS, a maioria dos apps de Android).
"""
import re, sys
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, FloatObject, NameObject, NumberObject,
                           StreamObject, TextStringObject)

PADRAO = re.compile(r'QZ([tc]\d+(?:[ab]|x\d+))ZQ')

def achar(pdf):
    """{página: [(id, x0, y0, x1, y1)]} em pontos do PDF (origem embaixo à esquerda)."""
    doc = pdfium.PdfDocument(pdf); achados = {}
    for i in range(len(doc)):
        tp = doc[i].get_textpage(); n = tp.count_chars()
        if not n: continue
        texto = tp.get_text_range(0, n)
        for m in PADRAO.finditer(texto):
            boxes = [tp.get_charbox(j) for j in range(m.start(), m.end()) if j < n]
            boxes = [b for b in boxes if b[2] > b[0] or b[3] > b[1]] or boxes
            x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
            achados.setdefault(i, []).append((m.group(1), x0, y0, x1, y1))
    return achados

def fonte(nome, base):
    return DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'),
                             NameObject('/BaseFont'): NameObject(base), NameObject('/Encoding'): NameObject('/WinAnsiEncoding')} if nome == '/Helv' else
                            {NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject(base)})

def aparencia(w, h, conteudo, w_res):
    s = StreamObject(); s._data = conteudo.encode('latin-1')
    s.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
              NameObject('/BBox'): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(w), FloatObject(h)]),
              NameObject('/Resources'): w_res})
    return s

def main(arq, caixa_px=26):
    achados = achar(arq)
    r = PdfReader(arq); w = PdfWriter(clone_from=r)
    helv, zadb = w._add_object(fonte('/Helv', '/Helvetica')), w._add_object(fonte('/ZaDb', '/ZapfDingbats'))
    dr = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): helv, NameObject('/ZaDb'): zadb})})
    campos = ArrayObject(); nt = nc = 0
    lado = caixa_px * 0.75  # px do CSS → pt
    for pi, itens in achados.items():
        page = w.pages[pi]
        annots = page.get('/Annots'); annots = annots.get_object() if annots is not None else ArrayObject()
        porid = {i[0]: i for i in itens}
        for cid, x0, y0, x1, y1 in itens:
            if cid.startswith('t') and cid.endswith('a'):
                fim = porid.get(cid[:-1] + 'b')
                if not fim: continue
                xa, xb = x1 + 2, fim[1] - 2; base = (y0 + y1) / 2
                if xb - xa < 20: continue
                rect = [xa, base - 3, xb, base + 14]
                d = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
                                      NameObject('/FT'): NameObject('/Tx'), NameObject('/T'): TextStringObject(f'p{pi + 1}_{cid[:-1]}'),
                                      NameObject('/Rect'): ArrayObject([FloatObject(v) for v in rect]), NameObject('/F'): NumberObject(4),
                                      NameObject('/DA'): TextStringObject('/Helv 10 Tf 0.09 0.19 0.16 rg'), NameObject('/P'): page.indirect_reference})
                nt += 1
            elif cid.startswith('c'):
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 9 * 0.75; h = lado * 0.86  # o marcador fica 9px abaixo do centro
                rect = [cx - h / 2, cy - h / 2, cx + h / 2, cy + h / 2]
                res = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/ZaDb'): zadb})})
                on = aparencia(h, h, f'q 0.12 0.75 0.42 rg 0 0 {h:.2f} {h:.2f} re f BT /ZaDb {h * 0.8:.1f} Tf 1 1 1 rg {h * 0.14:.1f} {h * 0.2:.1f} Td (4) Tj ET Q', res)
                off = aparencia(h, h, '', DictionaryObject())
                d = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
                                      NameObject('/FT'): NameObject('/Btn'), NameObject('/T'): TextStringObject(f'p{pi + 1}_{cid}'),
                                      NameObject('/Rect'): ArrayObject([FloatObject(v) for v in rect]), NameObject('/F'): NumberObject(4),
                                      NameObject('/V'): NameObject('/Off'), NameObject('/AS'): NameObject('/Off'),
                                      NameObject('/MK'): DictionaryObject({NameObject('/CA'): TextStringObject('4')}),
                                      NameObject('/DA'): TextStringObject('/ZaDb 0 Tf 0.07 0.57 0.34 rg'),
                                      NameObject('/AP'): DictionaryObject({NameObject('/N'): DictionaryObject({NameObject('/Yes'): w._add_object(on), NameObject('/Off'): w._add_object(off)})}),
                                      NameObject('/P'): page.indirect_reference})
                nc += 1
            else:
                continue
            ref = w._add_object(d); annots.append(ref); campos.append(ref)
        page[NameObject('/Annots')] = annots
    w._root_object[NameObject('/AcroForm')] = DictionaryObject({NameObject('/Fields'): campos, NameObject('/NeedAppearances'): BooleanObject(True),
                                                                NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'), NameObject('/DR'): dr})
    with open(arq, 'wb') as fh: w.write(fh)
    print(arq, f'{nt} campos de texto, {nc} caixas de marcar')

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1], *(int(x) for x in sys.argv[2:3]))
