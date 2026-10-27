// Identidade visual da fábrica. Cada vídeo escolhe um "estilo" no JSON;
// aplicarEstilo() troca cores, fontes e painéis de todos os componentes.
const D = {
  anton: "'Anton', Impact, 'Arial Narrow', sans-serif",
  bebas: "'Bebas Neue', 'Anton', Impact, sans-serif",
  bangers: "'Bangers', 'Anton', Impact, sans-serif",
  russo: "'Russo One', 'Anton', sans-serif",
  archivo: "'Archivo Black', 'Arial Black', sans-serif",
  archivoTexto: "'Archivo Texto', 'Archivo Black', 'Arial', sans-serif",
};

export const ESTILOS = {
  // games, tech, nostalgia anos 80
  synthwave: {
    cor: {tinta: '#0A0618', branco: '#F8F6FF', amarelo: '#FFD600', rosa: '#FF2E78', ciano: '#00E1FF', violeta: '#8C3CFF', verde: '#00D278', apagado: '#A096CD'},
    painel: 'linear-gradient(180deg, rgba(30,12,60,.92), rgba(14,6,32,.92))', painelSolido: 'rgba(14,6,32,.92)', legenda: 'rgba(8,4,20,.80)',
    fonte: {display: D.anton, apoio: D.archivo},
  },
  // filmes: sala escura, holofote, granulado, dourado
  cinema: {
    cor: {tinta: '#07070A', branco: '#F5F1E8', amarelo: '#E8B04B', rosa: '#D7263D', ciano: '#8EC5CC', violeta: '#7D6BA6', verde: '#6FBF73', apagado: '#9B9488'},
    painel: 'linear-gradient(180deg, rgba(28,24,20,.94), rgba(10,9,8,.94))', painelSolido: 'rgba(12,11,10,.94)', legenda: 'rgba(0,0,0,.78)',
    fonte: {display: D.bebas, apoio: D.archivo},
  },
  // animes: linhas de velocidade, retícula de mangá, vermelho
  anime: {
    cor: {tinta: '#0B0B10', branco: '#FFFFFF', amarelo: '#FFE14D', rosa: '#FF3B3B', ciano: '#3BB2FF', violeta: '#B04BFF', verde: '#3DDC84', apagado: '#A8A8B8'},
    painel: 'linear-gradient(180deg, rgba(20,20,28,.95), rgba(8,8,12,.95))', painelSolido: 'rgba(10,10,14,.95)', legenda: 'rgba(0,0,0,.82)',
    fonte: {display: D.bangers, apoio: D.archivo},
  },
  // games retrô: tela CRT, pixels, verde fósforo
  arcade: {
    cor: {tinta: '#040A06', branco: '#E8FFE8', amarelo: '#FFE600', rosa: '#FF3EA5', ciano: '#3EFF8B', violeta: '#7A5CFF', verde: '#3EFF8B', apagado: '#7FA68A'},
    painel: 'linear-gradient(180deg, rgba(6,24,12,.94), rgba(2,10,5,.94))', painelSolido: 'rgba(3,12,6,.94)', legenda: 'rgba(0,8,2,.84)',
    fonte: {display: D.russo, apoio: D.archivo},
  },
  // séries/streaming: manchas de luz desfocadas, vidro
  streaming: {
    cor: {tinta: '#050814', branco: '#F4F6FF', amarelo: '#FFC94D', rosa: '#FF4D6D', ciano: '#4DD2FF', violeta: '#7B61FF', verde: '#3DDCA0', apagado: '#93A0C4'},
    painel: 'linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.04))', painelSolido: 'rgba(12,16,36,.88)', legenda: 'rgba(5,8,20,.72)',
    fonte: {display: D.bebas, apoio: D.archivo},
  },
  // ficção científica, espaço, lançamentos "épicos"
  espaco: {
    cor: {tinta: '#03030C', branco: '#EEF3FF', amarelo: '#FFD86B', rosa: '#FF5FA2', ciano: '#5CE1FF', violeta: '#9B6BFF', verde: '#5CFFC4', apagado: '#8C93B8'},
    painel: 'linear-gradient(180deg, rgba(20,24,60,.85), rgba(6,8,24,.9))', painelSolido: 'rgba(6,8,24,.9)', legenda: 'rgba(3,3,12,.78)',
    fonte: {display: D.anton, apoio: D.archivo},
  },
};

// finanças (canal Din no Chão): caderno de contas claro, verde dinheiro, vermelho dívida
ESTILOS.grana = {
  claro: true,
  cor: {tinta: '#EEF3EE', branco: '#12241B', amarelo: '#C77700', rosa: '#E03E2D', ciano: '#0E8A5F', violeta: '#3557D6', verde: '#0E9F6E', apagado: '#5C6F64', destaque: '#E03E2D', papel: '#FFFFFF'},
  painel: 'linear-gradient(180deg, #FFFFFF, #F7FAF7)', painelSolido: '#FFFFFF', legenda: 'rgba(255,255,255,.94)',
  fonte: {display: D.archivo, apoio: D.archivoTexto},
};

export const COR = {...ESTILOS.synthwave.cor, painel: ESTILOS.synthwave.painel, painelSolido: ESTILOS.synthwave.painelSolido, legenda: ESTILOS.synthwave.legenda};
export const CORES_ITEM = {};
export const FONTE = {...ESTILOS.synthwave.fonte};

export const aplicarEstilo = (nome) => {
  const e = ESTILOS[nome] || ESTILOS.synthwave;
  Object.assign(COR, {destaque: undefined, papel: undefined}, e.cor, {painel: e.painel, painelSolido: e.painelSolido, legenda: e.legenda, claro: !!e.claro});
  Object.assign(CORES_ITEM, {rosa: COR.rosa, ciano: COR.ciano, amarelo: COR.amarelo, verde: COR.verde, violeta: COR.violeta});
  Object.assign(FONTE, e.fonte);
  return nome in ESTILOS ? nome : 'synthwave';
};
aplicarEstilo('synthwave');

export const W = 1080;
export const H = 1920;

export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const easeOut = (t) => 1 - Math.pow(1 - clamp(t), 3);
export const easeInOut = (t) => {
  t = clamp(t);
  return t * t * (3 - 2 * t);
};
export const back = (t) => {
  t = clamp(t);
  const c = 1.7;
  return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2);
};
// mola: 0 -> 1 com um quique amortecido
export const mola = (x, k = 5.5, w = 9) => (x <= 0 ? 0 : 1 - Math.exp(-k * x) * Math.cos(w * x));

export const dinheiro = (v, moeda = '$', casas = 0) => {
  const n = v.toFixed(casas).replace('.', ',');
  return moeda === 'R$' ? `R$ ${n}` : `${moeda}${n}`;
};
