---
id: risk-control-governance
title: "Risk Control & Governance"
type: topic
domain: risk-management
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-vol-surface-exotics-notes, src-rbc-gam-quantdev-notes]
---
# Risk Control & Governance

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
<!-- section: risk-measures | prerequisites: [sharpe-ratio] | related: [win-rate-expectancy] | sources: [src-squarepoint-dqa-workbook, src-rbc-gam-quantdev-notes] | tags: [var, es, drawdown, tracking-error] -->

The Sharpe ratio summarises only the mean and standard deviation. Tails and path need their own measures.

### Formulas
$$MDD=\max_t\Big(1-\frac{V_t}{\max_{s\le t}V_s}\Big),\qquad VaR_\alpha=\alpha\text{-quantile of }L,\qquad ES_\alpha=E[L\mid L\ge VaR_\alpha],\qquad TE=\sigma(R-R_b),\qquad IR=\frac{E[R-R_b]}{TE}$$

**Variables:**

- $MDD$ maximum drawdown
- $V_t$ portfolio value (wealth) at $t$
- $L$ loss over the horizon
- $\alpha$ confidence level (e.g. 99%)
- $VaR_\alpha$ value at risk; $ES_\alpha$ expected shortfall
- $R$ portfolio return; $R_b$ benchmark return
- $TE$ tracking error
- $IR$ information ratio

**Max drawdown in pandas:** `wealth = (1 + rets).cumprod()`, then `(wealth / wealth.cummax() - 1).min()`.

### Connections
- **Builds on:** [[sharpe-ratio]]. **Related:** [[win-rate-expectancy]].

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
