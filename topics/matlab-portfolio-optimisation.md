---
id: matlab-portfolio-optimisation
title: "Portfolio Optimisation in MATLAB"
type: topic
domain: quant-dev
sources: [src-rbc-gam-quantdev-notes]
---
# Portfolio Optimisation in MATLAB

This chapter is the tooling view of portfolio construction: which Optimization Toolbox solver fits which portfolio problem, how the Financial Toolbox `Portfolio` object sets up and solves mean–variance problems, and how to go beyond it with custom objectives and constraints — and when to use the object versus writing the QP directly.

**Prerequisites:** [[matlab-name-value-arguments]], [[matlab-memory-model]] (the `Portfolio` object is a value object), [[eigen-svd-psd]] (PSD covariance, convexity).

**Leads to:** the theory in [[mean-variance-optimization]], [[risk-budgeting]] and [[black-litterman]].

**Sections:** [[matlab-optimization-solvers]] · [[matlab-portfolio-object]] · [[matlab-custom-portfolio-optimization]]

Conventions as in [[matlab-quant-dev]]: **(sourced)** = official documentation; **(自己推理)** = own reasoning; MATLAB code was not executed. Risk aversion is written $\lambda$ here, as in the code (`lambda`); elsewhere in the wiki it is $\gamma$.

<a id="matlab-optimization-solvers"></a>

## Optimisation Solvers in MATLAB
<!-- section: matlab-optimization-solvers | prerequisites: [matlab-name-value-arguments, eigen-svd-psd] | related: [mean-variance-optimization, root-finding, matlab-custom-portfolio-optimization] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, quadprog, fmincon, coneprog, optimization-toolbox] -->

Each problem class has a specialised solver; a mean–variance problem with linear constraints is a quadratic programme solved by `quadprog`, which MATLAB also exposes through a problem-based API similar to Python's cvxpy.

### Solver map (sourced: MathWorks Optimization Toolbox docs)

| Problem | Solver | Toolbox |
|---|---|---|
| Scalar, bounded | `fminbnd` | base MATLAB |
| Unconstrained, non-smooth OK | `fminsearch` | base |
| Root f(x)=0 | `fzero` | base |
| LP | `linprog` | Optimization |
| MILP | `intlinprog` | Optimization |
| QP | `quadprog` | Optimization |
| SOCP | `coneprog` | Optimization |
| General nonlinear constrained | `fmincon` | Optimization |
| Unconstrained smooth | `fminunc` | Optimization |
| Least squares | `lsqlin` / `lsqnonlin` / `lsqcurvefit` | Optimization |
| Global / MINLP | `ga`, `particleswarm`, `surrogateopt`, `MultiStart` | Global Optimization (separate licence) |

Optimization Toolbox solvers assume smooth problems; specialised LP/QP solvers beat `fmincon` on LP/QP.

### Portfolio problem → solver (自己推理)

| Problem | Solver |
|---|---|
| Standard MVO / min variance with linear constraints | `quadprog` |
| Max alpha s.t. TE ≤ cap (quadratic constraint) | `coneprog` or `fmincon` |
| Risk parity / budgeting | `fmincon` or `riskBudgetingPortfolio` |
| Max N holdings (cardinality) | integer variables (`intlinprog` if linear) |

### Formula: `quadprog` standard form
$$\min_x\ \tfrac12x^\top Hx+f^\top x\quad\text{s.t.}\quad Ax\le b,\quad A_{eq}x=b_{eq},\quad lb\le x\le ub$$

**Variables:**

- $x$ decision vector (portfolio weights)
- $H$ quadratic term ($2\lambda\Sigma$ for mean–variance)
- $f$ linear term ($-\mu$)
- $A,b$ linear inequality constraints
- $A_{eq},b_{eq}$ linear equality constraints
- $lb,ub$ lower and upper bounds
- $\lambda$ risk aversion; $\Sigma$ covariance; $\mu$ expected returns

Minimising $\lambda\,w^\top\Sigma w-\mu^\top w$ is the mean–variance objective of [[mean-variance-optimization]] with the sign flipped; it is convex when $\Sigma$ is PSD ([[eigen-svd-psd]]).

```matlab
H = 2*lambda*Sigma;  f = -mu;
Aeq = ones(1,n); beq = 1;  lb = zeros(n,1); ub = 0.1*ones(n,1);
w = quadprog(H, f, [], [], Aeq, beq, lb, ub);
```
Python: `cvxpy` — `cp.Maximize(mu @ w - lam*cp.quad_form(w, Sigma))`.

### Problem-based API (like cvxpy)
```matlab
w = optimvar('w', n, 'LowerBound', 0, 'UpperBound', 0.1);
prob = optimproblem('ObjectiveSense', 'maximize');
prob.Objective = mu'*w - lambda*(w'*Sigma*w);
prob.Constraints.budget = sum(w) == 1;
sol = solve(prob);     % auto-detects QP → quadprog
sol.w
```

**References:**

- MathWorks: [Problems handled by Optimization Toolbox](https://de.mathworks.com/help/optim/ug/problems-handled-by-optimization-toolbox-functions.html) · [Optimization decision table](https://in.mathworks.com/help/optim/ug/optimization-decision-table.html) · [solve](https://www.mathworks.com/help/optim/ug/optim.problemdef.optimizationproblem.solve.html)

### Connections
- **Builds on:** [[matlab-name-value-arguments]] (`optimoptions`), [[eigen-svd-psd]] (convexity).
- **Theory:** [[mean-variance-optimization]]. **Root finding in general:** [[root-finding]].
- **Next:** [[matlab-portfolio-object]].

<a id="matlab-portfolio-object"></a>

## The `Portfolio` Object (Financial Toolbox)
<!-- section: matlab-portfolio-object | prerequisites: [matlab-optimization-solvers, matlab-memory-model] | related: [mean-variance-optimization, risk-budgeting, sharpe-ratio, matlab-custom-portfolio-optimization] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, portfolio-object, efficient-frontier, max-sharpe, estimation-error] -->

The `Portfolio` object is a Financial Toolbox class (introduced **R2011a**) for **mean–variance portfolio optimisation and analysis** (sourced). It is a container for the whole problem definition — **data** (μ, Σ) + **constraints** + **methods** to solve and analyse — and it is a **value object**, so every `set*` returns a new object: `p = setBounds(p, ...)`; `setBounds(p, ...)` alone does nothing ([[matlab-memory-model]]).

### Formula: default problem
(The formula is a transcription of the documented setup.)

$$\min_w\ w^\top\Sigma w\quad\text{s.t.}\quad\mu^\top w=r^*,\quad\mathbf 1^\top w=1,\quad w\ge0$$

**Variables:**

- $w$ portfolio weights
- $\Sigma$ asset covariance (`AssetCovar`)
- $\mu$ asset mean returns (`AssetMean`)
- $r^*$ target return (one per frontier point)
- $\mathbf 1$ vector of ones

### Creation syntax (sourced)
```matlab
p = Portfolio;                                   % empty (all properties [])
p = Portfolio('Name1', v1, 'Name2', v2);         % name-value pairs
p = Portfolio(p, 'Name1', v1);                   % copy & modify
```
- Names are **case-insensitive** but must be **fully spelled**.
- Shortcuts: `'mean'` (AssetMean), `'covar'` (AssetCovar), `'lb'`/`'ub'`, `'budget'` (both budget bounds).
- `NumAssets` is inferred from the inputs; **scalar expansion** (`'lb', 0` → N×1).
- Dot notation (`p.UpperBound = ...`) works but **bypasses error checking** → prefer `set*`.

```matlab
mu = [0.10; 0.08; 0.06; 0.05];
Sigma = [0.040 0.018 0.006 0.005; 0.018 0.030 0.005 0.004;
         0.006 0.005 0.020 0.012; 0.005 0.004 0.012 0.018];
p = Portfolio('AssetList', ["AAPL" "MSFT" "RY" "TD"], 'AssetMean', mu, 'AssetCovar', Sigma, ...
              'RiskFreeRate', 0.03, 'lb', 0, 'ub', 0.4, 'budget', 1);
w = estimateMaxSharpeRatio(p);
```
Equivalent step by step: `setAssetMoments`, `setBounds`, `setBudget`. (`...` = line continuation.)

### Main functions

| Purpose | Functions |
|---|---|
| Data | `setAssetMoments`, `estimateAssetMoments`, `setAssetList` |
| Constraints | `setDefaultConstraints`, `setBounds`, `setBudget`, `setGroups`, `setGroupRatio`, `setEquality`, `setInequality`, `setTurnover`, `setOneWayTurnover`, `setTrackingError`, `setMinMaxNumAssets`, `setConditionalBudget` |
| Costs/cash | `BuyCost`, `SellCost`, `RiskFreeRate`, `InitPort` |
| Solve | `estimateFrontier`, `estimateFrontierByReturn`, `estimateFrontierByRisk`, `estimateMaxSharpeRatio` |
| Analyse | `estimatePortMoments`, `plotFrontier` |
| Solver | `setSolver` (`'quadprog'` default, `'lcprog'`, `'fmincon'`) |

Related: `PortfolioCVaR`, `PortfolioMAD` (same interface; **no tracking-error constraint**).

### Walkthrough of the basic example
```matlab
% R: T×N daily returns (rows = dates, cols = assets)
p = Portfolio('AssetList', ["AAPL" "MSFT" "RY" "TD"], 'RiskFreeRate', 0.03/252);
p = estimateAssetMoments(p, R);
p = setDefaultConstraints(p);
pwgt   = estimateFrontier(p, 20);
wSharp = estimateMaxSharpeRatio(p);
[risk, ret] = estimatePortMoments(p, wSharp);
plotFrontier(p, 20); hold on
plot(risk, ret, 'r*');
```

| Line | What it does |
|---|---|
| `Portfolio(...)` | Labels assets; `RiskFreeRate` is **daily** (`0.03/252`) because R is daily — units must match |
| `estimateAssetMoments(p, R)` | Sample mean & covariance → `AssetMean`, `AssetCovar`. Input obs × assets (also table/timetable); default `'DataFormat','Returns'` (or `'Prices'`); by default drops NaN rows (`'MissingData', true` → ECM); output periodicity = input |
| `setDefaultConstraints` | Budget sum = 1 + long-only |
| `estimateFrontier(p,20)` | **N×20** matrix, **each column** = one portfolio, spaced **equally in return** from min-risk to max-return; default NumPorts = 10; optional `[pwgt,pbuy,psell]` |
| `estimateMaxSharpeRatio` | Tangency portfolio; default `'direct'` (single QP), alternative `'iterative'` (`fminbnd`) |
| `estimatePortMoments` | `risk` = std, `ret` = mean — **daily** here → annualise with `*sqrt(252)`, `*252` |
| `plotFrontier` / `plot(...,'r*')` | x = std, y = mean; `hold on` overlays the red star |

$$\hat\mu_i=\frac1T\sum_{t=1}^TR_{t,i},\qquad \max_w\ \frac{\hat\mu^\top w-r_f}{\sqrt{w^\top\hat\Sigma w}}$$

**Variables:**

- $R_{t,i}$ return of asset $i$ on day $t$
- $T$ number of days
- $\hat\mu,\hat\Sigma$ sample mean vector and covariance
- $r_f$ risk-free rate per period (`RiskFreeRate`, daily here)

### Worked example: numerical run (replicated in Python; true annual means 14/12/8/7%)

| | AAPL | MSFT | RY | TD |
|---|---|---|---|---|
| True mean | 14% | 12% | 8% | 7% |
| **Estimated** | **−4.2%** | 10.1% | **30.5%** | 12.9% |
| Estimated vol | 27.8% | 23.0% | 16.3% | 15.3% |

| Frontier | AAPL | MSFT | RY | TD | Ret | Vol |
|---|---|---|---|---|---|---|
| Min-risk | 0 | .22 | .24 | .55 | 16.4% | 14.0% |
| | 0 | .19 | .43 | .37 | 20.0% | 14.2% |
| | 0 | .17 | .63 | .20 | 23.5% | 14.5% |
| | 0 | .15 | .82 | .03 | 27.0% | 15.2% |
| Max-return | 0 | 0 | 1 | 0 | 30.5% | 16.3% |

Max Sharpe = **100% RY** (daily risk 0.0103, return 0.00121; annual 16.3% vol, 30.5% return, Sharpe ≈ 1.69).

**Lesson — estimation error ("MVO = error maximizer"):** with 3 years of data the standard error of an annualised mean is ≈ 16%/√3 ≈ 9% (formula in [[mean-variance-optimization]]). Fixes: model alphas instead of sample means ([[grinold-alpha]]), shrinkage / Black–Litterman ([[black-litterman]]), position bounds, a factor or shrinkage risk model ([[eigen-svd-psd]]).

### Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Annual rf with daily R | Wrong Sharpe portfolio | Same periodicity everywhere |
| Forgetting `p = ...` | Constraint silently missing | Always reassign |
| NaN in R | Rows dropped | Check data / `'MissingData', true` |
| Sample-mean noise | Corner solutions | Alphas, shrinkage, bounds |
| Reading `pwgt` by row | Wrong weights | Columns are portfolios |

### More `Portfolio` examples
```matlab
% Active vs benchmark (closest to a quant-equity process)
p = Portfolio('AssetMean', mu, 'AssetCovar', Sigma);
p = setDefaultConstraints(p);
p = setBounds(p, 0, 0.05);
p = setGroups(p, SectorMatrix, secLower, secUpper);   % G×N membership
p = setTrackingPort(p, wb);  p = setTrackingError(p, 0.03);
p = setInitPort(p, w0);      p = setTurnover(p, 0.10);
p = setCosts(p, 0.001, 0.001);
w = estimateFrontierByRisk(p, 0.15);
% Note: TrackingPort ≠ InitPort (separate properties, per docs)

% Risk parity / budgeting (R2022a+)
w_rp = riskBudgetingPortfolio(Sigma);
w_rb = riskBudgetingPortfolio(Sigma, [0.1;0.2;0.3;0.4]);

% CVaR
p = PortfolioCVaR;  p = setScenarios(p, R);  p = setDefaultConstraints(p);
p = setProbabilityLevel(p, 0.95);  w = estimateFrontierByReturn(p, targetRet);

% Cardinality
p = setMinMaxNumAssets(p, 20, 50);
p = setBounds(p, 0.01, 0.05, 'BoundType', 'Conditional');   % 0 or 1–5%
```

`riskBudgetingPortfolio` targets $RC_i/\sum_jRC_j=b_i$, with $RC_i$ the risk contribution of asset $i$ and $b_i$ its target budget ([[risk-budgeting]]).

(`setTurnover`, `setCosts`, `setProbabilityLevel`, `estimateFrontierByRisk/ByReturn` argument orders not individually verified.)

**References:**

- MathWorks: [Portfolio](https://www.mathworks.com/help/finance/portfolio.html) · [Creating the Portfolio object](https://www.mathworks.com/help/finance/constructing-the-portfolio-object.html) · [estimateAssetMoments](https://www.mathworks.com/help/finance/portfolio.estimateassetmoments.html) · [estimateFrontier](https://www.mathworks.com/help/finance/portfolio.estimatefrontier.html) · [estimateMaxSharpeRatio](https://www.mathworks.com/help/finance/portfolio.estimatemaxsharperatio.html) · [estimatePortMoments](https://www.mathworks.com/help/finance/portfolio.estimateportmoments.html) · [Supported constraints](https://www.mathworks.com/help/finance/supported-constraints-for-portfolio-optimization-using-portfolio-object.html) · [Tracking-error constraints](https://www.mathworks.com/help/finance/working-with-tracking-error-constraints-using-portfolio-object.html) · [setBounds](https://www.mathworks.com/help/finance/portfolio.setbounds.html) · [Conditional bounds / cardinality](https://www.mathworks.com/help/finance/working-with-integrality-constraints-using-portfolio-object.html) · [riskBudgetingPortfolio](https://www.mathworks.com/help/finance/riskbudgetingportfolio.html)

### Connections
- **Builds on:** [[matlab-optimization-solvers]], [[matlab-memory-model]].
- **Theory:** [[mean-variance-optimization]] (tangency portfolio, estimation error), [[sharpe-ratio]], [[risk-budgeting]].
- **Next:** [[matlab-custom-portfolio-optimization]].

<a id="matlab-custom-portfolio-optimization"></a>

## Custom Objectives & Constraints; `Portfolio` vs `quadprog`
<!-- section: matlab-custom-portfolio-optimization | prerequisites: [matlab-portfolio-object] | related: [mean-variance-optimization, grinold-alpha, exposure-neutrality] | sources: [src-rbc-gam-quantdev-notes] | tags: [matlab, optimproblem, fmincon, transaction-costs, tracking-error] -->

A realistic quant rebalance maximises alpha minus active risk minus trading costs under sector, beta and turnover limits. There are three levels of control — the `Portfolio` object, its custom-objective extension, and writing the problem yourself — and the choice trades convenience against transparency.

### Three levels of control

| Level | Tool | Objective | Constraints | Solver |
|---|---|---|---|---|
| 1 | `Portfolio` + `set*` | Mean–variance fixed | Built-in + custom **linear** | `setSolver` |
| 2 | `Portfolio` + `estimateCustomObjectivePortfolio` (R2022b+) | Any function of w | Same as level 1 | Internal |
| 3 | `optimproblem` or `quadprog`/`fmincon` | Anything | Anything | You choose |

**Level 1**
```matlab
p = setInequality(p, betas', 1.05);                       % custom linear A*w <= b
p = setSolver(p, 'quadprog', 'Display', 'off');
opts = optimoptions('fmincon', 'Algorithm', 'interior-point', 'Display', 'off');
p = setSolver(p, 'fmincon', opts);
```

**Level 2** (the objective must be continuous and depend only on the weights; convex if there are cardinality/conditional bounds)
```matlab
objFun = @(w) alpha'*w - lambda*(w - wb)'*Sigma*(w - wb);
w = estimateCustomObjectivePortfolio(p, objFun, ObjectiveSense="maximize");
```

### Formula: level 3a — problem-based (recommended for a custom quant rebalance)
$$\max_{w,b,s}\ \alpha^\top w-\lambda\,(w-w_b)^\top\Sigma\,(w-w_b)-c^\top(b+s)\qquad\text{s.t.}\quad w-w_0=b-s,\ \ b,s\ge0$$

**Variables:**

- $w$ new portfolio weights
- $\alpha$ vector of alphas (expected returns, [[grinold-alpha]])
- $w_b$ benchmark weights
- $\lambda$ risk aversion
- $\Sigma$ covariance matrix
- $c$ unit trading cost per asset
- $b,s$ buys and sells (non-negative)
- $w_0$ current weights

Splitting $|w-w_0|$ into $b+s$ keeps the problem a QP.

```matlab
w    = optimvar('w', N, 'LowerBound', 0, 'UpperBound', 0.05);
buy  = optimvar('buy', N, 'LowerBound', 0);
sell = optimvar('sell', N, 'LowerBound', 0);
act  = w - wb;
prob = optimproblem('ObjectiveSense', 'maximize');
prob.Objective = alpha'*w - lambda*(act'*Sigma*act) - c'*(buy + sell);
prob.Constraints.budget   = sum(w) == 1;
prob.Constraints.trades   = w - w0 == buy - sell;       % split |w-w0| to stay a QP
prob.Constraints.turnover = sum(buy + sell) <= 0.20;
prob.Constraints.secUp    = S*act <=  0.03;
prob.Constraints.secDown  = S*act >= -0.03;
prob.Constraints.beta     = betas'*w <= 1.05;
opts = optimoptions('quadprog', 'Display', 'off');
[sol, fval, exitflag] = solve(prob, 'Options', opts);
wOpt = sol.w;          % check exitflag > 0
```

### Level 3b — solver-based
```matlab
H = 2*lambda*Sigma;
f = -(alpha + 2*lambda*Sigma*wb);                 % expanded active-risk term
A = [S; -S];  b = [0.03 + S*wb; 0.03 - S*wb];
w = quadprog(H, f, A, b, ones(1,N), 1, zeros(N,1), 0.05*ones(N,1), [], opts);

% fmincon: non-quadratic objective / nonlinear constraint
negSharpe = @(w) -(alpha'*w) / sqrt(w'*Sigma*w);
nonlcon   = @(w) deal(sqrt(w'*Sigma*w) - 0.15, []);   % vol <= 15%
w = fmincon(negSharpe, ones(N,1)/N, [], [], Aeq, beq, lb, ub, nonlcon, opts);
% order: fmincon(fun, x0, A, b, Aeq, beq, lb, ub, nonlcon, options); [] for unused
```

### `Portfolio` object vs `quadprog`
**Drawbacks of `Portfolio`:**

| Drawback | Why |
|---|---|
| Mean–variance objective (sourced) | Alpha − risk − TC needs level 2 (R2022b+) or leaving the object |
| Less transparent (自己推理) | Can't see H/f/A/b; harder to debug infeasibility |
| Constraint menu | Built-ins + linear only; TE not in CVaR/MAD (sourced) |
| Extra licence | Financial Toolbox |
| Overhead (自己推理) | Validation + copies per `set*`; matters in big backtests |
| Silent failures | Missing `p =`; dot notation skips checks (sourced) |
| Portability | No direct Python equivalent; an explicit QP maps to `cvxpy` |

**Drawbacks of raw `quadprog`:** manual matrix-algebra errors (sign flips, H/f expansion, stacked constraints), more code and tests, no frontier/Sharpe/plot helpers, long positional argument lists.

**Middle ground:** `optimproblem` — math-like, named constraints, full control.

| Use case | Choice (自己推理) |
|---|---|
| Asset allocation, frontier, max Sharpe | `Portfolio` |
| Stock-level rebalance with alphas, active risk, TC | `optimproblem` |
| Hot backtest loop / legacy parity | raw `quadprog` |
| Possible Python migration | `optimproblem` / `quadprog` (→ `cvxpy`) |

**References:**

- MathWorks: [setSolver](https://www.mathworks.com/help/finance/portfolio.setsolver.html) · [estimateCustomObjectivePortfolio](https://www.mathworks.com/help/finance/portfolio.estimatecustomobjectiveportfolio.html)

### Connections
- **Builds on:** [[matlab-portfolio-object]].
- **Theory:** [[mean-variance-optimization]] (why optimised weights are extreme), [[grinold-alpha]] (alpha inputs), [[exposure-neutrality]] (active and beta exposure).
