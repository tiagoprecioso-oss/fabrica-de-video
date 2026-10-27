import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig} from 'remotion';
import {COR, FONTE, clamp, easeOut, mola} from '../tema';
import {palavras} from './Legenda';

/* =========================================================
   CAMADA GAMEPLAY — o padrão dos canais dark de games:
   gameplay rodando sem parar, com cortes a cada poucos segundos.
   "gameplay": {
     "arquivo": "gameplay/gta5-voo.mp4",   // em public/
     "layout": "cheia" | "dividida",       // tela toda ou metade de baixo
     "duracaoClipe": 24,                   // segundos do arquivo
     "corte": 2.5,                         // troca de trecho a cada N s (0 = sem cortes)
     "inicio": 0,                          // de onde começar no arquivo
     "escurecer": 0.35                     // véu escuro por cima (legibilidade)
   }
   ========================================================= */
export const DIVISAO = 1000;   // y onde começa a gameplay no layout dividido

const trecho = (g, k) => {
  const corte = g.corte ?? 2.5;
  const util = Math.max(1, (g.duracaoClipe || 20) - (corte || 0) - 0.2);
  // passo "irracional" para não repetir a mesma ordem de cenas
  return ((g.inicio || 0) + k * util * 0.618) % util;
};

export const Gameplay = ({g, t, dur}) => {
  const {fps} = useVideoConfig();
  const corte = g.corte ?? 2.5;
  const dividida = g.layout === 'dividida';
  const caixa = dividida ? {top: DIVISAO, height: 1920 - DIVISAO} : {top: 0, height: 1920};
  const n = corte > 0 ? Math.ceil(dur / corte) : 1;
  const k = corte > 0 ? Math.floor(t / corte) : 0;
  const lt = corte > 0 ? t - k * corte : t;
  // "soco" de zoom em cada corte, depois um zoom lento contínuo
  const z = 1.08 + 0.05 * (1 - easeOut(lt / 0.25)) + 0.015 * lt;
  return (
    <div style={{position: 'absolute', left: 0, width: 1080, overflow: 'hidden', background: '#000', ...caixa}}>
      {Array.from({length: n}).map((_, i) => (
        <Sequence key={i} from={Math.round(i * (corte || dur) * fps)} durationInFrames={Math.round((corte || dur) * fps) + 1} layout="none">
          <AbsoluteFill style={{transform: i === k ? `scale(${z})` : 'none'}}>
            <OffthreadVideo src={staticFile(g.arquivo)} muted startFrom={Math.round(trecho(g, i) * fps)}
              style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </AbsoluteFill>
        </Sequence>
      ))}
      <AbsoluteFill style={{background: `rgba(0,0,0,${g.escurecer ?? (dividida ? 0.15 : 0.35)})`}} />
      {/* clarão rápido no corte */}
      {corte > 0 && k > 0 && <AbsoluteFill style={{background: '#fff', opacity: 0.18 * (1 - clamp(lt / 0.12))}} />}
      {dividida && <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 6, background: COR.amarelo, boxShadow: `0 0 24px ${COR.amarelo}`}} />}
    </div>
  );
};

/* Os blocos de dados no layout dividido: encolhidos para a metade de cima. */
export const MetadeDeCima = ({children}) => (
  <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: DIVISAO, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, transform: 'translateY(-150px) scale(0.74)', transformOrigin: '50% 0'}}>
      {children}
    </div>
  </div>
);

/* =========================================================
   LEGENDA DUPLA — frase pequena + palavra-chave grande.
   A frase corre em uma linha fina; a palavra marcada com *asteriscos*
   aparece grande, uma por frase.
   ========================================================= */
export const LegendaDupla = ({texto, lt, dur, layout, gancho}) => {
  const ws = palavras(texto);
  const chave = (ws.filter((p) => p.hl).map((p) => p.w).join(' ') || ws[ws.length - 1]?.w || '').replace(/[.,!?;:…]+$/, '');
  const dividida = layout === 'dividida';
  const yFrase = dividida ? DIVISAO + 70 : 1290;
  const yChave = dividida ? 1520 : 1480;
  const yGancho = dividida ? 40 : 120;
  const a = clamp(lt / 0.18);
  const s = Math.min(1.08, 0.6 + 0.48 * mola(lt * 1.6));
  const sai = clamp((dur - lt) / 0.15);
  const tam = chave.length > 12 ? 92 : chave.length > 7 ? 120 : 150;
  return (
    <>
      {gancho && !dividida && (
        <div style={{position: 'absolute', left: 60, right: 60, top: yGancho, textAlign: 'center'}}>
          <span style={{display: 'inline-block', padding: '10px 22px', borderRadius: 14, background: 'rgba(0,0,0,.72)',
            fontFamily: FONTE.apoio, fontSize: 34, lineHeight: 1.2, color: COR.branco}}>{gancho}</span>
        </div>
      )}
      <div style={{position: 'absolute', left: 70, right: 70, top: yFrase, textAlign: 'center', opacity: a * sai}}>
        <span style={{display: 'inline-block', padding: '10px 22px', borderRadius: 14, background: COR.legenda,
          fontFamily: FONTE.apoio, fontSize: 38, lineHeight: 1.25, color: COR.branco}}>
          {ws.map((p, i) => <span key={i} style={{color: p.hl ? COR.amarelo : COR.branco}}>{p.w}{i < ws.length - 1 ? ' ' : ''}</span>)}
        </span>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: yChave, transform: `translateY(-50%) scale(${s * sai})`, textAlign: 'center',
        fontFamily: FONTE.display, fontSize: tam, lineHeight: 1, color: COR.amarelo, opacity: a,
        WebkitTextStroke: '8px #000', paintOrder: 'stroke fill', textShadow: '0 0 40px rgba(0,0,0,.7), 6px 8px 0 rgba(0,0,0,.7)'}}>
        {chave}
      </div>
    </>
  );
};
