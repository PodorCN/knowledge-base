---
id: estimation-testing
title: "Estimation & Hypothesis Testing"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Estimation & Hypothesis Testing

**Sections:** [[estimator-properties]] · [[linear-regression-assumptions]] · [[lln-clt]] · [[maximum-likelihood]] · [[confidence-intervals]] · [[hypothesis-testing]] · [[multiple-testing]] · [[bootstrap]]

<a id="estimator-properties"></a>

## Estimator Properties (bias, variance, MSE, consistency)
<!-- section: estimator-properties | prerequisites: [variance-covariance-correlation] | related: [bias-variance-tradeoff, ridge-regression, maximum-likelihood, lln-clt] | sources: [src-squarepoint-dqa-workbook] | tags: [bias, mse, degrees-of-freedom] -->

### Formulas
$$\mathrm{Bias}(\hat\theta)=E[\hat\theta]-\theta,\qquad \mathrm{MSE}(\hat\theta)=\mathrm{Var}(\hat\theta)+\mathrm{Bias}(\hat\theta)^2$$
$$s^2=\frac{1}{n-1}\sum_i(X_i-\bar X)^2\ \ \text{(unbiased)},\qquad \mathrm{Var}(\bar X)=\frac{\sigma^2}{n}$$

**Variables:**

- $\theta$ true parameter
- $\hat\theta$ estimator
- $X_i$ iid sample
- $\bar X$ sample mean
- $n$ sample size

### Key points
- **Why $n-1$:** estimating $\bar X$ forces $\sum(X_i-\bar X)=0$ → one residual degree of freedom lost; $E[\sum(X_i-\bar X)^2]=(n-1)\sigma^2$.
- Dividing by $n$ is biased downward but is the normal MLE.
- **Unbiased ≠ consistent**; and an unbiased estimator need not minimise MSE → motivates shrinkage.
- Standard error of mean $=\sigma/\sqrt n$ (estimated by $s/\sqrt n$).

### Connections
- **Motivates:** [[ridge-regression]] (accept bias to cut variance), [[bias-variance-tradeoff]].
- **Related:** [[maximum-likelihood]], [[lln-clt]].

<a id="linear-regression-assumptions"></a>

## Linear Regression: Assumptions & Violations
<!-- section: linear-regression-assumptions | prerequisites: [ols-regression, estimator-properties, hypothesis-testing] | related: [gauss-markov-assumptions, robust-standard-errors, omitted-variable-bias, multicollinearity, regression-invariances, stationarity-ar1, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [linear-regression, assumptions, gauss-markov, violations] -->

For the linear model

$$Y=X\beta+\varepsilon,\qquad \hat\beta=\beta+(X^\top X)^{-1}X^\top\varepsilon$$

### Assumption map

| Assumption | What it supports | If it is violated |
|---|---|---|
| **Correct linear mean / functional form** | $\beta_j$ is the conditional change in $Y$ for a one-unit change in $X_j$ | Misspecified fit; coefficients can be biased or lose their economic interpretation, and out-of-sample prediction can fail. |
| **Zero conditional mean / exogeneity:** $E[\varepsilon\mid X]=0$ | OLS is unbiased and consistent under the linear model | Omitted variables, reverse causality, selection, or measurement error correlated with $X$ bias $\hat\beta$ and can make it inconsistent. Robust SEs do not fix this. |
| **Full column rank** | A unique coefficient vector exists | Perfect collinearity makes coefficients non-unique; near-collinearity makes them unstable and high-variance. |
| **Homoskedasticity:** $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$ | Classical standard errors and t/F inference | Coefficients can remain unbiased if exogeneity holds, but classical SEs, p-values, and confidence intervals are wrong; use heteroskedasticity-robust or clustered SEs. |
| **Independent errors** | Classical iid standard errors and inference | Serial correlation, clustering, or duplicated rows make SEs unreliable and reduce the effective sample size; use HAC/clustered SEs and account for dependence. |
| **Normal errors** | Exact finite-sample t/F tests and normal-theory intervals | Non-normal errors can make finite-sample p-values and intervals inaccurate; unbiasedness does not require normality. Large samples or robust/asymptotic methods are alternatives. |
| **No influential outliers / leverage points** | A stable fitted line and stable inference | A small number of points can move coefficients, fitted values, and SEs; inspect diagnostics and decide whether the data or model needs attention. |

### Finance and time-series failure modes

- **Autocorrelated or duplicated rows:** the apparent sample size is too large; naive annualisation and standard errors overstate precision. See [[effective-sample-size]] and [[regression-invariances]].
- **Non-stationary levels:** a regression can be highly significant but spurious; stationarity must be checked before interpreting the slope. See [[stationarity-ar1]].
- **Look-ahead or post-decision data:** OLS can fit an impossible information set and produce an inflated fit or backtest; this is a data-construction failure, not something robust SEs repair. See [[cross-validation-leakage]].

### Quick diagnosis

- **Coefficients biased or unstable:** inspect functional form, omitted variables, endogeneity, and multicollinearity.
- **Coefficients stable but p-values wrong:** inspect heteroskedasticity, serial correlation, clustering, and influential points.
- **A clean-looking fit but bad out-of-sample behaviour:** check leakage, time ordering, and whether the model is being evaluated on data unavailable at decision time.

### Connections
- **Detailed OLS view:** [[ols-regression]]; **Gauss–Markov conditions:** [[gauss-markov-assumptions]].
- **Bias:** [[omitted-variable-bias]]; **variance:** [[robust-standard-errors]], [[multicollinearity]].
- **Signal-research implementation:** [[linear-regression]], [[regression-invariances]], [[cross-validation-leakage]].

<a id="lln-clt"></a>

## Law of Large Numbers & Central Limit Theorem
<!-- section: lln-clt | prerequisites: [estimator-properties, normal-distribution] | related: [confidence-intervals, effective-sample-size, monte-carlo-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [clt, standard-error] -->

### Formula
$$\frac{\sqrt n(\bar X-\mu)}{\sigma}\Rightarrow N(0,1)$$

**Variables:**

- $\bar X$ sample mean of $n$ iid draws
- $\mu,\sigma$ population mean / std dev (finite, $\sigma>0$)

### Key points
- LLN: $\bar X\to\mu$. CLT: the **sample mean** is ≈ normal; the observations themselves don't become normal.
- 4× data halves the SE — only for **independent** data (duplicated / correlated rows don't count).
- Fails / slow with dependence, heavy tails (infinite variance), tiny samples.

### Connections
- **Used by:** [[confidence-intervals]], [[monte-carlo-pricing]] (MC error $\propto 1/\sqrt{N}$).
- **Adjust for dependence:** [[effective-sample-size]].

<a id="maximum-likelihood"></a>

## Maximum Likelihood Estimation (MLE)
<!-- section: maximum-likelihood | prerequisites: [distributions-reference, estimator-properties] | related: [beta-bernoulli-conjugacy, logistic-regression, ols-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [mle, map, likelihood] -->

### Formulas
$$\ell(\theta)=\sum_i\log f(x_i;\theta),\qquad \text{Bernoulli: }\hat p=\frac hn,\qquad \text{Normal: }\hat\mu=\bar x,\ \hat\sigma^2_{\text{MLE}}=\frac1n\sum(x_i-\bar x)^2$$

**Variables:**

- $f(x;\theta)$ density/pmf
- $\theta$ parameter
- $h$ successes in $n$ trials

### Key points
- Data fixed, $\theta$ varies. MLE gives a point, **not** a distribution over $\theta$ (that needs a prior).
- Boundary case: all 0s or all 1s → maximum at boundary; don't divide by zero in the FOC.
- 60 heads / 100: $\hat p=0.6$, SE $\approx\sqrt{0.6\cdot0.4/100}=0.049$ (Wald interval; poor near 0/1 — use score intervals).
- MLE vs **MAP** (posterior mode) vs **posterior mean** — generally different.

### Connections
- **Contrast:** [[beta-bernoulli-conjugacy]] (Bayesian). **Special cases:** [[ols-regression]] = Gaussian MLE; [[logistic-regression]] = Bernoulli MLE (cross-entropy).

<a id="confidence-intervals"></a>

## Confidence Intervals
<!-- section: confidence-intervals | prerequisites: [lln-clt, normal-distribution] | related: [hypothesis-testing, prediction-vs-confidence-interval, bootstrap] | sources: [src-squarepoint-dqa-workbook] | tags: [ci, t-interval] -->

### Formulas
$$\bar x\pm1.96\frac{\sigma}{\sqrt n}\ \ (\sigma\text{ known}),\qquad \bar x\pm t_{n-1,0.975}\frac{s}{\sqrt n}\ \ (\sigma\text{ unknown, normal data})$$

**Variables:**

- $\bar x$ sample mean
- $\sigma$ / $s$ true / sample std dev
- $n$ sample size
- $t_{\nu,u}$ $u$-quantile of $t_\nu$

### Key points
- **Interpretation:** 95% of intervals *built by this procedure* cover the fixed true $\mu$. A realised interval is not a 95% posterior probability.
- Example: $n=100$, $\bar x=0.2$, $s=1$ → approx $[0.004, 0.396]$.

### Connections
- **Dual of:** [[hypothesis-testing]]. **Non-parametric alternative:** [[bootstrap]]. **Regression version:** [[prediction-vs-confidence-interval]].

<a id="hypothesis-testing"></a>

## Hypothesis Testing, p-values & Power
<!-- section: hypothesis-testing | prerequisites: [confidence-intervals] | related: [multiple-testing, sharpe-ratio, conditional-probability-bayes, gauss-markov-assumptions] | sources: [src-squarepoint-dqa-workbook] | tags: [p-value, t-test, power] -->

### Formula
$$t=\frac{\bar x-\mu_0}{s/\sqrt n}\sim t_{n-1}\ \text{under }H_0\ (\text{iid normal})$$

**Variables:**

- $\mu_0$ null mean
- $\bar x,s,n$ sample mean, std dev, size

### Key points
- p-value $=P_{H_0}(|T|\ge|t_{obs}|)$. **Not** $P(H_0\text{ true})$, not "prob. it happened by chance". p = 0.03 ≠ 97% the alternative is true.
- Type I (reject true $H_0$, rate α) / Type II (miss, β) / power $=1-\beta$ ↑ with $n$, effect size, lower noise.
- Example: $n=100,\bar x=0.2,s=1$ → $t=2$, p ≈ 0.0455.
- Statistical significance ≠ profit after costs.
- **Sharpe link:** $t=\sqrt n\,\widehat{SR}_{\text{period}}$.

### Connections
- **Pitfall:** [[multiple-testing]]. **Finance:** [[sharpe-ratio]]. **Bayesian contrast:** [[conditional-probability-bayes]].

<a id="multiple-testing"></a>

## Multiple Testing & Selection Bias
<!-- section: multiple-testing | prerequisites: [hypothesis-testing] | related: [backtest-pitfalls, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [bonferroni, fdr, data-snooping] -->

### Formulas
$$E[\#\text{false rejections}]=m\alpha,\qquad P(\ge1\text{ false})=1-(1-\alpha)^m\ (\text{indep.}),\qquad \text{Bonferroni: test at }\alpha/m$$

**Variables:**

- $m$ number of true-null tests
- $\alpha$ per-test level

### Key points
- 1,000 true nulls at 5% → expect 50 false positives (no independence needed for the expectation).
- Bonferroni controls FWER without independence (conservative). FDR (e.g. BH) controls the expected share of false discoveries.
- **Finance:** searching thousands of signals and reporting the best Sharpe is selection bias; nominal p-values are misleading.

### Connections
- **Core cause of:** [[backtest-pitfalls]]. **Inflates:** [[sharpe-ratio]].

<a id="bootstrap"></a>

## Bootstrap (iid and block)
<!-- section: bootstrap | prerequisites: [confidence-intervals] | related: [stationarity-ar1, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [resampling] -->

### Key points
- Row-wise resampling assumes (approximately) iid rows.
- Serial dependence → **block bootstrap** (contiguous blocks; block length & stationarity matter).
- Not a cure for tiny samples or extreme tails.

### Connections
- **Alternative to:** analytic [[confidence-intervals]]. **Dependence issues:** [[stationarity-ar1]], [[effective-sample-size]].
