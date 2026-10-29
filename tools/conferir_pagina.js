// Confere uma página HTML de artifact (sem <html>/<head>) como o visitante vê:
// desktop claro (1440) e celular escuro (390), página inteira, mais largura de rolagem e erros de script.
// Uso: node tools/conferir_pagina.js <arquivo.html> <pasta-saida>
// As imagens relativas (img/...) são copiadas junto. Saída: <pasta>/desktop.png e <pasta>/celular.png
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const [arq, dir] = process.argv.slice(2);
if (!arq || !dir) { console.error('uso: node tools/conferir_pagina.js <arquivo.html> <pasta>'); process.exit(1); }
fs.mkdirSync(dir, {recursive: true});
const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + fs.readFileSync(arq, 'utf8') + '</body></html>';
fs.writeFileSync(path.join(dir, 'index.html'), html);
const img = path.join(path.dirname(arq), 'img');
if (fs.existsSync(img)) fs.cpSync(img, path.join(dir, 'img'), {recursive: true});
(async () => {
  const b = await chromium.launch();
  for (const [w, h, nome, tema] of [[1440, 900, 'desktop', 'light'], [390, 844, 'celular', 'dark']]) {
    const p = await b.newPage({viewport: {width: w, height: h}, colorScheme: tema});
    const erros = []; p.on('pageerror', e => erros.push(e.message));
    await p.goto('file://' + path.resolve(dir, 'index.html')); await p.waitForTimeout(1500);
    await p.screenshot({path: path.join(dir, nome + '.png'), fullPage: true});
    const larg = await p.evaluate(() => document.documentElement.scrollWidth);
    console.log(nome, larg > w ? `ROLAGEM LATERAL (${larg}px)` : 'largura ok', erros.length ? 'ERROS: ' + erros.join(' | ') : 'sem erros');
  }
  await b.close();
})();
