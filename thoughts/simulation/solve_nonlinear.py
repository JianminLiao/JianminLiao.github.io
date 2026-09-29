from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize, LinearConstraint, linprog

ROOT=Path(__file__).resolve().parent
n, b, rho, m, q, seed = 100, 1.05, 1.01, 1., 1., 20260928
w=b**np.arange(n)
# y_i is intrinsic expenditure discounted to the first cycle.
A=(b-rho)*np.tril(np.ones((n,n)),-1)+b*np.eye(n)
h=(b-rho)+(rho-1)/w
scale=w[-1]

def objective(y):
    return -np.sum(m*w*y+q*np.sqrt(w*y))/scale

def gradient(y):
    return -(m*w+.5*q*np.sqrt(w/y))/scale

y0=np.full(n, .003)
result=minimize(objective,y0,jac=gradient,method='SLSQP',
    bounds=[(1e-16,None)]*n,constraints=[LinearConstraint(A,-np.inf,h)],
    options={'maxiter':2000,'ftol':1e-14})
y=result.x
# Concavity gives a global upper bound through a linear optimization problem.
g=-gradient(y)*scale
certificate=linprog(-g,A_ub=A,b_ub=h,bounds=(0,None),method='highs')
value=-objective(y)*scale
gap=max(0.,-certificate.fun-np.dot(g,y))
c=w*(1-np.r_[0,np.cumsum(y[:-1])])
t=w*y
p=t/c
E=b*(c-t)
B=E-1
slack=B-rho*np.r_[0,B[:-1]]
rng=np.random.default_rng(seed)
coefficients=rng.uniform(.8,1.2,n)
I=m*t+coefficients*np.sqrt(t)
summary=dict(cycles=n,b=b,rho=rho,m=m,expected_sqrt_coefficient=q,seed=seed,
    formula='I_i = t_i + A_i*sqrt(t_i), E_i = 1.05*(c_i-t_i), d_i = 1; A_i iid Uniform[0.8,1.2]',
    allocation=p.tolist(),expenditure=c.tolist(),intrinsic_expenditure=t.tolist(),
    intrinsic_increment=I.tolist(),cumulative_intrinsic=np.cumsum(I).tolist(),
    balance=B.tolist(),coefficients=coefficients.tolist(),
    expected_objective=value,realized_objective=float(I.sum()),
    solver_success=bool(result.success),solver_message=result.message,
    global_upper_bound=value+gap,absolute_optimality_gap=gap,relative_optimality_gap=gap/value,
    minimum_reserve_slack=float(slack.min()),minimum_scaled_slack=float((h-A@y).min()),
    information='Allocation is chosen before the current coefficient. Coefficients affect intrinsic rewards only, so the budget path and optimal allocations are deterministic.',
    certificate='The expected objective is strictly concave in discounted expenditures and the constraints are linear. The linear tangent maximum is a global upper bound.')
(ROOT/'nonlinear-result.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({key:summary[key] for key in ['solver_success','solver_message','expected_objective','realized_objective','relative_optimality_gap','minimum_reserve_slack']},indent=2))
for i in [0,9,19,39,59,79,99]:
    print(i+1, 'allocation',p[i], 'cumulative',np.cumsum(I)[i], 'expenditure',c[i])
assert result.success and certificate.success
assert gap/value<1e-6
assert slack.min()>-1e-8
assert np.all(p>0) and np.all(p<1)
assert np.allclose(c[1:],E[:-1])
