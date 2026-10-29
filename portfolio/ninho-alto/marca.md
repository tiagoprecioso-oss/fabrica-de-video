# Ninho Alto Coffee — marca vitrine (projeto conceitual)

Marca **fictícia** da Precioso Productions para o portfólio em inglês (clientes em dólar/euro). Toda peça leva: "Concept project — fictional brand by Precioso Productions".

## Conceito
Loja online americana (DTC) de café especial brasileiro de altitude, da Mantiqueira (MG). Promessa: **"Grown above 1,100 m. Roasted the week you order."** Torra sob demanda, envio em 72 h, assinatura com 15% de desconto.

## Identidade (v2, 29/10 — refeita após pesquisa de lojas de café de referência: SEY, Coffee Collective, Tim Wendelboe, La Cabra, Onyx, Kinto)
- **O que aprendemos:** as melhores lojas deixam a **imagem do produto** contar a história; tipografia pequena e exata; cores só na embalagem; dados reais (altitude, processo, variedade) no lugar de enfeites.
- **Assinatura visual:** cada rótulo é um **mapa topográfico** da encosta do lote, com um ponto na altitude (gerado por `tools/rotulo_ninho.py`).
- **Wordmark:** NINHO ALTO em caixa alta espaçada (Hanken Grotesk 600).
- **Cores:** pedra `#ECE9E4` · tinta `#1C1B19` · ocre `#B0761E` (Sunrise) · azul-noite `#24385C` (Night) · sangue-de-boi `#8C2622` (Reserve).
- **Tipos:** Hanken Grotesk (tudo) · IBM Plex Mono (fichas e números).
- **Fotos:** 100% 3D no Blender (`blender/ninho_produto.py`): pacotes stand-up, grãos, laje de pedra, luz de janela. Pipeline: `tools/pecas_ninho.sh`.
- **Voz:** direta, técnica sem ser esnobe; sempre um dado concreto.

## Produtos (ilustrativos)
| Café | Notas | Processo | Altitude | Torra | Preço |
|---|---|---|---|---|---|
| Cerrado Sunrise (amarelo) | chocolate ao leite, avelã, casca de laranja | cereja descascado | 1.150 m | média | US$ 19 / 12 oz |
| Mantiqueira Night (azul) | cacau, melaço, amêndoa | natural | 1.250 m | média-escura | US$ 21 / 12 oz |
| Ninho Reserve (vermelho) | frutas vermelhas, rapadura, jasmim | natural anaeróbico | 1.400 m | clara | US$ 26 / 12 oz |

## Entregas do portfólio
- [x] Rótulos topográficos dos 3 lotes
- [x] Fotos de produto 3D (hero + 3 pacotes)
- [x] Site/loja conceito v2 (artifact "Ninho Alto Coffee"; fonte: `site.html`)
- [ ] Macro dos grãos em 3D (cena `graos` ainda parece chocolate: falta textura, cor irregular e fenda funda)
- [ ] 3 Reels verticais na fábrica (lançamento do Reserve, "por que altitude muda o café", receita de pour-over)
- [ ] Vídeo de produto 3D no Blender (cena `pacote` já anima o giro: renderizar no PC do Tiago com GPU)
- [ ] 2 anúncios verticais (Meta/TikTok) e 1 carrossel
- [ ] Projeto no Behance com tudo acima
