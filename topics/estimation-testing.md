---
id: estimation-testing
title: "Estimation & Hypothesis Testing"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Estimation & Hypothesis Testing

**Sections:** [[estimator-properties]] · [[linear-regression-assumptions]] · [[lln-clt]] · [[maximum-likelihood]] · [[confidence-intervals]] · [[hypothesis-testing]] · [[multiple-testing]] · [[bayesianized-p-value]] · [[bayesian-p-value]] · [[bootstrap]]

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
<!-- section: linear-regression-assumptions | prerequisites: [ols-regression, estimator-properties, hypothesis-testing] | related: [gauss-markov-assumptions, robust-standard-errors, omitted-variable-bias, multicollinearity, regression-invariances, stationarity-ar1, effective-sample-size] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [linear-regression, assumptions, gauss-markov, violations] -->

For the linear model

$$Y=X\beta+\varepsilon,\qquad \hat\beta=(X^\top X)^{-1}X^\top Y=\beta+(X^\top X)^{-1}X^\top\varepsilon$$

**Variables:**

- $Y$ $N\times1$ dependent variable (e.g. fund returns)
- $X$ $N\times k$ design matrix of regressors (e.g. factor returns)
- $\beta$ $k\times1$ true coefficients
- $\varepsilon$ $N\times1$ errors
- $\hat\beta$ OLS estimate of $\beta$

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

### Key points interviewers look for

- **Gauss–Markov:** under linearity, independent sampling, full rank, exogeneity and $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$, OLS is **BLUE** (Best Linear Unbiased Estimator; "best" = minimum variance among linear unbiased estimators).
- **Only endogeneity causes bias.** Heteroskedasticity / autocorrelation break the SEs, not the coefficients.
- **Normality is not required** for BLUE; with large $N$ the CLT makes t-tests approximately valid.
- Linearity is in **β**, not in $X$: using $x^2$ or $\log x$ as a regressor is still linear regression.
- **Sources of endogeneity:** omitted variables, measurement error in $X$, simultaneity / reverse causality.

### Diagnostics and fixes

| Problem | Test | Fix |
|---|---|---|
| Heteroskedasticity | Breusch–Pagan, White; fan-shaped residual plot | White/HC robust SE, WLS |
| Autocorrelation | Durbin–Watson, Breusch–Godfrey, Ljung–Box | Newey–West (HAC) SE, GLS |
| Multicollinearity (imperfect) | VIF > 10, condition number | Drop/combine, ridge, PCA |
| Endogeneity | Hausman test | IV / 2SLS |
| Non-normality | Jarque–Bera, QQ plot | Large $N$, bootstrap |

### Finance and time-series failure modes

- **Autocorrelated or duplicated rows:** the apparent sample size is too large; naive annualisation and standard errors overstate precision. See [[effective-sample-size]] and [[regression-invariances]].
- **Non-stationary levels:** a regression can be highly significant but spurious; stationarity must be checked before interpreting the slope. See [[stationarity-ar1]].
- **Look-ahead or post-decision data:** OLS can fit an impossible information set and produce an inflated fit or backtest; this is a data-construction failure, not something robust SEs repair. See [[cross-validation-leakage]].

### Factor-regression angle (自己推理)

In factor regressions $R_{p,t}-R_{f,t}=\alpha+\beta^\top F_t+\varepsilon_t$:

- **Overlapping returns** (monthly data, 12-month windows) → autocorrelation by construction → Newey–West SEs.
- **Volatility clustering** → heteroskedasticity almost always present → HAC SEs.
- **Correlated factors** (Value vs Profitability) → unstable betas, overall fit unaffected ([[multicollinearity]]).
- **Omitted factor** → shows up as spurious **alpha** ([[omitted-variable-bias]]).

**One-liner:** "Only exogeneity threatens unbiasedness. Heteroskedasticity and autocorrelation only affect inference, so in finance we almost always use robust or HAC standard errors."

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

## Multiple Testing & Selection Bias (FWER, FDR, Holm)
<!-- section: multiple-testing | prerequisites: [hypothesis-testing] | related: [backtest-pitfalls, sharpe-ratio, bayesianized-p-value, information-coefficient] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [bonferroni, fdr, fwer, holm, data-snooping, factor-zoo] -->

### Formulas
$$E[\#\text{false rejections}]=m\alpha,\qquad \text{FWER}=P(V\ge1),\qquad \text{FWER}_{\text{indep}}=1-(1-\alpha)^m,\qquad \text{FDR}=E\Big[\frac{V}{R}\Big]$$

**Variables:**

- $m$ number of hypotheses
- $V$ number of false discoveries (true nulls rejected)
- $R$ total rejections ($V/R:=0$ if $R=0$)
- $\alpha$ per-test level

| $m$ | 1 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|
| FWER at α=5% | 5.0% | 22.6% | 40.1% | 64.2% | 92.3% | 99.4% |

### Key points
- 1,000 true nulls at 5% → expect 50 false positives (no independence needed for the expectation).
- **Weak control:** FWER ≤ α only when all nulls are true. **Strong control:** for any configuration (what we want; Bonferroni/Holm/Hochberg give it).
- **Finance:** searching thousands of signals and reporting the best Sharpe is selection bias; nominal p-values are misleading. Harvey–Liu–Zhu derive a **t ≈ 3** hurdle under Holm.

### Procedures

| Procedure | Rule | Assumption |
|---|---|---|
| Bonferroni | $p_i\le\alpha/m$ | None (conservative) |
| Šidák | $p_i\le1-(1-\alpha)^{1/m}$ | Independence |
| Holm (step-down) | $p_{(k)}\le\alpha/(m-k+1)$ | None; dominates Bonferroni |
| Hochberg (step-up) | same thresholds, from the largest | Independence / positive dependence |
| Romano–Wolf | bootstrap step-down | Exploits dependence |
| Benjamini–Hochberg | largest $k$ with $p_{(k)}\le k\alpha/m$ | FDR; indep / PRDS |
| Benjamini–Yekutieli | BH with extra penalty | FDR; any dependence |

| | FWER | FDR |
|---|---|---|
| Controls | $P(V\ge1)$ | $E[V/R]$ |
| Question | "Any mistake?" | "What fraction of discoveries are mistakes?" |
| Power | Lower | Higher |
| Use | Confirmatory, concentrated bets | Exploratory signal screening |

### Worked example (10 factors, α = 5%)

p-values: 0.001, 0.008, 0.012, 0.025, 0.035, 0.044, 0.06, 0.10, 0.15, 0.40

| Method | Result |
|---|---|
| Naive | 6 significant |
| Bonferroni (0.005) | 1 |
| Holm | k=1: 0.001 ≤ 0.005 ✓; k=2: 0.008 > 0.0056 ✗ stop → **1** |
| BH (threshold $0.005k$) | k=1 ✓ (0.005), k=2 ✓ (0.010), k=3 ✓ (0.015), k=4 ✗ 0.025 > 0.020, k=5 ✗ 0.035 > 0.025, k=6 ✗ 0.044 > 0.030 → **3** |

✏️ Correction: the original chat said BH ≈ 5; applying the BH rule (largest $k$ with $p_{(k)}\le k\alpha/m$) gives **3**. Conclusion unchanged: naive 6 → FWER 1 → FDR 3; the method choice matters a lot.

**Subtleties:** "family" is a researcher degree of freedom (pre-register it); FWER becomes useless at large $m$ (genomics moved to FDR); controls frequency, not magnitude; don't mix one- and two-sided p-values.

### Holm–Bonferroni step-down

1. Sort: $p_{(1)}\le\dots\le p_{(m)}$.
2. Threshold: $\alpha/(m-k+1)$.
3. Reject while $p_{(k)}\le\alpha/(m-k+1)$; at the first failure, **stop** and keep all remaining nulls.

**Variables:**

- $k$ rank (1 = smallest)
- $m-k+1$ hypotheses not yet rejected

| k | Factor | $p_{(k)}$ | Threshold | Decision |
|---|---|---|---|---|
| 1 | Value | 0.003 | 0.010 | reject |
| 2 | Momentum | 0.008 | 0.0125 | reject |
| 3 | Quality | 0.020 | 0.0167 | **stop** |
| 4 | Low-vol | 0.030 | 0.025 | not tested |
| 5 | Growth | 0.045 | 0.050 | not tested: even though 0.045 ≤ 0.05, you never reach back after stopping |

Bonferroni (0.01 for all) keeps only Value; Holm keeps Value + Momentum at the same FWER.

- **Why it works:** after rejecting one, only $m-k$ nulls can still be true, so the error budget is recycled. Strong FWER control under **any dependence** (closed testing principle, Marcus–Peritz–Gabriel 1976).
- Holm is uniformly more powerful than Bonferroni at no cost. Correlated factors: still valid but conservative → Romano–Wolf.

### Holm-adjusted p-values

$$\tilde p_{(k)}=\min\Big(\max_{j\le k}\big[(m-j+1)\,p_{(j)}\big],\ 1\Big),\qquad \text{reject }H_{(k)}\iff\tilde p_{(k)}\le\alpha$$

**Variables:**

- $\tilde p_{(k)}$ adjusted p-value for rank $k$
- $p_{(j)}$ $j$-th smallest raw p-value
- running max enforces monotonicity; cap at 1 keeps a valid probability

| k | Raw p | ×(m−k+1) | Running max | Adjusted | Bonferroni min(5p,1) |
|---|---|---|---|---|---|
| 1 | 0.003 | 0.015 | 0.015 | **0.015** | 0.015 |
| 2 | 0.008 | 0.032 | 0.032 | **0.032** | 0.040 |
| 3 | 0.020 | 0.060 | 0.060 | **0.060** | 0.100 |
| 4 | 0.030 | 0.060 | 0.060 | **0.060** | 0.150 |
| 5 | 0.045 | 0.045 | 0.060 | **0.060** | 0.225 |

Same decisions as the step-down procedure. If Momentum had $p=0.011$: Bonferroni 0.055 (fail), Holm 0.044 (reject).

```python
from statsmodels.stats.multitest import multipletests
reject, adj_p, _, _ = multipletests([0.003, 0.008, 0.020, 0.030, 0.045], alpha=0.05, method='holm')
# adj_p: [0.015, 0.032, 0.060, 0.060, 0.060]; returned in original input order
```

```r
p.adjust(c(0.003, 0.008, 0.020, 0.030, 0.045), method = "holm")
```

**Interpretation:** the smallest family-wise α at which $H_i$ can be rejected; still frequentist, **not** $P(H_0\mid\text{data})$ (see [[bayesianized-p-value]]).

### Connections
- **Core cause of:** [[backtest-pitfalls]]. **Inflates:** [[sharpe-ratio]].
- **Bayesian alternative:** [[bayesianized-p-value]] (priors on $H_0$ per factor family).

<a id="bayesianized-p-value"></a>

## Bayesianized p-values: Priors on H₀ & the Minimum Bayes Factor
<!-- section: bayesianized-p-value | prerequisites: [hypothesis-testing, conditional-probability-bayes] | related: [multiple-testing, bayesian-p-value, backtest-pitfalls] | sources: [src-quant-finance-study-notes] | tags: [bayes-factor, mbf, prior, factor-zoo, harvey] -->

A report converts a frequentist p-value into $P(H_0\mid\text{data})$, with $H_0$: the factor has no true premium (Harvey framework).

### Formula
$$P(H_0\mid\text{data})=\frac{\pi_0\cdot BF_{01}}{\pi_0\cdot BF_{01}+(1-\pi_0)},\qquad MBF=-e\cdot p\cdot\ln(p)\ \ (p<1/e)$$

**Variables:**

- $\pi_0$ prior probability the null is true
- $BF_{01}$ Bayes factor $p(\text{data}\mid H_0)/p(\text{data}\mid H_1)$, approximated by the MBF
- $MBF$ Minimum Bayes Factor: lower bound over reasonable alternatives (the most favourable case for $H_1$; Sellke–Bayarri–Berger 2001)
- $p$ frequentist p-value
- $e\approx2.718$

| Factor family | $\pi_0$ | Meaning |
|---|---|---|
| Value | 0.50 | Agnostic: long theoretical and empirical record |
| Growth | 0.75 | 3:1 prior odds against: poor out-of-sample record |
| Others | 0.66 | ~2:1 against: default factor-zoo skepticism |

**Example:** $p=0.01$ → $MBF\approx0.125$.

- Value: $\frac{0.5\times0.125}{0.5\times0.125+0.5}\approx$ **11.1%** chance spurious.
- Growth: $\frac{0.75\times0.125}{0.75\times0.125+0.25}\approx$ **27.3%** chance spurious.

Same evidence, different conclusion. Background: Harvey, Liu & Zhu (2016): hundreds of "discovered" factors → $t>2$ is too lax.

- **Why different priors?** Different track records and theory → different credibility.
- **Isn't that snooping the prior?** Priors must be set **before** testing and disclosed (pre-registration).
- **How to set it?** Replication base rates for that family; expert elicitation; sensitivity across a range of $\pi_0$.

### Understanding π₀

$$P(H_0\mid\text{data})=\frac{P(\text{data}\mid H_0)\cdot\pi_0}{P(\text{data})}$$

**Variables:**

- $P(H_0\mid\text{data})$ posterior (what decisions need)
- $P(\text{data}\mid H_0)$ likelihood under the null
- $\pi_0$ prior
- $P(\text{data})$ normalising constant

- You cannot invert "P(data | H)" into "P(H | data)" without a prior.
- **Sources of π₀ (not just consensus):** empirical base rates (most defensible; e.g. 70% of growth factors fail to replicate → 0.70) · expert belief · non-informative 0.5 · pre-registered priors · decision-theoretic (target FDR). The question is *what fraction of hypotheses in this reference class are true*.

### What if the prior is wrong?

$$\frac{P(H_0\mid\text{data})}{P(H_1\mid\text{data})}=\frac{\pi_0}{1-\pi_0}\times BF_{01}$$

**Variables:**

- left side: posterior odds
- $\frac{\pi_0}{1-\pi_0}$ prior odds
- $BF_{01}$ Bayes factor

- (a) **Bar too high:** $\pi_0=0.95$ → prior odds 19:1; reaching posterior odds 1:10 needs $BF_{01}\le1/190$ ($t\gg3$) → real effects missed (Type II).
- (b) **Infinite data washes out the prior** (if $0<\pi_0<1$), but return samples are finite.
- (c) **Dogmatic priors** ($\pi_0=1$) = faith, not analysis.
- **Mitigation:** sensitivity analysis over $\pi_0\in\{0.25,0.5,0.75,0.9\}$.

### Equivalent π₀ for a frequentist p-value

$$\pi_0^{\text{equiv}}=\frac{p}{MBF\cdot(1-p)+p}$$

**Variables:**

- $\pi_0^{\text{equiv}}$ prior that would make the posterior equal $p$

| $p$ | MBF | $\pi_0^{\text{equiv}}$ |
|---|---|---|
| 0.10 | 0.626 | 0.151 |
| 0.05 | 0.407 | 0.114 |
| 0.01 | 0.125 | 0.075 |
| 0.001 | 0.018 | 0.052 |

- **Key insight:** reading $p=0.05$ as "5% chance the null is true" implicitly assumes you were already ~89% sure the effect was real. With $\pi_0=0.5$, $p=0.05$ → $P(H_0\mid\text{data})\approx$ **28.9%**, ~6× larger (Sellke–Bayarri–Berger).
- Why not always 0.5? The base rate of true factors is much lower. Link to FDR: both target the share of false rejections; Storey's q-value bridges them. Frequentist tests have an implicit prior too.

### Where is the p-value in Bayes' theorem?

**It does not appear directly.**

$$p=P\big(T(\text{data})\ge T(\text{observed})\mid H_0\big)\quad\text{vs.}\quad P(\text{data}\mid H_0)$$

**Variables:**

- $T(\cdot)$ test statistic (e.g. t-stat)

| | p-value | Likelihood in Bayes |
|---|---|---|
| Object | Tail probability (integral) | Point density |
| Data considered | Observed **+ more extreme** | Only observed |

**Chain:** $p\longrightarrow MBF\longrightarrow$ posterior odds $\longrightarrow$ posterior probability of $H_0$.

### Worked example: t = 2.5, p = 0.012, π₀ = 0.66

1. MBF $=-2.718\times0.012\times\ln(0.012)\approx0.144$ (data only ~6.9× more likely under $H_1$ at best).
2. Prior odds $0.66/0.34\approx1.94$.
3. Posterior odds $1.94\times0.144\approx0.279$.
4. $P(H_0\mid\text{data})=0.279/1.279\approx$ **21.8%**, 18× the p-value.

| Misconception | Reality |
|---|---|
| p = P(data \| H₀) | No: tail integral, not a density |
| p = P(H₀ \| data) | No: that's the posterior (**prosecutor's fallacy**) |
| Bayes uses p as likelihood | No: MBF is a transformation approximating the likelihood ratio |

**Why MBF?** A real Bayes factor needs a full alternative (a prior on alpha size). MBF gives $H_1$ its best shot → conservative toward $H_0$, desirable for a factor zoo. Breaks down for $p\ge1/e$ or tiny samples.

### Connections
- **Builds on:** [[conditional-probability-bayes]] (posterior odds = prior odds × likelihood ratio), [[hypothesis-testing]].
- **Frequentist counterpart:** [[multiple-testing]]. **Model-checking cousin:** [[bayesian-p-value]].

<a id="bayesian-p-value"></a>

## Bayesian (Posterior Predictive) p-value
<!-- section: bayesian-p-value | prerequisites: [conditional-probability-bayes, hypothesis-testing] | related: [bayesianized-p-value, monte-carlo-pricing] | sources: [src-quant-finance-study-notes] | tags: [posterior-predictive, model-checking, mcmc] -->

A model-checking tool: *"If my model is correct, how unusual is the data I actually saw?"*

### Formula
$$p_B=\Pr\big(T(y_{\text{rep}},\theta)\ge T(y_{\text{obs}},\theta)\ \big|\ y_{\text{obs}}\big),\qquad \hat p_B=\frac1S\sum_{s=1}^S\mathbb 1\big\{T(y_{\text{rep}}^{(s)},\theta^{(s)})\ge T(y_{\text{obs}},\theta^{(s)})\big\}$$

**Variables:**

- $y_{\text{obs}}$ observed data
- $y_{\text{rep}}$ replicated data from the posterior predictive $p(y_{\text{rep}}\mid y_{\text{obs}})$
- $\theta$ parameters drawn from the posterior $p(\theta\mid y_{\text{obs}})$
- $T(\cdot,\cdot)$ discrepancy measure (max, variance, tail, autocorrelation…)
- $S$ number of posterior draws
- $\mathbb 1\{\cdot\}$ indicator

**MCMC recipe:** draw $\theta^{(s)}$ → simulate $y_{\text{rep}}^{(s)}$ → compare $T$ → average the indicator.

### Key points
- $p_B\approx0.5$ = typical (good fit); near 0 or 1 = model fails to reproduce that feature. A diagnostic, not a test (no Type I error rate).

| Aspect | Frequentist p-value | Bayesian (PPP) p-value |
|---|---|---|
| Null distribution | Fixed θ (point null) | Marginalised over the posterior |
| Replication | Resampling under $H_0$ | Posterior predictive draws |
| Statistic | $T(y)$ | Can be $T(y,\theta)$ |
| Purpose | Reject/accept | Diagnose fit |
| Uniform under truth? | Yes | **No**: conservative (pulled toward 0.5) |

- **Weakness:** "double use" of data (Bayarri & Berger 2000) → low power. Fixes: partial / conditional predictive p-values.
- **Why not uniform?** The posterior conditions on $y_{\text{obs}}$, so $y_{\text{rep}}$ is pulled toward $y_{\text{obs}}$.
- **How to choose T?** A feature the model is **not** fit to (e.g. skewness/max for a Gaussian fit by mean/variance).
- **PPP vs Bayes factor:** PPP = absolute fit of one model; BF = relative fit between models.

### Connections
- **Contrast:** [[hypothesis-testing]] (frequentist p-value), [[bayesianized-p-value]] (posterior probability of $H_0$).

<a id="bootstrap"></a>

## Bootstrap (iid and block)
<!-- section: bootstrap | prerequisites: [confidence-intervals] | related: [stationarity-ar1, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [resampling] -->

### Key points
- Row-wise resampling assumes (approximately) iid rows.
- Serial dependence → **block bootstrap** (contiguous blocks; block length & stationarity matter).
- Not a cure for tiny samples or extreme tails.

### Connections
- **Alternative to:** analytic [[confidence-intervals]]. **Dependence issues:** [[stationarity-ar1]], [[effective-sample-size]].
