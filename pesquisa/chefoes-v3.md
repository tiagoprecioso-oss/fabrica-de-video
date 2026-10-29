# Pesquisa: ebook interativo v3 (29/10/2026)

Pedido do Felipe: simulador mais didático, mais chefões, mais ataques e um gancho para o próximo produto (quem já quitou).

## 1. Simulador mais didático
- Bret Victor, *Explorable Explanations* (https://worrydream.com/ExplorableExplanations/): documentos reativos (o leitor muda as premissas e vê a conclusão mudar), exemplos exploráveis (o leitor testa casos que o autor não escolheu) e informação no contexto.
- Nicky Case (Evolution of Trust, Polygons): o leitor **prevê antes de ver**; cada passo explica uma regra só; a simulação pode andar um passo de cada vez.
- Aplicação:
  - **Aposta antes da luta** ("qual estratégia termina primeiro?"): o placar só abre depois da aposta (ou de um botão "revelar").
  - **Modo mês a mês** com um extrato em 3 linhas: (1) os chefões atacam (+juros de cada um), (2) você paga os mínimos, (3) a sobra vai inteira para o ALVO e o porquê (maior taxa ou menor saldo).
  - Quando um chefão cai: "o pagamento dele agora reforça o seu ataque" (é o efeito que dá nome à bola de neve).
  - Mostrar o **dano real do mês** = o que você pagou − os juros.

## 2. Novos chefões (com fonte)
| Chefão | Dívida | Taxa | Fonte |
|---|---|---|---|
| Ogro do Consignado CLT | Consignado privado (carteira assinada) | 3,79% a.m. / 56,34% a.a. (ago/2026) | Média do BC, série SGS 20744, via https://meubolsoazul.com.br/br/banco/consignado-privado/banco-do-brasil/ |
| Tartaruga do Financiamento | Financiamento de veículos | 26,2% a.a. (set/2026) | BC, via https://www.opovo.com.br/noticias/economia/2026/10/29/juro-medio-no-credito-livre-sobe-a-490-em-setembro-mostra-bc-cheque-especial-vai-a-139.html |
| Goblin das Contas Atrasadas | Luz, água, telefone em atraso | multa de 2% + juros de mora de 1% ao mês + correção; risco de corte do serviço | ANEEL/Procon-SP via https://www.infomoney.com.br/?p=235650 ; multa de 2% na luz: https://idec.org.br/em-acao/em-foco/novas-regras-de-energia-eletrica-ampliam-direitos-do-consumidor |
| Vampiro do FGTS | Antecipação do saque-aniversário | em geral 1,29% a 1,79% ao mês (2026); trava o saldo do FGTS se você for demitido | https://credited.com.br/financas/emprestimo/antecipacao-saque-aniversario-fgts-taxas-riscos/ |

Notas: o Vampiro do FGTS não entra no simulador (é pago com o próprio FGTS, não com parcelas do mês). O Goblin entra com 1% ao mês (a multa de 2% é única e fica no texto). Lição: consignado CLT custa quase o dobro do consignado médio (28,5% a.a.), então não é sempre "o mais fraco".

## 3. Novos ataques
- **Dinheiro extra** (13º, restituição do IR, venda de algo parado): um valor único em um mês, todo no alvo. Simulador: quanto encurta a batalha e quanto economiza de juros.
- **Antecipar parcelas com desconto**: CDC art. 52, §2º garante redução proporcional dos juros e encargos na liquidação antecipada, total ou parcial (https://www.idinheiro.com.br/glossario/quitacao-antecipada-como-pagar-menos-juros-ao-banco/).
- Mantidos: renegociar, portabilidade, trocar dívida cara por barata, pedir socorro.

## 4. Gancho para o próximo produto
- Progressão de jogo (https://www.leat.com/resources/blog/gamified-progression-paths): mapa visível do que vem depois, cada etapa vencida desbloqueia a próxima, marcos pequenos com recompensa.
- Duolingo/Habitica: próxima unidade aparece trancada, com cadeado e prévia.
- O próximo produto do funil é o minicurso em fases (`docs/plano-funil.md`): Power-ups (gastos invisíveis), Cofre (reserva), Próximo nível (orçamento).
- Aplicação: seção **"Mundo 2: o Cofre"** depois da Fase 6: calcula com os números do leitor quanto ele guarda quando o dinheiro das parcelas fica livre (sem rendimento, para não virar recomendação de investimento), mapa dos mundos trancados e chamada para a lista de espera. O link da lista é decisão do Tiago (constante `LINK_MUNDO2` na página; vazio = "em breve").
