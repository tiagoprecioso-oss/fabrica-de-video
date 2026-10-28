# O estúdio

A fábrica é um estúdio com 23 agentes, um por função, em 6 departamentos. Tudo o que os canais publicam e vendem passa por esta linha. O Tiago é o dono do estúdio: aprova, publica e cuida das contas.

Cada agente é um arquivo em `.claude/agents/` com o que recebe, o que faz, o que entrega e para quem passa.

## Departamentos

| Departamento | Agentes |
|---|---|
| Pauta | olheiro, editor-chefe |
| Roteiro e dados | pesquisador, roteirista |
| Arte e vídeo | diretor, diretor-de-arte, compositor, narrador (esperando a voz), editor-de-gameplay |
| Produtos | autor-de-ebook, diagramador, professor |
| Vendas | espiao-de-ofertas, copywriter, desenvolvedor-web, atendente-whatsapp, social-media, tradutor |
| Qualidade e números | checador, revisor, compliance, analista, produtor |

## As linhas de produção

**Vídeo curto (todos os canais)**
olheiro → editor-chefe → pesquisador → roteirista → checador → diretor-de-arte + compositor (+ narrador, + editor-de-gameplay) → diretor → render no GitHub → revisor → compliance → social-media → **Tiago aprova e posta**

**Ebook**
editor-chefe → pesquisador → autor-de-ebook → checador → diagramador → revisor → compliance → copywriter (página e Hotmart) → desenvolvedor-web → **Tiago sobe na Hotmart**

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
- Nada é postado ou vendido sem o Tiago.
- Todo número tem fonte; o checador refaz as contas.
- GTA nunca leva imagens do jogo; gameplay só gravada pelo Tiago, de jogo que permite monetizar (`docs/direitos.md`).
- Finanças é educativo: sem recomendar investimento nem prometer ganho.
- Variação real entre vídeos (formato, estilo, assunto), para não parecer conteúdo em massa.

## Andamento
- Ativos: olheiro (06:47), pesquisador, roteirista, diretor, revisor, checador, diretor-de-arte, compositor, editor-chefe, social-media, compliance, produtor.
- Em construção: estilo `grana` e blocos de finanças; autor-de-ebook e diagramador (ebook "Chefões do cartão").
- Esperando o Tiago: narrador (escolher a voz), editor-de-gameplay (gravação do Fortnite), atendente-whatsapp e desenvolvedor-web (contas e ferramenta de e-mail), analista (canais no ar).
