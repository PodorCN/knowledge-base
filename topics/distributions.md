---
id: distributions
title: "Distributions"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Distributions

This chapter is the catalogue of distributions used throughout the wiki: a reference table, then the three that matter most in finance — the normal family (for statistics and Brownian motion), the lognormal (for prices) and the exponential/Poisson pair (for arrivals and jumps).

**Prerequisites:** [[probability-rules-counting]].

**Leads to:** [[expectation-linearity-indicators]] (moments), [[brownian-motion]] (normal increments), [[geometric-brownian-motion]] (lognormal prices), [[jump-diffusion]] (Poisson jumps).

**Sections:** [[distributions-reference]] · [[normal-distribution]] · [[lognormal-distribution]] · [[exponential-poisson-process]]

<a id="distributions-reference"></a>

## Common Distributions (reference)
<!-- section: distributions-reference | prerequisites: [probability-rules-counting] | related: [normal-distribution, lognormal-distribution, exponential-poisson-process] | sources: [src-squarepoint-dqa-workbook] | tags: [distributions, reference] -->

The probability mass or density function, mean and variance of the standard distributions.

### Definitions

| Distribution | PMF / PDF | Mean | Variance |
|---|---|---|---|
| Bernoulli($p$) | $P(1)=p$ | $p$ | $p(1-p)$ |
| Binomial($n,p$) | $\binom nk p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| Geometric($p$), trials to 1st success | $(1-p)^{k-1}p$ | $1/p$ | $(1-p)/p^2$ |
| Poisson($\lambda$) | $e^{-\lambda}\lambda^k/k!$ | $\lambda$ | $\lambda$ |
| Uniform($a,b$) | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| Exponential($\lambda$) | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| Normal($\mu,\sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$ | $\mu$ | $\sigma^2$ |
| Beta($a,b$) | $x^{a-1}(1-x)^{b-1}/B(a,b)$ | $\frac{a}{a+b}$ | $\frac{ab}{(a+b)^2(a+b+1)}$ |

**Variables:**

- $p$ success probability
- $n$ number of trials
- $k$ value of a discrete outcome
- $x$ value of a continuous outcome
- $\lambda$ rate
- $a,b$ bounds (Uniform) or shape parameters (Beta)
- $B(a,b)$ Beta function (normalising constant)
- $\mu,\sigma^2$ mean and variance

### Key points
- **Convention trap:** the geometric distribution counted as "failures before the first success" has support starting at 0 and mean $(1-p)/p$.
- A density value is not a probability and can exceed 1.
- Memoryless distributions: Exponential (continuous) and Geometric (discrete) only.

### Connections
- **Detailed in:** [[normal-distribution]], [[lognormal-distribution]], [[exponential-poisson-process]], [[beta-bernoulli-conjugacy]] (Beta prior).
- **Used by:** [[order-statistics]], [[first-step-analysis]], [[maximum-likelihood]].

<a id="normal-distribution"></a>

## Normal Distribution & Friends (χ², t, F)
<!-- section: normal-distribution | prerequisites: [distributions-reference] | related: [lln-clt, hypothesis-testing, lognormal-distribution, brownian-motion] | sources: [src-squarepoint-dqa-workbook] | tags: [normal, chi-square, t-distribution] -->

Standardising a normal variable gives $N(0,1)$; sums of squared standard normals, and ratios built from them, give the $\chi^2$, $t$ and $F$ distributions used in tests.

### Formulas
$$Z=\frac{X-\mu}{\sigma}\sim N(0,1);\quad \sum_{i=1}^{\nu}Z_i^2\sim\chi^2_\nu;\quad \frac{Z}{\sqrt{U/\nu}}\sim t_\nu;\quad \frac{U/a}{V/b}\sim F_{a,b}$$

**Variables:**

- $X\sim N(\mu,\sigma^2)$ normal random variable
- $\mu,\sigma$ mean and standard deviation
- $Z,Z_i$ independent standard normals
- $U\sim\chi^2_\nu$ (or $\chi^2_a$ in the $F$ ratio), independent of $Z$
- $V\sim\chi^2_b$, independent of $U$
- $\nu,a,b$ degrees of freedom

Notation used throughout the wiki: $N(\cdot)$ is the standard normal CDF and $\phi(\cdot)$ its density.

### Key points
- 68 / 95 / 99.7% of the mass lies within 1 / 2 / 3 σ; the central 95% uses 1.96.
- Linear combinations of **jointly** normal variables are normal; normal marginals alone are not enough.
- $t$ has heavier tails and tends to the normal as $\nu\to\infty$. $\chi^2_\nu$ has mean $\nu$ and variance $2\nu$.
- $E[Z^4]=3$ for a standard normal (used in $\mathrm{Var}(Z^2)=3-1=2$).

### Connections
- **Used by:** [[hypothesis-testing]] (t and F tests), [[confidence-intervals]], [[brownian-motion]] (normal increments), [[black-scholes-formula]] ($N(d_1),N(d_2)$).

<a id="lognormal-distribution"></a>

## Lognormal Distribution
<!-- section: lognormal-distribution | prerequisites: [normal-distribution] | related: [geometric-brownian-motion, black-scholes-formula, jensens-inequality] | sources: [src-squarepoint-dqa-workbook] | tags: [lognormal] -->

A variable is lognormal when its logarithm is normal. It is the terminal law of a stock price in the Black–Scholes model.

### Formula
$$\ln X\sim N(m,s^2)\ \Rightarrow\ E[X]=e^{m+s^2/2},\qquad \mathrm{Var}(X)=(e^{s^2}-1)e^{2m+s^2}$$

**Variables:**

- $X>0$ lognormal random variable
- $m$ mean of $\ln X$
- $s^2$ variance of $\ln X$

### Key points
- Right-skewed: the median $e^m$ is below the mean $e^{m+s^2/2}$. This is why the delta of an ATM-forward call is above 0.5 ([[delta-vs-itm-probability]]).
- The $s^2/2$ term is [[jensens-inequality]] in action.

### Connections
- **Is the terminal law of:** [[geometric-brownian-motion]]; the Black–Scholes assumption whose failure creates the [[volatility-skew]].

<a id="exponential-poisson-process"></a>

## Exponential Distribution & Poisson Process
<!-- section: exponential-poisson-process | prerequisites: [distributions-reference] | related: [first-step-analysis, total-expectation-variance, jump-diffusion] | sources: [src-squarepoint-dqa-workbook] | tags: [memoryless, arrivals, order-flow] -->

Exponential waiting times are memoryless; counting the arrivals they generate gives the Poisson process, the standard model for order arrivals and for jumps.

### Formulas
$$P(T>s+t\mid T>s)=P(T>t)=e^{-\lambda t}$$
$$N_t\sim\mathrm{Poisson}(\lambda t),\qquad \min(X,Y)\sim\mathrm{Exp}(\lambda+\mu),\qquad P(X<Y)=\frac{\lambda}{\lambda+\mu}$$

**Variables:**

- $T\sim\mathrm{Exp}(\lambda)$ waiting time
- $s,t$ elapsed and additional waiting time
- $\lambda,\mu$ rates
- $N_t$ number of arrivals in $[0,t]$
- $X\sim\mathrm{Exp}(\lambda)$, $Y\sim\mathrm{Exp}(\mu)$ independent

### Key points
- Orders at 3 per minute: $P(\text{none in 30 s})=e^{-3\times0.5}=e^{-1.5}$.
- Counts in disjoint intervals are independent. Real order flow **clusters**, so check before assuming.
- Memorylessness is a *model* property, not a law of waiting times.

### Connections
- **Builds on:** [[distributions-reference]].
- **Used by:** [[total-expectation-variance]] (Poisson random sums: $E=\lambda m$, $\mathrm{Var}=\lambda(v+m^2)$), [[jump-diffusion]] (Poisson jump arrivals).
