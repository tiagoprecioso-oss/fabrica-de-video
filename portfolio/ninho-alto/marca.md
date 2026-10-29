# Ninho Alto Coffee — marca vitrine (projeto conceitual)

Marca **fictícia** da Precioso Productions para o portfólio em inglês (clientes em dólar/euro). Toda peça leva: "Concept project — fictional brand by Precioso Productions".

## Conceito
Loja online americana (DTC) de café especial brasileiro de altitude, da Mantiqueira (MG). Promessa: **"Grown above 1,100 m. Roasted the week you order."** Torra sob demanda, envio em 72 h, assinatura com 15% de desconto.

**Fonte única:** `marca.json` (cores, tipos, escala, logo, lotes, foto, motion, voz). O manual completo como design system é gerado dele: `python3 tools/manual_ninho.py` → `manual.html` (artifact "Ninho Alto Brand Manual"), `tokens.css` e `logo/` (wordmark em curvas e marca de altitude). Os rótulos (`tools/rotulo_ninho.py`) também leem do `marca.json`. Mudou cor, nome ou lote: muda no JSON e roda os dois scripts.

## Identidade (v2, 29/10 — refeita após pesquisa de lojas de café de referência: SEY, Coffee Collective, Tim Wendelboe, La Cabra, Onyx, Kinto)
- **O que aprendemos:** as melhores lojas deixam a **imagem do produto** contar a história; tipografia pequena e exata; cores só na embalagem; dados reais (altitude, processo, variedade) no lugar de enfeites.
- **Assinatura visual:** cada rótulo é um **mapa topográfico** da encosta do lote, com um ponto na altitude (gerado por `tools/rotulo_ninho.py`).
- **Wordmark:** NINHO ALTO em caixa alta espaçada (Hanken Grotesk 600, tracking 0.32 em), em curvas em `logo/`. O logo antigo (sol, montanha, Syne) foi aposentado.
- **Marca de altitude:** 4 curvas de nível + ponto, só para avatar, favicon e selo pequeno.
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
- [x] Manual completo como design system (`manual.html`, gerado de `marca.json`): logo e regras, marca de altitude, cores com contraste WCAG, tipos e escala, rótulos, foto, motion, componentes, espaço
- [x] Rótulos topográficos dos 3 lotes
- [x] Fotos de produto 3D (hero + 3 pacotes)
- [x] Site/loja conceito v2 (artifact "Ninho Alto Coffee"; fonte: `site.html`)
- [x] Fotos 3D v2 (29/10): texturas reais, papel com vincos, render na RTX 3060
- [ ] Macro dos grãos em 3D (v2 melhorou: fenda com película, cor por grão; ainda parece CG de perto)
- [ ] 3 Reels verticais na fábrica (lançamento do Reserve, "por que altitude muda o café", receita de pour-over)
- [ ] Vídeo de produto 3D no Blender (cena `pacote` já anima o giro: renderizar no PC do Tiago com GPU)
- [ ] 2 anúncios verticais (Meta/TikTok) e 1 carrossel
- [ ] Projeto no Behance com tudo acima
