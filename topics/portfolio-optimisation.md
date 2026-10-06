---
id: portfolio-optimisation
title: "Portfolio Optimisation"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-rbc-gam-quantdev-notes]
---
# Portfolio Optimisation

This chapter builds portfolios from expected returns and covariances. It starts with portfolio variance and diversification, asks when adding a lower-Sharpe strategy still helps, derives the minimum-variance and mean–variance (tangency) portfolios, explains why optimised portfolios are fragile, and ends with Black–Litterman, which stabilises the optimiser with a Bayesian prior.

**Prerequisites:** [[variance-covariance-correlation]], [[eigen-svd-psd]], [[sharpe-ratio]], [[conditional-probability-bayes]], [[taylor-expansions]].

**Leads to:** [[risk-contribution]], [[risk-budgeting]]; alpha inputs come from [[grinold-alpha]].

**Sections:** [[portfolio-variance-diversification]] · [[marginal-sharpe-improvement]] · [[minimum-variance-portfolio]] · [[mean-variance-optimization]] · [[black-litterman]]

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

### Connections
- **Builds on:** [[sharpe-ratio]], [[portfolio-variance-diversification]].
- **Related:** [[mean-variance-optimization]] (the global version), [[risk-contribution]] (marginal risk).

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

### Worked examples
Uncorrelated assets with vols 10% / 20% → weights 0.8 / 0.2; 10% / 30% → 0.9 / 0.1: **inverse-variance**, not inverse-vol.

### Key points
- Uses no expected returns. Long-only: clip to [0,1] (the problem stays convex).

### Connections
- **Builds on:** [[portfolio-variance-diversification]].
- **Related:** [[mean-variance-optimization]], [[risk-budgeting]] (another μ-free construction).

<a id="mean-variance-optimization"></a>

## Mean–Variance Optimisation & Tangency Portfolio
<!-- section: mean-variance-optimization | prerequisites: [minimum-variance-portfolio, taylor-expansions] | related: [marginal-sharpe-improvement, risk-budgeting, ridge-regression, eigen-svd-psd, black-litterman, grinold-alpha, equal-weight-estimation-error] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-rbc-gam-quantdev-notes] | tags: [markowitz, tangency, max-sharpe, estimation-error] -->

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
- Fixes: shrink means/covariance (cf. [[ridge-regression]]), constraints, turnover penalties, comparison with equal-weight / min-var baselines ([[equal-weight-estimation-error]]), or skip $\mu$ entirely via [[risk-budgeting]] — or start from an equilibrium prior ([[black-litterman]]).

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
