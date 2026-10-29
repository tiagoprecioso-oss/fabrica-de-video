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
