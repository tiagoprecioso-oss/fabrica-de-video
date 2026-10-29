# O estúdio

A fábrica é um estúdio com 28 agentes, um por função, em 7 departamentos. Cada linha de produção segue uma receita de `receitas/`, e o receiteiro melhora a receita depois de cada entrega. Tudo o que os canais publicam e vendem passa por esta linha. O Tiago é o dono do estúdio: aprova, publica e cuida das contas.

Cada agente é um arquivo em `.claude/agents/` com o que recebe, o que faz, o que entrega e para quem passa.

## Departamentos

| Departamento | Agentes |
|---|---|
| Pauta | olheiro, editor-chefe |
| Roteiro e dados | pesquisador, roteirista |
| Arte e vídeo | diretor, diretor-de-arte, artista-3d, ilustrador, compositor, narrador (esperando a voz), editor-de-gameplay |
| Marcas e portfólio | designer-de-marca, desenvolvedor-web, artista-3d (fotos e motion de produto) |
| Produtos | autor-de-ebook, diagramador, planilheiro, professor |
| Vendas | espiao-de-ofertas, copywriter, desenvolvedor-web, atendente-whatsapp, social-media, tradutor |
| Qualidade e números | checador, revisor, compliance, analista, produtor, receiteiro |

## As linhas de produção

**Marca (portfólio ou cliente)** — `receitas/marca.md`, `foto-produto-3d.md`, `site.md`, `motion-3d.md`
designer-de-marca (pesquisa → nome → manual) → artista-3d (rótulos, fotos e motion no Blender) → desenvolvedor-web (site) → diretor (Reels) → revisor → receiteiro → **Tiago aprova e publica no portfólio**


**Vídeo curto (todos os canais)** — `receitas/video-curto.md`
olheiro → editor-chefe → pesquisador → roteirista → checador → diretor-de-arte + compositor (+ narrador, + editor-de-gameplay) → diretor → render no GitHub → revisor → compliance → social-media → **Tiago aprova e posta**

**Ebook**
editor-chefe → pesquisador → autor-de-ebook → checador → diagramador (PDF) + desenvolvedor-web (página interativa) + ilustrador (capa e mockups) + planilheiro (planilha bônus) → revisor → compliance → copywriter (página e Hotmart) → **Tiago sobe na Hotmart**

**Minicurso**
professor → checador → narrador → diretor (modelo horizontal) → revisor → compliance → **Tiago sobe as aulas**

**Funil**
copywriter → desenvolvedor-web (calculadora, captura, venda) → atendente-whatsapp (robô) → compliance → **Tiago conecta as contas**

**Toda semana**
analista (números) → editor-chefe (o que repetir) → produtor (andamento e Chão da Fábrica)

## Canais

| Canal | Idioma | Estilos | Produto |
|---|---|---|---|
| Cultura pop | português | synthwave, arcade, cinema, anime, streaming, espaço | — (anúncios) |
| Din no Chão (finanças) | português | grana | ebook "Chefões do cartão", depois minicurso |
| Cultura pop EN | inglês | os mesmos do pop | — (anúncios) |

## Regras que valem para todos
- Tudo sai da fábrica (script, JSON ou arquivo do repositório) e tudo que dá certo vira receita.
- Nada é postado ou vendido sem o Tiago.
- Todo número tem fonte; o checador refaz as contas.
- GTA nunca leva imagens do jogo; gameplay só gravada pelo Tiago, de jogo que permite monetizar (`docs/direitos.md`).
- Finanças é educativo: sem recomendar investimento nem prometer ganho.
- Variação real entre vídeos (formato, estilo, assunto), para não parecer conteúdo em massa.

## Andamento
- Ativos: olheiro (06:47), pesquisador, roteirista, diretor, revisor, checador, diretor-de-arte, compositor, editor-chefe, social-media, compliance, produtor.
- Em construção: estilo `grana` e blocos de finanças.
- Testados em 29/10: autor-de-ebook e diagramador (ebook "Chefões do cartão", `tools/ebook.py`).
- Esperando o Tiago: narrador (escolher a voz), editor-de-gameplay (gravação do Fortnite), atendente-whatsapp e desenvolvedor-web (contas e ferramenta de e-mail), analista (canais no ar).

## Desempenho dos agentes
Regra desde 29/10 (Felipe): toda etapa passa pelo agente da função, e aqui fica o que cada um fez bem ou mal, para aprimorar o arquivo dele em `.claude/agents/`.

| Data | Agente | Tarefa | Bom | A melhorar |
|---|---|---|---|---|
| 29/10 | (sessão principal) | ebook "Chefões do cartão" até a capa | — | Feito sem os agentes; a partir daqui, cada etapa vai pelo agente da função. |
| 29/10 | checador | Checagem independente do ebook (46 itens) | Refez todas as contas com código próprio e rodou o simulador da página; achou 11 problemas que a autochecagem deixou passar (regras jurídicas imprecisas, fonte de 2012, contradição texto × página, um arredondamento). | Citou 3 normas de memória sem abrir (REN 1.000/2021, Res. CMN 3.517/2007, art. 104-A do CDC): pedir que abra toda norma que sugerir. |
