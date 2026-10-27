import React from 'react';
import {COR, FONTE, clamp} from '../tema';

// "*palavra*" vira destaque amarelo. "R$ 10" fica junto na mesma palavra.
export const palavras = (texto) => {
  const out = [];
  let hl = false;
  texto.replace(/R\$ /g, 'R$ ').split(' ').filter(Boolean).forEach((w) => {
    let on = hl;
    if (w.startsWith('*')) { on = true; w = w.slice(1); }
    let fecha = false;
    if (w.endsWith('*')) { fecha = true; w = w.slice(0, -1); }
    else if (/\*[.,!?;:…]$/.test(w)) { fecha = true; w = w.replace('*', ''); }
    hl = on && !fecha;
    out.push({w: w.toUpperCase(), hl: on});
  });
  return out;
};

// Legenda corrida: a frase inteira, palavras surgindo em sequência com fade suave.
export const Legenda = ({texto, lt, dur, y = 1330}) => {
  const ws = palavras(texto);
  const total = ws.reduce((a, p) => a + p.w.length + 2, 0);
  const util = Math.max(0.6, dur * 0.7);
  let acc = 0;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, transform: 'translateY(-50%)', display: 'flex', justifyContent: 'center'}}>
      <div style={{
        maxWidth: 940, padding: '18px 34px', borderRadius: 26, background: COR.legenda, backdropFilter: 'blur(6px)',
        textAlign: 'center', fontFamily: FONTE.display, fontSize: 78, lineHeight: 1.12, letterSpacing: 0.5,
      }}>
        {ws.map((p, i) => {
          const t0 = (util * acc) / total;
          acc += p.w.length + 2;
          const a = clamp((lt - t0) / 0.14);
          return (
            <span key={i} style={{
              display: 'inline-block', marginRight: i < ws.length - 1 ? '0.26em' : 0,
              opacity: a, transform: `translateY(${(1 - a) * 14}px)`,
              color: p.hl ? COR.amarelo : COR.branco,
              WebkitTextStroke: '4px #000', paintOrder: 'stroke fill',
              textShadow: p.hl ? `0 0 28px rgba(255,214,0,.55), 4px 5px 0 rgba(0,0,0,.6)` : '4px 5px 0 rgba(0,0,0,.6)',
            }}>{p.w}</span>
          );
        })}
      </div>
    </div>
  );
};
