# Pesquisa de referências: ebook "Chefões do cartão" v2 (29/10/2026)

Motivo: a v1 saiu sem pesquisa e o Felipe achou o design horrível. Prints em `saida/ref/chefoes/` e `saida/ref/chefoes2/` (`python3 tools/referencias.py`).

## O que olhamos
| Referência | O que é | Por que importa |
|---|---|---|
| ncase.me/trust (The Evolution of Trust) | Explicação jogável, 30 min | O leitor **joga** cada ideia antes de ler a conclusão; texto em pedaços curtos entre interações; personagens simples e carismáticos |
| ncase.me/polygons (Parable of the Polygons) | "Post jogável" | Arrastar e soltar; simulação que roda na frente do leitor; gráfico que reage; humor |
| playspent.org (Spent) | Jogo sobre pobreza e escolhas | Começa com um saldo e uma escolha de cada vez; fundo escuro, ilustrações em blocos de cor; impacto emocional |
| neal.fun/spend (Spend Bill Gates' Money) | Viral: gastar uma fortuna | O número no topo, grudado na tela, mudando a cada clique (bloqueado por Cloudflare no print; conhecido) |
| undebt.it (snowball × avalanche) | Calculadora líder do nicho | Prova que o público quer **colocar as próprias dívidas** e ver o plano; mas visual de planilha, sem emoção |
| habitica.com | App de hábitos com **batalhas contra chefões** | A metáfora exata do nosso livro: suas ações tiram vida do chefão; pixel art, roxo profundo, recompensa |
| duolingo.com | Gamificação de aprendizado | Personagens redondos e expressivos, cores chapadas fortes, botões grandes, celebração a cada vitória, progresso visível |
| ciechanow.ski/gears | Explicação interativa premiada | Uma ideia por demonstração, controles simples (slider, play), texto calmo ao redor |
| pudding.cool | Ensaios visuais | Capas com blocos de cor saturada, tipografia com personalidade, dados como protagonistas |
| Hotmart: "Livre-se das dívidas em 30 dias", "Domine suas finanças e livre-se das dívidas" | Concorrentes diretos (US$ 10–27) | Capas genéricas de banco de imagem, PDF comum, nenhuma interação: **o espaço para se diferenciar está aberto** |

## O que os melhores têm em comum
1. **O leitor faz antes de ler**: digita a própria dívida, arrasta, aperta "atacar". A ideia chega pela experiência.
2. **Um número que manda na tela** (saldo, vida do chefão) sempre visível e reagindo.
3. **Personagens com cara**: poucos traços, muita expressão, que reagem (apanham, comemoram).
4. **Texto curto entre interações**, uma ideia por tela; rolagem conduz a história.
5. **Paleta forte e limitada** (2–3 cores saturadas + neutro), tipografia com personalidade só nos títulos.
6. **Celebração**: toda vitória tem feedback (animação, som opcional, selo).
7. **Funciona no celular primeiro** (Duolingo, Spent).

## O que evitar (o que a v1 fazia)
- Parecer documento/relatório: caixas coloridas empilhadas, tabelas, muito texto por página.
- Ilustração como enfeite: os chefões da v1 eram adesivos parados, sem reagir a nada.
- Verde-planilha e cinza: visual de banco, não de jogo.
- Dados só na leitura: o leitor nunca colocava os próprios números.

## Direção proposta para a v2
- **Produto principal: página interativa** (um link, funciona no celular), com o leitor montando o próprio "bestiário" de dívidas e vendo a batalha simulada mês a mês com as estratégias.
- **PDF** como versão secundária (imprimir as fichas), gerado do mesmo texto.
- Entrega na Hotmart: link na área de membros (decisão do Tiago: hospedagem — GitHub Pages ou página publicada).
