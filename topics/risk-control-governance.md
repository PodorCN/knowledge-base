---
id: risk-control-governance
title: "Risk Control"
type: topic
domain: risk-management
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-vol-surface-exotics-notes, src-rbc-gam-quantdev-notes]
---
# Risk Control

Beyond the Greeks of individual positions, a desk measures risk by full revaluation under scenarios, summarises tail risk with drawdown, VaR and expected shortfall, and controls the risk that the model itself is wrong.

**Prerequisites:** [[greeks]], [[sharpe-ratio]], [[autocallables]], [[call-spread-overhedge]].

**Leads to:** [[pricing-app-architecture]], [[model-release-regression-testing]].

**Sections:** [[scenario-risk-grids]] · [[risk-measures]] · [[model-risk-governance]]

<a id="scenario-risk-grids"></a>

## Scenario & Risk Grids
<!-- section: scenario-risk-grids | prerequisites: [greeks] | related: [dotnet-concurrency-wpf, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [scenarios, stress] -->

Greeks are local. Revaluing the whole book under a grid of market moves captures the non-linearity they miss.

### Standard scenarios
- Spot ladder (±1%, ±5%, ±20%)
- Vol bumps (parallel, skew tilt, term structure)
- Spot × vol grid
- Time roll (tomorrow, next week)
- Dividend & borrow bumps
- Correlation bumps for baskets

### Key points
- Full revaluation captures non-linearity that [[greeks]] miss.

### Connections
- **Builds on:** [[greeks]]. **Implemented in:** [[dotnet-concurrency-wpf]] (responsive grids), [[pricing-app-architecture]].

<a id="risk-measures"></a>

## Drawdown, VaR, Expected Shortfall, Information Ratio
<!-- section: risk-measures | prerequisites: [sharpe-ratio, normal-distribution] | related: [win-rate-expectancy, information-ratio] | sources: [src-squarepoint-dqa-workbook, src-rbc-gam-quantdev-notes] | tags: [var, es, drawdown, tracking-error] -->

The Sharpe ratio summarises only the mean and standard deviation. Tail risk, path drawdown, benchmark-relative performance, and coherent capital allocation require dedicated risk measures.

### Formulas
$$MDD=\max_t\Big(1-\frac{V_t}{\max_{s\le t}V_s}\Big),\qquad TE=\sigma(R-R_b)$$
$$VaR_\alpha(L)=\inf\{x\in\mathbb R : P(L\le x)\ge\alpha\},\qquad ES_\alpha(L)=E[L\mid L\ge VaR_\alpha(L)]=\frac{1}{1-\alpha}\int_\alpha^1 VaR_u(L)\,du$$
$$\text{Gaussian loss }L\sim N(\mu_L,\sigma_L^2):\quad VaR_\alpha(L)=\mu_L+\sigma_L z_\alpha,\qquad ES_\alpha(L)=\mu_L+\sigma_L\frac{\phi(z_\alpha)}{1-\alpha}$$

**Variables:**

- $MDD$ maximum drawdown over the sample horizon
- $V_t, V_s$ portfolio wealth at times $t$ and $s\le t$
- $R, R_b$ portfolio return and benchmark return
- $TE$ tracking error (active risk), the denominator of the information ratio ([[information-ratio]])
- $L$ portfolio loss over the risk horizon ($L = -\Delta V$)
- $\alpha\in(0,1)$ confidence level (e.g. $\alpha = 0.99$ for 99% VaR or $\alpha = 0.975$ for FRTB 97.5% ES)
- $VaR_\alpha(L), ES_\alpha(L)$ Value at Risk and Expected Shortfall (Conditional VaR / CVaR) at confidence $\alpha$
- $x, u$ loss threshold level and quantile integration variable
- $\mu_L, \sigma_L$ mean and standard deviation of loss $L$
- $z_\alpha = \Phi^{-1}(\alpha)$ standard normal $\alpha$-quantile ($\Phi$: standard normal CDF; $\phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$: standard normal PDF)

### Coherent risk measures (Artzner et al. 1999)

A risk measure $\rho(L)$ mapping loss $L$ to required capital is **coherent** if it satisfies four axioms for any losses $L, L_1, L_2$, constant $c\in\mathbb R$, and scalar $\lambda > 0$:

1. **Monotonicity:** $L_1 \le L_2$ a.s. $\Rightarrow \rho(L_1) \le \rho(L_2)$ (larger loss requires more capital).
2. **Translation invariance (cash additivity):** $\rho(L + c) = \rho(L) + c$ (adding deterministic loss $c$ increases capital by $c$).
3. **Positive homogeneity:** $\rho(\lambda L) = \lambda\,\rho(L)$ for $\lambda > 0$ (scaling a position scales risk linearly).
4. **Subadditivity (diversification):** $\rho(L_1 + L_2) \le \rho(L_1) + \rho(L_2)$ (merging two books never increases total required capital).

**Variables:**

- $\rho(\cdot)$ risk measure mapping a random loss to a capital figure
- $L_1, L_2$ loss random variables of two positions or sub-portfolios
- $c$ deterministic cash loss shift
- $\lambda > 0$ positive position scaling factor

### Key points
- **VaR vs Expected Shortfall (interview classic):**
  - **Tail blindness:** $VaR_\alpha$ is a single quantile — it tells you the threshold exceeded with probability $1-\alpha$, but nothing about *how catastrophic* the loss is when that threshold is breached. $ES_\alpha$ averages all losses in the $(1-\alpha)$ tail.
  - **Failure of subadditivity:** $VaR_\alpha$ is **not coherent** because it can violate subadditivity for skewed/credit/digital payoffs (unless returns are jointly elliptical, where VaR *is* subadditive). **Counterexample:** Two independent defaultable bonds each lose $\$100$ with probability $0.8\%$ and $\$0$ with probability $99.2\%$. At $\alpha=99\%$, each individual bond has $VaR_{0.99}(L_1)=VaR_{0.99}(L_2)=0$, but the combined portfolio loses $\ge \$100$ with probability $1 - 0.992^2 = 1.594\% > 1\%$, so $VaR_{0.99}(L_1+L_2)=100 > 0+0$. Expected Shortfall $ES_\alpha$ is **always coherent**.
  - **Basel FRTB:** Replaced 99% VaR with **97.5% Expected Shortfall** (under Gaussian losses, $\phi(z_{0.975})/(1-0.975) \approx 2.338 \approx z_{0.99} = 2.326$, giving nearly identical capital for normal tails while penalising fat tails).
- **Parametric vs Historical vs Monte Carlo VaR:** Parametric ($\mu_L+\sigma_L z_\alpha$) is fast and differentiable (marginal/component VaR $= (\Sigma w)_i / \sigma_p \cdot z_\alpha$) but misses fat tails and option non-linearity; Historical Simulation preserves empirical fat tails and cross-asset dependence without distributional assumptions but is bounded by past window size; Monte Carlo handles full option revaluation (delta-gamma or full grid) at higher compute cost.
- **Max drawdown in pandas:** `wealth = (1 + rets).cumprod()`, then `(wealth / wealth.cummax() - 1).min()`.

### Connections
- **Builds on:** [[sharpe-ratio]], [[normal-distribution]]. **Related:** [[win-rate-expectancy]].

<a id="model-risk-governance"></a>

## Model Risk, Reserves & Governance
<!-- section: model-risk-governance | prerequisites: [call-spread-overhedge] | related: [pricing-app-architecture, model-release-regression-testing, autocallables, vol-surface-construction, barrier-options] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [model-risk, osfi-e23, ipv, reserves] -->

**Model risk:** the wrong model, a wrong implementation, or use outside the validated range. It is controlled by governance, reserves and independent price verification.

### Key points
- **Controls:** only approved models per product; version tracking; input validation and warnings (arbitrage in the surface, extrapolated vol); an audit log; alignment with validation (Canada: **OSFI Guideline E-23**).
- **Reserves:** model reserve, barrier/digital overhedges ([[call-spread-overhedge]], [[barrier-options]]), correlation and dividend reserves ([[autocallables]]).
- **Independent price verification:** against consensus (S&P Global **Totem**: 150+ contributors, 10th/90th percentiles for prudent valuation); daily P&L explain ([[vol-surface-construction]]).

### Connections
- **Builds on:** [[call-spread-overhedge]].
- **Implemented through:** [[pricing-app-architecture]], [[model-release-regression-testing]].
