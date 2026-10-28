# Pesquisa — Street Fighter vs Resident Evil: qual filme de game venceu?

**Pergunta:** entre os dois filmes de videogame de 2026 nos cinemas, qual foi melhor de bilheteria?

## Dados
| dado | Resident Evil (2026) | Street Fighter (2026) | referência | fonte |
|---|---|---|---|---|
| estreia nos EUA (EUA+Canadá) | US$ 60.152.878 (18–20/09/2026) | US$ 30.775.377 (16–18/10/2026) | fds de estreia | The Numbers (páginas dos filmes); Wikipedia lista nº1 EUA 2026 |
| estreia no Brasil | R$ 10,67 mi (17–21/09, 2º lugar) | R$ 5,69 mi (15–18/10, 2º lugar) | Comscore/Rentrak | Omelete (bilheteria BR 17–21/set; 15–18/out); QG do POP |
| 2º fds nos EUA | US$ 23.012.848 (−62%) | US$ 8.587.187 (−72%) | 2º fds | The Numbers |
| acumulado EUA após 10 dias (2º domingo) | US$ 103.189.095 (até 27/09) | US$ 46.925.821 (até 25/10) | mesmo ponto da carreira | The Numbers |
| orçamento de produção | US$ 75 mi (The Numbers, AP/WECT) · US$ 80 mi (Wikipedia) | US$ 82 mi | sem marketing | The Numbers; Wikipedia; EventHubs ("$82 million movie") |
| bilheteria mundial até agora | US$ 383.891.734 (até 25/10) | US$ 80.283.997 (até 26/10) | acumulado | The Numbers |
| estúdio / direção | Sony (Columbia) · Zach Cregger | Paramount (Legendary/Capcom) · Kitao Sakurai | | The Numbers; The Star |
| 2º fds no Brasil | — | R$ 2,28 mi (4º lugar, 22–25/10) | | Exame |
| Super Mario Galaxy: O Filme, mundial | US$ 1.000.028.930 (jun/2026, ainda em cartaz então) | | | VGC citando Box Office Mojo |

## Contas (Python)
- Queda 2º fds: RE 1 − 23,01/60,15 = 61,7% (≈ −62%); SF 1 − 8,59/30,78 = 72,1% (−72%).
- 10 dias EUA: 103,19 / 46,93 = 2,2× a favor de RE.
- Estreia BR: 10,67 / 5,69 = 1,88×.
- Mundo / orçamento: RE 383,9/75 = 5,1× (4,8× com 80); SF 80,28/82 = 0,98× → faltam US$ 1,7 mi só para cobrir a produção (sem marketing).
- Soma dos dois no mundo: 464,2 mi = 46% do Mario Galaxy (US$ 1,0 bi) → "não chegam à metade".

## Dúvidas
- Orçamento de RE diverge (75 x 80) — o vídeo mostra "$75–80 MI"; nos dois casos é menor que os US$ 82 mi de SF.
- Períodos de estreia no Brasil são os do relatório Comscore de cada semana (RE 17–21/09, 5 dias; SF 15–18/10, 4 dias) — a comparação BR é aproximada; dito como "estreia no Brasil".
- A pauta dizia "RE caiu uns 61%": o The Numbers registra −62% (61,7%). Usado −62%.
- Sem dado de público (ingressos) no Brasil.

## Fontes
- https://www.the-numbers.com/movie/Resident-Evil-(2026)
- https://www.the-numbers.com/movie/Street-Fighter-%282026%29
- https://en.wikipedia.org/wiki/List_of_2026_box_office_number-one_films_in_the_United_States
- https://www.wect.com/2026/09/21/box-office-resident-evil-tops-box-office-with-franchise-best-debut-60-million/
- https://en.wikipedia.org/wiki/Resident_Evil_(2026_film)
- https://www.eventhubs.com/news/2026/oct/26/street-fighter-box-office-disaster/
- https://www.thestar.com.my/news/world/2026/10/19/street-fighter-tops-north-american-box-office-in-opening-weekend
- https://www.omelete.com.br/filmes/bilheteria-brasil-17-a-21-set-estreia-resident-evil-minha-melhor-amiga-lidera-3a-semana
- https://www.omelete.com.br/filmes/bilheteria-brasil-15-18-outubro-verity-lideranca-estreia-street-fighter-dentro-da-baleia
- https://exame.com/pop/cara-de-barro-lidera-bilheteria-mundial-mas-cinemas-brasileiros-tem-pior-resultado-do-ano/
- https://www.videogameschronicle.com/news/the-super-mario-galaxy-movie-has-finally-passed-1-billion-globally-making-it-the-first-2026-film-to-do-so/
