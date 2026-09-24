---
id: portfolio-optimisation
title: "Portfolio Optimisation"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook]
---
# Portfolio Optimisation

**Sections:** [[portfolio-variance-diversification]] · [[minimum-variance-portfolio]] · [[mean-variance-optimization]]

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
<!-- section: mean-variance-optimization | prerequisites: [minimum-variance-portfolio] | related: [marginal-sharpe-improvement, risk-budgeting, ridge-regression, eigen-svd-psd] | sources: [src-squarepoint-dqa-workbook] | tags: [markowitz, tangency, max-sharpe, estimation-error] -->

$$\max_w\ w^\top\mu-\tfrac\gamma2w^\top\Sigma w\ \Rightarrow\ w^*=\tfrac1\gamma\Sigma^{-1}\mu,\qquad SR_{max}=\sqrt{\mu^\top\Sigma^{-1}\mu},\qquad w_T=\frac{\Sigma^{-1}\mu}{\mathbf 1^\top\Sigma^{-1}\mu}$$

**Variables:**

- $\mu$ expected **excess** returns
- $\Sigma$ covariance
- $\gamma$ risk aversion
- $w_T$ fully invested tangency portfolio (needs $\mathbf 1^\top\Sigma^{-1}\mu>0$)

### Why optimised portfolios fail
- μ is noisy, Σ unstable; $\Sigma^{-1}$ **amplifies errors** in small-eigenvalue directions ([[eigen-svd-psd]]) → extreme weights, turnover.
- Fixes: shrink means/covariance (cf. [[ridge-regression]]), constraints, turnover penalties, compare with equal-weight / min-var baselines, or skip μ entirely via [[risk-budgeting]].
