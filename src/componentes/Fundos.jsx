import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {COR} from '../tema';
import {Fundo as Synthwave} from './Fundo';

// Todos os fundos são periódicos na duração do vídeo: o último quadro casa com o primeiro (loop).
const TAU = Math.PI * 2;
const vinheta = (forca = .6) => <AbsoluteFill style={{background: `radial-gradient(ellipse 85% 70% at 50% 45%, transparent 50%, rgba(0,0,0,${forca}) 100%)`}} />;
const pts = (n, chave) => new Array(n).fill(0).map((_, i) => ({x: random(chave + 'x' + i), y: random(chave + 'y' + i), s: random(chave + 's' + i), p: random(chave + 'p' + i)}));

/* ---------- CINEMA: holofotes, poeira no feixe, granulado ---------- */
const POEIRA = pts(70, 'po');
const Cinema = ({t, dur}) => {
  const c = t / dur;
  const a1 = -18 + 10 * Math.sin(TAU * 2 * c), a2 = 18 + 10 * Math.sin(TAU * 2 * c + 2);
  const semente = Math.floor(t * 12) % 8;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse 120% 80% at 50% 110%, #2A1A0E 0%, #0C0907 55%, #050404 100%)'}}>
      {[a1, a2].map((a, i) => (
        <div key={i} style={{position: 'absolute', left: i ? '78%' : '22%', top: -200, width: 900, height: 2600, marginLeft: -450,
          transformOrigin: '50% 0%', transform: `rotate(${a}deg)`,
          background: 'linear-gradient(180deg, rgba(255,226,170,.30), rgba(255,226,170,.06) 60%, transparent)',
          clipPath: 'polygon(46% 0, 54% 0, 100% 100%, 0 100%)', filter: 'blur(18px)', mixBlendMode: 'screen'}} />
      ))}
      {POEIRA.map((d, i) => {
        const y = ((d.y - c * (1 + Math.round(d.s * 2))) % 1 + 1) % 1;
        return <div key={i} style={{position: 'absolute', left: `${d.x * 100}%`, top: `${y * 100}%`, width: 2 + d.s * 4, height: 2 + d.s * 4, borderRadius: '50%',
          background: '#FFE7B8', opacity: .15 + .35 * Math.abs(Math.sin(TAU * 3 * c + d.p * 6))}} />;
      })}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 520, background: 'linear-gradient(180deg, transparent, rgba(232,176,75,.10))'}} />
      <svg width="1080" height="1920" style={{position: 'absolute', inset: 0, opacity: .14, mixBlendMode: 'overlay'}}>
        <filter id="grao"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed={semente} /></filter>
        <rect width="100%" height="100%" filter="url(#grao)" />
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 120, background: 'linear-gradient(180deg, #000, transparent)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 160, background: 'linear-gradient(0deg, #000, transparent)'}} />
      {vinheta(.75)}
    </AbsoluteFill>
  );
};

/* ---------- ANIME: linhas de velocidade, retícula de mangá, faixa vermelha ---------- */
const Anime = ({t, dur}) => {
  const c = t / dur;
  const giro = 4 * Math.sin(TAU * 6 * c);
  const pulso = .5 + .5 * Math.sin(TAU * 18 * c);
  return (
    <AbsoluteFill style={{background: '#0B0B10', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: '50%', top: '42%', width: 3200, height: 3200, marginLeft: -1600, marginTop: -1600,
        transform: `rotate(${giro}deg)`,
        background: 'repeating-conic-gradient(from 0deg, rgba(255,255,255,.10) 0deg 1.2deg, transparent 1.2deg 6deg)',
        WebkitMaskImage: 'radial-gradient(circle at 50% 50%, transparent 14%, #000 40%)', opacity: .7 + .3 * pulso}} />
      <div style={{position: 'absolute', left: -200, right: -200, top: 760, height: 260, background: COR.rosa, opacity: .85,
        transform: `rotate(-12deg) translateX(${Math.sin(TAU * c) * 60}px)`, boxShadow: `0 0 80px ${COR.rosa}`}} />
      <div style={{position: 'absolute', left: -200, right: -200, top: 1010, height: 26, background: COR.branco, opacity: .8, transform: 'rotate(-12deg)'}} />
      <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(255,255,255,.22) 28%, transparent 30%)', backgroundSize: '22px 22px',
        WebkitMaskImage: 'linear-gradient(180deg, transparent 45%, #000 100%)', opacity: .5}} />
      {vinheta(.7)}
    </AbsoluteFill>
  );
};

/* ---------- ARCADE: tela CRT, estrelas de pixel, cidade em blocos ---------- */
const PIX = pts(90, 'px');
const PREDIOS = (() => { let acc = 0; return new Array(24).fill(0).map((_, i) => { const w = 60 + random('bw' + i) * 90; const b = {w, h: 120 + random('bh' + i) * 380, left: acc}; acc += w + 8; return b; }); })();
const LARG = PREDIOS.reduce((a, b) => a + b.w + 8, 0);
const Arcade = ({t, dur}) => {
  const c = t / dur;
  const off = (c * 3 * LARG) % LARG;
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #020604 0%, #06160C 60%, #0A2414 100%)', overflow: 'hidden'}}>
      {PIX.map((p, i) => {
        const y = (p.y + c * (2 + Math.round(p.s * 3))) % 1;
        const s = p.s > .7 ? 8 : 4;
        return <div key={i} style={{position: 'absolute', left: Math.round(p.x * 1080 / 4) * 4, top: Math.round(y * 1300 / 4) * 4, width: s, height: s,
          background: p.s > .85 ? COR.amarelo : COR.verde, opacity: .5 + .5 * ((Math.floor(t * 4 + p.p * 10)) % 2)}} />;
      })}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 300, height: 520}}>
        {[0, 1].flatMap((k) => PREDIOS.map((b, i) => (
          <div key={k + '-' + i} style={{position: 'absolute', bottom: 0, left: b.left + k * LARG - off, width: b.w, height: b.h,
            background: '#0D2A18', borderTop: `4px solid ${COR.verde}55`,
            backgroundImage: `linear-gradient(${COR.amarelo}66 8px, transparent 8px)`, backgroundSize: '24px 36px', backgroundPosition: '8px 20px'}} />
        )))}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 300, background: '#041008', borderTop: `4px solid ${COR.verde}`, boxShadow: `0 0 30px ${COR.verde}`}} />
      <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,.35) 0px, rgba(0,0,0,.35) 2px, transparent 2px, transparent 5px)'}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse 75% 65% at 50% 45%, transparent 55%, rgba(0,0,0,.85) 100%)`}} />
    </AbsoluteFill>
  );
};

/* ---------- STREAMING: manchas de luz desfocadas em movimento ---------- */
const Streaming = ({t, dur}) => {
  const c = t / dur;
  const manchas = [
    {cor: COR.rosa, r: 520, x: 300, y: 500, ax: 160, ay: 120, f: 1},
    {cor: COR.violeta, r: 620, x: 800, y: 900, ax: 140, ay: 200, f: 2},
    {cor: COR.ciano, r: 460, x: 400, y: 1400, ax: 200, ay: 140, f: 1},
    {cor: COR.amarelo, r: 300, x: 850, y: 300, ax: 90, ay: 90, f: 3},
  ];
  return (
    <AbsoluteFill style={{background: COR.tinta, overflow: 'hidden'}}>
      {manchas.map((m, i) => (
        <div key={i} style={{position: 'absolute', width: m.r * 2, height: m.r * 2, borderRadius: '50%', background: m.cor, opacity: .38,
          left: m.x - m.r + m.ax * Math.sin(TAU * m.f * c + i), top: m.y - m.r + m.ay * Math.cos(TAU * m.f * c + i * 2), filter: 'blur(140px)'}} />
      ))}
      <div style={{position: 'absolute', left: -400, top: 0, width: 300, height: 2600, background: 'linear-gradient(90deg, transparent, rgba(255,255,255,.07), transparent)',
        transform: `rotate(18deg) translateX(${((c * 2) % 1) * 2200}px)`}} />
      <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(255,255,255,.05) 1px, transparent 1px)', backgroundSize: '6px 6px'}} />
      {vinheta(.55)}
    </AbsoluteFill>
  );
};

/* ---------- ESPAÇO: estrelas em 3 camadas, nebulosa, planeta ---------- */
const CAMADAS = [pts(140, 'e1'), pts(70, 'e2'), pts(30, 'e3')];
const Espaco = ({t, dur}) => {
  const c = t / dur;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 30% 30%, #12123A 0%, #05051A 50%, #020208 100%)', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: -200, top: 200, width: 1100, height: 700, borderRadius: '50%', background: COR.violeta, opacity: .28, filter: 'blur(160px)',
        transform: `rotate(${10 * Math.sin(TAU * c)}deg)`}} />
      <div style={{position: 'absolute', left: 400, top: 900, width: 900, height: 600, borderRadius: '50%', background: COR.ciano, opacity: .18, filter: 'blur(150px)'}} />
      {CAMADAS.map((cam, k) => cam.map((s, i) => {
        const x = ((s.x - c * (k + 1)) % 1 + 1) % 1;
        const r = (k + 1) * 1.4;
        return <div key={k + '-' + i} style={{position: 'absolute', left: `${x * 100}%`, top: `${s.y * 100}%`, width: r * 2, height: r * 2, borderRadius: '50%',
          background: '#fff', opacity: .3 + .5 * Math.abs(Math.sin(TAU * 5 * c + s.p * 6)), boxShadow: k === 2 ? '0 0 8px #fff' : 'none'}} />;
      }))}
      <div style={{position: 'absolute', left: 620, top: 1380, width: 760, height: 760, borderRadius: '50%',
        background: `radial-gradient(circle at 30% 30%, ${COR.ciano}, #1B2A6B 45%, #05061A 75%)`, boxShadow: `0 0 120px ${COR.ciano}55`}} />
      <div style={{position: 'absolute', left: 520, top: 1700, width: 960, height: 120, borderRadius: '50%', border: `6px solid ${COR.amarelo}88`, transform: 'rotate(-14deg)'}} />
      {vinheta(.6)}
    </AbsoluteFill>
  );
};

const FUNDOS = {synthwave: Synthwave, cinema: Cinema, anime: Anime, arcade: Arcade, streaming: Streaming, espaco: Espaco};
export const FundoEstilo = ({estilo, t, dur}) => {
  const F = FUNDOS[estilo] || Synthwave;
  return <F t={t} dur={dur} />;
};
