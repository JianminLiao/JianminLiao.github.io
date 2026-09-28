from pathlib import Path
from decimal import Decimal, getcontext
import json
getcontext().prec=40
n=16
b,rho,delta=map(Decimal,['1.11','1.05','0.1'])
K=1
while (b-rho)*sum(rho**j for j in range(K))<=1:
    K+=1
balance=Decimal(0)
rows=[]
total=Decimal(0)
for i in range(1,n+1):
    c=1+balance
    next_balance=b*c-1 if i<=n-K else rho*balance
    p=1-(1+next_balance)/(b*c)
    intrinsic=p*c
    total+=intrinsic
    assert next_balance>=max(delta,rho*balance)
    rows.append([float(x) for x in [c,next_balance,p,intrinsic,total]])
    balance=next_balance
result={'model':'Fixed linear functions: f(c)=c, g(c)=b*c, h(e)=e',
'cycles':n,'b':float(b),'rho':float(rho),'delta':float(delta),'K':K,
'initial_full_external_cycles':n-K,'mixed_cycles':K,
'expenditure':[r[0] for r in rows],'balance':[r[1] for r in rows],
'allocation':[r[2] for r in rows],'intrinsic_increment':[r[3] for r in rows],
'cumulative_intrinsic':[r[4] for r in rows],
'optimality':'Exact policy from the linear theorem, computed with 40-digit decimal arithmetic.'}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
