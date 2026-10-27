import React from 'react';
import {Composition} from 'remotion';
import {DadoMedido} from './DadoMedido';
import exemplo from '../videos/gta6-preco.json';

// Cada vídeo da fábrica é um JSON (pasta videos/) que alimenta um modelo.
export const Root = () => (
  <Composition
    id="DadoMedido"
    component={DadoMedido}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={Math.round(exemplo.duracao * 30)}
    defaultProps={{video: exemplo}}
    calculateMetadata={({props}) => ({durationInFrames: Math.round(props.video.duracao * 30)})}
  />
);
