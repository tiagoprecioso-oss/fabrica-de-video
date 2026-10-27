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

## Próximos modelos (a construir)
- `TresProvas` — gancho + 3 provas numeradas com mídia (print/clipe) em quadro.
- `Ranking` — top 5 com barras horizontais correndo.
- `Curiosidades` — lista numerada com mídia em tela cheia.
