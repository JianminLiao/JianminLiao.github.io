from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize

n, rho, delta, seed = 16, 1.05, .1, 20260928
rng = np.random.default_rng(seed)
scales = np.array([rng.uniform(.9, 1.1, n), rng.uniform(1.25, 1.65, n), rng.uniform(.85, .95, n)])
curves = rng.uniform(.05, .15, (3,n))

def function(k, i, x):
    a, q = scales[k,i], curves[k,i]
    return a*x*(1+q*x/(1+x)), a*(1+q*(1-1/(1+x)**2))

def trajectory(p, derivatives=False):
    c, B = 1., 0.
    dc, dB = np.zeros(n), np.zeros(n)
    objective, gradient = 0., np.zeros(n)
    constraints, jacobian, rows = [], [], []
    for i in range(n):
        f, df = function(0,i,c)
        g, dg = function(1,i,c)
        E = (1-p[i])*g
        I = p[i]*f
        dE = (1-p[i])*dg*dc
        dE[i] -= g
        dI = p[i]*df*dc
        dI[i] += f
        Bnew = B+E-c
        dBnew = dB+dE-dc
        required = delta if i==0 else rho*B
        constraints.append(Bnew-required)
        jacobian.append(dBnew if i==0 else dBnew-rho*dB)
        rows.append([c,Bnew,p[i],I,E])
        objective += I
        gradient += dI
        c, dh = function(2,i,E)
        dc = dh*dE
        B, dB = Bnew, dBnew
    return objective, gradient, np.array(constraints), np.array(jacobian), np.array(rows)

reference = trajectory(np.zeros(n))
constraint_scale = np.maximum(1.,reference[-1][:,0])
objective_scale = reference[-1][-1,0]

def fun(p):
    v, dv, *_ = trajectory(p)
    return -v/objective_scale, -dv/objective_scale

def constraints(p):
    return trajectory(p)[2]/constraint_scale

def jacobian(p):
    return trajectory(p)[3]/constraint_scale[:,None]

def start(cutoff, fraction=1.):
    c, B = 1., 0.
    p = np.zeros(n)
    for i in range(n):
        g = function(1,i,c)[0]
        required = max(delta,rho*B)
        pmax = 1-(c+required-B)/g
        p[i] = 0 if i<cutoff else max(0,pmax)*fraction
        E = (1-p[i])*g
        B += E-c
        c = function(2,i,E)[0]
    return p

# These are numerical starts for one fixed function sequence, not separate simulations.
solutions = []
for cutoff in range(n+1):
    initial = start(cutoff)
    result = minimize(fun, initial, jac=True, method='SLSQP', bounds=[(0,1)]*n,
        constraints={'type':'ineq','fun':constraints,'jac':jacobian},
        options={'ftol':1e-12,'maxiter':1000})
    v,dv,residual,J,rows=trajectory(result.x)
    solutions.append({'cutoff':cutoff,'success':bool(result.success),'objective':v,
        'minimum_scaled_slack':float(np.min(residual/constraint_scale)),
        'allocation':result.x.tolist(),'iterations':result.nit})
    print(cutoff, result.success, round(v,8), float(np.min(residual/constraint_scale)), flush=True)
feasible = [s for s in solutions if s['success'] and s['minimum_scaled_slack']>-1e-8]
best = max(feasible,key=lambda s:s['objective'])
p = np.array(best['allocation'])
p[p<1e-9]=0
v,dv,residual,J,rows=trajectory(p)
# Recompute the final active-balance phase exactly to remove solver roundoff.
first_intrinsic = int(np.flatnonzero(p>1e-7)[0])
candidate = start(first_intrinsic)
cv,*_=trajectory(candidate)
if abs(cv-v)<1e-6 and np.min(trajectory(candidate)[2])>-1e-9:
    p=candidate
    v,dv,residual,J,rows=trajectory(p)

# Verify the analytic derivatives by a centered finite difference at an interior allocation.
probe = np.full(n,.03)
eps=1e-6
numeric_gradient=np.array([(fun(probe+eps*np.eye(n)[i])[0]-fun(probe-eps*np.eye(n)[i])[0])/(2*eps) for i in range(n)])
numeric_jacobian=np.column_stack([(constraints(probe+eps*np.eye(n)[i])-constraints(probe-eps*np.eye(n)[i]))/(2*eps) for i in range(n)])
gradient_error=float(np.max(np.abs(numeric_gradient-fun(probe)[1])))
jacobian_error=float(np.max(np.abs(numeric_jacobian-jacobian(probe))))
assert gradient_error<1e-6 and jacobian_error<1e-6
assert np.min(residual)>-1e-8
assert np.all(rows[:,1]>=delta-1e-8)
assert np.all((p>=0)&(p<=1))
assert np.ptp([s['objective'] for s in feasible])<1e-5

summary={'seed':seed,'cycles':n,'rho':rho,'delta':delta,
    'formula':'F_i(x) = a_i*x*(1 + q_i*x/(1+x))',
    'scales':scales.tolist(),'curves':curves.tolist(),
    'allocation':p.tolist(),'expenditure':rows[:,0].tolist(),'balance':rows[:,1].tolist(),
    'intrinsic_increment':rows[:,3].tolist(),'cumulative_intrinsic':rows[:,3].cumsum().tolist(),
    'initial_full_external_cycles':first_intrinsic,'objective':v,
    'minimum_balance_slack':float(residual.min()),
    'gradient_error':gradient_error,'jacobian_error':jacobian_error,
    'numerical_starts':solutions,
    'scope':'One deterministic trajectory; SLSQP numerical solution, not a global optimality certificate.'}
Path(__file__).with_name('result.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:summary[k] for k in ['allocation','intrinsic_increment','cumulative_intrinsic','minimum_balance_slack','gradient_error','jacobian_error']},indent=2))
