---
id: estimation-testing
title: "Estimation & Confidence Intervals"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Estimation & Confidence Intervals

This chapter covers how to estimate an unknown parameter from data and how to quantify the uncertainty of the estimate: estimator quality (bias, variance, MSE), the limit theorems that make sample means work, maximum likelihood, the Bayesian alternative, and interval estimates (analytic and bootstrap).

**Prerequisites:** [[variance-covariance-correlation]], [[normal-distribution]], [[conditional-probability-bayes]].

**Leads to:** [[hypothesis-testing]] (the dual of a confidence interval), [[ols-regression]], [[bias-variance-tradeoff]], [[monte-carlo-pricing]] (CLT error).

**Sections:** [[estimator-properties]] · [[lln-clt]] · [[maximum-likelihood]] · [[beta-bernoulli-conjugacy]] · [[confidence-intervals]] · [[bootstrap]]

<a id="estimator-properties"></a>

## Estimator Properties (bias, variance, MSE, consistency)
<!-- section: estimator-properties | prerequisites: [variance-covariance-correlation] | related: [bias-variance-tradeoff, ridge-regression, maximum-likelihood, lln-clt] | sources: [src-squarepoint-dqa-workbook] | tags: [bias, mse, degrees-of-freedom] -->

An estimator is a rule that maps data to a guess of a parameter. Its quality is judged by bias (systematic error) and variance (noise), which combine into mean-squared error.

### Formulas
$$\mathrm{Bias}(\hat\theta)=E[\hat\theta]-\theta,\qquad \mathrm{MSE}(\hat\theta)=\mathrm{Var}(\hat\theta)+\mathrm{Bias}(\hat\theta)^2$$
$$s^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar X)^2\ \ \text{(unbiased)},\qquad \mathrm{Var}(\bar X)=\frac{\sigma^2}{n}$$

**Variables:**

- $\theta$ true parameter
- $\hat\theta$ estimator of $\theta$
- $X_i$ iid sample, $i=1,\dots,n$
- $\bar X$ sample mean
- $s^2$ sample variance
- $\sigma^2$ population variance
- $n$ sample size

### Key points
- **Why $n-1$:** estimating $\bar X$ forces $\sum(X_i-\bar X)=0$, so one residual degree of freedom is lost; $E[\sum(X_i-\bar X)^2]=(n-1)\sigma^2$.
- Dividing by $n$ is biased downward, but it is the normal MLE ([[maximum-likelihood]]).
- **Unbiased ≠ consistent**; and an unbiased estimator need not minimise MSE → this motivates shrinkage.
- Standard error of the mean $=\sigma/\sqrt n$ (estimated by $s/\sqrt n$).

### Connections
- **Motivates:** [[ridge-regression]] (accept bias to cut variance), [[bias-variance-tradeoff]].
- **Related:** [[maximum-likelihood]], [[lln-clt]].

<a id="lln-clt"></a>

## Law of Large Numbers & Central Limit Theorem
<!-- section: lln-clt | prerequisites: [estimator-properties, normal-distribution] | related: [confidence-intervals, effective-sample-size, monte-carlo-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [clt, standard-error] -->

The law of large numbers says the sample mean converges to the true mean; the central limit theorem says its error is approximately normal with standard deviation $\sigma/\sqrt n$.

### Formula
$$\bar X\to\mu\ \ \text{(LLN)},\qquad \frac{\sqrt n(\bar X-\mu)}{\sigma}\Rightarrow N(0,1)\ \ \text{(CLT)}$$

**Variables:**

- $\bar X$ sample mean of $n$ iid draws
- $\mu$ population mean
- $\sigma$ population standard deviation (finite, $\sigma>0$)
- $n$ number of draws
- $\Rightarrow$ convergence in distribution

### Key points
- The CLT is about the **sample mean**: it is approximately normal; the observations themselves don't become normal.
- 4× the data halves the standard error — only for **independent** data (duplicated or correlated rows don't count).
- The CLT fails or is slow with dependence, heavy tails (infinite variance) or tiny samples.

### Connections
- **Used by:** [[confidence-intervals]], [[monte-carlo-pricing]] (Monte Carlo error $\propto 1/\sqrt{M}$ for $M$ paths).
- **Adjust for dependence:** [[effective-sample-size]].

<a id="maximum-likelihood"></a>

## Maximum Likelihood Estimation (MLE)
<!-- section: maximum-likelihood | prerequisites: [distributions-reference, estimator-properties] | related: [beta-bernoulli-conjugacy, logistic-regression, ols-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [mle, map, likelihood] -->

MLE chooses the parameter value under which the observed data are most probable. The data are held fixed and the parameter varies.

### Formulas
$$\ell(\theta)=\sum_{i=1}^n\ln f(x_i;\theta),\qquad \hat\theta_{\text{MLE}}=\arg\max_\theta\ell(\theta)$$
$$\text{Bernoulli: }\hat p=\frac hn,\qquad \text{Normal: }\hat\mu=\bar x,\ \ \hat\sigma^2_{\text{MLE}}=\frac1n\sum_{i=1}^n(x_i-\bar x)^2$$

**Variables:**

- $\ell(\theta)$ log-likelihood
- $f(x;\theta)$ density or pmf with parameter $\theta$
- $x_i$ observed data, $i=1,\dots,n$
- $\bar x$ sample mean
- $h$ number of successes in $n$ Bernoulli trials
- $\hat p,\hat\mu,\hat\sigma^2_{\text{MLE}}$ maximum-likelihood estimates

### Worked example
60 heads in 100 tosses: $\hat p=0.6$, standard error $\approx\sqrt{0.6\cdot0.4/100}=0.049$ (Wald interval; poor near 0 or 1 — use score intervals there).

### Key points
- MLE gives a point, **not** a distribution over $\theta$ (that needs a prior, [[beta-bernoulli-conjugacy]]).
- Boundary case: all 0s or all 1s → the maximum is at the boundary; don't divide by zero in the first-order condition.
- MLE vs **MAP** (posterior mode) vs **posterior mean** — generally different.

### Connections
- **Contrast:** [[beta-bernoulli-conjugacy]] (Bayesian).
- **Special cases:** [[ols-regression]] = Gaussian MLE; [[logistic-regression]] = Bernoulli MLE (cross-entropy).

<a id="beta-bernoulli-conjugacy"></a>

## Bayesian Estimation: Beta–Bernoulli Conjugacy
<!-- section: beta-bernoulli-conjugacy | prerequisites: [conditional-probability-bayes, distributions-reference, maximum-likelihood] | related: [ridge-regression, black-litterman] | sources: [src-squarepoint-dqa-workbook] | tags: [bayes, conjugate-prior, shrinkage] -->

The Bayesian alternative to MLE puts a prior on the unknown probability and updates it with the data. With a Beta prior and Bernoulli data the posterior is again Beta, so the update is just adding counts.

### Formulas
$$\theta\sim\mathrm{Beta}(a,b)\ \Rightarrow\ \theta\mid D\sim\mathrm{Beta}(a+h,\ b+t),\qquad P(H_{\text{next}}\mid D)=\frac{a+h}{a+b+h+t}$$
$$\frac{a+h}{a+b+n}=\underbrace{\frac{a+b}{a+b+n}}_{\text{prior weight}}\cdot\frac{a}{a+b}+\underbrace{\frac{n}{a+b+n}}_{\text{data weight}}\cdot\frac{h}{n}$$

**Variables:**

- $\theta$ unknown head probability
- $a,b>0$ prior pseudo-counts of heads and tails
- $D$ observed tosses
- $h$ number of heads, $t$ number of tails, $n=h+t$
- $H_{\text{next}}$ event that the next toss is a head

### Worked example
A uniform prior is Beta(1,1). After HHH the posterior is Beta(4,1) and the predictive probability of another head is $4/5$ (Laplace's rule of succession).

### Key points
- The posterior mean is a **weighted average** of the prior mean $a/(a+b)$ and the MLE $h/n$ → the prior washes out as $n$ grows.
- This is a different model from "choose between two specific coins" (a discrete prior, [[conditional-probability-bayes]]).
- MLE $h/n$, MAP (posterior mode) and posterior mean all differ ([[maximum-likelihood]]).

### Connections
- **Builds on:** [[conditional-probability-bayes]], [[distributions-reference]] (Beta pdf and mean), [[maximum-likelihood]].
- **Same idea as:** [[ridge-regression]] (Gaussian prior ⇒ shrinkage toward the prior mean), [[black-litterman]] (prior × views → posterior).

<a id="confidence-intervals"></a>

## Confidence Intervals
<!-- section: confidence-intervals | prerequisites: [lln-clt, normal-distribution] | related: [hypothesis-testing, prediction-vs-confidence-interval, bootstrap] | sources: [src-squarepoint-dqa-workbook] | tags: [ci, t-interval] -->

A confidence interval is a range computed from the data by a procedure that covers the true parameter in a stated fraction of repeated samples.

### Formulas
$$\bar x\pm1.96\,\frac{\sigma}{\sqrt n}\ \ (\sigma\text{ known}),\qquad \bar x\pm t_{n-1,0.975}\,\frac{s}{\sqrt n}\ \ (\sigma\text{ unknown, normal data})$$

**Variables:**

- $\bar x$ sample mean
- $\sigma$ true standard deviation
- $s$ sample standard deviation
- $n$ sample size
- $t_{\nu,u}$ $u$-quantile of the $t_\nu$ distribution

### Worked example
$n=100$, $\bar x=0.2$, $s=1$: $0.2\pm1.96\times0.1$ → approximately $[0.004,\ 0.396]$.

### Key points
- **Interpretation:** 95% of intervals *built by this procedure* cover the fixed true $\mu$. A realised interval is not a 95% posterior probability.

### Connections
- **Dual of:** [[hypothesis-testing]]. **Non-parametric alternative:** [[bootstrap]]. **Regression version:** [[prediction-vs-confidence-interval]].

<a id="bootstrap"></a>

## Bootstrap (iid and block)
<!-- section: bootstrap | prerequisites: [confidence-intervals] | related: [stationarity-ar1, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [resampling] -->

The bootstrap estimates the sampling distribution of a statistic by resampling the observed data instead of relying on a formula.

### Key points
- Row-wise resampling assumes (approximately) iid rows.
- Serial dependence → **block bootstrap**: resample contiguous blocks; block length and stationarity matter.
- It is not a cure for tiny samples or extreme tails.

### Connections
- **Alternative to:** analytic [[confidence-intervals]].
- **Dependence issues:** [[stationarity-ar1]], [[effective-sample-size]].
