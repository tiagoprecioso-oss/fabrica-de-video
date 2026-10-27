import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {COR} from '../tema';

const ESTRELAS = new Array(120).fill(0).map((_, i) => ({
  x: random('ex' + i) * 100,
  y: random('ey' + i) * 58,
  r: 1 + random('er' + i) * 2.4,
  ph: random('ep' + i) * Math.PI * 2,
}));

// Céu synthwave com sol listrado e chão em grade 3D de verdade (CSS perspective).
// Tudo é periódico na duração do vídeo, para o loop fechar sem salto.
export const Fundo = ({t, dur}) => {
  const ciclo = t / dur;
  const chaoY = (ciclo * 40 * 120) % 120; // a grade anda 40 casas por vídeo
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #08041A 0%, #160830 35%, #30104A 60%, #0E041C 60.2%)'}}>
      {ESTRELAS.map((s, i) => (
        <div key={i} style={{
          position: 'absolute', left: `${s.x}%`, top: `${s.y}%`, width: s.r * 2, height: s.r * 2, borderRadius: '50%',
          background: '#fff', opacity: 0.35 + 0.3 * Math.sin(2 * Math.PI * 14 * ciclo + s.ph),
        }} />
      ))}
      {/* brilho do horizonte */}
      <div style={{position: 'absolute', left: 0, right: 0, top: '40%', height: '22%',
        background: 'radial-gradient(ellipse 60% 70% at 50% 100%, rgba(255,60,150,.45), rgba(255,60,150,0) 70%)'}} />
      {/* sol */}
      <div style={{
        position: 'absolute', left: '50%', top: 880, width: 600, height: 600, marginLeft: -300, borderRadius: '50%',
        background: 'linear-gradient(180deg, #FFD050 0%, #FF8A5A 55%, #FF2E8C 100%)',
        WebkitMaskImage: 'linear-gradient(180deg, #000 0%, #000 52%, transparent 52%, transparent 55%, #000 55%, #000 63%, transparent 63%, transparent 67%, #000 67%, #000 74%, transparent 74%, transparent 79%, #000 79%, #000 85%, transparent 85%, transparent 91%, #000 91%)',
        boxShadow: '0 0 120px rgba(255,80,160,.35)',
        filter: 'saturate(1.1)',
      }} />
      {/* chão: plano inclinado em 3D */}
      <div style={{position: 'absolute', left: 0, right: 0, top: '60%', bottom: 0, overflow: 'hidden', perspective: 520, perspectiveOrigin: '50% 0%'}}>
        <div style={{
          position: 'absolute', left: '-150%', right: '-150%', top: 0, height: 2600,
          transformOrigin: '50% 0%', transform: 'rotateX(76deg)',
          backgroundColor: '#12041F',
          backgroundImage: `linear-gradient(${COR.violeta} 3px, transparent 3px), linear-gradient(90deg, ${COR.violeta} 3px, transparent 3px)`,
          backgroundSize: '120px 120px',
          backgroundPosition: `0px ${chaoY}px`,
          opacity: 0.85,
        }} />
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(14,4,28,.9) 0%, rgba(14,4,28,0) 30%)'}} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: '60%', height: 4, background: '#FF50C8', boxShadow: '0 0 24px #FF50C8'}} />
      {/* vinheta */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 85% 70% at 50% 45%, transparent 55%, rgba(0,0,0,.55) 100%)'}} />
    </AbsoluteFill>
  );
};
