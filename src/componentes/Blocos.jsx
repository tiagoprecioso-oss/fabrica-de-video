import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {COR, CORES_ITEM, FONTE, clamp, easeOut, easeInOut, back, mola, dinheiro} from '../tema';

const neon = (cor, forca = 1) => `0 0 ${18 * forca}px ${cor}, 0 0 ${48 * forca}px ${cor}88`;

/* ---------- câmera: presets de ângulo aplicados ao bloco inteiro (3D real) ---------- */
export const camera = (preset, p, t, batida) => {
  const fase = (t % batida) / batida;
  const soco = 1 + 0.008 * Math.exp(-fase * 8);
  const e = easeInOut(p);
  switch (preset) {
    case 'orbita': return `rotateX(${6 - 2 * e}deg) rotateY(${-9 + 18 * e}deg) scale(${1.0 * soco})`;
    case 'inclinar': return `rotateX(${16 - 13 * e}deg) rotateY(${-3 + 3 * e}deg) scale(${(0.98 + 0.06 * e) * soco})`;
    case 'mergulho': return `rotateX(${-10 + 10 * e}deg) translateZ(${-260 + 260 * e}px) scale(${soco})`;
    case 'empurrar':
    default: return `rotateX(${5 - 5 * e}deg) scale(${(1 + 0.07 * e) * soco})`;
  }
};

/* ---------- número gigante contando ---------- */
export const BlocoNumero = ({b, lt}) => {
  const k = back(lt / 0.45);
  const v = b.valor * easeOut(lt / 1.3);
  const nota = easeOut((lt - 1.3) / 0.4);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 26, top: -380}}>
      {b.chip && <div style={{fontFamily: FONTE.apoio, fontSize: 32, color: COR.branco, padding: '14px 30px', borderRadius: 40,
        border: '2px solid rgba(255,255,255,.45)', background: 'rgba(255,255,255,.08)', opacity: clamp(lt / 0.3)}}>{b.chip}</div>}
      <div style={{fontFamily: FONTE.display, fontSize: 300, lineHeight: 1, color: COR.rosa, transform: `scale(${k})`,
        textShadow: `${neon(COR.rosa, 1.2)}, 6px 8px 0 rgba(0,0,0,.45), 12px 16px 0 rgba(0,0,0,.3)`}}>{dinheiro(v, b.moeda || '$', b.casas ?? 2)}</div>
      {b.nota && <div style={{fontFamily: FONTE.apoio, fontSize: 32, color: COR.apagado, opacity: nota}}>{b.nota}</div>}
      {b.nota2 && <div style={{fontFamily: FONTE.apoio, fontSize: 32, color: COR.amarelo, opacity: nota, textShadow: neon(COR.amarelo, .5)}}>{b.nota2}</div>}
    </AbsoluteFill>
  );
};

/* ---------- título de virada ---------- */
export const BlocoTitulo = ({b, lt}) => {
  const k = Math.max(0.01, back(lt / 0.45));
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', top: -300}}>
      <div style={{fontFamily: FONTE.display, fontSize: 130, color: COR.branco, transform: `scale(${k})`, lineHeight: 1}}>{b.linha1}</div>
      <div style={{fontFamily: FONTE.display, fontSize: 250, color: COR.amarelo, transform: `scale(${k})`, lineHeight: 1.05,
        textShadow: `${neon(COR.amarelo, 1.1)}, 6px 8px 0 rgba(0,0,0,.45), 12px 16px 0 rgba(0,0,0,.3)`}}>{b.linha2}</div>
      <div style={{width: 620 * k, height: 12, marginTop: 26, borderRadius: 6, background: b.corLinha ? CORES_ITEM[b.corLinha] : COR.verde,
        boxShadow: neon(b.corLinha ? CORES_ITEM[b.corLinha] : COR.verde, .8)}} />
    </AbsoluteFill>
  );
};

/* ---------- gráfico de barras com "antes -> depois" ---------- */
const Selo = ({texto, k, style}) => (
  <div style={{position: 'absolute', transform: `translate(-50%, -50%) scale(${k})`, fontFamily: FONTE.display, fontSize: 54,
    color: COR.tinta, background: COR.amarelo, padding: '6px 22px', borderRadius: 14, whiteSpace: 'nowrap',
    boxShadow: neon(COR.amarelo, .9), ...style}}>{texto}</div>
);

export const BlocoBarras = ({b, t}) => {
  const PX0 = 60, PX1 = 1020, PY0 = 290, PY1 = 1150;          // painel
  const X0 = PX0 + 110, X1 = PX1 - 40, YB = PY1 - 100, YT = PY0 + 160; // área do gráfico
  const sc = (v) => YB - ((YB - YT) * v) / b.max;
  const n = b.itens.length;
  const slot = (X1 - X0) / n;
  const bw = Math.min(260, slot * 0.6);
  const depois = b.morphEm != null && t >= b.morphEm;
  const destaque = (() => {
    let d = null;
    (b.destaques || []).forEach((x) => { if (t >= x.em) d = x.indices; });
    return d;
  })();
  const casas = b.casas ?? 0;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: PX0, top: PY0, width: PX1 - PX0, height: PY1 - PY0, borderRadius: 36,
        background: COR.painel, border: '2px solid rgba(255,255,255,.12)',
        boxShadow: '0 30px 80px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.12)'}} />
      <div style={{position: 'absolute', left: PX0, width: PX1 - PX0, top: PY0 + 50, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 32,
        color: depois ? COR.amarelo : COR.branco, textShadow: depois ? neon(COR.amarelo, .5) : 'none'}}>{depois ? b.tituloDepois : b.titulo}</div>
      {(b.grade || []).map((v) => (
        <React.Fragment key={v}>
          <div style={{position: 'absolute', left: X0, width: X1 - X0, top: sc(v), height: 2, background: 'rgba(255,255,255,.10)'}} />
          <div style={{position: 'absolute', left: X0 - 108, width: 96, top: sc(v) - 14, textAlign: 'right', fontFamily: FONTE.apoio, fontSize: 22, color: COR.apagado}}>
            {dinheiro(v, b.moeda, 0)}</div>
        </React.Fragment>
      ))}
      <div style={{position: 'absolute', left: X0, width: X1 - X0, top: YB, height: 3, background: 'rgba(255,255,255,.75)'}} />
      {b.itens.map((it, i) => {
        const entra = it.entra ?? b.de + 0.2 + i * 0.12;
        const g = mola((t - entra) * 1.3);
        if (g <= 0) return null;
        const mx = b.morphEm != null ? t - b.morphEm - i * 0.08 : -1;
        const m = it.valorDepois == null ? 0 : mx <= 0 ? 0 : 1 - Math.exp(-5 * mx) * Math.cos(8 * mx);
        const alvo = it.valorDepois ?? it.valor;
        const v = (it.valor + (alvo - it.valor) * m) * g;
        const vRot = (it.valor + (alvo - it.valor) * clamp(m)) * Math.min(g, 1);
        const cx = X0 + slot * (i + 0.5);
        const cor = CORES_ITEM[it.cor || 'ciano'];
        const on = !destaque || destaque.includes(i);
        const op = on ? 1 : 0.38;
        const y = sc(v);
        return (
          <React.Fragment key={i}>
            {m > 0.02 && it.valorDepois != null && (
              <div style={{position: 'absolute', left: cx - bw / 2, width: bw, top: sc(it.valor), height: YB - sc(it.valor),
                border: '3px dashed rgba(255,255,255,.5)', borderBottom: 'none', borderRadius: '14px 14px 0 0', opacity: op * clamp(m)}}>
                {b.notaFantasma && <div style={{position: 'absolute', top: 10, width: '100%', textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 20, color: '#fff'}}>{b.notaFantasma}</div>}
              </div>
            )}
            <div style={{position: 'absolute', left: cx - bw / 2, width: bw, top: y, height: Math.max(0, YB - y), opacity: op,
              borderRadius: '16px 16px 0 0', background: `linear-gradient(180deg, ${cor}EE 0%, ${cor} 55%, ${cor}AA 100%)`,
              boxShadow: on ? `${neon(cor, .9)}, inset 0 2px 0 rgba(255,255,255,.6)` : 'none'}}>
              <div style={{position: 'absolute', left: 10, top: 10, bottom: 10, width: 10, borderRadius: 5, background: 'rgba(255,255,255,.22)'}} />
            </div>
            <div style={{position: 'absolute', left: cx - 150, width: 300, top: y - 66, textAlign: 'center', fontFamily: FONTE.display,
              fontSize: casas ? 50 : 48, color: on ? COR.branco : COR.apagado, opacity: on ? 1 : 0.7}}>{dinheiro(vRot, b.moeda, casas)}</div>
            {b.mostrarDiferenca && m > 0.6 && it.valorDepois != null && (
              <div style={{position: 'absolute', left: cx - 100, width: 200, top: y - 100, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 22,
                color: COR.amarelo, opacity: easeOut((m - 0.6) / 0.4) * op}}>+{dinheiro(it.valorDepois - it.valor, b.moeda, 0)}</div>
            )}
            <div style={{position: 'absolute', left: cx - slot / 2, width: slot, top: YB + 16, textAlign: 'center', fontFamily: FONTE.apoio,
              fontSize: n > 4 ? 22 : 30, color: on ? COR.branco : COR.apagado, whiteSpace: 'nowrap'}}>{it.nome}</div>
            <div style={{position: 'absolute', left: cx - slot / 2, width: slot, top: YB + (n > 4 ? 46 : 54), textAlign: 'center', fontFamily: FONTE.apoio,
              fontSize: 20, color: COR.apagado}}>{it.ano}</div>
          </React.Fragment>
        );
      })}
      {b.selo && t >= b.selo.em && (() => {
        const i = b.selo.indice; const it = b.itens[i];
        const cx = X0 + slot * (i + 0.5);
        const alvo = it.valorDepois ?? it.valor;
        const k = back((t - b.selo.em) / 0.35);
        const sy = Math.max(sc(alvo) - 150, PY0 + 135);
        const sx = Math.min(cx, X1 - 190);
        return (<>
          <div style={{position: 'absolute', left: cx - 2, width: 4, top: sy + 30, height: Math.max(0, sc(alvo) - 70 - (sy + 30)), background: COR.amarelo, opacity: clamp(k)}} />
          <Selo texto={b.selo.texto} k={k} style={{left: sx, top: sy}} />
          <Particulas t={t} rajadas={[{em: b.selo.em, x: sx, y: sy}]} />
        </>);
      })()}
      {b.formula && t >= b.formula.de && t < b.formula.ate && (() => {
        const a = easeOut((t - b.formula.de) / 0.4) * (1 - easeOut((t - b.formula.ate + 0.4) / 0.4));
        return (
          <div style={{position: 'absolute', left: 540, top: 660, transform: `translate(-50%, -50%) scale(${0.9 + 0.1 * a})`, opacity: a,
            padding: '26px 40px', borderRadius: 24, background: COR.painelSolido, border: `3px solid ${COR.amarelo}`, textAlign: 'center',
            boxShadow: neon(COR.amarelo, .5)}}>
            <div style={{fontFamily: FONTE.apoio, fontSize: 30, color: COR.amarelo}}>{b.formula.linha1}</div>
            <div style={{fontFamily: FONTE.display, fontSize: 54, color: COR.branco, marginTop: 10, whiteSpace: 'nowrap'}}>{b.formula.linha2}</div>
          </div>
        );
      })()}
    </AbsoluteFill>
  );
};

/* ---------- partículas nos selos ---------- */
export const Particulas = ({t, rajadas}) => (
  <AbsoluteFill>
    {rajadas.flatMap((r, j) => new Array(46).fill(0).map((_, i) => {
      const dt = t - r.em;
      const vida = 0.6 + random(`v${j}-${i}`) * 0.6;
      if (dt < 0 || dt > vida) return null;
      const ang = random(`a${j}-${i}`) * Math.PI * 2;
      const vel = 260 + random(`s${j}-${i}`) * 560;
      const x = r.x + Math.cos(ang) * vel * dt;
      const y = r.y + (Math.sin(ang) * vel - 300) * dt + 900 * dt * dt;
      const s = 4 + random(`r${j}-${i}`) * 8;
      return <div key={`${j}-${i}`} style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: '50%',
        background: COR.amarelo, opacity: 1 - dt / vida, boxShadow: neon(COR.amarelo, .6)}} />;
    }))}
  </AbsoluteFill>
);
