import React from 'react';
import {Composition} from 'remotion';
import {DadoMedido} from './DadoMedido';
import dado from '../videos/gta6-preco.json';
import ranking from '../videos/gta-ranking-precos.json';
import versus from '../videos/gta6-vs-gta5.json';
import curiosidades from '../videos/gta6-5-fatos.json';

// Todos os modelos usam o mesmo motor; o JSON decide os blocos.
const MODELOS = [['DadoMedido', dado], ['Ranking', ranking], ['Versus', versus], ['Curiosidades', curiosidades]];

export const Root = () => (
  <>
    {MODELOS.map(([id, ex]) => (
      <Composition key={id} id={id} component={DadoMedido} width={1080} height={1920} fps={30}
        durationInFrames={Math.round(ex.duracao * 30)} defaultProps={{video: ex}}
        calculateMetadata={({props}) => ({durationInFrames: Math.round(props.video.duracao * 30)})} />
    ))}
  </>
);
