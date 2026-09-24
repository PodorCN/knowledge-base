---
id: measuring-performance
title: "Measuring Performance"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook]
---
# Measuring Performance

**Sections:** [[sharpe-ratio]] · [[marginal-sharpe-improvement]] · [[exposure-neutrality]]

<a id="sharpe-ratio"></a>

## Sharpe Ratio (annualisation, leverage, pitfalls)
<!-- section: sharpe-ratio | prerequisites: [variance-covariance-correlation, returns-simple-log] | related: [hypothesis-testing, multiple-testing, stationarity-ar1, portfolio-variance-diversification, marginal-sharpe-improvement, risk-measures] | sources: [src-squarepoint-dqa-workbook] | tags: [sharpe, annualisation, performance] -->

$$SR=\frac{E[R-r_f]}{\sigma(R-r_f)},\qquad SR_T=\sqrt T\,SR_1,\qquad t=\sqrt n\,\widehat{SR}_{\text{period}}$$
$$\mathrm{Var}\Big(\sum_{t=1}^TZ_t\Big)=T\sigma^2+2\sum_{k=1}^{T-1}(T-k)\gamma_k$$

**Variables:**

- $Z=R-r_f$ excess return per period
- $T$ periods aggregated (e.g. 252 days)
- $n$ observations
- $\gamma_k$ autocovariance at lag $k$

### Key points
- Daily μ=0.1%, σ=2% → daily SR 0.05 → annual ≈ 0.794.
- $\sqrt T$ scaling needs **uncorrelated, stationary, summed** returns. Positive autocorrelation ⇒ naive annualisation **overstates** SR.
- **Leverage** $k>0$ leaves SR unchanged ($k\mu/k\sigma$) in frictionless world; raises drawdown / ruin risk.
- Daily SR 0.1 over 100 days → t = 1 even though annualised SR ≈ 1.59.
- High SR can mislead: few obs, selection, stale prices, short-option (negative skew) payoffs, ignored costs, regime change.

### Connections
- **Is a t-stat in disguise:** [[hypothesis-testing]]; inflated by [[multiple-testing]]; autocorrelation from [[stationarity-ar1]].
- **Portfolio:** [[portfolio-variance-diversification]], [[marginal-sharpe-improvement]]. **Beyond σ:** [[risk-measures]].

<a id="marginal-sharpe-improvement"></a>

## When a Lower-Sharpe Strategy Improves a Portfolio
<!-- section: marginal-sharpe-improvement | prerequisites: [sharpe-ratio, portfolio-variance-diversification] | related: [mean-variance-optimization, risk-contribution] | sources: [src-squarepoint-dqa-workbook] | tags: [marginal, correlation] -->

$$SR(\varepsilon)=\frac{\mu_P+\varepsilon\mu_A}{\sqrt{\sigma_P^2+2\varepsilon c+\varepsilon^2\sigma_A^2}},\qquad \frac{dSR}{d\varepsilon}\Big|_0>0\iff SR_A>\rho_{PA}\,SR_P$$

**Variables:**

- $P$ existing portfolio
- $A$ candidate strategy
- $\varepsilon$ small financed allocation
- $c=\mathrm{Cov}(P,A)$
- $\rho_{PA}$ correlation

Portfolio SR 1.2; new strategy SR 0.4, ρ=0.2 → $0.4>0.24$ ✓ adds value (locally, frictionless).

<a id="exposure-neutrality"></a>

## Gross/Net Exposure, Neutrality & Trading Costs
<!-- section: exposure-neutrality | prerequisites: [capm-alpha-beta] | related: [win-rate-expectancy] | sources: [src-squarepoint-dqa-workbook] | tags: [long-short, beta-neutral, bid-ask] -->

$$\text{Gross}=\sum_i|w_i|,\qquad \text{Net}=\sum_i w_i$$

**Variables:** $w_i$ portfolio weights.

- Dollar-neutral ≠ beta-neutral (long and short legs may have different betas); sector/style/nonlinear exposures can remain.
- Bid–ask spread: crossing costs half-spread vs mid. 1 bp = 0.0001.
