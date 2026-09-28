"""One fixed-coefficient illustration of the IID theorem; no sampling."""
from pathlib import Path
from decimal import Decimal, getcontext
import json
import sys

getcontext().prec = 40
n = 13
b, d, rho, delta = map(Decimal, ['1.11', '1.05', '1.05', '0.1'])
A = D = Decimal(0)
K = 0
while d*b*A + b*D <= 1:
    S = d*b*A + b*D
    A, D = 1-D+(S-1)/b, D+(rho-1)*(S-1)/b
    K += 1

c, balance, total = Decimal(1), Decimal(0), Decimal(0)
rows = []
for i in range(1, n+1):
    external = b*c if i <= n-K else c+(rho-1)*balance
    q = external/(b*c)
    p = 1-q
    intrinsic = c-external/b
    next_balance = balance+external-c if i <= n-K else rho*balance
    total += intrinsic
    assert next_balance >= max(delta, rho*balance)
    rows.append([float(x) for x in (c, next_balance, p, intrinsic, total)])
    c, balance = d*external, next_balance

result = {
    'model': 'Fixed linear coefficients, a degenerate IID law: f(c)=c, g(c)=b*c, h(e)=d*e',
    'cycles': n, 'b': float(b), 'd': float(d), 'rho': float(rho), 'delta': float(delta), 'K': K,
    'initial_full_external_cycles': n-K, 'mixed_cycles': K,
    'expenditure': [r[0] for r in rows], 'balance': [r[1] for r in rows],
    'allocation': [r[2] for r in rows], 'intrinsic_increment': [r[3] for r in rows],
    'cumulative_intrinsic': [r[4] for r in rows],
    'optimality': 'Bellman threshold and optimal policy computed with 40-digit Decimal arithmetic.',
    'monotonicity': 'Here d=rho, so the reserve-to-budget ratio strictly decreases in every mixed cycle.'
}
(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('result.json')).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'cycles': n, 'K': K, 'initial_external': n-K,
                  'first_intrinsic_share': rows[n-K][2], 'last_intrinsic_share': rows[-1][2],
                  'total_intrinsic': rows[-1][4]}, indent=2))
