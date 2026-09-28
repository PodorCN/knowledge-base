---
id: portfolio-optimisation
title: "Portfolio Optimisation"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Portfolio Optimisation

**Sections:** [[portfolio-variance-diversification]] · [[minimum-variance-portfolio]] · [[mean-variance-optimization]] · [[black-litterman]]

<a id="portfolio-variance-diversification"></a>

## Portfolio Variance & Diversification
<!-- section: portfolio-variance-diversification | prerequisites: [variance-covariance-correlation] | related: [sharpe-ratio, minimum-variance-portfolio, risk-contribution, worst-of-correlation, pca] | sources: [src-squarepoint-dqa-workbook] | tags: [diversification, correlation] -->

$$\mu_p=w^\top\mu,\quad \sigma_p^2=w^\top\Sigma w,\quad \sigma_p^2=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\sigma_1\sigma_2$$
Two equal strategies: $\sigma_p=\sigma\sqrt{\tfrac{1+\rho}{2}}$, $SR_p=SR\sqrt{\tfrac{2}{1+\rho}}$. $n$ equicorrelated: $\sigma_p^2=\sigma^2\big[\rho+\tfrac{1-\rho}{n}\big]$.

**Variables:**

- $w$ weights
- $\mu$ expected excess returns
- $\Sigma$ covariance
- $\rho$ correlation
- $n$ assets

- SR 0.5, ρ=0 → 50/50 SR ≈ 0.707; ρ=1 → 0.5 (no benefit). 10 uncorrelated SR-0.5 → $0.5\sqrt{10}\approx1.58$.
- Positive common ρ leaves a **floor** $\rho\sigma^2$ as $n\to\infty$. Valid equicorrelation needs $\rho\ge-1/(n-1)$.
- Averaging Sharpes or adding σ's is wrong — use covariance.

### Connections
- **Leads to:** [[minimum-variance-portfolio]], [[mean-variance-optimization]], [[risk-contribution]].
- **Correlation as a traded risk:** [[worst-of-correlation]].

<a id="minimum-variance-portfolio"></a>

## Minimum-Variance Portfolio (2-asset & GMV)
<!-- section: minimum-variance-portfolio | prerequisites: [portfolio-variance-diversification] | related: [mean-variance-optimization, risk-budgeting] | sources: [src-squarepoint-dqa-workbook] | tags: [gmv, optimisation] -->

$$w_1^*=\frac{\sigma_2^2-\rho\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2},\qquad w_{GMV}=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^\top\Sigma^{-1}\mathbf 1},\qquad \sigma^2_{GMV}=\frac{1}{\mathbf 1^\top\Sigma^{-1}\mathbf 1}$$

**Variables:**

- $\sigma_1,\sigma_2$ vols
- $\rho$ correlation
- $\Sigma$ covariance (positive definite)
- $\mathbf 1$ vector of ones

- Uncorrelated 10% / 20% → 0.8 / 0.2; 10% / 30% → 0.9 / 0.1: **inverse-variance**, not inverse-vol.
- Uses no expected returns. Long-only: clip to [0,1] (convex problem).

<a id="mean-variance-optimization"></a>

## Mean–Variance Optimisation & Tangency Portfolio
<!-- section: mean-variance-optimization | prerequisites: [minimum-variance-portfolio] | related: [marginal-sharpe-improvement, risk-budgeting, ridge-regression, eigen-svd-psd, black-litterman, taylor-expansions] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [markowitz, tangency, max-sharpe, estimation-error] -->

$$\max_w\ w^\top\mu-\tfrac\gamma2w^\top\Sigma w\ \Rightarrow\ w^*=\tfrac1\gamma\Sigma^{-1}\mu,\qquad SR_{max}=\sqrt{\mu^\top\Sigma^{-1}\mu},\qquad w_T=\frac{\Sigma^{-1}\mu}{\mathbf 1^\top\Sigma^{-1}\mu}$$

**Variables:**

- $\mu$ expected **excess** returns
- $\Sigma$ covariance
- $\gamma$ risk aversion
- $w_T$ fully invested tangency portfolio (needs $\mathbf 1^\top\Sigma^{-1}\mu>0$)

### Why the objective is $\mu-\tfrac\gamma2\sigma^2$: certainty equivalent
$$E[U(W)]\approx U(\mu)+\tfrac12U''(\mu)\sigma^2,\qquad U(CE)\approx U(\mu)+U'(\mu)(CE-\mu)\ \Rightarrow\ CE\approx\mu-\tfrac12A\sigma^2,\qquad A=-\frac{U''(\mu)}{U'(\mu)}$$

**Variables:**

- $W$ random wealth; $\mu,\sigma^2$ its mean and variance
- $CE$ certainty equivalent
- $A$ Arrow–Pratt absolute risk aversion

→ the theoretical basis of the mean–variance objective (second-order Taylor, [[taylor-expansions]]).

### Why optimised portfolios fail
- μ is noisy, Σ unstable; $\Sigma^{-1}$ **amplifies errors** in small-eigenvalue directions ([[eigen-svd-psd]]) → extreme weights, turnover.
- Fixes: shrink means/covariance (cf. [[ridge-regression]]), constraints, turnover penalties, compare with equal-weight / min-var baselines, or skip μ entirely via [[risk-budgeting]].

<a id="black-litterman"></a>

## Black–Litterman (equilibrium prior + views)
<!-- section: black-litterman | prerequisites: [mean-variance-optimization, conditional-probability-bayes] | related: [grinold-alpha, information-coefficient, risk-budgeting, beta-bernoulli-conjugacy] | sources: [src-quant-finance-study-notes] | tags: [black-litterman, bayesian, reverse-optimisation, views, idzorek] -->

**Problem:** Markowitz MVO is very sensitive to expected-return inputs → unstable, concentrated portfolios. BL (Black & Litterman, Goldman Sachs, 1990–92) starts from equilibrium and tilts toward views in proportion to confidence.

### Step 1: prior (implied equilibrium returns)
$$\Pi=\delta\,\Sigma\,w_{mkt}$$

**Variables:**

- $\Pi$ implied excess returns
- $\delta$ risk aversion (often calibrated from the market Sharpe ratio)
- $\Sigma$ covariance matrix
- $w_{mkt}$ market-cap (or benchmark) weights

### Step 2: views
$$P\mu=Q+\varepsilon,\qquad \varepsilon\sim N(0,\Omega)$$

**Variables:**

- $P$ pick matrix ($k$ views × $n$ assets); absolute view → one 1; relative view → +1 / −1
- $Q$ view returns ($k\times1$)
- $\Omega$ view uncertainty (diagonal)

### Step 3: posterior
$$E[R]=\big[(\tau\Sigma)^{-1}+P^\top\Omega^{-1}P\big]^{-1}\big[(\tau\Sigma)^{-1}\Pi+P^\top\Omega^{-1}Q\big],\qquad M=\big[(\tau\Sigma)^{-1}+P^\top\Omega^{-1}P\big]^{-1}$$

**Variables:**

- $\tau$ scalar uncertainty of the prior (commonly 0.025–0.05)
- $M$ posterior uncertainty of the mean; covariance used for optimisation $=\Sigma+M$

### Step 4: optimise
Feed $E[R]$ and $\Sigma+M$ into MVO. **No views → market portfolio.** Tilts only where you have views, sized by confidence.

### Idzorek-style confidence mapping
$$\Omega_{ii}=\Big(\frac1{c_i}-1\Big)\tau\,P_i\Sigma P_i^\top$$

**Variables:**

- $c_i\in(0,1)$ confidence in view $i$ → higher $c$ → smaller $\Omega_{ii}$ → the view dominates
- $P_i$ row $i$ of the pick matrix

**One-liner:** "Start with the market's wisdom, then tilt where you have an edge, in proportion to your confidence."

### Production run (code actually run)
Code (`black_litterman.py`): `View` and `BlackLittermanModel` dataclasses, Idzorek Ω, posterior mean/covariance, SLSQP optimiser with weight bounds, a budget constraint and a tracking-error constraint.

**Universe:** US_EQ, EU_EQ, EM_EQ, US_GOVT, US_IG, US_HY, CMDTY, GOLD; benchmark 35/20/10/15/8/4/5/3; δ = 2.5, τ = 0.05; bounds [−5%, 60%]; TE ≤ 4%.

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

Realised TE = 4.00% (constraint binding).

**Observation from the run (自己推理):** the bullish absolute EM view (12% vs a 4.1% prior) did **not** raise EM's posterior (it fell to 3.8%). The high-confidence US − EU view pulls EU's return down, and because EM is highly correlated with EU in Σ, EM gets dragged down too; the low-confidence (0.40) EM view can't offset that. In BL, views propagate through Σ, so a view on one asset moves correlated assets as well. Always check the posterior implied view $P\,E[R]$ against $Q$ (here: US−EU 2.8% vs 4%; EM 3.8% vs 12%; IG−UST −0.5% vs −2%; Gold−Cmdty 2.1% vs 5%).

### What production adds
- **Covariance:** factor risk model (Barra / Axioma / internal), Ledoit–Wolf shrinkage, mixed frequencies, calendar alignment.
- **Views:** generated systematically from signals (momentum, carry, valuation z-scores); confidence mapped from the signal's historical **IC** ([[information-coefficient]], [[grinold-alpha]]).
- **Risk:** turnover penalties vs the current book, factor exposure limits (beta, duration, spread duration), liquidity tiers, stress tests.
- **Loop:** scheduled rebalance (daily/weekly) → refreshed views → optimiser → OMS.

### Connections
- **Builds on:** [[mean-variance-optimization]] (reverse optimisation), [[conditional-probability-bayes]] (prior × views → posterior; same shrinkage idea as [[beta-bernoulli-conjugacy]]).
- **Front end:** [[grinold-alpha]] turns signals into the view returns $Q$.
