---
id: measuring-performance
title: "Performance"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook]
---
# Performance

Before building portfolios we need to measure them. This chapter covers the Sharpe ratio and its statistical pitfalls, why a high win rate says little about profitability, and how gross/net exposure and neutrality describe a long-short book.

**Prerequisites:** [[returns-simple-log]], [[variance-covariance-correlation]], [[hypothesis-testing]], [[stationarity-ar1]], [[capm-alpha-beta]].

**Leads to:** [[portfolio-variance-diversification]], [[marginal-sharpe-improvement]], [[risk-measures]] (tail measures beyond σ).

**Sections:** [[sharpe-ratio]] · [[win-rate-expectancy]] · [[exposure-neutrality]]

<a id="sharpe-ratio"></a>

## Sharpe Ratio (annualisation, leverage, pitfalls)
<!-- section: sharpe-ratio | prerequisites: [variance-covariance-correlation, returns-simple-log, hypothesis-testing] | related: [multiple-testing, stationarity-ar1, portfolio-variance-diversification, marginal-sharpe-improvement, risk-measures, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [sharpe, annualisation, performance] -->

The Sharpe ratio is mean excess return per unit of volatility. It scales with the square root of the horizon only when returns are uncorrelated, and its sample estimate is a t-statistic in disguise.

### Formulas
$$SR=\frac{E[R-r_f]}{\sigma(R-r_f)},\qquad SR_h=\sqrt h\,SR_1,\qquad t=\sqrt n\,\widehat{SR}_{\text{period}}$$
$$\mathrm{Var}\Big(\sum_{t=1}^hZ_t\Big)=h\,\sigma^2+2\sum_{k=1}^{h-1}(h-k)\,\gamma_k$$

**Variables:**

- $R$ strategy return per period; $r_f$ risk-free return per period
- $Z_t=R_t-r_{f,t}$ excess return in period $t$, with variance $\sigma^2$
- $SR_1$ one-period Sharpe ratio; $SR_h$ Sharpe ratio over $h$ periods
- $h$ number of periods aggregated (e.g. 252 days for annualising daily data)
- $n$ number of observations in the sample
- $\widehat{SR}_{\text{period}}$ estimated per-period Sharpe ratio
- $\gamma_k$ autocovariance of $Z$ at lag $k$

### Worked examples
- Daily $\mu$ = 0.1%, $\sigma$ = 2% → daily SR 0.05 → annual ≈ $0.05\sqrt{252}\approx0.794$.
- Daily SR 0.1 over 100 days → $t=\sqrt{100}\times0.1=1$, even though the annualised SR ≈ 1.59.

### Key points
- $\sqrt h$ scaling needs **uncorrelated, stationary, summed** returns. Positive autocorrelation makes the $\gamma_k$ terms positive, so naive annualisation **overstates** the SR ([[effective-sample-size]]).
- **Leverage** by $k>0$ leaves the SR unchanged ($k\mu/k\sigma$) in a frictionless world, but raises drawdown and ruin risk.
- A high SR can mislead: few observations, selection ([[multiple-testing]]), stale prices, short-option (negative-skew) payoffs, ignored costs, regime change.

### Connections
- **Is a t-stat in disguise:** [[hypothesis-testing]]; inflated by [[multiple-testing]]; autocorrelation from [[stationarity-ar1]].
- **Portfolio level:** [[portfolio-variance-diversification]], [[marginal-sharpe-improvement]]. **Beyond σ:** [[risk-measures]].

<a id="win-rate-expectancy"></a>

## Win Rate vs Expected Value
<!-- section: win-rate-expectancy | prerequisites: [expectation-linearity-indicators] | related: [risk-measures, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [expectancy] -->

The profitability of a trade depends on the sizes of wins and losses, not only on how often it wins.

### Formula
$$E[\Pi]=p\,g-(1-p)\,\ell-c$$

**Variables:**

- $E[\Pi]$ expected profit per trade
- $p$ probability of a win
- $g$ gain on a win
- $\ell$ loss on a loss
- $c$ cost per trade

### Worked example
90% win rate, +1 on wins and −20 on losses (no costs) → $0.9\times1-0.1\times20=0.9-2=-1.1$ per trade.

### Key points
- A high win rate ≠ positive expectation (typical of short-option strategies).

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Related:** [[sharpe-ratio]], [[risk-measures]].

<a id="exposure-neutrality"></a>

## Gross/Net Exposure, Neutrality & Trading Costs
<!-- section: exposure-neutrality | prerequisites: [capm-alpha-beta] | related: [win-rate-expectancy, relative-value-long-short] | sources: [src-squarepoint-dqa-workbook] | tags: [long-short, beta-neutral, bid-ask] -->

Gross exposure measures total capital at risk, net exposure the directional tilt. Being neutral in one sense (dollars) does not make a book neutral in another (beta, sector, style).

### Formulas
$$\text{Gross}=\sum_i|w_i|,\qquad \text{Net}=\sum_iw_i$$

**Variables:**

- $w_i$ portfolio weight of asset $i$ (negative for shorts)

### Key points
- Dollar-neutral ≠ beta-neutral (the long and short legs may have different betas); sector, style and nonlinear exposures can remain.
- Bid–ask spread: crossing costs the half-spread relative to the mid. 1 bp = 0.0001.

### Connections
- **Builds on:** [[capm-alpha-beta]].
- **Used by:** [[relative-value-long-short]] (beta-adjusted notionals).
