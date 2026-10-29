"""Transforma uma página de artifact (sem <html>/<head>) num site independente, pronto para hospedar
fora do claude.ai (GitHub Pages, Netlify, Cloudflare Pages, área de membros) ou abrir direto no navegador.
Uso: python3 tools/pagina_publica.py produtos/chefoes-do-cartao/web/index.html produtos/chefoes-do-cartao/publico/index.html
"""
import sys
from pathlib import Path

RESET = ('*,*::before,*::after{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);'
         'padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}')

def main(origem, destino):
    corpo = Path(origem).read_text(encoding='utf-8')
    doc = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<meta name="robots" content="noindex">'
           f'<style>{RESET}</style></head><body>{corpo}</body></html>')
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    Path(destino).write_text(doc, encoding='utf-8')
    print(destino, len(doc) // 1024, 'KB')

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
