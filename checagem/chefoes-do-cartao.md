# Checagem: ebook "Chefões do cartão" (29/10/2026)

Conferido contra `pesquisa/chefoes-do-cartao.md` e refeito em `python3 produtos/chefoes-do-cartao/contas.py`.
Obs.: checagem feita na mesma sessão que escreveu o texto (sem checador independente). Vale uma segunda leitura humana antes de vender.

| Item no texto | Fonte / conta | Resultado |
|---|---|---|
| Rotativo 451,7% a.a. · parcelado 193,0% · cheque especial 139,0% · pessoal 110,9% · consignado 28,5% | BC, set/2026 (notícias de 29/10/2026) | OK |
| Equivalentes ao mês 15,29% · 9,37% · 7,53% · 6,42% · 2,11% | (1+a)^(1/12)−1 | OK |
| R$ 1.000 por 1 mês: 152,94 · 75,31 · 21,12 | 1000 × taxa a.m. | OK |
| Rotativo dobraria em 5 meses sem teto | 1,1529^5 = 2,04 (4 meses = 1,77) | OK |
| Teto: R$ 1.000 vira no máximo R$ 2.000 | Lei 14.690/2023, Res. CMN 5.112 art. 2º-C | OK |
| Teto do cheque especial 8% a.m. | Res. CMN 4.765/2019 | OK (média 7,53% < 8%) |
| Endividamento 50,1% da renda de 12 meses; comprometimento 29% | BC, ago/2026 | **CORRIGIDO**: texto dizia "metade da renda comprometida" e "29% do salário" |
| R$ 800 × 0,0753 = R$ 60,24; sobe R$ 10,24 com R$ 50 | conta | OK |
| Ana: Avalanche 17 meses / R$ 4.323,76; Bola de Neve 18 / R$ 4.581,38; diferença R$ 257,62 | contas.py | OK |
| Ana: só mínimos, 12 meses: pagou R$ 3.600, deve R$ 7.523,34 | contas.py (12 × 300) | OK |
| Primeira vitória: mês 3 (bola de neve) e mês 8 (avalanche) | contas.py | OK |
| Troca por consignado: 11 meses, R$ 755,97; economia ≈ R$ 3.567 | 4.323,76 − 755,97 = 3.567,79 | OK |
| Portabilidade do cartão desde jul/2024, sem custo | Res. CMN 5.112 | OK |
| Desenrola com adesões até ago/2026 | Portaria (DGABC 31/7/2026) | OK; texto não promete programa aberto |
| Mínimo existencial | em julgamento no STF (2026) | OK: texto não crava valor |

**Veredito:** APROVADO depois da correção acima.

## PDF oficial v2 (29/10/2026, noite)
| Item no texto | Fonte / conta | Resultado |
|---|---|---|
| Juros de 1 mês sobre R$ 1.000: 152,94 · 93,72 · 75,31 · 64,16 · 37,94 · 21,12 · 19,58 · 10,00 | 1000 × taxa a.m. (consignado CLT 56,34% a.a.; contas 1% a.m.) | OK (CLT corrigido de 37,90 para 37,94) |
| Extrato mês 1 (Avalanche): juros 187,44 + 60,25 + 192,48 = 440,16; mínimos 300; sobra 300 no Golem; dano 159,84 | contas.py, mês a mês | OK |
| Extrato mês 8: juros 284,73; mínimos 223,95 (Golem quitado pelo mínimo); sobra 376,05 na Sombra; dano 315,27; mês 9 sobra 400 | contas.py | OK |
| Gráfico da Ana: Avalanche 17 meses, Bola de Neve 18, só mínimo cresce | contas.historico() | OK |
| Gastos invisíveis: 40 + 60 + 120 + 35 + 30 = 285/mês; × 12 = 3.420 | conta | OK |
| Mundo 2: R$ 600 × 12 = R$ 7.200, sem rendimento | conta | OK |

## Checagem independente (agente checador, 29/10/2026)

Feita por quem não escreveu o ebook. Fontes abertas uma a uma (WebFetch). Contas refeitas com código próprio (simulação mês a mês escrita do zero, sem importar o contas.py), e a função `simular` da página rodada em Node com os dados da Ana. Arquivos conferidos: `produtos/chefoes-do-cartao/texto.md`, `produtos/chefoes-do-cartao/web/index.html`, `produtos/chefoes-do-cartao/contas.py`.

### A. Dados e fontes

| # | Item | Fonte/conta | OK ou CORRIGIR | Correção exata |
|---|---|---|---|---|
| 1 | Rotativo 451,7% a.a. e parcelado 193,0% (set/2026) | O Povo/AE, 29/10/2026: "subiu de 444,9% ao ano em agosto para 451,7% ao ano em setembro"; parcelado "de 192,1% para 193,0%" | OK | — |
| 2 | Cheque especial 139,0%, crédito pessoal 110,9%, consignado 28,5%, veículos 26,2% (set/2026) | O Povo/AE, 29/10/2026 (trechos literais conferidos) | OK | — |
| 3 | Crédito livre às famílias 62,4% a.a. (set/2026) | O Povo e SouBrasília: 62,4% em setembro | OK | (o número está só na ficha, não no texto) |
| 4 | Endividamento 50,1% da renda de 12 meses (ago/2026) | O Povo: "de 49,9% em julho para 50,1% em agosto" | OK | — |
| 5 | Comprometimento 29% (ago/2026) | O Povo: "de 28,8% para 29,0%" (com o SFN) | OK | — |
| 6 | Consignado CLT 3,79% a.m. / 56,34% a.a. (ago/2026, SGS 20744) | meubolsoazul: "competência 2026-08 é 3,79% ao mês"; "56,34% ao ano"; "séries SGS 20744" | OK | Ressalva: é fonte de terceiros que repassa o dado do BC, e o mês (ago) é diferente do das outras taxas (set). O texto avisa as duas coisas. Antes de vender, conferir direto no SGS do BC. |
| 7 | Teto de 100% (Lei 14.690/2023, Res. CMN 5.112, desde jan/2024), com juros, multa e mora | PDF da Res. 5.112, art. 2º-C (inclui "multa e juros de mora", art. 2º-A, III); vale para "rotativo e de parcelamento de fatura" | OK | O link do Monitor Mercantil na ficha não abre (erro do site). Trocar na ficha pelo PDF da resolução, que já está lá. |
| 8 | Rotativo só até a fatura seguinte, depois parcelamento mais barato (Res. 4.549/2017) | Idec: "A partir do segundo mês, o saldo deverá ser quitado ou parcelado" | OK | — |
| 9 | Cheque especial: teto de 8% a.m. (Res. 4.765/2019) | PDF do BC, art. 3º: "no máximo, 8% (oito por cento) ao mês"; vigência 6/1/2020 | OK | — |
| 10 | Portabilidade do cartão (rotativo e parcelado) desde jul/2024, sem custo | Finsiders: "Entrou em vigor nesta segunda-feira (1/7)", "inclui rotativo e parcelamento", "gratuitamente" | OK | — |
| 11 | Lei 14.181/2021: "permite juntar **todas** as dívidas em um plano único" (texto.md, Fase 4 "Pedir socorro"; index.html linha 648; ficha de pesquisa §4) | Lei 14.181/2021 (CDC art. 104-A, §1º): ficam de fora dívidas com garantia real, financiamento imobiliário e crédito rural, além das contraídas sem intenção de pagar | **CORRIGIR** | Trocar "permite juntar todas as dívidas em um plano único de pagamento" por "permite juntar as dívidas de consumo em um plano único de pagamento (ficam de fora, por exemplo, financiamento imobiliário e dívidas com garantia, como o carro financiado)". |
| 12 | Mínimo existencial sem valor fixo | Migalhas: julgamento no STF começou em 22/4/2026, foi suspenso e tem maioria pela atualização periódica pelo CMN | OK | O texto não informa valor. |
| 13 | Contas atrasadas: multa 2% + 1% a.m. "segundo o Procon-SP" (texto.md e index.html, Fontes) | InfoMoney (p=235650) é de **26/09/2012**; os números vêm da ANEEL e da Sabesp, não do Procon-SP. A correção citada lá é pelo IGP-M. A matéria do Idec é sobre um texto **preliminar** de 2010 | **CORRIGIR** | (a) Fonte desatualizada: trocar pela regra atual da ANEEL (REN 1.000/2021: multa de até 2%, juros de mora de 1% a.m. e atualização monetária) e conferir o texto vigente. (b) Na lista de Fontes, trocar "(regras da ANEEL e das concessionárias, segundo o Procon-SP)" por "(ANEEL, Resolução Normativa 1.000/2021, e contratos das concessionárias)". Os números 2% e 1% podem ficar. |
| 14 | FGTS: 1,29% a 1,79% a.m. (2026) | Credited, 5/9/2026 com atualização em 16/10/2026: "giram entre 1,29% e 1,79% ao mês" | OK | Fonte fraca (blog). Melhor conferir também se há teto oficial para a taxa (Conselho Curador do FGTS). |
| 15 | FGTS: "se você for demitido, o saldo usado fica travado e você só recebe a multa de 40%" (texto.md bestiário; index.html linha 773) | Credited: a regra vale para a demissão **sem justa causa** | **CORRIGIR** | Trocar "se você for demitido" por "se você for demitido sem justa causa". |
| 16 | CDC art. 52, §2º: desconto proporcional dos juros ao antecipar, total ou parcial | idinheiro: "liquidação antecipada do débito, total ou parcialmente, mediante redução proporcional dos juros" | OK | — |
| 17 | "Comece pelas **últimas parcelas**: são as que carregam mais juros embutidos" (texto.md, Antecipar parcelas) | A fonte citada não diz isso. No sistema Price, antecipar as últimas parcelas dá o maior desconto (são trazidas a valor presente por mais meses). Mas "carregam mais juros embutidos" é uma explicação imprecisa e não tem fonte | **CORRIGIR** | Trocar por: "Comece pelas **últimas parcelas** do contrato: como estão mais longe, são as que recebem o maior desconto de juros ao serem antecipadas." |
| 18 | CDC art. 49 (7 dias) | Está na lista de Fontes do texto.md, mas não aparece no corpo do livro | OK | É uma regra válida (direito de arrependimento). Pode ficar ou sair. |
| 19 | "O banco é obrigado a informar" a taxa e o CET (Fase 2) | A informação está certa (Res. CMN 3.517/2007 obriga a informar o CET), mas a norma não está na ficha nem nas Fontes | **CORRIGIR** | Acrescentar às Fontes: "Resolução CMN nº 3.517/2007: obrigação de informar o CET." |

### B. Contas (refeitas com código próprio)

| # | Item | Conta | OK ou CORRIGIR | Correção exata |
|---|---|---|---|---|
| 20 | Taxas ao mês: 15,29 · 9,37 · 7,53 · 6,42 · 3,79 · 2,11 · 1,96 | (1+a)^(1/12)−1 = 15,2945 · 9,3719 · 7,5309 · 6,4159 · 3,7941 · 2,1116 · 1,9581 | OK | — |
| 21 | Juros de 1 mês sobre R$ 1.000: 152,94 · 93,72 · 75,31 · 64,16 · 37,94 · 21,12 · 19,58 · 10,00 | 1000 × taxa a.m. | OK | — |
| 22 | "O mais forte cobra mais de 15 vezes o que cobra o mais fraco" | 15,29/1,00 = 15,29× (Goblin, 1%) | OK | Só vale se "o mais fraco" for o Goblin; ver item 30. |
| 23 | Rotativo dobraria em 5 meses sem teto | 1,1529^4 = 1,767; ^5 = 2,037 | OK | — |
| 24 | Teto: R$ 1.000 vira no máximo R$ 2.000 | Simulação (página): juros acumulados param em R$ 1.000,00 | OK | — |
| 25 | R$ 800 × 0,0753 = R$ 60,24; sobe R$ 10,24 pagando R$ 50 | 60,24 (com a taxa exata: 60,25) e 60,24 − 50 = 10,24 | OK | — |
| 26 | Extrato mês 1: 187,44 + 60,25 + 192,48 = 440,16; mínimos 300; sobra 300 no Golem; dano 159,84 | Simulação própria | OK | — |
| 27 | Extrato mês 8: 2,05 + 67,03 + 215,64 = 284,73; mínimos 223,95; sobra 376,05 na Sombra; dano 315,27; mês 9 sobra 400 | Simulação própria (mês 9: sobra 400,00) | OK | — |
| 28 | Avalanche 17 meses / R$ 4.323,76; Bola de Neve 18 / R$ 4.581,38; diferença R$ 257,62; 1ª vitória mês 8 (Golem) e mês 3 (Sombra); "cinco meses antes"; "um mês antes" | Simulação própria: AV (17; 4.323,76; Golem 8, Sombra 10, Cavaleiro 17), BN (18; 4.581,38; Sombra 3) | OK | — |
| 29 | Só mínimos, 12 meses: pagou R$ 3.600, deve R$ 7.523,34 | 12 × 300 = 3.600; saldo 7.523,34 | OK | — |
| 30 | Troca por consignado: 11 meses, R$ 755,97; "economia de cerca de **R$ 3.567**" | 11 meses, 755,97; 4.323,76 − 755,97 = **3.567,79** | **CORRIGIR** | Arredondamento errado: 3.567,79 arredonda para 3.568. Trocar "cerca de **R$ 3.567**" por "cerca de **R$ 3.568**" (ou "R$ 3.567,79"). |
| 31 | Dinheiro extra: R$ 1.000 no mês 2 → 13 meses e R$ 1.567,46 a menos | Simulação própria: 13 meses, juros 2.756,30; 4.323,76 − 2.756,30 = 1.567,46 | OK | — |
| 32 | "No mês 1 os juros levavam R$ 440... no mês 8, só R$ 285" | 440,16 e 284,73 | OK | — |
| 33 | Gastos invisíveis 285/mês e 3.420/ano | 40+60+120+35+30 = 285; × 12 = 3.420 | OK | — |
| 34 | Mundo 2: R$ 600 × 12 = R$ 7.200, sem rendimento | conta | OK | — |
| 35 | Ogro CLT "quase o dobro do consignado médio" | 56,34/28,5 = 1,98× ao ano; 3,79/2,11 = 1,80× ao mês | OK | — |

### C. Página interativa e coerência

| # | Item | Conferência | OK ou CORRIGIR | Correção exata |
|---|---|---|---|---|
| 36 | Objeto TIPOS: anuais iguais ao texto e ao contas.py; contas 1% a.m.; FGTS fora do simulador | index.html linhas 746 a 780 | OK | — |
| 37 | `simular` (JS) com a mesma lógica do contas.py: juros, depois teto só em rotativo e parcelado, depois mínimos, depois sobra no alvo (Avalanche pela taxa, Bola de Neve pelo saldo depois dos mínimos) | Lida linha a linha e rodada em Node com os dados da Ana: 17 / 4.323,76 / 1ª vitória no mês 8; 18 / 4.581,38 / mês 3; extra 13 / 2.756,30; só mínimos 7.523,34 em 12 meses; extratos dos meses 1, 8 e 9 iguais | OK | — |
| 38 | Chips e introdução da página: "5 chefões" (linha 421) e "os cinco chefões mais comuns" (linha 463) | O bestiário da própria página tem 9 ("O bestiário: 9 chefões"), e o simulador tem 8 tipos | **CORRIGIR** | Linha 421: "5 chefões" → "9 chefões". Linha 463: "os cinco chefões mais comuns" → "os nove chefões mais comuns". |
| 39 | Lacaio do Consignado: "É o mais fraco da lista" e nível 1 (texto.md bestiário; index.html linha 761) | Pela própria lista ele não é o mais fraco: veículos tem 1,96% a.m., contas atrasadas 1% e FGTS 1,29% a 1,79%, todos abaixo de 2,11%. A frase também contradiz o item 22, em que "o mais fraco" é o Goblin | **CORRIGIR** | Trocar "É o mais fraco da lista e pode virar arma contra os outros" por "É um dos mais fracos da lista e pode virar arma contra os outros". Opcional: rever o nível (a Tartaruga tem nível 2 com taxa menor). |
| 40 | Tipo "Chefão sem ficha" (`outro`) entra com 5% a.m. como padrão (index.html linhas 774 e 779) | Número sem fonte que aparece preenchido para o leitor | **CORRIGIR** | Mostrar junto do campo: "5% é só um valor de exemplo: troque pela taxa do seu contrato". |

### D. Afirmações sem fonte, promessa de resultado, recomendação de investimento

| # | Item | Conferência | OK ou CORRIGIR | Correção exata |
|---|---|---|---|---|
| 41 | "Quem quita e não muda nada costuma estar devendo de novo em poucos meses" (texto.md, abertura da Fase 5; index.html linha 663) | Afirmação de frequência sem fonte | **CORRIGIR** | Trocar por "Quem quita e não muda nada corre o risco de voltar a dever. Equipe os seus quatro escudos." (na página, manter o resto da frase). |
| 42 | "alguns batem mais forte que o dragão" (Chefões sem ficha: texto.md e index.html linha 497) | Não há fonte que mostre crediário ou empréstimo de app acima de 15,29% a.m. | **CORRIGIR** | Trocar por "e alguns podem bater tão forte quanto os piores da lista". Outra opção é acrescentar uma fonte com a taxa. |
| 43 | Promessa de resultado | Aviso "não promete resultado" presente; Fase 6 diz "você sabe quanto deve", e não "quita em 90 dias"; a página diz "talvez nem todos os chefões estejam derrotados" | OK | — |
| 44 | Recomendação de investimento | Mundo 2 sem rendimento, com "Conta simples, sem rendimento"; não cita nenhum produto financeiro | OK | Atenção para o próximo produto: "onde guardar" (Mundo 2) não pode indicar um investimento específico. |
| 45 | Simulação da troca por consignado sem IOF/CET | O texto fala em "taxa média" e o alerta geral manda conferir o CET | OK | Opcional: acrescentar "sem contar IOF e tarifas". |
| 46 | Datas: 1ª edição em out/2026, dados de set/2026 divulgados em 29/10/2026, teto desde jan/2024, portabilidade desde jul/2024 | Fontes conferidas | OK | — |

**Resumo:** 46 itens conferidos, 35 OK e 11 CORRIGIR (itens 11, 13, 15, 17, 19, 30, 38, 39, 40, 41 e 42). Todas as contas batem com a simulação independente, exceto o arredondamento do item 30. A lógica da página é a mesma do contas.py. O que precisa corrigir são regras jurídicas imprecisas (superendividamento, FGTS), fontes desatualizadas ou atribuídas errado (contas atrasadas), frases sem fonte e contradições internas (5 contra 9 chefões, "o mais fraco").

**Veredito: CORRIGIR.** Volta para o autor (roteirista/autor-de-ebook) com as correções acima, nos dois arquivos (texto.md e index.html) e na ficha de pesquisa (§4: "todas as dívidas" e o link quebrado do Monitor Mercantil). Depois de corrigido, uma nova conferência rápida dos itens marcados basta para aprovar.
