---
id: risk-budgeting-position-sizing
title: "Risk Budgeting & Position Sizing"
type: topic
domain: portfolio-construction
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook]
---
# Risk Budgeting & Position Sizing

**Sections:** [[risk-contribution]] · [[risk-budgeting]] · [[signal-to-weight]]

<a id="risk-contribution"></a>

## Marginal & Component Risk Contribution
<!-- section: risk-contribution | prerequisites: [portfolio-variance-diversification] | related: [risk-budgeting, marginal-sharpe-improvement] | sources: [src-squarepoint-dqa-workbook, src-signal-to-weight] | tags: [euler, risk-decomposition] -->

$$\frac{\partial\sigma_p}{\partial w_i}=\frac{(\Sigma w)_i}{\sigma_p},\qquad RC_i=w_i\frac{(\Sigma w)_i}{\sigma_p},\qquad \sum_iRC_i=\sigma_p$$

**Variables:**

- $w$ weights
- $\Sigma$ covariance
- $\sigma_p=\sqrt{w^\top\Sigma w}$
- $RC_i$ component contribution (Euler decomposition, since $\sigma_p$ is homogeneous of degree 1)

Low standalone vol ≠ low marginal risk (correlation matters).

### Connections
- **Inverted to solve for weights in:** [[risk-budgeting]].

<a id="risk-budgeting"></a>

## Risk Budgeting (Bruder & Roncalli 2012)
<!-- section: risk-budgeting | prerequisites: [risk-contribution] | related: [signal-to-weight, mean-variance-optimization, minimum-variance-portfolio] | sources: [src-signal-to-weight] | tags: [risk-parity, erc, risk-budget] -->

$$RC_i(w)=w_i\frac{(\Sigma w)_i}{\sigma(w)}=TE_i\cdot\sigma(w)$$

**ρ = 0 closed form:** $w_i\propto\sqrt{TE_i}/\sigma_i$.

**Variables:**

- $w_i$ weight of asset $i$
- $\Sigma$ covariance
- $\sigma(w)$ portfolio vol
- $TE_i$ risk budget of asset $i$ (budgets sum to 1)
- $\sigma_i$ asset vol

### Key points
- The paper takes $TE_i$ as given; [[signal-to-weight]] shows how to feed a signal into $TE_i$.

**References:**

- Bruder, B. & Roncalli, T. (2012), *Managing Risk Exposures Using the Risk Budgeting Approach*.

### Connections
- **Builds on:** [[risk-contribution]] (turned around to solve for $w_i$).
- **Fed by:** [[signal-to-weight]].

<a id="signal-to-weight"></a>

## Signal-to-Weight Bridge (score → risk budget → weight)
<!-- section: signal-to-weight | prerequisites: [time-series-momentum, risk-budgeting] | related: [risk-contribution, portfolio-variance-diversification] | sources: [src-signal-to-weight] | tags: [position-sizing, risk-budget, vol-scaling] -->

$$\textbf{exact: } TE_i\propto s_i^2,\quad w_i=\mathrm{sign}(s_i)\frac{\sqrt{TE_i}}{\sigma_i}\propto\frac{s_i}{\sigma_i}\qquad\qquad \textbf{shortcut: } w_i=s_i\times\frac{TE_i}{\sigma_i}$$

**Variables:**

- $s_i$ clipped signal of asset $i$
- $TE_i$ risk budget
- $\sigma_i$ asset vol
- $w_i$ weight

### Exact vs shortcut
- **Exact** matches Bruder–Roncalli's ρ = 0 closed form ($w\propto\sqrt{TE}/\sigma$). Needs $TE\ge0$, hence $s^2$; `sign` restores direction. Risk used never exceeds the budget.
- **Shortcut** = (weight per unit conviction $TE_i/\sigma_i$) × conviction $s_i$. Risk used $w_i\sigma_i=s_iTE_i$ scales **linearly** with $s$: at full clip ($|s|=2$) you spend $2\times TE_i$. So $TE_i$ means "risk per 1σ of conviction", not a hard cap.

### Connections
- **Builds on:** [[time-series-momentum]] (the score), [[risk-budgeting]] (the budget→weight map).
