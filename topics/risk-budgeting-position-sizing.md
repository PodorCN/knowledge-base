---
id: risk-budgeting-position-sizing
title: "Risk Budgeting"
type: topic
domain: portfolio-construction
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook]
---
# Risk Budgeting

Instead of optimising noisy expected returns, a portfolio can be built by deciding how much risk each position may contribute. This chapter decomposes portfolio volatility into per-asset contributions, inverts that decomposition to solve for weights given risk budgets (Bruder & Roncalli), and connects a signal score to a risk budget and hence to a position size.

**Prerequisites:** [[portfolio-variance-diversification]], [[time-series-momentum]].

**Leads to:** [[fx-carry-spot-slide]] (risk parity across components); compare [[mean-variance-optimization]].

**Sections:** [[risk-contribution]] · [[risk-budgeting]] · [[signal-to-weight]]

<a id="risk-contribution"></a>

## Marginal & Component Risk Contribution
<!-- section: risk-contribution | prerequisites: [portfolio-variance-diversification] | related: [risk-budgeting, marginal-sharpe-improvement, ic-contribution] | sources: [src-squarepoint-dqa-workbook, src-signal-to-weight] | tags: [euler, risk-decomposition] -->

Because portfolio volatility is homogeneous of degree 1 in the weights, it splits exactly into one contribution per asset: weight × marginal risk (Euler decomposition).

### Formulas
$$\sigma_p=\sqrt{w^\top\Sigma w},\qquad \frac{\partial\sigma_p}{\partial w_i}=\frac{(\Sigma w)_i}{\sigma_p},\qquad RC_i=w_i\,\frac{(\Sigma w)_i}{\sigma_p},\qquad \sum_iRC_i=\sigma_p$$

**Variables:**

- $w$ weight vector; $w_i$ weight of asset $i$
- $\Sigma$ covariance matrix; $(\Sigma w)_i$ the $i$-th entry of $\Sigma w$
- $\sigma_p$ portfolio volatility
- $\partial\sigma_p/\partial w_i$ marginal risk contribution of asset $i$
- $RC_i$ component risk contribution of asset $i$

### Key points
- Low standalone vol ≠ low marginal risk: correlation matters.

### Connections
- **Builds on:** [[portfolio-variance-diversification]].
- **Inverted to solve for weights in:** [[risk-budgeting]]. **Same additive idea:** [[ic-contribution]].

<a id="risk-budgeting"></a>

## Risk Budgeting (Bruder & Roncalli 2012)
<!-- section: risk-budgeting | prerequisites: [risk-contribution] | related: [signal-to-weight, mean-variance-optimization, minimum-variance-portfolio] | sources: [src-signal-to-weight] | tags: [risk-parity, erc, risk-budget] -->

Risk budgeting fixes each asset's share of portfolio risk in advance and solves for the weights that deliver it. Equal budgets give risk parity (ERC).

### Formula
$$RC_i(w)=w_i\,\frac{(\Sigma w)_i}{\sigma(w)}=b_i\cdot\sigma(w),\qquad \sum_ib_i=1;\qquad \rho=0:\ \ w_i\propto\frac{\sqrt{b_i}}{\sigma_i}$$

**Variables:**

- $w_i$ weight of asset $i$
- $\Sigma$ covariance matrix
- $\sigma(w)$ portfolio volatility
- $RC_i(w)$ risk contribution of asset $i$ ([[risk-contribution]])
- $b_i$ risk budget of asset $i$ (budgets sum to 1)
- $\sigma_i$ volatility of asset $i$
- $\rho$ correlation between assets (the closed form holds for $\rho=0$)

### Key points
- The paper takes $b_i$ as given; [[signal-to-weight]] shows how to feed a signal into $b_i$.
- No expected returns are needed (compare [[mean-variance-optimization]] and [[minimum-variance-portfolio]]).

### When risk parity equals the max-Sharpe portfolio
The equal-risk-contribution (ERC) portfolio coincides with the tangency portfolio ([[mean-variance-optimization]]) when every asset has the **same Sharpe ratio** and all pairwise **correlations are equal**; with zero correlation it reduces to inverse-volatility weights. Risk parity is therefore an implicit bet that all assets have equal Sharpe — say this out loud in an interview.

**References:**

- Bruder, B. & Roncalli, T. (2012), *Managing Risk Exposures Using the Risk Budgeting Approach*.

### Connections
- **Builds on:** [[risk-contribution]] (turned around to solve for $w_i$).
- **Fed by:** [[signal-to-weight]].

<a id="signal-to-weight"></a>

## Signal-to-Weight Bridge (score → risk budget → weight)
<!-- section: signal-to-weight | prerequisites: [time-series-momentum, risk-budgeting] | related: [risk-contribution, portfolio-variance-diversification, grinold-alpha] | sources: [src-signal-to-weight] | tags: [position-sizing, risk-budget, vol-scaling] -->

A clipped signal score is mapped to a risk budget and then, via the $\rho=0$ risk-budgeting solution, to a signed weight. Two versions are used: an exact one and a linear shortcut.

### Formula
$$\textbf{exact: }\ b_i\propto s_i^2,\quad w_i=\mathrm{sign}(s_i)\,\frac{\sqrt{b_i}}{\sigma_i}\ \propto\ \frac{s_i}{\sigma_i}\qquad\qquad \textbf{shortcut: }\ w_i=s_i\times\frac{b_i}{\sigma_i}$$

**Variables:**

- $s_i$ clipped signal of asset $i$ (e.g. $s_t$ of [[time-series-momentum]])
- $b_i$ risk budget of asset $i$
- $\sigma_i$ volatility of asset $i$
- $w_i$ signed weight of asset $i$

### Exact vs shortcut
- **Exact** matches the Bruder–Roncalli $\rho=0$ closed form ($w\propto\sqrt b/\sigma$). It needs $b\ge0$, hence $s^2$; `sign` restores the direction. The risk used never exceeds the budget.
- **Shortcut** = (weight per unit of conviction, $b_i/\sigma_i$) × conviction $s_i$. The risk used, $w_i\sigma_i=s_ib_i$, scales **linearly** with $s$: at full clip ($|s|=2$) you spend $2\times b_i$. So $b_i$ means "risk per 1σ of conviction", not a hard cap.

### Connections
- **Builds on:** [[time-series-momentum]] (the score), [[risk-budgeting]] (the budget → weight map).
- **Same shape as:** [[grinold-alpha]] ($w\propto IC\cdot z/\sigma$).
