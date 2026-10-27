import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {COR, CORES_ITEM, FONTE, clamp, easeOut, back, mola, dinheiro} from '../tema';
import {Particulas} from './Blocos';

const neon = (cor, f = 1) => `0 0 ${18 * f}px ${cor}, 0 0 ${48 * f}px ${cor}88`;
const fmt = (v, b) => (typeof v === 'number' ? dinheiro(v, b.moeda || '', b.casas ?? 0) : v);

/* ---------- mídia (print ou clipe do Tiago, em public/midias) com zoom lento ---------- */
export const Midia = ({src, p, style}) => {
  if (!src) return null;
  const z = 1.04 + 0.1 * p;
  const s = {width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`};
  return (
    <div style={{position: 'absolute', overflow: 'hidden', ...style}}>
      {/\.(mp4|webm|mov)$/i.test(src)
        ? <OffthreadVideo src={staticFile(src)} muted style={s} />
        : <Img src={staticFile(src)} style={s} />}
    </div>
  );
};

/* =========================================================
   RANKING — contagem regressiva (do último ao 1º lugar)
   Formato comprovado: "Top 5 games mais vendidos", "10 animes mais assistidos".
   ========================================================= */
export const BlocoRanking = ({b, t}) => {
  const n = b.itens.length;                       // itens já em ordem: 1º lugar primeiro
  const ini = b.de + 0.5, fim = b.revelarAte ?? b.ate - 2.2;
  const quando = (i) => (b.revelacoes && b.revelacoes[i] != null) ? b.revelacoes[i] : ini + ((n - 1 - i) * (fim - ini)) / Math.max(1, n - 1);
  const max = b.max ?? Math.max(...b.itens.map((x) => x.valor)) * 1.08;
  const Y0 = 420, rowH = Math.min(150, 760 / n), X0 = 90, X1 = 960, BX = 390;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 50, top: 250, width: 980, height: 1050 - 250 + 60 + (n > 5 ? 40 : 0), borderRadius: 36,
        background: COR.painel, border: '2px solid rgba(255,255,255,.12)',
        boxShadow: '0 30px 80px rgba(0,0,0,.55)'}} />
      <div style={{position: 'absolute', left: 50, width: 980, top: 290, textAlign: 'center', fontFamily: FONTE.display, fontSize: 64, color: COR.branco,
        textShadow: neon(COR.violeta, .6)}}>{b.titulo}</div>
      {b.subtitulo && <div style={{position: 'absolute', left: 50, width: 980, top: 372, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 26, color: COR.amarelo}}>{b.subtitulo}</div>}
      {b.itens.map((it, i) => {
        const q = quando(i);
        const a = easeOut((t - q) / 0.35);
        if (a <= 0) return null;
        const y = Y0 + 40 + i * rowH;
        const g = Math.min(1, mola((t - q - 0.1) * 1.4));
        const w = (X1 - BX) * (it.valor / max) * Math.max(0, g);
        const top1 = i === 0;
        const cor = CORES_ITEM[it.cor || (top1 ? 'amarelo' : 'ciano')];
        return (
          <div key={i} style={{position: 'absolute', left: 0, top: y, width: 1080, height: rowH, opacity: a, transform: `translateX(${(1 - a) * 160}px)`}}>
            <div style={{position: 'absolute', left: X0, top: rowH / 2 - 42, width: 84, height: 84, borderRadius: 42, display: 'grid', placeItems: 'center',
              background: top1 ? COR.amarelo : 'rgba(255,255,255,.1)', border: top1 ? 'none' : '2px solid rgba(255,255,255,.35)',
              fontFamily: FONTE.display, fontSize: 44, color: top1 ? COR.tinta : COR.branco, boxShadow: top1 ? neon(COR.amarelo, .8) : 'none'}}>{i + 1}º</div>
            <div style={{position: 'absolute', left: X0 + 100, top: rowH / 2 - (it.sub ? 38 : 20), width: BX - X0 - 106, fontFamily: FONTE.apoio, fontSize: it.nome.length > 9 ? 24 : 28, color: COR.branco, lineHeight: 1.05, whiteSpace: 'nowrap', overflow: 'hidden'}}>{it.nome}</div>
            {it.sub && <div style={{position: 'absolute', left: X0 + 100, top: rowH / 2 + 4, whiteSpace: 'nowrap', fontFamily: FONTE.apoio, fontSize: 20, color: COR.apagado}}>{it.sub}</div>}
            <div style={{position: 'absolute', left: BX, top: rowH / 2 - 26, width: Math.max(0, w), height: 52, borderRadius: 12,
              background: `linear-gradient(90deg, ${cor}AA, ${cor})`, boxShadow: neon(cor, top1 ? .9 : .45)}} />
            <div style={{position: 'absolute', left: BX + Math.max(0, w) + 14, top: rowH / 2 - 30, fontFamily: FONTE.display, fontSize: 48, color: COR.branco, whiteSpace: 'nowrap'}}>
              {fmt(typeof it.valor === 'number' ? it.valor * Math.min(1, Math.max(0, g)) : it.valor, b)}{b.unidade ? ` ${b.unidade}` : ''}</div>
          </div>
        );
      })}
      {t >= quando(0) && <Particulas t={t} rajadas={[{em: quando(0) + 0.15, x: 540, y: Y0 + 40 + rowH / 2}]} />}
    </AbsoluteFill>
  );
};

/* =========================================================
   VERSUS — lado a lado, atributo por atributo
   Formato comprovado: "GTA 6 vs GTA 5", "Goku vs Naruto".
   ========================================================= */
export const BlocoVersus = ({b, t, lt}) => {
  const [A, B] = b.lados;
  const k = back(lt / 0.5);
  const linhas = b.linhas || [];
  const ini = b.de + 1.0, fim = b.linhasAte ?? b.ate - 1.2;
  const quando = (i) => (linhas[i].em != null ? linhas[i].em : ini + (i * (fim - ini)) / Math.max(1, linhas.length));
  const corA = CORES_ITEM[A.cor || 'ciano'], corB = CORES_ITEM[B.cor || 'rosa'];
  const placar = linhas.reduce((p, l, i) => (t >= quando(i) + 0.4 ? (l.vence === 'a' ? [p[0] + 1, p[1]] : l.vence === 'b' ? [p[0], p[1] + 1] : p) : p), [0, 0]);
  return (
    <AbsoluteFill>
      {/* metades com mídia opcional */}
      {[A, B].map((L, j) => (
        <div key={j} style={{position: 'absolute', top: 230, height: 300, left: j ? 545 : 35, width: 500, borderRadius: 30, overflow: 'hidden',
          transform: `translateX(${(1 - k) * (j ? 300 : -300)}px)`,
          background: `linear-gradient(160deg, ${(j ? corB : corA)}55, ${COR.painelSolido})`, border: `3px solid ${j ? corB : corA}`, boxShadow: neon(j ? corB : corA, .5)}}>
          <Midia src={L.midia} p={clamp(lt / (b.ate - b.de))} style={{inset: 0, opacity: 0.85}} />
          <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, transparent 30%, rgba(0,0,0,.75))'}} />
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 56, textAlign: 'center', fontFamily: FONTE.display, fontSize: 84, color: COR.branco, lineHeight: 1}}>{L.nome}</div>
          {L.sub && <div style={{position: 'absolute', left: 0, right: 0, bottom: 20, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 26, color: COR.branco, opacity: .85}}>{L.sub}</div>}
          <div style={{position: 'absolute', top: 18, [j ? 'right' : 'left']: 22, fontFamily: FONTE.display, fontSize: 56, color: j ? corB : corA, textShadow: '0 2px 0 #000'}}>{placar[j]}</div>
        </div>
      ))}
      <div style={{position: 'absolute', left: 20, width: 1040, top: 570, height: 650, borderRadius: 30, background: COR.painelSolido,
        border: '2px solid rgba(255,255,255,.1)', opacity: clamp(lt / 0.6)}} />
      <div style={{position: 'absolute', left: 540, top: 380, transform: `translate(-50%, -50%) scale(${k}) rotate(-6deg)`, fontFamily: FONTE.display, fontSize: 120,
        color: COR.amarelo, textShadow: `${neon(COR.amarelo, 1)}, 5px 7px 0 rgba(0,0,0,.45)`}}>VS</div>
      {linhas.map((l, i) => {
        const a = easeOut((t - quando(i)) / 0.35);
        if (a <= 0) return null;
        const y = 600 + i * 104;
        const win = t >= quando(i) + 0.4 ? l.vence : null;
        const cel = (v, lado) => {
          const ganhou = win === lado;
          const c = lado === 'a' ? corA : corB;
          return (
            <div style={{position: 'absolute', top: 0, [lado === 'a' ? 'left' : 'right']: 35, width: 330, height: 88, borderRadius: 18, display: 'grid', placeItems: 'center',
              background: ganhou ? c : 'rgba(255,255,255,.07)', border: `2px solid ${ganhou ? c : 'rgba(255,255,255,.18)'}`, boxShadow: ganhou ? neon(c, .6) : 'none',
              fontFamily: FONTE.display, fontSize: 42, color: ganhou ? COR.tinta : COR.branco, textAlign: 'center', lineHeight: 1}}>{v}</div>
          );
        };
        return (
          <div key={i} style={{position: 'absolute', left: 0, width: 1080, top: y, height: 88, opacity: a, transform: `translateY(${(1 - a) * 30}px)`}}>
            {cel(l.a, 'a')}
            <div style={{position: 'absolute', left: 375, width: 330, top: 0, height: 88, display: 'grid', placeItems: 'center', fontFamily: FONTE.apoio, fontSize: 24,
              color: COR.branco, textAlign: 'center', lineHeight: 1.1}}>{l.rotulo}</div>
            {cel(l.b, 'b')}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* =========================================================
   EVOLUÇÃO — linha do tempo que a câmera percorre
   Formato comprovado: "evolução do Homem-Aranha" (278 mil), "evolução dos gráficos do GTA" (104 mil).
   ========================================================= */
export const BlocoEvolucao = ({b, t}) => {
  const it = b.itens;
  const n = it.length;
  const ini = b.de + 0.6, fim = b.ate - 2;
  const quando = (i) => (it[i].em != null ? it[i].em : ini + (i * (fim - ini)) / Math.max(1, n - 1));
  // posição contínua da câmera: vai de um marco ao outro com suavização
  let pos = 0;
  for (let i = 1; i < n; i++) pos += easeOut((t - quando(i) + 0.15) / 0.7);
  const ESP = 720, CX = 540;
  const off = CX - pos * ESP;
  const gap = (i) => it[i].intervalo;
  return (
    <AbsoluteFill>
      {b.titulo && <div style={{position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', fontFamily: FONTE.display, fontSize: 70, color: COR.branco,
        textShadow: neon(COR.violeta, .6)}}>{b.titulo}</div>}
      {/* trilho */}
      <div style={{position: 'absolute', left: 0, width: 1080, top: 1060, height: 8, background: 'rgba(255,255,255,.15)'}} />
      <div style={{position: 'absolute', left: 0, width: Math.max(0, off + pos * ESP), top: 1060, height: 8, background: COR.amarelo, boxShadow: neon(COR.amarelo, .6)}} />
      {it.map((m, i) => {
        const x = off + i * ESP;
        if (x < -600 || x > 1680) return null;
        const foco = clamp(1 - Math.abs(pos - i));
        const a = easeOut((t - quando(i) + 0.3) / 0.4);
        const cor = CORES_ITEM[m.cor || (i === n - 1 ? 'rosa' : 'ciano')];
        return (
          <React.Fragment key={i}>
            {i > 0 && gap(i) && (
              <div style={{position: 'absolute', left: x - ESP / 2 - 150, width: 300, top: 1090, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 28,
                color: COR.amarelo, opacity: .4 + .6 * clamp(pos - i + 1)}}>{gap(i)}</div>
            )}
            <div style={{position: 'absolute', left: x - 22, top: 1042, width: 44, height: 44, borderRadius: 22, background: i <= pos + 0.01 ? COR.amarelo : 'rgba(255,255,255,.3)',
              boxShadow: foco > .5 ? neon(COR.amarelo, .7) : 'none'}} />
            <div style={{position: 'absolute', left: x - 290, width: 580, top: 380, height: 620, borderRadius: 34, overflow: 'hidden',
              opacity: Math.max(.35, a) * (0.45 + 0.55 * foco), transform: `scale(${0.82 + 0.18 * foco})`,
              background: COR.painel, border: `3px solid ${foco > .5 ? cor : 'rgba(255,255,255,.15)'}`, boxShadow: foco > .5 ? neon(cor, .5) : 'none'}}>
              <Midia src={m.midia} p={foco} style={{left: 0, top: 0, width: 580, height: 330}} />
              {!m.midia && <div style={{position: 'absolute', left: 0, top: 0, width: 580, height: 330, background: `radial-gradient(ellipse at 50% 60%, ${cor}66, transparent 70%)`}} />}
              <div style={{position: 'absolute', left: 0, right: 0, top: m.midia ? 220 : 70, textAlign: 'center', fontFamily: FONTE.display, fontSize: 150, lineHeight: 1,
                color: COR.branco, textShadow: `${neon(cor, .8)}, 4px 6px 0 rgba(0,0,0,.5)`}}>{m.ano}</div>
              <div style={{position: 'absolute', left: 20, right: 20, top: 380, textAlign: 'center', fontFamily: FONTE.display, fontSize: 64, color: cor, lineHeight: 1}}>{m.nome}</div>
              {m.texto && <div style={{position: 'absolute', left: 30, right: 30, top: 470, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 26, color: COR.branco, lineHeight: 1.25}}>{m.texto}</div>}
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

/* =========================================================
   CURIOSIDADE — "nº X de N", fato grande, mídia em tela cheia
   Formato comprovado: "10 curiosidades de Demon Slayer", "você percebeu…".
   ========================================================= */
export const BlocoCuriosidade = ({b, lt}) => {
  const dur = b.ate - b.de;
  const p = clamp(lt / dur);
  const k = back(lt / 0.4);
  const v = easeOut((lt - 0.25) / 0.5);
  const cor = CORES_ITEM[b.cor || 'rosa'];
  return (
    <AbsoluteFill>
      {b.midia
        ? <Midia src={b.midia} p={p} style={{left: 0, top: 0, width: 1080, height: 1920}} />
        : <div style={{position: 'absolute', left: 60, top: 250, width: 960, height: 880, borderRadius: 40,
            background: `radial-gradient(ellipse at 30% 20%, ${cor}55, ${COR.painelSolido} 65%)`, border: `2px solid ${cor}88`, boxShadow: neon(cor, .35)}} />}
      {b.midia && <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(8,4,20,.55) 0%, rgba(8,4,20,.1) 35%, rgba(8,4,20,.85) 70%)'}} />}
      {/* progresso X de N */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 200, display: 'flex', justifyContent: 'center', gap: 14}}>
        {new Array(b.total).fill(0).map((_, i) => (
          <div key={i} style={{width: i + 1 === b.numero ? 70 : 22, height: 22, borderRadius: 11,
            background: i + 1 <= b.numero ? COR.amarelo : 'rgba(255,255,255,.25)', boxShadow: i + 1 === b.numero ? neon(COR.amarelo, .5) : 'none'}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: 110, top: 300, transform: `scale(${k})`, transformOrigin: '0 0', fontFamily: FONTE.display, fontSize: 210, lineHeight: 1,
        color: cor, textShadow: `${neon(cor, 1)}, 6px 8px 0 rgba(0,0,0,.6)`}}>#{b.numero}</div>
      {b.valor && (
        <div style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', fontFamily: FONTE.display, fontSize: b.valor.length > 9 ? 120 : 170,
          color: COR.branco, opacity: v, transform: `scale(${0.85 + 0.15 * v})`, textShadow: `${neon(COR.amarelo, .7)}, 6px 8px 0 rgba(0,0,0,.6)`}}>{b.valor}</div>
      )}
      <div style={{position: 'absolute', left: 90, right: 90, top: b.valor ? 800 : 640, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 46, lineHeight: 1.15,
        color: COR.amarelo, opacity: v, textShadow: '0 3px 0 #000'}}>{b.titulo}</div>
      {b.texto && <div style={{position: 'absolute', left: 120, right: 120, top: b.valor ? 930 : 780, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 30, lineHeight: 1.25,
        color: COR.branco, opacity: easeOut((lt - 0.6) / 0.5)}}>{b.texto}</div>}
    </AbsoluteFill>
  );
};
