# Pesquisa: planilha "Placar dos Chefões" (bônus 1 do ebook, 29/10/2026)

Motivo: regra 4 do CLAUDE.md. Antes de desenhar a planilha, ver o que as planilhas de dívidas mais usadas fazem e do que as pessoas reclamam.

## Fontes olhadas
- **Vertex42 Debt Reduction Calculator** (a mais citada em inglês): descrição em AAII (aaii.com/journal/article/vertex-42-debt-reduction-calculator) e no Get Rich Slowly (getrichslowly.org/free-debt-snowball-spreadsheet), com comentários de leitores.
- **Modelos à venda para Google Planilhas/Excel** (Etsy, Gumroad, Payhip, Spreadsheetshub "dark theme"): rastreadores com Avalanche + Bola de Neve, registro mensal de pagamentos, barra de progresso por dívida, aba de instruções.
- **Planilhas em português**: YouExec "Rastreador de Dívidas" (9 abas, painel, cronograma, saldo ao longo do tempo, comparação de métodos), Financial Aha (calculadora de quitação), ClickUp (lista de 16 modelos).
- **Explicações brasileiras dos métodos**: blog do Nubank e Suno (listar todas as dívidas com juros e vencimento, pagar o mínimo de todas, sobra para a primeira da lista).
- **Motivação visual**: Nasdaq, "Keep an Eye on Debt Using Creative Visual Aids" (termômetro na geladeira, pintar 10% por vez, "pequenas doses de dopamina").

## O que as melhores fazem
1. **Uma tabela só de entrada** por dívida: nome, saldo, taxa, mínimo. Mais que isso afasta (o motivo nº 1 para largar a planilha é dar trabalho preencher).
2. **Quanto sobra depois dos mínimos** em destaque (o "snowball" do Vertex42: R$ disponível − mínimos = dinheiro do alvo).
3. **Avalanche e Bola de Neve lado a lado**, com a ordem montada sozinha.
4. **Alerta quando o pagamento não cobre os juros** (o Vertex42 pinta a célula de vermelho). É o recurso que mais conversa com o nosso livro ("ele está crescendo").
5. **Registro mês a mês** com o saldo caindo e um gráfico de "saldo ao longo do tempo".
6. **Progresso visível**: barra/termômetro de quanto já foi derrotado. Pequenas vitórias seguram a pessoa.
7. **Aba de instruções curta** no começo.

## Do que as pessoas reclamam (evitar)
- Arquivo que só funciona num programa (o Vertex42 já saiu como .exe; usuários de Mac/Google pediram versão compatível) → só fórmulas clássicas (SUMPRODUCT, INDEX/MATCH, IFERROR, COUNT, REPT), sem macro, sem XLOOKUP/FILTER/SORT.
- Datas de quitação erradas destroem a confiança → não prometer data; mostrar o que é conta exata (ataque do mês, vida total) e deixar a simulação longa para o simulador do ebook, que já é conferido por `contas.py`.
- Mínimo fixo: no cartão o mínimo muda a cada fatura → o registro mensal deixa a pessoa anotar o que pagou de verdade.
- Planilhas de 9 abas com renda/despesa por categoria: viram orçamento completo e cansam. Aqui são 4 abas de uso + 1 de taxas.
- Visual branco de planilha "de escritório" (pedido do Felipe) e modelos genéricos de IA → paleta do canal, fundo sálvia, vocabulário do jogo (vida, ataque, alvo, fase vencida).

## Decisões do desenho
- Abas: Como usar · Meus chefões · Placar mensal · Plano de 90 dias · Taxas (fonte).
- Taxa sugerida vem da aba Taxas pela fórmula do livro, (1 + anual)^(1/12) − 1, com as anuais do Banco Central. Assim o exemplo da Ana bate com `contas.py` no centavo (440,16), e não 440,24 como daria com taxas arredondadas.
- Coluna "Minha taxa" separada da sugerida: a pessoa digita por cima sem apagar fórmula.
- Gráfico de colunas (não de linha) no Placar: meses ainda vazios ficam sem barra no Excel, no LibreOffice e no Google Planilhas, sem precisar de #N/D.
- "Ataque que você tomou" no Placar = vida do mês anterior + o que pagou − vida de agora: mostra os juros reais sem pedir mais nenhum número.
- Plano de 90 dias com lista suspensa "Feito" (caixa de seleção nativa do Google não existe no .xlsx) e barra de progresso com REPT.
