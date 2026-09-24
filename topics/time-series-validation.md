---
id: time-series-validation
title: "Time Series & Validation"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook]
---
# Time Series & Validation

**Sections:** [[stationarity-ar1]] · [[effective-sample-size]] · [[cross-validation-leakage]]

<a id="stationarity-ar1"></a>

## Stationarity & AR(1)
<!-- section: stationarity-ar1 | prerequisites: [variance-covariance-correlation] | related: [effective-sample-size, robust-standard-errors, sharpe-ratio, markov-chains] | sources: [src-squarepoint-dqa-workbook] | tags: [time-series, random-walk, spurious-regression] -->

Weak stationarity: constant mean, finite constant variance, $\mathrm{Cov}(X_t,X_{t-k})=\gamma_k$ depends only on lag.
$$X_t=c+\varphi X_{t-1}+\varepsilon_t,\ |\varphi|<1:\quad E=\frac{c}{1-\varphi},\ \mathrm{Var}=\frac{\sigma_\varepsilon^2}{1-\varphi^2},\ \rho_k=\varphi^k$$

**Variables:**

- $c$ constant
- $\varphi$ AR coefficient
- $\varepsilon_t$ iid innovations (var $\sigma_\varepsilon^2$)
- $\rho_k=\gamma_k/\gamma_0$ autocorrelation

- $\varphi=1$: random walk, non-stationary → regressing unrelated price **levels** gives spurious "relationships".
- A stable-looking plot is not proof of stationarity.

### Connections
- **Consequences:** [[effective-sample-size]], [[robust-standard-errors]], Sharpe annualisation in [[sharpe-ratio]].

<a id="effective-sample-size"></a>

## Effective Sample Size under Autocorrelation
<!-- section: effective-sample-size | prerequisites: [stationarity-ar1, lln-clt] | related: [sharpe-ratio, regression-invariances, bootstrap] | sources: [src-squarepoint-dqa-workbook] | tags: [autocorrelation, standard-error] -->

$$\mathrm{Var}(\bar X)=\frac{\sigma^2}{n}\Big[1+2\sum_{k=1}^{n-1}\big(1-\tfrac kn\big)\rho_k\Big],\qquad n_{\text{eff}}\approx\frac{n}{1+2\sum_{k\ge1}\rho_k}\overset{AR(1)}{=}n\frac{1-\varphi}{1+\varphi}$$

**Variables:**

- $\rho_k$ lag-$k$ autocorrelation
- $\varphi$ AR(1) coefficient

- $\varphi=0.5$ → $n_{\text{eff}}\approx n/3$. Negative dependence can give $n_{\text{eff}}>n$.
- 1,000 stocks on one date ≠ 1,000 independent observations (common shock) → cluster / block.

### Connections
- **Applies to:** [[sharpe-ratio]] (autocorrelated returns), [[regression-invariances]] (duplicated rows), [[bootstrap]] (block version).

<a id="cross-validation-leakage"></a>

## Validation, Walk-Forward CV & Leakage
<!-- section: cross-validation-leakage | prerequisites: [bias-variance-tradeoff] | related: [backtest-pitfalls, stationarity-ar1, research-workflow] | sources: [src-squarepoint-dqa-workbook] | tags: [walk-forward, purging, leakage] -->

- **Train** fits params; **validation** picks hyper-params; **test** is touched once. Re-using the test set turns it into validation.
- Time series: **walk-forward** (train on past, test on next window, roll). **Purge / gap** overlapping label windows.

### Leakage checklist
- Random splits with overlapping labels.
- Training labels extending into the validation period.
- Standardising / selecting features using future data.
- Revised (not point-in-time) economic data.
- Trading at a close you couldn't have observed before deciding.

### Connections
- **Main cause of:** [[backtest-pitfalls]]. **Part of:** [[research-workflow]].
