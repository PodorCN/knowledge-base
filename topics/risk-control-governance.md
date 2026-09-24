---
id: risk-control-governance
title: "Risk Control & Governance"
type: topic
domain: risk-management
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-vol-surface-exotics-notes]
---
# Risk Control & Governance

**Sections:** [[scenario-risk-grids]] · [[risk-measures]] · [[model-risk-governance]]

<a id="scenario-risk-grids"></a>

## Scenario & Risk Grids
<!-- section: scenario-risk-grids | prerequisites: [greeks] | related: [dotnet-concurrency-wpf, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [scenarios, stress] -->

- Spot ladder (±1%, ±5%, ±20%)
- Vol bumps (parallel, skew tilt, term structure)
- Spot × vol grid
- Time roll (tomorrow, next week)
- Dividend & borrow bumps
- Correlation bumps for baskets

Full revaluation captures non-linearity that [[greeks]] miss.

<a id="risk-measures"></a>

## Drawdown, VaR, Expected Shortfall, Information Ratio
<!-- section: risk-measures | prerequisites: [sharpe-ratio] | related: [win-rate-expectancy] | sources: [src-squarepoint-dqa-workbook] | tags: [var, es, drawdown] -->

$$MDD=\max_t\Big(1-\frac{W_t}{\max_{s\le t}W_s}\Big),\quad VaR_\alpha=\alpha\text{-quantile of }L,\quad ES_\alpha=E[L\mid L\ge VaR_\alpha],\quad IR=\frac{E[R-R_b]}{\sigma(R-R_b)}$$

**Variables:**

- $W_t$ wealth
- $L$ loss
- $\alpha$ confidence level
- $R_b$ benchmark return (denominator = tracking error)

Sharpe only summarises mean & std; tails need these.

<a id="model-risk-governance"></a>

## Model Risk, Reserves & Governance
<!-- section: model-risk-governance | prerequisites: [pricing-app-architecture] | related: [model-release-regression-testing, call-spread-overhedge, autocallables, vol-surface-construction] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [model-risk, osfi-e23, ipv, reserves] -->

**Model risk:** wrong model, wrong implementation, or use outside validated range.

- Controls: only approved models per product; version tracking; input validation & warnings (arbitrage in surface, extrapolated vol); audit log; alignment with validation (Canada: **OSFI Guideline E-23**).
- **Reserves:** model reserve, barrier/digital overhedges, correlation and dividend reserves.
- **Independent price verification:** vs consensus (S&P Global **Totem**: 150+ contributors, 10th/90th percentiles for prudent valuation); daily P&L explain.
