"""One optimal IID trajectory: choose the allocation before drawing its returns."""
from pathlib import Path
import json
import sys
import numpy as np

n, rho, seed = 20, 1.045, 20260928
low = np.array([1.5, 1.05, 1.0])
high = np.array([2.5, 1.15, 1.2])
b = low[1]
mean_a, w, mean_d = (low + high) / 2
v = w * mean_d

# The policy needs only b, E[b_i], E[b_i d_i], and the observed budget and reserve.
A, D, S = [0.0], [0.0], [0.0]
for m in range(1, n + 1):
    if S[-1] > 1:
        next_A, next_D = S[-1] - D[-1], D[-1]
    else:
        next_A = 1 - D[-1] + (S[-1] - 1) / b
        next_D = D[-1] + (rho - 1) * (S[-1] - 1) / b
    A.append(next_A)
    D.append(next_D)
    S.append(v * next_A + w * next_D)
K = next(m for m, s in enumerate(S) if s > 1)

rng = np.random.Generator(np.random.PCG64(seed))
c, balance, total = 1.0, 0.0, 0.0
rows = []
for cycle in range(1, n + 1):
    external = c if S[n-cycle] > 1 else (c + (rho-1) * balance) / b
    p = 1 - external/c
    worst_margin = b * external - c - (rho-1) * balance
    ai, bi, di = rng.uniform(low, high)
    income = bi * external
    intrinsic = ai * (c-external)
    next_balance = balance + income - c
    total += intrinsic
    rows.append(dict(cycle=cycle, a=ai, b=bi, d=di, expenditure=c,
                     intrinsic_share=p, intrinsic_increment=intrinsic,
                     cumulative_intrinsic=total, balance=next_balance,
                     reserve_margin=next_balance-rho*balance,
                     worst_case_reserve_margin=worst_margin))
    c, balance = di*income, next_balance
assert min(row['worst_case_reserve_margin'] for row in rows) > -1e-10

result = dict(
    model='Independent uniform coefficients within each cycle; IID vectors across cycles.',
    cycles=n, rho=rho, seed=seed,
    ranges={name: [float(lo), float(hi)] for name, lo, hi in zip(['a','b','d'],low,high)},
    b_min=b, mean_b=w, mean_bd=v, K=K, initial_full_external_cycles=n-K,
    mixed_cycles=K, expected_total_intrinsic=mean_a*A[n],
    expenditure=[r['expenditure'] for r in rows],
    balance=[r['balance'] for r in rows],
    allocation=[r['intrinsic_share'] for r in rows],
    intrinsic_increment=[r['intrinsic_increment'] for r in rows],
    cumulative_intrinsic=[r['cumulative_intrinsic'] for r in rows],
    trajectory=rows,
)
destination = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('result.json')
destination.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'cycles':n,'K':K,'initial_external':n-K,
                  'total_intrinsic':total,'expected_total_intrinsic':mean_a*A[n],
                  'allocation_percent':np.round(100*np.array(result['allocation']),5).tolist()},indent=2))
