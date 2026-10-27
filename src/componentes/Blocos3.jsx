import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COR, FONTE, clamp, easeOut, back, mola} from '../tema';

/* Blocos do canal de finanças (estilo "grana"): dinheiro como jogo. */

const reais = (v, casas = 0) => 'R$ ' + v.toFixed(casas).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
const reaisC = (v) => {
  const [i, d] = v.toFixed(2).split('.');
  return 'R$ ' + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + d;
};
const INK = () => COR.branco;

/* ---------- o chefão monstro (desenho próprio, formas simples) ---------- */
const Monstro = ({t, raiva, travado}) => {
  const bob = Math.sin(t * 4) * 10;
  const shake = travado ? Math.sin(t * 60) * 6 * clamp(1 - travado) : 0;
  const s = 1 + 0.15 * raiva;
  return (
    <div style={{position: 'absolute', left: 540 - 150, top: 440 + bob, width: 300, height: 260, transform: `translateX(${shake}px) scale(${s})`, transformOrigin: '50% 100%'}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: '46% 46% 34% 34%', background: `linear-gradient(180deg, ${COR.rosa}, #A8241A)`,
        boxShadow: '0 18px 0 rgba(18,36,27,.18)', border: '6px solid #12241B'}} />
      {[0, 1].map((k) => (
        <div key={k} style={{position: 'absolute', top: 80, left: k ? 168 : 62, width: 70, height: 70, borderRadius: '50%', background: '#fff', border: '5px solid #12241B'}}>
          <div style={{position: 'absolute', left: k ? 14 : 26, top: 24, width: 26, height: 26, borderRadius: '50%', background: '#12241B'}} />
        </div>
      ))}
      <div style={{position: 'absolute', top: 56, left: 52, width: 92, height: 14, background: '#12241B', borderRadius: 7, transform: 'rotate(18deg)'}} />
      <div style={{position: 'absolute', top: 56, left: 156, width: 92, height: 14, background: '#12241B', borderRadius: 7, transform: 'rotate(-18deg)'}} />
      <div style={{position: 'absolute', top: 180, left: 80, width: 140, height: 34, borderRadius: '0 0 70px 70px', background: '#12241B'}} />
      <div style={{position: 'absolute', top: -40, left: 110, width: 80, height: 60, borderRadius: 12, background: COR.amarelo, border: '5px solid #12241B',
        display: 'grid', placeItems: 'center', fontFamily: FONTE.display, fontSize: 30, color: '#12241B'}}>%</div>
    </div>
  );
};

/* =========================================================
   CHEFÃO — uma dívida como chefão de jogo: a barra de vida é o saldo,
   que cresce mês a mês com os juros. Opcional: teto legal que trava a barra.
   ========================================================= */
export const BlocoChefao = ({b, t}) => {
  const ini = b.inicio ?? b.de + 2, fim = b.fim ?? b.ate - 3;
  const meses = b.meses ?? 12, taxa = b.taxa, divida = b.divida;
  const m = clamp((t - ini) / (fim - ini)) * meses;          // mês contínuo
  const semLei = divida * Math.pow(1 + taxa, m);
  const max = divida * Math.pow(1 + taxa, meses);
  const teto = b.teto ? divida * b.teto : Infinity;
  const real = Math.min(semLei, teto);
  const mTeto = b.teto ? Math.log(b.teto) / Math.log(1 + taxa) : Infinity;
  const tTeto = ini + (mTeto / meses) * (fim - ini);
  const travou = t >= tTeto;
  const aTrava = clamp((t - tTeto) / 0.5);
  const entra = easeOut((t - b.de) / 0.6);
  const X0 = 90, BW = 900, BY = 850, BH = 76;
  const w = (v) => BW * v / max;
  const fase = clamp((t - ini) / 0.4);
  return (
    <AbsoluteFill style={{opacity: entra}}>
      <div style={{position: 'absolute', left: 60, top: 190, width: 960, textAlign: 'center'}}>
        <div style={{display: 'inline-block', fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 28, letterSpacing: 6, color: '#fff', background: '#12241B', padding: '8px 20px', borderRadius: 8}}>{b.rotulo || 'CHEFÃO'}</div>
        <div style={{fontFamily: FONTE.display, fontSize: 74, lineHeight: 1.02, color: INK(), marginTop: 14}}>{b.nome}</div>
      </div>
      <Monstro t={t} raiva={clamp(real / (b.teto ? teto : max)) * (travou ? 0.6 : 1)} travado={travou ? aTrava : 0} />
      {/* ataque */}
      <div style={{position: 'absolute', left: 90, top: 770, width: 900, display: 'flex', justifyContent: 'space-between', fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 30, color: INK()}}>
        <span>VIDA: <span style={{color: COR.rosa}}>{reais(real)}</span></span>
        <span>ATAQUE: {b.taxaTexto}</span>
      </div>
      {/* barra de vida */}
      <div style={{position: 'absolute', left: X0, top: BY, width: BW, height: BH, borderRadius: 14, background: '#fff', border: '5px solid #12241B', overflow: 'hidden'}}>
        {/* fantasma sem a lei */}
        {b.teto && semLei > teto && <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: w(semLei), background: `repeating-linear-gradient(135deg, ${COR.rosa}33 0 14px, transparent 14px 28px)`}} />}
        <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: Math.max(0, w(real) * fase), background: `linear-gradient(90deg, #F06A4F, ${COR.rosa})`}} />
      </div>
      {/* parede da lei */}
      {b.teto && (
        <div style={{position: 'absolute', left: X0 + w(teto) - 6, top: BY - 20, width: 12, height: BH + 40, background: '#12241B', borderRadius: 6,
          opacity: clamp((t - ini) / 0.6), transform: `scaleY(${travou ? 1 + 0.15 * (1 - aTrava) : 1})`}} />
      )}
      {b.teto && <div style={{position: 'absolute', left: X0 + w(teto) - 120, top: BY + BH + 30, width: 240, textAlign: 'center', fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 26, color: INK()}}>TETO DA LEI<br />{reais(teto)}</div>}
      {/* contador */}
      <div style={{position: 'absolute', left: 60, top: 1065, width: 960, textAlign: 'center'}}>
        <div style={{fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 30, color: COR.apagado, letterSpacing: 2}}>MÊS {Math.min(meses, Math.floor(m))} DE {meses}</div>
        {b.teto && semLei > teto && (
          <div style={{fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 34, color: COR.rosa, marginTop: 6, textDecoration: travou ? 'line-through' : 'none', opacity: 0.8}}>sem a lei: {reais(semLei)}</div>
        )}
      </div>
      {/* selo travado */}
      {travou && b.selo && (
        <div style={{position: 'absolute', left: 610, top: 560, width: 420, padding: '14px 8px', textAlign: 'center', borderRadius: 16,
          border: `8px solid ${COR.verde}`, color: COR.verde, background: 'rgba(255,255,255,.94)', fontFamily: FONTE.display, fontSize: 44, lineHeight: 1,
          transform: `rotate(-8deg) scale(${back(aTrava * 1.2)})`, opacity: clamp(aTrava * 3)}}>
          {b.selo}
        </div>
      )}
    </AbsoluteFill>
  );
};

/* =========================================================
   EXTRATO — linhas de um extrato/recibo aparecendo uma a uma, com total.
   ========================================================= */
export const BlocoExtrato = ({b, t}) => {
  const entra = easeOut((t - b.de) / 0.5);
  const n = b.linhas.length;
  const Y0 = 360, LH = 108;
  const tt = b.total;
  const aT = tt ? easeOut((t - tt.em) / 0.4) : 0;
  return (
    <AbsoluteFill style={{opacity: entra}}>
      <div style={{position: 'absolute', left: 90, top: 200, width: 900, height: Y0 - 200 + n * LH + (tt ? 170 : 60), background: '#fff', border: '5px solid #12241B', borderRadius: 18,
        boxShadow: '0 20px 0 rgba(18,36,27,.12)', transform: `translateY(${(1 - entra) * 60}px)`}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: -2, height: 26, background: `radial-gradient(circle at 13px -2px, ${COR.tinta} 12px, transparent 13px) 0 0 / 34px 26px repeat-x`}} />
      </div>
      <div style={{position: 'absolute', left: 140, top: 250, width: 800, fontFamily: FONTE.display, fontSize: 58, lineHeight: 1.05, color: INK()}}>{b.titulo}</div>
      {b.subtitulo && <div style={{position: 'absolute', left: 140, top: 250 + 70 * Math.ceil(b.titulo.length / 22), width: 800, fontFamily: FONTE.apoio, fontWeight: 600, fontSize: 26, color: COR.apagado}}>{b.subtitulo}</div>}
      {b.linhas.map((l, i) => {
        const a = easeOut((t - l.em) / 0.35);
        if (a <= 0) return null;
        const y = Y0 + 60 + i * LH;
        return (
          <div key={i} style={{position: 'absolute', left: 140, top: y, width: 800, display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
            borderBottom: '3px dashed rgba(18,36,27,.25)', paddingBottom: 16, opacity: a, transform: `translateX(${(1 - a) * 80}px)`}}>
            <span style={{fontFamily: FONTE.apoio, fontWeight: 600, fontSize: 36, color: INK()}}>{l.texto}</span>
            <span style={{fontFamily: FONTE.display, fontSize: 48, color: l.cor === 'vermelho' ? COR.rosa : l.cor === 'verde' ? COR.verde : INK()}}>{l.valor}</span>
          </div>
        );
      })}
      {tt && aT > 0 && (
        <div style={{position: 'absolute', left: 140, top: Y0 + 60 + n * LH + 10, width: 800, display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', opacity: aT,
          transform: `scale(${0.9 + 0.1 * mola(t - tt.em)})`, transformOrigin: '100% 50%'}}>
          <span style={{fontFamily: FONTE.apoio, fontWeight: 800, fontSize: 40, color: INK()}}>{tt.texto}</span>
          <span style={{fontFamily: FONTE.display, fontSize: 72, color: tt.cor === 'verde' ? COR.verde : COR.rosa}}>{tt.valor}</span>
        </div>
      )}
    </AbsoluteFill>
  );
};

export {reais, reaisC};
