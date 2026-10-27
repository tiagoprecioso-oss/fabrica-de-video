import React, {useState} from 'react';
import {AbsoluteFill, Audio, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {FundoEstilo} from './componentes/Fundos';
import {Legenda} from './componentes/Legenda';
import {BlocoBarras, BlocoNumero, BlocoTitulo, camera} from './componentes/Blocos';
import {BlocoRanking, BlocoVersus, BlocoCuriosidade, BlocoEvolucao} from './componentes/Blocos2';

const BLOCOS = {barras: BlocoBarras, numero: BlocoNumero, titulo: BlocoTitulo, ranking: BlocoRanking, versus: BlocoVersus, curiosidade: BlocoCuriosidade, evolucao: BlocoEvolucao};
import {COR, FONTE, W, easeOut, clamp, aplicarEstilo} from './tema';

/* fontes locais (não depende de internet na hora de renderizar) */
const fontesCss = `
@font-face{font-family:'Anton';src:url('${staticFile('fonts/Anton.woff')}') format('woff');}
@font-face{font-family:'Archivo Black';src:url('${staticFile('fonts/ArchivoBlack.woff')}') format('woff');}
@font-face{font-family:'Bebas Neue';src:url('${staticFile('fonts/BebasNeue.woff')}') format('woff');}
@font-face{font-family:'Bangers';src:url('${staticFile('fonts/Bangers.woff')}') format('woff');}
@font-face{font-family:'Russo One';src:url('${staticFile('fonts/RussoOne.woff')}') format('woff');}`;
const useFontes = () => {
  const [h] = useState(() => delayRender('fontes'));
  React.useEffect(() => {
    Promise.all([
      new FontFace('Anton', `url(${staticFile('fonts/Anton.woff')})`).load(),
      new FontFace('Archivo Black', `url(${staticFile('fonts/ArchivoBlack.woff')})`).load(),
      new FontFace('Bebas Neue', `url(${staticFile('fonts/BebasNeue.woff')})`).load(),
      new FontFace('Bangers', `url(${staticFile('fonts/Bangers.woff')})`).load(),
      new FontFace('Russo One', `url(${staticFile('fonts/RussoOne.woff')})`).load(),
    ]).then((fs) => { fs.forEach((f) => document.fonts.add(f)); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

const WHIP_IN = 0.22, WHIP_OUT = 0.2, LOOP_OUT = 0.35;

/* deslize com borrão de movimento na entrada/saída dos blocos */
const whip = (b, t, dur) => {
  let x = 0;
  if (b.entrada === 'whip' && t < b.de + WHIP_IN) x = (1 - easeOut((t - b.de) / WHIP_IN)) * W * 0.9;
  const fim = b.saida === 'loop' ? LOOP_OUT : WHIP_OUT;
  if ((b.saida === 'whip' || b.saida === 'loop') && t > b.ate - fim) x = -easeOut((t - (b.ate - fim)) / fim) * W * 0.95;
  return {x, blur: Math.min(28, Math.abs(x) / 30)};
};

export const DadoMedido = ({video}) => {
  const estilo = aplicarEstilo(video.estilo);
  useFontes();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const dur = video.duracao;
  const batida = dur / (video.batidas || Math.round(dur / (60 / 104)));
  const ativos = video.blocos.filter((b) => t >= b.de && t < b.ate);
  const leg = video.legendas.find((l) => t >= l.de && t < l.ate);
  const fonte = [...(video.rodape || [])].reverse().find((r) => t >= r.de);
  const ultimo = video.blocos[video.blocos.length - 1];
  const legW = ultimo.saida === 'loop' && t > dur - LOOP_OUT ? -easeOut((t - (dur - LOOP_OUT)) / LOOP_OUT) * W * 0.95 : 0;
  return (
    <AbsoluteFill style={{background: COR.tinta}}>
      <style>{fontesCss}</style>
      <FundoEstilo estilo={estilo} t={t} dur={dur} />
      {ativos.map((b, i) => {
        const p = clamp((t - b.de) / (b.ate - b.de));
        const lt = t - b.de;
        const {x, blur} = whip(b, t, dur);
        const Comp = BLOCOS[b.tipo] || BlocoTitulo;
        return (
          <AbsoluteFill key={i} style={{perspective: 1800, perspectiveOrigin: '50% 40%', transform: `translateX(${x}px)`, filter: blur ? `blur(${blur}px)` : 'none'}}>
            <AbsoluteFill style={{transform: camera(b.camera, p, t, batida), transformOrigin: '50% 40%', transformStyle: 'preserve-3d'}}>
              <Comp b={b} t={t} lt={lt} />
            </AbsoluteFill>
          </AbsoluteFill>
        );
      })}
      <AbsoluteFill style={{transform: `translateX(${legW}px)`, filter: legW ? `blur(${Math.min(28, Math.abs(legW) / 30)}px)` : 'none'}}>
        {leg && <Legenda texto={leg.texto} lt={t - leg.de} dur={leg.ate - leg.de} />}
        {fonte && <div style={{position: 'absolute', left: 0, right: 0, top: 1530, textAlign: 'center', fontFamily: FONTE.apoio, fontSize: 22, color: COR.apagado}}>{fonte.texto}</div>}
      </AbsoluteFill>
      {video.trilha && <Audio src={staticFile(video.trilha)} />}
    </AbsoluteFill>
  );
};
