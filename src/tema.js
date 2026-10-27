// Identidade visual da fábrica. Trocar aqui muda todos os vídeos.
export const COR = {
  tinta: '#0A0618',
  branco: '#F8F6FF',
  amarelo: '#FFD600',
  rosa: '#FF2E78',
  ciano: '#00E1FF',
  violeta: '#8C3CFF',
  verde: '#00D278',
  apagado: '#A096CD',
};
export const CORES_ITEM = {rosa: COR.rosa, ciano: COR.ciano, amarelo: COR.amarelo, verde: COR.verde, violeta: COR.violeta};
export const FONTE = {
  display: "'Anton', Impact, 'Arial Narrow', sans-serif",
  apoio: "'Archivo Black', 'Arial Black', sans-serif",
};
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
