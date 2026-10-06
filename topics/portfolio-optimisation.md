---
id: portfolio-optimisation
title: "Portfolio Optimisation"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-rbc-gam-quantdev-notes]
---
# Portfolio Optimisation

This chapter builds portfolios from expected returns and covariances. It starts with portfolio variance and diversification, asks when adding a lower-Sharpe strategy still helps, derives the minimum-variance and mean–variance (tangency) portfolios, explains why optimised portfolios are fragile, and covers Black–Litterman, which stabilises the optimiser with a Bayesian prior. The constrained-optimisation tools (Lagrange multipliers, KKT conditions, duality) are introduced before the minimum-variance derivation that uses them; the chapter ends with constraints as regularisation and shadow prices, and with debugging an optimiser that returns infeasible.

**Prerequisites:** [[variance-covariance-correlation]], [[eigen-svd-psd]], [[sharpe-ratio]], [[conditional-probability-bayes]], [[taylor-expansions]].

**Leads to:** [[risk-contribution]], [[risk-budgeting]], [[portfolio-construction-pipeline]]; alpha inputs come from [[grinold-alpha]].

**Sections:** [[portfolio-variance-diversification]] · [[marginal-sharpe-improvement]] · [[lagrange-kkt-duality]] · [[minimum-variance-portfolio]] · [[mean-variance-optimization]] · [[black-litterman]] · [[constraints-shadow-prices]] · [[optimiser-infeasibility]]

Notation for this chapter: $w$ weight vector, $\mu$ vector of expected **excess** returns, $\Sigma$ covariance matrix, $\sigma_p$ portfolio volatility, $\gamma$ risk aversion, $\mathbf 1$ vector of ones.

<a id="portfolio-variance-diversification"></a>

## Portfolio Variance & Diversification
<!-- section: portfolio-variance-diversification | prerequisites: [variance-covariance-correlation] | related: [sharpe-ratio, minimum-variance-portfolio, risk-contribution, worst-of-correlation, pca, risk-on-risk-off] | sources: [src-squarepoint-dqa-workbook] | tags: [diversification, correlation] -->

A portfolio's variance is a quadratic form in its weights. Less-than-perfect correlation lowers portfolio volatility relative to the average of the individual volatilities — the diversification benefit — but a common positive correlation leaves a floor that no number of assets removes.

### Formulas
$$\mu_p=w^\top\mu,\qquad \sigma_p^2=w^\top\Sigma w,\qquad \sigma_p^2=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\sigma_1\sigma_2\ \ \text{(two assets)}$$
$$\text{Two equal strategies: }\ \sigma_p=\sigma\sqrt{\tfrac{1+\rho}{2}},\quad SR_p=SR\sqrt{\tfrac{2}{1+\rho}};\qquad n\text{ equicorrelated: }\ \sigma_p^2=\sigma^2\Big[\rho+\frac{1-\rho}{n}\Big]$$

**Variables:**

- $w$ weight vector (in the two-asset formula, $w$ is the weight of asset 1 and $1-w$ of asset 2)
- $\mu$ expected excess returns; $\mu_p$ portfolio expected excess return
- $\Sigma$ covariance matrix; $\sigma_p$ portfolio volatility
- $\sigma_1,\sigma_2$ volatilities of the two assets; $\sigma$ common volatility
- $\rho$ correlation (pairwise, common)
- $SR$ Sharpe ratio of each strategy; $SR_p$ of the equal-weight portfolio
- $n$ number of assets

### Worked examples
- SR 0.5 each, $\rho=0$ → the 50/50 portfolio has SR ≈ 0.707; with $\rho=1$ it stays 0.5 (no benefit).
- 10 uncorrelated strategies with SR 0.5 → $0.5\sqrt{10}\approx1.58$.

### Key points
- A positive common $\rho$ leaves a **floor** $\rho\sigma^2$ on the variance as $n\to\infty$. A valid equicorrelation matrix needs $\rho\ge-1/(n-1)$ ([[eigen-svd-psd]]).
- Averaging Sharpe ratios or adding volatilities is wrong — use the covariance.

### Connections
- **Builds on:** [[variance-covariance-correlation]].
- **Leads to:** [[marginal-sharpe-improvement]], [[minimum-variance-portfolio]], [[mean-variance-optimization]], [[risk-contribution]].
- **Correlation as a traded risk:** [[worst-of-correlation]]. **When correlations jump:** [[risk-on-risk-off]].

<a id="marginal-sharpe-improvement"></a>

## When a Lower-Sharpe Strategy Improves a Portfolio
<!-- section: marginal-sharpe-improvement | prerequisites: [sharpe-ratio, portfolio-variance-diversification] | related: [mean-variance-optimization, risk-contribution] | sources: [src-squarepoint-dqa-workbook] | tags: [marginal, correlation] -->

Adding a small allocation to a new strategy raises the portfolio's Sharpe ratio exactly when the new strategy's Sharpe exceeds its correlation with the portfolio times the portfolio's Sharpe.

### Formula
$$SR(\varepsilon)=\frac{\mu_P+\varepsilon\,\mu_A}{\sqrt{\sigma_P^2+2\varepsilon\,c+\varepsilon^2\sigma_A^2}},\qquad \frac{dSR}{d\varepsilon}\Big|_{\varepsilon=0}>0\iff SR_A>\rho_{PA}\,SR_P$$

**Variables:**

- $P$ existing portfolio, with expected excess return $\mu_P$, volatility $\sigma_P$ and Sharpe $SR_P$
- $A$ candidate strategy, with $\mu_A$, $\sigma_A$ and $SR_A$
- $\varepsilon$ small financed allocation to $A$
- $c=\mathrm{Cov}(P,A)$
- $\rho_{PA}$ correlation of $P$ and $A$

### Worked example
Portfolio SR 1.2; new strategy SR 0.4 with $\rho$ = 0.2 → $0.4>0.2\times1.2=0.24$ ✓ it adds value (locally, frictionless).

### Derivation
The allocation $\varepsilon$ is financed (excess returns, no capital taken from $P$). Differentiating $SR(\varepsilon)$ at $\varepsilon=0$:

$$\frac{dSR}{d\varepsilon}\Big|_{0}=\frac{\mu_A}{\sigma_P}-\frac{\mu_P\,c}{\sigma_P^3}>0\iff\mu_A>\frac{c}{\sigma_P^2}\,\mu_P$$

**Variables:**

- $\mu_P,\sigma_P$ expected excess return and volatility of the portfolio
- $\mu_A$ expected excess return of the candidate
- $c=\mathrm{Cov}(r_P,r_A)$ covariance of the two return streams

Dividing both sides by $\sigma_A$ and using $c/(\sigma_P\sigma_A)=\rho_{PA}$ gives $SR_A>\rho_{PA}\,SR_P$.

### Reading it
- **It is an alpha test.** $c/\sigma_P^2=\beta_{A|P}$, the slope of a regression of $A$'s returns on $P$'s ([[capm-alpha-beta]]). The condition $\mu_A>\beta_{A|P}\,\mu_P$ says "$A$ has positive alpha relative to $P$".
- **With negative correlation even a negative Sharpe can help.** $SR_P=1$, $\rho=-0.5$, $SR_A=-0.2$: since $-0.2>-0.5$, a small allocation raises the portfolio Sharpe; $A$ works as a hedge.
- **It is only a local condition.** The more of $A$ is added, the more correlated it becomes with the new portfolio, until the inequality becomes an equality — that point is the optimal allocation.
- Assumes no frictions, no costs and known parameters; in practice subtract trading costs and check capacity.

### At the optimum: every asset satisfies $SR_i=\rho_{i,P}\,SR_P$
From the first-order condition of [[mean-variance-optimization]], $\mu=\gamma\Sigma w$:

$$\mu_i=\gamma\,(\Sigma w)_i=\gamma\,\mathrm{Cov}(r_i,r_P),\qquad \mu_P=\gamma\,\sigma_P^2\ \Rightarrow\ \mu_i=\mu_P\,\frac{\mathrm{Cov}(r_i,r_P)}{\sigma_P^2}\ \Rightarrow\ \frac{\mu_i}{\sigma_i}=\rho_{i,P}\,\frac{\mu_P}{\sigma_P}$$

**Variables:**

- $\mu_i,\sigma_i$ expected excess return and volatility of asset $i$
- $r_i,r_P$ returns of asset $i$ and of the optimal portfolio $P$
- $\rho_{i,P}$ correlation of asset $i$ with $P$
- $\gamma$ risk aversion; $w$ optimal weights; $\Sigma$ covariance matrix

At the mean–variance optimum no asset passes or fails the marginal test any more: the local rule holds with equality for every asset.

### Connections
- **Builds on:** [[sharpe-ratio]], [[portfolio-variance-diversification]].
- **Related:** [[mean-variance-optimization]] (the global version), [[risk-contribution]] (marginal risk), [[capm-alpha-beta]] (the beta/alpha reading).

<a id="lagrange-kkt-duality"></a>

## Lagrange Multipliers, KKT Conditions & Duality
<!-- section: lagrange-kkt-duality | prerequisites: [] | related: [minimum-variance-portfolio, constraints-shadow-prices, optimiser-infeasibility, matlab-optimization-solvers] | sources: [src-portopt-pm-interview] | tags: [lagrange, kkt, duality, shadow-price, constrained-optimisation] -->

Most portfolio problems are optimisations with constraints, where the best point usually sits on the edge of the allowed region and the gradient is not zero there. A Lagrange multiplier handles an equality constraint; the KKT (Karush–Kuhn–Tucker) conditions extend it to inequalities. Every multiplier is a **shadow price**: how much the optimum improves when its constraint is relaxed by one unit.

### Formula: the problem and the Lagrangian
$$\max_x\ f(x)\quad\text{s.t.}\quad g_j(x)\le c_j,\ \ h_k(x)=d_k$$
$$L(x,\mu,\lambda)=f(x)-\sum_j\mu_j\big(g_j(x)-c_j\big)-\sum_k\lambda_k\big(h_k(x)-d_k\big)$$

**Variables:**

- $x$ decision variables (in portfolios, the weights $w$)
- $f(x)$ objective (utility, Sharpe, minus variance)
- $g_j(x)\le c_j$ inequality constraints, $j=1,\dots,m$ (position caps, long-only, TE limit)
- $h_k(x)=d_k$ equality constraints, $k=1,\dots,p$ (fully invested, dollar-neutral)
- $L$ the Lagrangian
- $\mu_j$ multiplier on inequality $j$; $\lambda_k$ multiplier on equality $k$

### Equality constraints: Lagrange multipliers
Set all partial derivatives of $L$ to zero: $\nabla f(x)=\lambda\nabla h(x)$ together with the constraint $h(x)=d$ itself.

**Geometric intuition:** walking along the constraint looking for the highest $f$, if $\nabla f$ had any component along the constraint you could step that way and do better. So at the optimum $\nabla f$ is perpendicular to the constraint, as is $\nabla h$: the two gradients are parallel and $\lambda$ is the scale factor.

$$\lambda=\frac{\partial f^*}{\partial d}$$

**Variables:**

- $f^*$ optimal objective value
- $d$ bound of the equality constraint

**Example:** maximise $xy$ s.t. $x+y=10$. $L=xy-\lambda(x+y-10)$ gives $y=\lambda$, $x=\lambda$, so $x=y=5$, $\lambda=5$, $f^*=25$. Check the shadow price: with budget $d$, $f^*=d^2/4$ and $df^*/dd=d/2=5=\lambda$ ✓; raising the budget to 11 gives $f^*=30.25$ (about $+\lambda$).

### Inequality constraints: the four KKT conditions
At the optimum an inequality is either **slack** ($g_j(x)<c_j$, it doesn't matter, $\mu_j=0$) or **binding** ($g_j(x)=c_j$, it acts like an equality, $\mu_j\ge0$).

| # | Condition | Formula | In words |
|---|---|---|---|
| 1 | Stationarity | $\nabla f=\sum_j\mu_j\nabla g_j+\sum_k\lambda_k\nabla h_k$ | No improving direction is left that keeps every rule |
| 2 | Primal feasibility | $g_j(x)\le c_j$, $h_k(x)=d_k$ | The portfolio obeys the constraints |
| 3 | Dual feasibility | $\mu_j\ge0$ ($\lambda_k$ free) | The shadow prices have the right sign |
| 4 | Complementary slackness | $\mu_j\big(g_j(x)-c_j\big)=0$ | Either the constraint binds or its price is zero |

**Notes:**

- **Primal** = the original decision variables; **dual** = the multipliers. Primal feasibility asks whether the portfolio is allowed (e.g. $w=(60\%,40\%)$ with a 50% cap per name is primal infeasible).
- **Why $\mu_j\ge0$:** raising $c_j$ loosens a $\le$ constraint, the allowed set grows, so the optimum can only improve: $\partial f^*/\partial c_j\ge0$. An equality can bind in either direction, so $\lambda_k$ has any sign.
- **Why complementary slackness:** a constraint that doesn't touch the solution can be relaxed without changing anything, so its shadow price is 0; a positive price means it binds.
- Sign conventions differ between textbooks (min vs max, $+\mu$ vs $-\mu$); the invariant is that an inequality's shadow price has the sign that makes relaxing it helpful.

### Worked example: a position cap
$$\max_w\ \alpha w-\frac{\gamma}{2}\sigma^2w^2\quad\text{s.t.}\quad w\le w_{\max};\qquad \text{stationarity: }\ \alpha-\gamma\sigma^2w-\mu=0$$

**Variables:**

- $w$ position weight; $w_{\max}$ position cap
- $\alpha$ expected return (per year)
- $\sigma$ volatility (per year); $\gamma$ risk aversion
- $\mu\ge0$ multiplier on the cap

$\alpha=4\%$, $\sigma=20\%$, $\gamma=5$ → $\gamma\sigma^2=0.2$, unconstrained optimum $\bar w=0.04/0.2=20\%$.

- **Cap 30% (slack):** try $\mu=0$ → $w=20\%<30\%$, feasible; complementary slackness holds.
- **Cap 10% (binding):** $\mu=0$ would give 20% > 10% ✗, so $w=10\%$ and $\mu=0.04-0.2\times0.10=0.02\ge0$ ✓. Raising the cap by 1 percentage point adds about $0.02\times0.01=0.0002$ = **2 bp of risk-adjusted return** — the number to take to the risk committee.
- **Dual infeasibility as a diagnostic:** with the cap at 30%, wrongly assuming it binds gives $\mu=0.04-0.2\times0.30=-0.02<0$. A negative shadow price says the position is being pushed *up* to a cap it doesn't want to reach; release the constraint ($w=20\%$, $\mu=0$). Active-set solvers work this way: guess the binding set, solve, release any constraint whose multiplier comes out negative.

### Duality: bounds from both sides
$$q(\mu)=\max_x\ L(x,\mu);\qquad f(x)\le L(x,\mu)\le q(\mu)\ \ \text{for any feasible }x\text{ and any }\mu\ge0;\qquad f(x)\le f^*\le q(\mu)$$

**Variables:**

- $q(\mu)$ dual function: maximise the Lagrangian over $x$ with the constraints removed, charging $\mu_j$ per unit of violation ("fines" instead of prohibitions)
- $f^*$ true optimal value

**Notes:**

- **Weak duality.** The first inequality needs $\mu\ge0$: for feasible $x$, $g_j(x)-c_j\le0$, so the penalty $-\mu_j(g_j(x)-c_j)\ge0$. That is why dual feasibility matters. Every primal-feasible point is a lower bound on the optimum, every dual-feasible point an upper bound; the **dual problem** is $\min_{\mu\ge0}q(\mu)$.
- **Strong duality.** For convex problems (mean–variance with linear constraints) under Slater's condition (some point strictly satisfies every inequality), $\min_{\mu\ge0}q(\mu)=f^*$. The gap $q(\mu)-f(x)$ is the **duality gap**; interior-point solvers stop when it is below tolerance.
- **KKT sufficiency.** For convex problems any KKT point is the global optimum. With non-convex constraints (cardinality, integer lots) KKT points may be only local optima. KKT is *necessary* under a constraint qualification such as Slater's.

**Example (position cap, cap 10%):** $q(\mu)=\dfrac{(\alpha-\mu)^2}{2\gamma\sigma^2}+\mu w_{\max}=\dfrac{(0.04-\mu)^2}{0.4}+0.1\mu$, minimised at $\mu^*=0.02$ — the same shadow price as above (computed).

| Point | Feasible? | Value | Role |
|---|---|---|---|
| Primal $w=5\%$ | ✓ | $f=0.00175$ | lower bound |
| Primal $w^*=10\%$ | ✓ | $f^*=0.003$ | optimum |
| Dual $\mu=0$ | ✓ | $q=0.004$ | upper bound |
| Dual $\mu^*=0.02$ | ✓ | $q=0.003$ | $=f^*$ (strong duality) |

### Key points
- Solvers (Gurobi, MOSEK, CVXPY) report the multipliers as **dual values**; that is where shadow prices come from in practice ([[constraints-shadow-prices]]).
- Solver statuses "primal infeasible" / "dual infeasible" are read in [[optimiser-infeasibility]].
- Reference: Boyd & Vandenberghe, *Convex Optimization*, Ch. 5 (cited from memory — verify).

### Connections
- **Used by:** [[minimum-variance-portfolio]] (GMV via one multiplier), [[constraints-shadow-prices]] (Jagannathan–Ma, shadow prices), [[optimiser-infeasibility]], [[transaction-costs-no-trade]] (the no-trade band is the same logic at a kink).
- **Related:** [[matlab-optimization-solvers]] (QP standard form).

<a id="minimum-variance-portfolio"></a>

## Minimum-Variance Portfolio (2-asset & GMV)
<!-- section: minimum-variance-portfolio | prerequisites: [portfolio-variance-diversification] | related: [mean-variance-optimization, risk-budgeting] | sources: [src-squarepoint-dqa-workbook] | tags: [gmv, optimisation] -->

The portfolio with the lowest possible variance needs no expected-return inputs, only the covariance matrix.

### Formulas
$$w_1^*=\frac{\sigma_2^2-\rho\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2},\qquad w_{GMV}=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^\top\Sigma^{-1}\mathbf 1},\qquad \sigma^2_{GMV}=\frac{1}{\mathbf 1^\top\Sigma^{-1}\mathbf 1}$$

**Variables:**

- $w_1^*$ minimum-variance weight of asset 1 in a two-asset portfolio (asset 2 gets $1-w_1^*$)
- $\sigma_1,\sigma_2$ volatilities; $\rho$ correlation
- $w_{GMV}$ global minimum-variance weights (fully invested)
- $\sigma^2_{GMV}$ its variance
- $\Sigma$ covariance matrix (positive definite)
- $\mathbf 1$ vector of ones

### Derivation via a Lagrange multiplier
$$\min_w\ \tfrac12\,w^\top\Sigma w\ \ \text{s.t.}\ \ \mathbf 1^\top w=1;\qquad L=\tfrac12\,w^\top\Sigma w-\lambda(\mathbf 1^\top w-1)\ \Rightarrow\ \Sigma w=\lambda\mathbf 1\ \Rightarrow\ w=\lambda\,\Sigma^{-1}\mathbf 1$$

**Variables:**

- $L$ Lagrangian ([[lagrange-kkt-duality]])
- $\lambda$ multiplier on the budget constraint
- $w$ weights; $\Sigma$ covariance matrix; $\mathbf 1$ vector of ones ($\mathbf 1^\top w$ = sum of weights)

Plugging into the constraint, $\lambda\,\mathbf 1^\top\Sigma^{-1}\mathbf 1=1$, so $\lambda=1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)=\sigma^2_{GMV}$: **the multiplier equals the GMV variance**. As a shadow price: scaling the budget from 1 to $1+\epsilon$ raises the minimum of $\tfrac12$variance by about $\lambda\epsilon$.

### Worked examples
Uncorrelated assets with vols 10% / 20% → weights 0.8 / 0.2; 10% / 30% → 0.9 / 0.1: **inverse-variance**, not inverse-vol.

### Key points
- Uses no expected returns. Long-only: clip to [0,1] (the problem stays convex).

### Connections
- **Builds on:** [[portfolio-variance-diversification]].
- **Related:** [[mean-variance-optimization]], [[risk-budgeting]] (another μ-free construction).

<a id="mean-variance-optimization"></a>

## Mean–Variance Optimisation & Tangency Portfolio
<!-- section: mean-variance-optimization | prerequisites: [minimum-variance-portfolio, taylor-expansions] | related: [marginal-sharpe-improvement, risk-budgeting, ridge-regression, eigen-svd-psd, black-litterman, grinold-alpha] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-rbc-gam-quantdev-notes] | tags: [markowitz, tangency, max-sharpe, estimation-error] -->

Markowitz optimisation trades expected return against variance. Its solution is proportional to $\Sigma^{-1}\mu$, which also gives the maximum-Sharpe (tangency) portfolio — and which is very sensitive to errors in $\mu$ and $\Sigma$.

### Formulas
$$\max_w\ w^\top\mu-\tfrac\gamma2\,w^\top\Sigma w\ \Rightarrow\ w^*=\tfrac1\gamma\,\Sigma^{-1}\mu,\qquad SR_{\max}=\sqrt{\mu^\top\Sigma^{-1}\mu},\qquad w_T=\frac{\Sigma^{-1}\mu}{\mathbf 1^\top\Sigma^{-1}\mu}$$

**Variables:**

- $\mu$ expected **excess** returns
- $\Sigma$ covariance matrix
- $\gamma$ risk aversion
- $w^*$ optimal (unconstrained) weights
- $SR_{\max}$ highest attainable Sharpe ratio
- $w_T$ fully invested tangency portfolio (needs $\mathbf 1^\top\Sigma^{-1}\mu>0$)

### Deriving the first-order condition
The derivative is taken with respect to the **weight vector** $w$, the decision variable: differentiate with respect to each $w_i$ and stack the results.

| Expression | Gradient w.r.t. $w$ | Scalar analogue |
|---|---|---|
| $w^\top\mu$ | $\mu$ | $\frac{d}{dw}(w\mu)=\mu$ |
| $w^\top\Sigma w$ | $2\Sigma w$ ($\Sigma$ symmetric) | $\frac{d}{dw}(\sigma^2w^2)=2\sigma^2w$ |

$$\nabla_wU=\mu-\gamma\Sigma w=0\ \Rightarrow\ w^*=\tfrac1\gamma\Sigma^{-1}\mu,\qquad \nabla^2_wU=-\gamma\Sigma$$

**Variables:**

- $U(w)=w^\top\mu-\tfrac\gamma2w^\top\Sigma w$ the mean–variance objective
- $\nabla_wU$ gradient; $\nabla^2_wU$ Hessian (matrix of second derivatives)

**Why a maximum:** $\Sigma$ is positive definite, so the Hessian $-\gamma\Sigma$ is negative definite, $U$ is concave and the stationary point is the global maximum. **Two-asset check:** with $\Sigma=\mathrm{diag}(\sigma_1^2,\sigma_2^2)$, $w_i^*=\mu_i/(\gamma\sigma_i^2)$ — position ∝ return / **variance**.

### Why $SR_{\max}=\sqrt{\mu^\top\Sigma^{-1}\mu}$
**Plug in.** With $SR(w)=w^\top\mu/\sqrt{w^\top\Sigma w}$: numerator $w^{*\top}\mu=\tfrac1\gamma\mu^\top\Sigma^{-1}\mu$; denominator $\sqrt{w^{*\top}\Sigma w^*}=\tfrac1\gamma\sqrt{\mu^\top\Sigma^{-1}\mu}$. The ratio is $\sqrt{\mu^\top\Sigma^{-1}\mu}$; $\gamma$ cancels (risk aversion sets leverage, not Sharpe).

**Prove it is the maximum (Cauchy–Schwarz).**

$$a=\Sigma^{1/2}w,\quad b=\Sigma^{-1/2}\mu:\qquad w^\top\mu=a^\top b\le\lVert a\rVert\,\lVert b\rVert=\sqrt{w^\top\Sigma w}\,\sqrt{\mu^\top\Sigma^{-1}\mu}$$

**Variables:**

- $\Sigma^{1/2}$ matrix square root ($\Sigma^{1/2}\Sigma^{1/2}=\Sigma$)
- $a,b$ auxiliary vectors; $\lVert\cdot\rVert$ Euclidean norm

Dividing by $\sqrt{w^\top\Sigma w}$ gives $SR(w)\le\sqrt{\mu^\top\Sigma^{-1}\mu}$ for **every** $w$, with equality iff $a\propto b$, i.e. $w\propto\Sigma^{-1}\mu$.

**Uncorrelated assets:** $\mu^\top\Sigma^{-1}\mu=\sum_i(\mu_i/\sigma_i)^2$, so $SR_{\max}=\sqrt{\sum_iSR_i^2}$; two assets with SR 0.5 give $\sqrt{0.5}\approx0.707$, as in [[portfolio-variance-diversification]].

### Why the objective is $\mu-\tfrac\gamma2\sigma^2$: certainty equivalent
$$E[U(V)]\approx U(\mu)+\tfrac12U''(\mu)\,\sigma^2,\qquad U(CE)\approx U(\mu)+U'(\mu)(CE-\mu)\ \Rightarrow\ CE\approx\mu-\tfrac12A\sigma^2,\qquad A=-\frac{U''(\mu)}{U'(\mu)}$$

**Variables:**

- $V$ random end-of-period wealth, with mean $\mu$ and variance $\sigma^2$
- $U$ utility function; $U',U''$ its derivatives
- $CE$ certainty equivalent: the sure amount with the same expected utility
- $A$ Arrow–Pratt absolute risk aversion (plays the role of $\gamma$ in the objective)

→ The theoretical basis of the mean–variance objective is a second-order Taylor expansion of utility ([[taylor-expansions]]).

### Why optimised portfolios fail
- $\mu$ is noisy and $\Sigma$ unstable; $\Sigma^{-1}$ **amplifies errors** in small-eigenvalue directions ([[eigen-svd-psd]]) → extreme weights and turnover.
- **"MVO = error maximizer":** sample means are very noisy. With $Y$ years of data the standard error of an annualised mean is

$$SE(\hat\mu_{\text{ann}})\approx\frac{\sigma_{\text{ann}}}{\sqrt Y}=\frac{16\%}{\sqrt3}\approx9\%$$

**Variables:**

- $\hat\mu_{\text{ann}}$ estimated annual mean return
- $\sigma_{\text{ann}}$ annual volatility
- $Y$ years of data

**Notes:**

- Worked example (a 3-year sample in which the estimated means are far from the true ones and max-Sharpe goes 100% into one asset): [[matlab-portfolio-object]].
- Fixes: shrink means/covariance (cf. [[ridge-regression]]; covariance estimation in [[covariance-estimation]]), constraints (which act as shrinkage: [[constraints-shadow-prices]]), turnover penalties ([[transaction-costs-no-trade]]), comparison with equal-weight / min-var baselines, or skip $\mu$ entirely via [[risk-budgeting]] — or start from an equilibrium prior ([[black-litterman]]).

### Connections
- **Builds on:** [[minimum-variance-portfolio]], [[taylor-expansions]].
- **Inputs from:** [[grinold-alpha]]. **Stabilised by:** [[black-litterman]], [[ridge-regression]]-style shrinkage.

<a id="black-litterman"></a>

## Black–Litterman (equilibrium prior + views)
<!-- section: black-litterman | prerequisites: [mean-variance-optimization, conditional-probability-bayes] | related: [grinold-alpha, information-coefficient, risk-budgeting, beta-bernoulli-conjugacy] | sources: [src-quant-finance-study-notes] | tags: [black-litterman, bayesian, reverse-optimisation, views, idzorek] -->

**Problem:** Markowitz MVO is very sensitive to expected-return inputs → unstable, concentrated portfolios. Black–Litterman (Black & Litterman, Goldman Sachs, 1990–92) starts from the returns implied by market equilibrium and tilts them toward the investor's views in proportion to confidence.

### Step 1: prior (implied equilibrium returns)
$$\Pi=\gamma\,\Sigma\,w_{mkt}$$

**Variables:**

- $\Pi$ implied excess returns (reverse optimisation of the MVO solution)
- $\gamma$ risk aversion (written $\delta$ in the Black–Litterman literature; often calibrated from the market Sharpe ratio)
- $\Sigma$ covariance matrix
- $w_{mkt}$ market-cap (or benchmark) weights

### Step 2: views
$$P\mu=Q+\varepsilon,\qquad \varepsilon\sim N(0,\Omega)$$

**Variables:**

- $\mu$ unknown expected excess returns
- $P$ pick matrix ($k$ views × $n$ assets): an absolute view has one 1 in its row; a relative view has +1 / −1
- $Q$ view returns ($k\times1$)
- $\varepsilon$ view error
- $\Omega$ view uncertainty (diagonal)

### Step 3: posterior
$$E[R]=\big[(\tau\Sigma)^{-1}+P^\top\Omega^{-1}P\big]^{-1}\big[(\tau\Sigma)^{-1}\Pi+P^\top\Omega^{-1}Q\big],\qquad M=\big[(\tau\Sigma)^{-1}+P^\top\Omega^{-1}P\big]^{-1}$$

**Variables:**

- $E[R]$ posterior expected excess returns
- $\tau$ scalar uncertainty of the prior (commonly 0.025–0.05)
- $M$ posterior uncertainty of the mean; the covariance used for optimisation is $\Sigma+M$

### Step 4: optimise
Feed $E[R]$ and $\Sigma+M$ into MVO. **No views → the market portfolio.** The portfolio tilts only where there are views, sized by confidence.

### Idzorek-style confidence mapping
$$\Omega_{ii}=\Big(\frac1{c_i}-1\Big)\,\tau\,P_i\Sigma P_i^\top$$

**Variables:**

- $c_i\in(0,1)$ confidence in view $i$: higher $c_i$ → smaller $\Omega_{ii}$ → the view dominates
- $P_i$ row $i$ of the pick matrix

**Interview answer:** "Start with the market's wisdom, then tilt where you have an edge, in proportion to your confidence."

### Worked example (production run, code actually run)
Code (`black_litterman.py`): `View` and `BlackLittermanModel` dataclasses, Idzorek Ω, posterior mean and covariance, an SLSQP optimiser with weight bounds, a budget constraint and a tracking-error constraint.

**Universe:** US_EQ, EU_EQ, EM_EQ, US_GOVT, US_IG, US_HY, CMDTY, GOLD; benchmark 35/20/10/15/8/4/5/3; $\gamma$ = 2.5, $\tau$ = 0.05; bounds [−5%, 60%]; tracking error ≤ 4%.

| View | P | Q | Confidence |
|---|---|---|---|
| US equities beat EU by 4% | US_EQ − EU_EQ | +4% | 0.75 |
| EM equities return 12% | EM_EQ | 12% | 0.40 |
| IG underperforms UST by 2% | US_IG − US_GOVT | −2% | 0.60 |
| Gold beats commodities by 5% | GOLD − CMDTY | +5% | 0.50 |

| Asset | Benchmark | Optimal | Active | Implied Π | Posterior | Tilt |
|---|---|---|---|---|---|---|
| US_EQ | 0.35 | 0.470 | +0.120 | 3.93% | 2.87% | −1.06% |
| EU_EQ | 0.20 | −0.050 | −0.250 | 3.88% | 0.10% | −3.78% |
| EM_EQ | 0.10 | 0.222 | +0.122 | 4.14% | 3.81% | −0.33% |
| US_GOVT | 0.15 | 0.267 | +0.117 | −0.12% | 0.55% | +0.67% |
| US_IG | 0.08 | −0.050 | −0.130 | 0.87% | 0.01% | −0.86% |
| US_HY | 0.04 | −0.050 | −0.090 | 2.32% | 0.06% | −2.26% |
| CMDTY | 0.05 | −0.050 | −0.100 | 1.76% | −0.18% | −1.94% |
| GOLD | 0.03 | 0.241 | +0.211 | 0.41% | 1.90% | +1.48% |

Realised tracking error = 4.00% (the constraint binds).

**Observation from the run (自己推理):** the bullish absolute EM view (12% vs a 4.1% prior) did **not** raise EM's posterior (it fell to 3.8%). The high-confidence US − EU view pulls EU's return down, and because EM is highly correlated with EU in $\Sigma$, EM is dragged down too; the low-confidence (0.40) EM view can't offset that. In BL, views propagate through $\Sigma$, so a view on one asset moves correlated assets as well. Always check the posterior implied view $P\,E[R]$ against $Q$ (here: US−EU 2.8% vs 4%; EM 3.8% vs 12%; IG−UST −0.5% vs −2%; Gold−Cmdty 2.1% vs 5%).

### What production adds
- **Covariance:** factor risk model (Barra / Axioma / internal), Ledoit–Wolf shrinkage, mixed frequencies, calendar alignment.
- **Views:** generated systematically from signals (momentum, carry, valuation z-scores); confidence mapped from the signal's historical **IC** ([[information-coefficient]], [[grinold-alpha]]).
- **Risk:** turnover penalties vs the current book, factor exposure limits (beta, duration, spread duration), liquidity tiers, stress tests.
- **Loop:** scheduled rebalance (daily/weekly) → refreshed views → optimiser → OMS.

### Connections
- **Builds on:** [[mean-variance-optimization]] (reverse optimisation), [[conditional-probability-bayes]] (prior × views → posterior; the same shrinkage idea as [[beta-bernoulli-conjugacy]]).
- **Front end:** [[grinold-alpha]] turns signals into the view returns $Q$.

<a id="constraints-shadow-prices"></a>

## Constraints as Regularisation & Shadow Prices
<!-- section: constraints-shadow-prices | prerequisites: [lagrange-kkt-duality, minimum-variance-portfolio, mean-variance-optimization] | related: [optimiser-infeasibility, ridge-regression, lasso-elastic-net, risk-measures, covariance-estimation] | sources: [src-portopt-pm-interview] | tags: [constraints, jagannathan-ma, shadow-price, regularisation] -->

A constraint can only lower the in-sample optimum, yet it often improves out-of-sample performance: the inputs ($\mu$, $\Sigma$) are noisy, the unconstrained solution turns the noise into extreme positions, and the constraint cuts them off — it regularises. The constraint's multiplier (shadow price) says what it costs.

### Jagannathan & Ma (2003): no short sales = covariance shrinkage
$$\min_w\ \tfrac12w^\top\Sigma w\ \ \text{s.t.}\ \ \mathbf 1^\top w=1,\ w\ge0;\qquad \text{KKT: }\ \Sigma w=\lambda\mathbf 1+\delta,\quad \delta\ge0,\quad \delta_iw_i=0$$

**Variables:**

- $w$ weights; $\Sigma$ covariance matrix; $\mathbf 1$ vector of ones
- $\lambda$ multiplier on the budget constraint
- $\delta$ $N\times1$ multipliers on $w\ge0$; $\delta_i>0$ means asset $i$ "wanted to be shorted but is stuck at 0"
- $\delta_iw_i=0$ complementary slackness ([[lagrange-kkt-duality]])

**Key step:**

$$\tilde\Sigma=\Sigma-(\delta\mathbf 1^\top+\mathbf 1\delta^\top):\qquad \tilde\Sigma w=\Sigma w-\delta(\mathbf 1^\top w)-\mathbf 1(\delta^\top w)=\Sigma w-\delta-0=\lambda\mathbf 1$$

**Variables:**

- $\tilde\Sigma$ modified covariance matrix
- uses $\mathbf 1^\top w=1$ and $\delta^\top w=0$ (complementary slackness)

So **the constrained solution is the unconstrained minimum-variance solution computed with $\tilde\Sigma$** ([[minimum-variance-portfolio]]).

**Reading it:**

- An asset the optimiser wants to short usually has high estimated covariances with the others. The constraint lowers each of its covariances by $\delta_i$ (its variance by $2\delta_i$) — shrinking covariances that were probably overestimated.
- Likewise an upper bound raises the covariances of assets the optimiser "wanted to buy too much of".
- One-line answer: *"A long-only constraint acts like covariance shrinkage: it shrinks the covariances of the assets the optimiser wanted to short, which are likely overestimated."*

### Shadow prices
$$\text{shadow price}_j=\frac{\partial U^*}{\partial c_j}$$

**Variables:**

- $U^*$ optimal objective value
- $c_j$ bound of constraint $j$ (e.g. a 10% sector cap)

**Uses:**

1. **Negotiating with risk:** "raising the sector cap from 10% to 11% adds $x$ bp of expected alpha a year" is a quantified business case.
2. **Finding the expensive constraints:** most constraints have shadow prices near 0 (not binding); only the few expensive ones are worth discussing.
3. **TE constraint (自己推理; standard result):** in $\max\alpha^\top w$ s.t. $TE\le TE_{\max}$, the optimum is $\alpha^*=TE_{\max}\cdot IR^*$ with $IR^*=\sqrt{\alpha^\top\Sigma^{-1}\alpha}$, so the TE constraint's shadow price is $IR^*$: each extra 1% of risk budget buys $IR^*\times1\%$ of alpha ([[mandate-tracking-error]]).

**Variables (point 3):** $\alpha$ active-return forecasts; $TE_{\max}$ tracking-error budget; $IR^*$ optimal information ratio.

### Other "constraint = regularisation" equivalences

| Constraint | Equivalent regularisation | Effect |
|---|---|---|
| Long-only / position caps | Covariance shrinkage (Jagannathan–Ma) | Cuts off extreme positions |
| Gross cap $\lVert w\rVert_1\le g$ | Lasso / L1 ([[lasso-elastic-net]]) | Sparse, concentrated in a few assets |
| $\lVert w\rVert_2^2\le k$ | Ridge / L2 ([[ridge-regression]]) | Spreads weights out, toward 1/N |

**References:**

- Jagannathan, R. & Ma, T. (2003), *Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps*, Journal of Finance (cited from memory — verify).
- DeMiguel, Garlappi, Nogales & Uppal (2009), norm-constrained portfolios, *Management Science* (cited from memory — verify).

### Connections
- **Builds on:** [[lagrange-kkt-duality]], [[minimum-variance-portfolio]], [[mean-variance-optimization]] (why unconstrained MVO is fragile).
- **Related:** [[ridge-regression]], [[lasso-elastic-net]], [[covariance-estimation]] (shrinkage done directly), [[optimiser-infeasibility]] (when constraints conflict).

<a id="optimiser-infeasibility"></a>

## Infeasible & Unbounded: Debugging the Optimiser
<!-- section: optimiser-infeasibility | prerequisites: [lagrange-kkt-duality, constraints-shadow-prices] | related: [eigen-svd-psd, exposure-neutrality, matlab-custom-portfolio-optimization, transaction-costs-no-trade, covariance-estimation] | sources: [src-portopt-pm-interview] | tags: [infeasibility, iis, phase-1, solver-status, production] -->

"Infeasible" means the feasible set is empty: no $w$ satisfies all constraints at once (no point is primal feasible, [[lagrange-kkt-duality]]). Debug it by checking the current portfolio, then the data, then asking the solver which constraints conflict; in production, design the constraints so the optimiser can never return infeasible.

### Solver statuses

| Status | Meaning | Typical portfolio cause |
|---|---|---|
| **Primal infeasible** | No portfolio satisfies all constraints | Conflicting caps; overnight drift + turnover cap |
| **Dual infeasible** | For a convex problem whose constraints can be met, the primal is **unbounded** | $\Sigma$ singular or not PSD ([[covariance-estimation]], [[eigen-svd-psd]]) and no leverage/gross limit → infinite leverage on a "riskless" portfolio |
| **Numerical issue** | Numerical trouble | $\Sigma$ not PSD, badly scaled inputs |
| **Optimal** | Primal and dual feasible, duality gap ≈ 0 | Normal |

MOSEK reports these names and can return a Farkas-type certificate for each infeasibility.

### Common causes (ordering by frequency is 自己推理)

1. **Directly contradictory constraints.** Long-only ($w\ge0$) + dollar-neutral ($\mathbf 1^\top w=0$) leaves only $w=0$; add gross = 200% and it is infeasible. Fully invested ($\mathbf 1^\top w=1$) + dollar-neutral is a direct contradiction ([[exposure-neutrality]]).
2. **Bounds that don't add up.** 20 names capped at 4% each: $20\times4\%=80\%<100\%$ fully invested. Sector minimums summing to more than 100%. A liquidity screen halves the universe and yesterday's feasible constraints fail — the most common "infeasible as of today" case.
3. **Current holdings violate a constraint + turnover cap (most common in production).** A stock rallies overnight from 4.8% to 6% against a 5% cap, while the turnover cap is 1% or its liquidity limit allows selling only 0.5%: it cannot get back inside the limit in one step.
4. **Data or unit errors.** A cap written as `5` instead of `0.05`; bp mixed with decimals; NaN betas or covariances; ADV = 0 forcing $w_i=0$ on a held name; an inequality written the wrong way round.
5. **Constraints too tight.** TE ≤ 0.5% while the benchmark contains restricted names; beta, size, value, momentum and sector neutrality at once with too few names (not enough degrees of freedom).
6. **Integer constraints.** Minimum trade sizes and round lots make it a mixed-integer programme (MIP), where feasibility is harder.

### Debugging steps
1. **Check whether the current portfolio $w_0$ satisfies every constraint** — if not, cause 3 is likely.
2. **Check the inputs:** NaNs, units, whether $\Sigma$ is PSD (smallest eigenvalue, [[eigen-svd-psd]]), whether today's universe changed.
3. **Ask the solver for the conflicting subset:** Gurobi `computeIIS()` (Irreducible Infeasible Subsystem, the smallest conflicting set), CPLEX conflict refiner, MOSEK infeasibility certificate.
4. **Phase-1 / slack method:**

$$\min_{w,s}\ \mathbf 1^\top s\quad\text{s.t.}\quad Aw\le c+s,\ \ s\ge0$$

**Variables:**

- $A,c$ linear constraint matrix and bound vector
- $s$ slack variables, one per constraint
- $\mathbf 1$ vector of ones

Constraints with $s_j>0$ are the conflicting ones; $s_j$ is how much each must be relaxed.

5. **Crude but effective:** drop constraints one at a time (or by bisection) until the problem is feasible.

### Production design
- **Tier the constraints.** Hard (regulatory, leverage, restricted list) must hold; soft (sector deviations, factor exposures, turnover) go into the objective as large penalties, $\text{penalty}\times\max(0,\text{violation})$, and can never cause infeasibility.
- **Constrain trades, not states.** A position already over its limit may "move in the compliant direction" instead of being forced into compliance in one step.
- **Fallback.** Never fail silently: alert, then run a reduce-risk-only trade or hold.

**Interview answer:** *"First I check whether the current portfolio is itself feasible, because overnight drift plus a turnover cap is the most common cause. Then data and units. Then I ask the solver for an IIS or run a slack phase-1 to see which constraints conflict. Long term, I make the non-regulatory constraints soft penalties so the optimiser can never return infeasible."*

### Connections
- **Builds on:** [[lagrange-kkt-duality]] (primal/dual feasibility), [[constraints-shadow-prices]].
- **Related:** [[eigen-svd-psd]], [[covariance-estimation]] (unbounded problems), [[matlab-custom-portfolio-optimization]] (explicit QP is easier to debug), [[transaction-costs-no-trade]] (turnover limits).
