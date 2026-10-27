# Modelos da fábrica

Cada vídeo é um arquivo JSON em `videos/<id>.json`. O agente **diretor** escreve esse JSON; `./fabricar.sh videos/<id>.json` renderiza.

## Modelo `DadoMedido` (pronto)

Vídeo vertical 1080×1920, 30 fps, com fundo synthwave, legendas corridas e final em loop.

```jsonc
{
  "id": "slug-do-video",            // nome do arquivo final
  "modelo": "DadoMedido",
  "titulo": "Título interno",
  "duracao": 44.5,                  // segundos; = "ate" do último bloco e da última legenda
  "batidas": 77,                    // nº inteiro de batidas no vídeo (≈ duracao / 0.577) — fecha o loop da trilha
  "trilha": "trilhas/slug-do-video.wav",
  "blocos": [ ... ],                // o que aparece na tela, em sequência, sem buracos
  "legendas": [ {"de": 0, "ate": 3.2, "texto": "Frase com *destaque*."} ],
  "rodape": [ {"de": 0, "texto": "Fonte: ..."} ],
  "fontes": [ {"titulo": "...", "url": "..."} ]
}
```

### Campos comuns de todo bloco
| campo | valores |
|---|---|
| `tipo` | `numero` · `barras` · `titulo` |
| `de`, `ate` | início e fim em segundos |
| `camera` | `empurrar` (zoom lento) · `orbita` (gira em Y) · `inclinar` (vem de cima) · `mergulho` (vem de longe) |
| `entrada` | `whip` (desliza com borrão) ou omitido |
| `saida` | `whip` · `loop` (obrigatório no último bloco) ou omitido |

### `numero` — número gigante contando
`valor`, `moeda` (`$` ou `R$`), `casas`, `chip` (etiqueta em cima), `nota`, `nota2` (amarela).

### `titulo` — virada de assunto
`linha1` (menor), `linha2` (gigante amarela), `corLinha` (`verde`, `rosa`, `ciano`, `amarelo`).

### `barras` — comparação com "antes → depois"
- `titulo`, `tituloDepois` (troca quando o valor corrigido entra)
- `moeda`, `casas`, `max` (topo do eixo, deixe ~25% de folga acima do maior valor), `grade` (linhas do eixo)
- `itens`: `{nome, ano, valor, valorDepois?, cor?, entra?}` — até 6 itens; `cor` padrão ciano, use `rosa` para o protagonista
- `morphEm`: segundo em que os valores viram `valorDepois`
- `destaques`: `[{em, indices}]` — quais barras ficam acesas a partir de `em` (`null` = todas)
- `formula`: `{de, ate, linha1, linha2}` — cartão mostrando a conta
- `selo`: `{em, texto, indice}` — selo amarelo com partículas
- `mostrarDiferenca`: mostra "+$45" acima de cada barra corrigida
- `notaFantasma`: texto dentro do contorno do valor antigo

## Regras de qualidade (o revisor confere)
1. Todo número na tela tem fonte em `fontes` e bate com ela.
2. Legendas: 1 frase por trecho, 2 linhas no máximo, 1–2 palavras em `*destaque*`.
3. Último bloco com `"saida": "loop"`, e a última legenda emenda no gancho da primeira.
4. Nada de logo, pôster ou arte oficial desenhada; prints e clipes oficiais só entram por cima, na edição.
5. Duração 25–45 s.

## Qual modelo usar (baseado no que viraliza no nicho, out/2026)
| modelo (`"modelo"`) | quando usar | exemplos que bombam |
|---|---|---|
| `DadoMedido` | um número muda tudo quando corrigido/comparado | "o preço de GTA 6, medido" |
| `Ranking` | lista ordenável por um número (vendas, preço, nota, audiência) | "5 games mais vendidos" (750 mil), "10 animes mais assistidos" (620 mil) |
| `Versus` | dois produtos rivais, atributo por atributo | "GTA 6 vs GTA 5" (657 mil), "Goku vs Naruto" (227 mil) |
| `Curiosidades` | 3–7 fatos curtos sobre um lançamento/obra | "10 curiosidades de Demon Slayer" (2,5 mi), "cada Homem-Aranha pula diferente" (960 mil) |
| `Evolucao` | algo que muda ao longo do tempo (datas, versões, gráficos, atores) | "evolução do Homem-Aranha" (278 mil), "evolução dos gráficos do GTA" (104 mil) |

Todos usam o mesmo motor; misture blocos quando fizer sentido (ex.: abrir um Ranking com um bloco `titulo`).

### `ranking` — contagem regressiva do último ao 1º
- `titulo`, `subtitulo`, `moeda`, `casas`, `unidade` (ex.: "mi"), `max`
- `itens`: em ordem do **1º lugar primeiro**: `{nome, sub, valor, cor?}` (até 7). O 1º fica amarelo com partículas.
- `revelacoes`: tempos (s) de entrada de cada item, na mesma ordem dos itens (o 1º é o último a aparecer). Sincronize com a legenda que fala aquele lugar.

### `versus` — lado a lado
- `lados`: `[{nome, sub, cor, midia?}, {…}]` (cor padrão: ciano × rosa)
- `linhas`: `{rotulo, a, b, vence?: "a"|"b", em}` (até 6). O placar no canto conta as vitórias.

### `curiosidade` — um fato por bloco
- `numero`, `total` (bolinhas de progresso no topo), `cor`, `valor` (o número/palavra gigante, curto), `titulo`, `texto`, `midia?`
- Um bloco por fato, 5–6 s cada, com `entrada`/`saida` whip; o último com `saida: loop`.

### `evolucao` — linha do tempo percorrida pela câmera
- `titulo`, `itens`: `{ano, nome, texto?, intervalo?, midia?, cor?, em}` (4–8). `em` = segundo em que a câmera chega naquele marco; sincronize com a legenda. `intervalo` aparece no trilho antes do item ("+13 ANOS").

## Estilos visuais (`"estilo"` no JSON)
Cada estilo troca fundo, cores, fontes e painéis de uma vez.
| estilo | visual | use para |
|---|---|---|
| `synthwave` (padrão) | sol listrado, grade neon 3D, roxo/rosa | games atuais, tecnologia |
| `arcade` | tela CRT, pixels, cidade em blocos, verde fósforo | games retrô, nostalgia, linhas do tempo de games |
| `cinema` | sala escura, holofotes, poeira, granulado, dourado | filmes, bilheteria, Oscar |
| `streaming` | manchas de luz desfocadas, vidro | séries, Netflix/Prime/HBO |
| `anime` | linhas de velocidade, retícula de mangá, faixa vermelha | animes e mangás |
| `espaco` | estrelas em camadas, nebulosa, planeta | ficção científica, lançamentos "épicos" |

Varie o estilo entre vídeos seguidos do mesmo tema.

### Mídia (print ou clipe)
`midia: "midias/arquivo.jpg"` (ou .mp4) em `curiosidade` e nos `lados` do `versus`. O arquivo vai em `public/midias/`. Só fontes oficiais, clipes de 3–5 s. Sem mídia o bloco tem visual próprio — nunca invente imagem.

## Camada gameplay (`"gameplay"` no JSON) — o visual que mais segura em games
Análise de out/2026 (Vitoca, Leley, Eri, GamerCosta): nos shorts de games que passam de milhões, o **jogo roda o vídeo inteiro** e a própria cena prova o fato. Funciona com qualquer modelo.

```json
"gancho": "O GTA mais caro da história (corrigido pela inflação)",
"gameplay": {"arquivo": "gameplay/gta5-voo.mp4", "layout": "cheia", "duracaoClipe": 60, "corte": 2.5, "inicio": 0, "escurecer": 0.4}
```
- `layout: "cheia"` — gameplay na tela toda; os painéis viram vidro escuro por cima. Bom para ranking, curiosidades e "você sabia".
- `layout: "dividida"` — dados na metade de cima, gameplay embaixo (y 1000–1920). Bom para versus, barras e evolução.
- `corte` — troca de trecho do clipe a cada N segundos, com soco de zoom e clarão (os virais trocam de cena a cada 1–3 s). `0` = sem cortes.
- `duracaoClipe` — duração real do arquivo em segundos (obrigatório).
- Com gameplay a legenda vira **dupla**: a frase pequena + a palavra entre `*asteriscos*` gigante. Marque **uma** palavra-chave por legenda. `gancho` fica fixo no topo (só no layout cheio).
- **Direitos:** só gameplay **gravada pelo Tiago** (pasta `public/gameplay/`) e de jogos que permitem monetizar (hoje: **Fortnite**; ver `docs/direitos.md`). Nunca baixar gameplay de outro canal. **GTA não**: a política da Rockstar proíbe uso comercial das imagens — pautas de GTA usam só as nossas animações ou gameplay de outro jogo no layout dividido. Vídeo com Fortnite leva o aviso da Epic na descrição. Como gravar: `docs/gravar-gameplay.md`.
- `gameplay/teste.mp4` é um clipe sintético só para testar o layout.

## Canal de finanças (estilo `grana`, composição `Financas`)
Formato próprio, diferente do canal de games: caderno de contas claro (quadriculado, margem vermelha, moedas), legenda em cartão branco com borda, destaque em vermelho-dívida. Dinheiro vira jogo.

### `chefao` — a dívida como chefão com barra de vida
```json
{"tipo": "chefao", "de": 0, "ate": 25, "rotulo": "CHEFÃO", "nome": "ROTATIVO DO CARTÃO", "divida": 1000,
 "taxa": 0.151752, "taxaTexto": "15,18% AO MÊS", "meses": 12, "teto": 2, "inicio": 4, "fim": 22, "selo": "TRAVADO PELA LEI"}
```
- A barra (vida = saldo) cresce mês a mês com juros compostos (`taxa` ao mês, fração) entre `inicio` e `fim`.
- `teto` (multiplicador, opcional): parede da lei; a barra trava ali e o resto vira "fantasma" listrado com o valor "sem a lei" riscado. Rotativo e parcelado do cartão: `teto: 2` (Lei 14.690/2023).
- Use a taxa que bate com a anual oficial: `taxa = (1 + anual)^(1/12) − 1`.

### `extrato` — linhas de um recibo aparecendo, com total
```json
{"tipo": "extrato", "titulo": "R$ 1.000 NO ROTATIVO", "linhas": [{"texto": "Dívida original", "valor": "R$ 1.000", "em": 25.6},
 {"texto": "Juros máximos (lei)", "valor": "+ R$ 1.000", "cor": "vermelho", "em": 26.6}], "total": {"texto": "Teto da dívida", "valor": "R$ 2.000", "cor": "vermelho", "em": 27.6}}
```
- Os modelos de sempre (ranking, versus, evolução, dado medido) também funcionam no estilo `grana`.
- Rodapé obrigatório: fonte oficial (Banco Central/IBGE com o código da série) e "Conteúdo educativo, não é recomendação financeira".
