---
id: probability-distributions
title: "Probability & Distributions"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Probability & Distributions

This chapter sets up the rules for combining probabilities and for updating them when information arrives. Every later statistical and pricing argument is built from these two steps: count (or measure) outcomes, then condition. It then gives the catalogue of distributions used throughout the wiki: a reference table, then the three that matter most in finance — the normal family (for statistics and Brownian motion), the lognormal (for prices) and the exponential/Poisson pair (for arrivals and jumps).

**Prerequisites:** none.

**Leads to:** [[expectation-linearity-indicators]] (moments), [[beta-bernoulli-conjugacy]] (Bayesian estimation), [[hypothesis-testing]] (frequentist contrast), [[brownian-motion]] (normal increments), [[geometric-brownian-motion]] (lognormal prices), [[jump-diffusion]] (Poisson jumps).

**Sections:** [[probability-rules-counting]] · [[conditional-probability-bayes]] · [[distributions-reference]] · [[normal-distribution]] · [[lognormal-distribution]] · [[exponential-poisson-process]]

<a id="probability-rules-counting"></a>

## Probability Rules & Counting
<!-- section: probability-rules-counting | prerequisites: [] | related: [conditional-probability-bayes, expectation-linearity-indicators] | sources: [src-squarepoint-dqa-workbook] | tags: [counting, complement, inclusion-exclusion] -->

The basic rules: add probabilities of unions (subtracting the overlap), use complements for "at least one", and count arrangements with permutations and combinations.

### Formulas
$$P(A\cup B)=P(A)+P(B)-P(A\cap B),\qquad P(A^c)=1-P(A)$$
$$P(n,k)=\frac{n!}{(n-k)!},\qquad \binom{n}{k}=\frac{n!}{k!\,(n-k)!}$$
$$P(\text{at least one})=1-(1-p)^n$$

**Variables:**

- $A,B$ events
- $A^c$ complement of $A$
- $P(n,k)$ number of ordered selections of $k$ items from $n$
- $\binom nk$ number of unordered selections of $k$ items from $n$
- $n$ number of items, or of independent trials
- $k$ number of items chosen
- $p$ per-trial probability (independent trials)

### Key points
- **Mutually exclusive ≠ independent.** Two exclusive events with positive probability are *dependent*: one rules out the other.
- Sampling **with** replacement gives independent draws; **without** replacement gives dependent draws. E.g. two aces without replacement: $\frac{4}{52}\cdot\frac{3}{51}=\frac{1}{221}$.
- At least one six in four rolls: $1-(5/6)^4\approx 0.5177$.
- Before using a ratio of counts, check the elementary outcomes are **equally likely**.

### Connections
- **Used by:** [[conditional-probability-bayes]] (conditioning is "restrict the sample space, renormalise"), [[expectation-linearity-indicators]] (indicator tricks often replace hard counting), [[distributions-reference]].

<a id="conditional-probability-bayes"></a>

## Conditional Probability & Bayes' Theorem
<!-- section: conditional-probability-bayes | prerequisites: [probability-rules-counting] | related: [beta-bernoulli-conjugacy, total-expectation-variance, maximum-likelihood, hypothesis-testing, bayesianized-p-value] | sources: [src-squarepoint-dqa-workbook] | tags: [bayes, base-rate, independence] -->

Conditioning on an event restricts attention to the outcomes where it happened and renormalises. Bayes' theorem turns "probability of the data given a hypothesis" into "probability of the hypothesis given the data".

### Formulas
$$P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(D)=\sum_j P(D\mid H_j)P(H_j)$$
$$P(H_i\mid D)=\frac{P(D\mid H_i)P(H_i)}{\sum_j P(D\mid H_j)P(H_j)},\qquad \frac{P(H_1\mid D)}{P(H_0\mid D)}=\frac{P(H_1)}{P(H_0)}\cdot\frac{P(D\mid H_1)}{P(D\mid H_0)}$$

**Variables:**

- $A,B$ events, $P(B)>0$
- $H_i$ disjoint hypotheses covering all cases
- $D$ observed data
- $P(H_i)$ prior probability of $H_i$
- $P(D\mid H_i)$ likelihood of the data under $H_i$
- $P(D)$ evidence (the normaliser, from the law of total probability)
- $P(H_i\mid D)$ posterior probability of $H_i$

The last formula reads: **posterior odds = prior odds × likelihood ratio**.

### Worked examples
- **Signal & base rate:** a favourable state occurs 10% of the time; a signal fires 80% of the time when the state is favourable and 20% otherwise. Then $P(F\mid S)=\frac{0.8\times0.1}{0.8\times0.1+0.2\times0.9}=\frac{0.08}{0.08+0.18}=4/13\approx30.8\%$. Rare states make even good detectors imprecise.
- **Selected coin:** pick a fair coin A or a biased coin B ($P(H)=3/4$), each with probability 1/2, and observe HHH. Then $P(B\mid HHH)=\frac{27/64}{27/64+8/64}=27/35$, and the probability that the next toss is a head is $\frac{27}{35}\cdot\frac34+\frac{8}{35}\cdot\frac12=97/140$.

### Key points
- **Conditional independence ≠ independence.** Tosses of the selected coin are independent *given the coin*, but unconditionally correlated because they share the hidden coin ($\mathrm{Cov}=\mathrm{Var}(\Theta)=1/64$, where $\Theta$ is the head probability of the selected coin). See [[total-expectation-variance]].
- Predict with the **posterior**, not the prior.

### Connections
- **Builds on:** [[probability-rules-counting]].
- **Extends to:** [[beta-bernoulli-conjugacy]] (continuous-parameter version), [[bayesianized-p-value]] (posterior probability of a null hypothesis).
- **Contrast:** [[maximum-likelihood]] (no prior) and [[hypothesis-testing]] (a p-value is a $P(\text{data}\mid H_0)$-type quantity, not $P(H_0\mid\text{data})$).
- **Finance link:** signal precision vs base rate → [[backtest-pitfalls]].

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
