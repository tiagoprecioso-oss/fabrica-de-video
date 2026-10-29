"""Contas do ebook 'Chefões do cartão'. Refaz todos os exemplos do texto.
Uso: python3 produtos/chefoes-do-cartao/contas.py"""
ANUAL = {'rotativo': 451.7, 'parcelado': 193.0, 'cheque': 139.0, 'pessoal': 110.9, 'consignado': 28.5}
M = {k: (1 + v / 100) ** (1 / 12) - 1 for k, v in ANUAL.items()}

def simular(dividas, orcamento, ordem):
    """dividas: lista de dicts nome, saldo, taxa (a.m.), minimo, teto (bool: juros acumulados <= saldo original).
    Paga os mínimos e joga a sobra na primeira dívida viva segundo 'ordem'. Retorna meses, juros totais, mês de quitação de cada."""
    ds = [dict(d, original=d['saldo'], juros=0.0, fim=None) for d in dividas]
    mes, juros_tot = 0, 0.0
    while any(d['saldo'] > 0.005 for d in ds):
        mes += 1
        for d in ds:
            if d['saldo'] <= 0.005: continue
            j = d['saldo'] * d['taxa']
            if d.get('teto'): j = max(0.0, min(j, d['original'] - d['juros']))
            d['saldo'] += j; d['juros'] += j; juros_tot += j
        sobra = orcamento
        for d in ds:
            if d['saldo'] <= 0.005: continue
            p = min(d['minimo'], d['saldo']); d['saldo'] -= p; sobra -= p
        for d in sorted([d for d in ds if d['saldo'] > 0.005], key=ordem):
            p = min(sobra, d['saldo']); d['saldo'] -= p; sobra -= p
            if sobra <= 0: break
        for d in ds:
            if d['saldo'] <= 0.005 and d['fim'] is None: d['fim'] = mes
        if mes > 600: return None, juros_tot, {d['nome']: round(d['saldo'], 2) for d in ds}
    return mes, juros_tot, {d['nome']: d['fim'] for d in ds}

def exemplo():
    return [
        dict(nome='Cartão parcelado', saldo=2000, taxa=M['parcelado'], minimo=100, teto=True),
        dict(nome='Cheque especial', saldo=800, taxa=M['cheque'], minimo=50),
        dict(nome='Crédito pessoal', saldo=3000, taxa=M['pessoal'], minimo=150),
    ]

def simular_meses(dividas, orcamento, meses):
    ds = [dict(d, original=d['saldo'], juros=0.0) for d in dividas]; jt = 0.0
    for _ in range(meses):
        for d in ds:
            j = d['saldo'] * d['taxa']
            if d.get('teto'): j = max(0.0, min(j, d['original'] - d['juros']))
            d['saldo'] += j; d['juros'] += j; jt += j
            d['saldo'] -= min(d['minimo'], d['saldo'])
    return {'saldo_total': round(sum(d['saldo'] for d in ds), 2), 'juros_pagos': round(jt, 2)}

if __name__ == '__main__':
    for k in M: print(f'{k:11s} {ANUAL[k]:6.1f}% a.a. = {M[k]*100:5.2f}% a.m.')
    print()
    # Cap. 1: R$ 1.000 no rotativo
    r = 1000 * M['rotativo']; print(f'R$ 1.000 no rotativo, juros do 1º mês: R$ {r:.2f}  | teto total: R$ 2.000')
    s, n = 1000.0, 0
    while s < 2000: s *= 1 + M['rotativo']; n += 1
    print(f'sem teto, dobraria em {n} meses; com teto, para em R$ 2.000')
    print(f'cheque especial R$ 1.000 por 1 mês: R$ {1000*M["cheque"]:.2f}; consignado: R$ {1000*M["consignado"]:.2f}')
    print()
    orc = 600
    av = simular(exemplo(), orc, lambda d: -d['taxa'])
    bn = simular(exemplo(), orc, lambda d: d['saldo'])
    sem = simular(exemplo(), 300, lambda d: 0)  # só os mínimos
    print('Avalanche   ', av[0], 'meses, juros R$', round(av[1], 2), av[2])
    print('Bola de neve', bn[0], 'meses, juros R$', round(bn[1], 2), bn[2])
    print('Só mínimos   nunca quita; depois de 12 meses:', simular_meses(exemplo(), 300, 12))
    # Cap. 4: trocar tudo por um consignado de 2,11% a.m., mesma parcela de 600
    tot = 5800
    s, n, j = tot, 0, 0.0
    while s > 0.005:
        n += 1; jj = s * M['consignado']; j += jj; s += jj; s -= min(600, s)
    print(f'Troca por consignado (R$ {tot}, R$ 600/mês): {n} meses, juros R$ {j:.2f}')
    # Price: parcela de 5800 em 12x a 2,11%
    i = M['consignado']; pmt = tot * i / (1 - (1 + i) ** -12)
    print(f'Consignado 12x: parcela R$ {pmt:.2f}, total R$ {pmt*12:.2f}')
