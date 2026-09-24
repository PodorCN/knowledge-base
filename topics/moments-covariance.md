---
id: moments-covariance
title: "Moments & Covariance"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Moments & Covariance

**Sections:** [[expectation-linearity-indicators]] · [[variance-covariance-correlation]] · [[jensens-inequality]] · [[total-expectation-variance]] · [[conditional-expectation-best-predictor]] · [[eigen-svd-psd]]

<a id="expectation-linearity-indicators"></a>

## Linearity of Expectation & Indicators
<!-- section: expectation-linearity-indicators | prerequisites: [probability-rules-counting] | related: [variance-covariance-correlation, first-step-analysis, jensens-inequality] | sources: [src-squarepoint-dqa-workbook] | tags: [expectation, indicator, linearity] -->

### Formulas
$$E[aX+bY+c]=aE[X]+bE[Y]+c,\qquad E[I_A]=P(A),\qquad N=\sum_i I_i\Rightarrow E[N]=\sum_i P(A_i)$$

**Variables:**

- $X,Y$ random variables
- $a,b,c$ constants
- $I_A$ indicator of event $A$ (1 if $A$ happens else 0)
- $N$ a count

### Key points
- **Hat-check problem:** $n$ random hats → each person matches w.p. $1/n$ → expected matches $=1$, for any $n$.
- In general $E[g(X)]\ne g(E[X])$ → see [[jensens-inequality]].

### Connections
- **Used by:** [[first-step-analysis]] (coupon collector = sum of stage waits), [[order-statistics]].
- **Next:** [[variance-covariance-correlation]] — variance is *not* linear; covariance terms appear.

<a id="variance-covariance-correlation"></a>

## Variance, Covariance & Correlation
<!-- section: variance-covariance-correlation | prerequisites: [expectation-linearity-indicators] | related: [portfolio-variance-diversification, total-expectation-variance, normal-distribution, ols-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [variance, covariance, correlation] -->

### Formulas
$$\mathrm{Var}(X)=E[X^2]-E[X]^2,\quad \mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y],\quad \rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}\in[-1,1]$$
$$\mathrm{Var}(aX+bY)=a^2\sigma_X^2+b^2\sigma_Y^2+2ab\,\rho\,\sigma_X\sigma_Y$$
$$\mathrm{Var}\Big(\sum_{i=1}^n X_i\Big)=n\sigma^2+n(n-1)\rho\sigma^2\ \ \text{(equicorrelated)}$$

**Variables:**

- $X,Y$ random variables
- $a,b$ constants
- $\sigma$ standard deviation
- $\rho$ correlation
- $n$ number of variables

### Key points
- $|\rho|\le1$ by Cauchy–Schwarz; undefined if a variance is 0.
- **Uncorrelated but dependent:** $X\sim N(0,1)$, $Y=X^2$ ⇒ $\mathrm{Cov}=E[X^3]=0$, yet $Y$ is a function of $X$.
- For **jointly normal** variables, zero covariance ⇔ independence (e.g. $X+Y \perp X-Y$ for iid normals).
- Scaling: $\mathrm{Var}(10X)=100\,\mathrm{Var}(X)$; positive scaling keeps $\rho$, negative flips its sign.

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Used by:** [[portfolio-variance-diversification]] ($w^\top\Sigma w$), [[ols-regression]] (slope $=\mathrm{Cov}/\mathrm{Var}$), [[pca]] (eigen-decomposition of $\Sigma$).
- **Extended by:** [[total-expectation-variance]] (law of total covariance).

<a id="jensens-inequality"></a>

## Jensen's Inequality
<!-- section: jensens-inequality | prerequisites: [expectation-linearity-indicators] | related: [geometric-brownian-motion, returns-simple-log, gamma-theta-pnl] | sources: [src-squarepoint-dqa-workbook] | tags: [convexity] -->

### Formula
$$g\ \text{convex}\Rightarrow g(E[X])\le E[g(X)];\qquad E[\log X]\le\log E[X]\ \ (X>0)$$

**Variables:**

- $X$ random variable
- $g$ a convex function (reverse for concave)

### Key points
- Arithmetic vs geometric growth: $E[\log(S_t/S_0)]=(\mu-\tfrac12\sigma^2)t < \mu t$.
- Convex option payoffs gain from mean-preserving spreads — the reason long options are "long vol".
- Higher variance alone doesn't rank *every* distribution for every convex payoff.

### Connections
- **Explains:** [[geometric-brownian-motion]] ($-\tfrac12\sigma^2$ drift), [[returns-simple-log]] (+10% then −10% = −1%), [[gamma-theta-pnl]] (convexity pays when realised vol is high).

<a id="total-expectation-variance"></a>

## Laws of Total Expectation, Variance & Covariance
<!-- section: total-expectation-variance | prerequisites: [variance-covariance-correlation, conditional-probability-bayes] | related: [conditional-expectation-best-predictor, exponential-poisson-process] | sources: [src-squarepoint-dqa-workbook] | tags: [conditioning, random-sum, hidden-dependence] -->

### Formulas
$$E[X]=E\big[E[X\mid Y]\big],\qquad \mathrm{Var}(X)=E[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(E[X\mid Y])$$
$$\mathrm{Cov}(X,Z)=E[\mathrm{Cov}(X,Z\mid Y)]+\mathrm{Cov}(E[X\mid Y],E[Z\mid Y])$$
**Random sum** $S=\sum_{i=1}^N X_i$ ($X_i$ iid mean $m$, variance $v$, $N$ independent):
$$E[S]=E[N]m,\qquad \mathrm{Var}(S)=E[N]v+\mathrm{Var}(N)m^2$$

**Variables:**

- $X,Z$ target variables
- $Y$ conditioning (hidden) variable
- $N$ random count

### Worked examples
- $Y\sim U(0,1)$, $X\mid Y\sim U(0,Y)$: $E[X]=1/4$, $\mathrm{Var}(X)=\frac{1/3}{12}+\frac{1/12}{4}=7/144$.
- $N\sim$ Poisson(10) trades, PnL mean 2, var 9: $E=20$, $\mathrm{Var}=10\cdot9+10\cdot4=130$ (the extra 40 = uncertainty in trade count).
- Selected-coin tosses: $\mathrm{Cov}(I_1,I_2)=\mathrm{Var}(\Theta)=1/64$ → hidden dependence.

### Key points
- Trap: if $N$ depends on the $X_i$ (stopping time), these formulas don't apply automatically — use a recursion ([[first-step-analysis]]).

### Connections
- **Builds on:** [[variance-covariance-correlation]], [[conditional-probability-bayes]].
- **Related:** [[conditional-expectation-best-predictor]] — same decomposition applied to prediction error.

<a id="conditional-expectation-best-predictor"></a>

## Conditional Expectation as Best Predictor
<!-- section: conditional-expectation-best-predictor | prerequisites: [total-expectation-variance] | related: [ols-regression, normal-distribution, bias-variance-tradeoff] | sources: [src-squarepoint-dqa-workbook] | tags: [prediction, mse, jointly-normal] -->

### Formulas
$$E[(X-g(Y))^2]=E[\mathrm{Var}(X\mid Y)]+E[(E[X\mid Y]-g(Y))^2]$$
Jointly normal:
$$E[Y\mid X=x]=\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\qquad \mathrm{Var}(Y\mid X=x)=\sigma_Y^2(1-\rho^2)$$

**Variables:**

- $g$ any square-integrable predictor
- $\mu,\sigma$ means / std devs
- $\rho$ correlation

### Key points
- $E[X\mid Y=y]$ is a number; $E[X\mid Y]$ is a random variable.
- Under joint normality the best predictor **is** linear with slope $\rho\sigma_Y/\sigma_X$ — exactly the OLS population slope.

### Connections
- **Bridge to:** [[ols-regression]] (linear approximation of $E[Y\mid X]$), [[bias-variance-tradeoff]].
- **Builds on:** [[total-expectation-variance]]; uses [[normal-distribution]].

<a id="eigen-svd-psd"></a>

## Eigen-decomposition, SVD & PSD Matrices
<!-- section: eigen-svd-psd | prerequisites: [] | related: [pca, multicollinearity, portfolio-variance-diversification] | sources: [src-squarepoint-dqa-workbook] | tags: [linear-algebra] -->

- $Av=\lambda v$; real symmetric ⇒ orthonormal eigenbasis.
- PSD: $v^\top Av\ge0$ ⇔ eigenvalues ≥ 0. Covariance is PSD since $v^\top\Sigma v=\mathrm{Var}(v^\top X)\ge0$.
- SVD $X=UDV^\top$; small singular values ⇒ unstable least squares.
- Invertible ⇔ full rank.

**Variables:**

- $A$ square matrix
- $v$ eigenvector
- $\lambda$ eigenvalue
- $\Sigma$ covariance
- $U,V$ orthogonal, $D$ diagonal singular values

### Connections
- **Used by:** [[pca]], [[multicollinearity]], [[portfolio-variance-diversification]] (valid correlation matrices), [[mean-variance-optimization]] (inverting Σ amplifies small-eigenvalue noise).
