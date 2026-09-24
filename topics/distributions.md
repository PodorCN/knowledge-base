---
id: distributions
title: "Distributions"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Distributions

**Sections:** [[distributions-reference]] · [[normal-distribution]] · [[lognormal-distribution]] · [[exponential-poisson-process]]

<a id="distributions-reference"></a>

## Common Distributions (reference)
<!-- section: distributions-reference | prerequisites: [probability-rules-counting] | related: [normal-distribution, lognormal-distribution, exponential-poisson-process] | sources: [src-squarepoint-dqa-workbook] | tags: [distributions, reference] -->

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

- $p$ success prob
- $n$ trials
- $k$ outcome
- $\lambda$ rate
- $a,b$ bounds (Uniform) or shape params (Beta)
- $\mu,\sigma^2$ mean/variance

### Key points
- **Convention trap:** geometric "failures before success" has support from 0 and mean $(1-p)/p$.
- A density value is not a probability and can exceed 1.
- Memoryless: Exponential (continuous) and Geometric (discrete) only.

### Connections
- **Detailed in:** [[normal-distribution]], [[lognormal-distribution]], [[exponential-poisson-process]], [[beta-bernoulli-conjugacy]].
- **Used by:** [[order-statistics]], [[first-step-analysis]].

<a id="normal-distribution"></a>

## Normal Distribution & Friends (χ², t, F)
<!-- section: normal-distribution | prerequisites: [distributions-reference] | related: [lln-clt, hypothesis-testing, lognormal-distribution, brownian-motion] | sources: [src-squarepoint-dqa-workbook] | tags: [normal, chi-square, t-distribution] -->

### Formulas
$$Z=\frac{X-\mu}{\sigma}\sim N(0,1);\quad \sum_{i=1}^{\nu}Z_i^2\sim\chi^2_\nu;\quad \frac{Z}{\sqrt{U/\nu}}\sim t_\nu;\quad \frac{U/a}{V/b}\sim F_{a,b}$$

**Variables:**

- $\mu,\sigma$ mean and std dev
- $Z_i$ iid standard normals
- $U\sim\chi^2_\nu$, $V\sim\chi^2_b$ independent
- $\nu,a,b$ degrees of freedom

### Key points
- 68 / 95 / 99.7% within 1/2/3 σ; central 95% uses 1.96.
- Linear combos of **jointly** normal variables are normal; normal marginals alone are not enough.
- $t$ has heavier tails, → normal as $\nu\to\infty$. $\chi^2_\nu$ has mean $\nu$, variance $2\nu$.
- $E[X^4]=3$ for standard normal (used in $\mathrm{Var}(X^2)=2$).

### Connections
- **Used by:** [[hypothesis-testing]] (t and F tests), [[confidence-intervals]], [[brownian-motion]] (normal increments), [[black-scholes-formula]] ($N(d_1), N(d_2)$).

<a id="lognormal-distribution"></a>

## Lognormal Distribution
<!-- section: lognormal-distribution | prerequisites: [normal-distribution] | related: [geometric-brownian-motion, black-scholes-formula, jensens-inequality] | sources: [src-squarepoint-dqa-workbook] | tags: [lognormal] -->

### Formula
$$\log X\sim N(m,s^2)\Rightarrow E[X]=e^{m+s^2/2},\quad \mathrm{Var}(X)=(e^{s^2}-1)e^{2m+s^2}$$

**Variables:** $m,s^2$ mean and variance of $\log X$.

### Key points
- Right-skewed: median $e^m$ < mean $e^{m+s^2/2}$ — why ATM-forward call delta > 0.5 ([[delta-vs-itm-probability]]).
- The $s^2/2$ term is [[jensens-inequality]] in action.

### Connections
- **Is the terminal law of:** [[geometric-brownian-motion]]; the BS assumption whose failure creates the [[volatility-skew]].

<a id="exponential-poisson-process"></a>

## Exponential Distribution & Poisson Process
<!-- section: exponential-poisson-process | prerequisites: [distributions-reference] | related: [first-step-analysis, total-expectation-variance, jump-diffusion] | sources: [src-squarepoint-dqa-workbook] | tags: [memoryless, arrivals, order-flow] -->

### Formulas
$$P(T>s+t\mid T>s)=P(T>t)=e^{-\lambda t}$$
$$N(t)\sim\mathrm{Poisson}(\lambda t),\qquad \min(X,Y)\sim\mathrm{Exp}(\lambda+\mu),\qquad P(X<Y)=\frac{\lambda}{\lambda+\mu}$$

**Variables:**

- $T$ waiting time
- $\lambda,\mu$ rates
- $N(t)$ arrivals in $[0,t]$
- $X\sim\mathrm{Exp}(\lambda)$, $Y\sim\mathrm{Exp}(\mu)$ independent

### Key points
- Orders at 3/min: $P(\text{none in 30s})=e^{-1.5}$.
- Counts in disjoint intervals are independent — real order flow **clusters**, so check before assuming.
- Memorylessness is a *model* property, not a law of waiting times.

### Connections
- **Builds on:** [[distributions-reference]].
- **Used by:** [[total-expectation-variance]] (Poisson random sums: $E=\lambda m$, $\mathrm{Var}=\lambda(v+m^2)$); [[jump-diffusion]] (Poisson jump arrivals).
