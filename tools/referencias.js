// Tira prints de sites de referência (topo + uma rolada) e monta folhas de contato para comparar.
// Uso: node tools/referencias.js <pasta-saida> <url1> <url2> ...
// Saída: <pasta>/<site>.png, <site>_2.png e <pasta>/folha_<n>.jpg (4 prints por folha)
const {chromium} = require('playwright');
const {execFileSync} = require('child_process');
const fs = require('fs'), path = require('path');
const [dir, ...sites] = process.argv.slice(2);
if (!dir || !sites.length) { console.error('uso: node tools/referencias.js <pasta> <url>...'); process.exit(1); }
fs.mkdirSync(dir, {recursive: true});
(async () => {
  const b = await chromium.launch();
  for (const u of sites) {
    const p = await b.newPage({viewport: {width: 1440, height: 900}});
    const n = u.replace(/https?:\/\/(www\.)?/, '').replace(/[\/.?=&]/g, '_').replace(/_+$/, '');
    try {
      await p.goto(u, {waitUntil: 'domcontentloaded', timeout: 30000}); await p.waitForTimeout(4000);
      await p.screenshot({path: path.join(dir, n + '.png')});
      await p.evaluate(() => window.scrollTo(0, 1200)); await p.waitForTimeout(1500);
      await p.screenshot({path: path.join(dir, n + '_2.png')});
      console.log('ok', u);
    } catch (e) { console.log('falhou', u, e.message.slice(0, 80)); }
    await p.close();
  }
  await b.close();
  execFileSync('python3', ['-c', `
import glob, sys
from PIL import Image
d = sys.argv[1]; fs = sorted(f for f in glob.glob(d + '/*.png'))
for k in range(0, len(fs), 4):
    s = Image.new('RGB', (1440, 900), 'white')
    for i, f in enumerate(fs[k:k + 4]): s.paste(Image.open(f).convert('RGB').resize((720, 450)), ((i % 2) * 720, (i // 2) * 450))
    s.save(f'{d}/folha_{k // 4}.jpg', quality=80); print('folha', k // 4)
`, dir], {stdio: 'inherit'});
})();
