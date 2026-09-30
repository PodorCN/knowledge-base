---
id: statistical-testing
title: "Hypothesis Testing"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Hypothesis Testing

This chapter covers deciding whether an effect is real: the single t-test and what a p-value does (and does not) mean, what goes wrong when many hypotheses are tested at once, and two Bayesian readings of the p-value. In finance this is the statistics of "is this signal or this Sharpe ratio genuine?".

**Prerequisites:** [[confidence-intervals]], [[conditional-probability-bayes]].

**Leads to:** [[gauss-markov-assumptions]] (t and F tests in regression), [[sharpe-ratio]] (a Sharpe ratio is a t-statistic), [[backtest-pitfalls]] (selection bias).

**Sections:** [[hypothesis-testing]] · [[multiple-testing]] · [[bayesianized-p-value]] · [[bayesian-p-value]]

<a id="hypothesis-testing"></a>

## Hypothesis Testing, p-values & Power
<!-- section: hypothesis-testing | prerequisites: [confidence-intervals] | related: [multiple-testing, sharpe-ratio, conditional-probability-bayes, gauss-markov-assumptions] | sources: [src-squarepoint-dqa-workbook] | tags: [p-value, t-test, power] -->

A test fixes a null hypothesis, computes a statistic, and asks how extreme the statistic would be if the null were true.

### Formula
$$t=\frac{\bar x-\mu_0}{s/\sqrt n}\sim t_{n-1}\ \text{under }H_0\ \text{(iid normal data)},\qquad p=P_{H_0}\big(|T|\ge|t_{\text{obs}}|\big)$$

**Variables:**

- $H_0$ null hypothesis ($\mu=\mu_0$)
- $\mu_0$ null mean
- $\bar x$ sample mean
- $s$ sample standard deviation
- $n$ sample size
- $T$ the test statistic as a random variable under $H_0$
- $t_{\text{obs}}$ the observed value of the statistic
- $p$ two-sided p-value

### Key points
- The p-value is **not** $P(H_0\text{ true})$, and not "the probability it happened by chance". $p=0.03$ does not mean 97% that the alternative is true ([[bayesianized-p-value]]).
- **Type I error:** reject a true $H_0$ (rate $\alpha$). **Type II error:** miss a true effect (rate $\beta$). **Power** $=1-\beta$ rises with $n$, effect size and lower noise.
- Statistical significance ≠ profit after costs.
- **Sharpe link:** $t=\sqrt n\,\widehat{SR}_{\text{period}}$ ([[sharpe-ratio]]).

### Worked example
$n=100$, $\bar x=0.2$, $s=1$ → $t=0.2/(1/10)=2$, $p\approx0.0455$ (compare the interval in [[confidence-intervals]]).

### Connections
- **Builds on:** [[confidence-intervals]] (duality).
- **Pitfall:** [[multiple-testing]]. **Finance:** [[sharpe-ratio]]. **Bayesian contrast:** [[conditional-probability-bayes]], [[bayesianized-p-value]].

<a id="multiple-testing"></a>

## Multiple Testing & Selection Bias (FWER, FDR, Holm)
<!-- section: multiple-testing | prerequisites: [hypothesis-testing] | related: [backtest-pitfalls, sharpe-ratio, bayesianized-p-value, information-coefficient] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [bonferroni, fdr, fwer, holm, data-snooping, factor-zoo] -->

Testing many hypotheses at level $\alpha$ each almost guarantees some false discoveries. Corrections either control the probability of any false discovery (FWER) or the expected fraction of false discoveries (FDR).

### Formulas
$$E[\#\text{false rejections}]=m\alpha,\qquad \text{FWER}=P(V\ge1),\qquad \text{FWER}_{\text{indep}}=1-(1-\alpha)^m,\qquad \text{FDR}=E\Big[\frac{V}{R}\Big]$$

**Variables:**

- $m$ number of hypotheses (all nulls true in the first and third formulas)
- $\alpha$ per-test significance level
- $V$ number of false discoveries (true nulls rejected)
- $R$ total number of rejections ($V/R:=0$ if $R=0$)
- FWER family-wise error rate
- FDR false discovery rate

| $m$ | 1 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|
| FWER at α = 5% | 5.0% | 22.6% | 40.1% | 64.2% | 92.3% | 99.4% |

### Key points
- 1,000 true nulls tested at 5% → expect 50 false positives (no independence needed for the expectation).
- **Weak control:** FWER ≤ α only when all nulls are true. **Strong control:** FWER ≤ α for any configuration of true and false nulls (what we want; Bonferroni, Holm and Hochberg give it).
- **Finance:** searching thousands of signals and reporting the best Sharpe is selection bias; nominal p-values are misleading. Harvey–Liu–Zhu derive a **t ≈ 3** hurdle under Holm.

### Procedures

| Procedure | Rule | Assumption |
|---|---|---|
| Bonferroni | $p_i\le\alpha/m$ | None (conservative) |
| Šidák | $p_i\le1-(1-\alpha)^{1/m}$ | Independence |
| Holm (step-down) | $p_{(k)}\le\alpha/(m-k+1)$ | None; dominates Bonferroni |
| Hochberg (step-up) | same thresholds, starting from the largest | Independence / positive dependence |
| Romano–Wolf | bootstrap step-down | Exploits dependence |
| Benjamini–Hochberg | largest $k$ with $p_{(k)}\le k\alpha/m$ | FDR; independence / PRDS |
| Benjamini–Yekutieli | BH with an extra penalty | FDR; any dependence |

Here $p_i$ is the p-value of hypothesis $i$ and $p_{(k)}$ the $k$-th smallest p-value.

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
| Bonferroni (threshold 0.005) | 1 |
| Holm | k=1: 0.001 ≤ 0.005 ✓; k=2: 0.008 > 0.0056 ✗ stop → **1** |
| BH (threshold $0.005k$) | k=1 ✓ (0.005), k=2 ✓ (0.010), k=3 ✓ (0.015), k=4 ✗ 0.025 > 0.020, k=5 ✗ 0.035 > 0.025, k=6 ✗ 0.044 > 0.030 → **3** |

✏️ Correction: the original chat said BH ≈ 5; applying the BH rule (largest $k$ with $p_{(k)}\le k\alpha/m$) gives **3**. Conclusion unchanged: naive 6 → FWER 1 → FDR 3; the method choice matters a lot.

**Subtleties:** the "family" is a researcher degree of freedom (pre-register it); FWER becomes useless at large $m$ (genomics moved to FDR); both control frequency, not magnitude; don't mix one- and two-sided p-values.

### Holm–Bonferroni step-down

1. Sort: $p_{(1)}\le\dots\le p_{(m)}$.
2. Threshold for rank $k$: $\alpha/(m-k+1)$.
3. Reject while $p_{(k)}\le\alpha/(m-k+1)$; at the first failure, **stop** and keep all remaining nulls.

**Variables:**

- $k$ rank (1 = smallest p-value)
- $m-k+1$ number of hypotheses not yet rejected

| k | Factor | $p_{(k)}$ | Threshold | Decision |
|---|---|---|---|---|
| 1 | Value | 0.003 | 0.010 | reject |
| 2 | Momentum | 0.008 | 0.0125 | reject |
| 3 | Quality | 0.020 | 0.0167 | **stop** |
| 4 | Low-vol | 0.030 | 0.025 | not tested |
| 5 | Growth | 0.045 | 0.050 | not tested: even though 0.045 ≤ 0.05, you never reach back after stopping |

Bonferroni (0.01 for all) keeps only Value; Holm keeps Value + Momentum at the same FWER.

- **Why it works:** after rejecting one hypothesis, only $m-k$ nulls can still be true, so the error budget is recycled. Strong FWER control under **any dependence** (closed testing principle, Marcus–Peritz–Gabriel 1976).
- Holm is uniformly more powerful than Bonferroni at no cost. With correlated factors it is still valid but conservative → Romano–Wolf.

### Holm-adjusted p-values

$$\tilde p_{(k)}=\min\Big(\max_{j\le k}\big[(m-j+1)\,p_{(j)}\big],\ 1\Big),\qquad \text{reject }H_{(k)}\iff\tilde p_{(k)}\le\alpha$$

**Variables:**

- $\tilde p_{(k)}$ adjusted p-value for rank $k$
- $p_{(j)}$ $j$-th smallest raw p-value
- $H_{(k)}$ hypothesis with the $k$-th smallest p-value

The running maximum enforces monotonicity; the cap at 1 keeps a valid probability.

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

**Interpretation:** the adjusted p-value is the smallest family-wise α at which $H_i$ can be rejected; it is still frequentist, **not** $P(H_0\mid\text{data})$ (see [[bayesianized-p-value]]).

### Connections
- **Builds on:** [[hypothesis-testing]].
- **Core cause of:** [[backtest-pitfalls]]. **Inflates:** [[sharpe-ratio]].
- **Bayesian alternative:** [[bayesianized-p-value]] (priors on $H_0$ per factor family).

<a id="bayesianized-p-value"></a>

## Bayesianized p-values: Priors on H₀ & the Minimum Bayes Factor
<!-- section: bayesianized-p-value | prerequisites: [hypothesis-testing, conditional-probability-bayes] | related: [multiple-testing, bayesian-p-value, backtest-pitfalls] | sources: [src-quant-finance-study-notes] | tags: [bayes-factor, mbf, prior, factor-zoo, harvey] -->

A p-value cannot by itself say how likely the null is. Combining it with a prior probability of the null through a (minimum) Bayes factor converts it into $P(H_0\mid\text{data})$ — here with $H_0$: "the factor has no true premium" (Harvey framework).

### Formula
$$P(H_0\mid\text{data})=\frac{\pi_0\cdot BF_{01}}{\pi_0\cdot BF_{01}+(1-\pi_0)},\qquad MBF=-e\cdot p\cdot\ln(p)\ \ (p<1/e)$$

**Variables:**

- $\pi_0$ prior probability that the null is true
- $BF_{01}$ Bayes factor $p(\text{data}\mid H_0)/p(\text{data}\mid H_1)$, approximated by the MBF
- $MBF$ minimum Bayes factor: lower bound over reasonable alternatives, i.e. the most favourable case for $H_1$ (Sellke–Bayarri–Berger 2001)
- $p$ frequentist p-value
- $e\approx2.718$ Euler's number

| Factor family | $\pi_0$ | Meaning |
|---|---|---|
| Value | 0.50 | Agnostic: long theoretical and empirical record |
| Growth | 0.75 | 3:1 prior odds against: poor out-of-sample record |
| Others | 0.66 | ~2:1 against: default factor-zoo skepticism |

### Worked example
$p=0.01$ → $MBF\approx0.125$.

- Value: $\frac{0.5\times0.125}{0.5\times0.125+0.5}\approx$ **11.1%** chance the factor is spurious.
- Growth: $\frac{0.75\times0.125}{0.75\times0.125+0.25}\approx$ **27.3%** chance the factor is spurious.

Same evidence, different conclusion. Background: Harvey, Liu & Zhu (2016) — with hundreds of "discovered" factors, $t>2$ is too lax.

- **Why different priors?** Different track records and theory → different credibility.
- **Isn't that snooping the prior?** Priors must be set **before** testing and disclosed (pre-registration).
- **How to set it?** Replication base rates for that family; expert elicitation; sensitivity across a range of $\pi_0$.

### Understanding π₀

$$P(H_0\mid\text{data})=\frac{P(\text{data}\mid H_0)\cdot\pi_0}{P(\text{data})}$$

**Variables:**

- $P(H_0\mid\text{data})$ posterior probability of the null (what decisions need)
- $P(\text{data}\mid H_0)$ likelihood of the data under the null
- $\pi_0$ prior probability of the null
- $P(\text{data})$ normalising constant

**Notes:**

- You cannot invert "P(data | H)" into "P(H | data)" without a prior ([[conditional-probability-bayes]]).
- **Sources of π₀ (not just consensus):** empirical base rates (most defensible; e.g. 70% of growth factors fail to replicate → 0.70) · expert belief · non-informative 0.5 · pre-registered priors · decision-theoretic (target FDR). The question is *what fraction of hypotheses in this reference class are true*.

### What if the prior is wrong?

$$\frac{P(H_0\mid\text{data})}{P(H_1\mid\text{data})}=\frac{\pi_0}{1-\pi_0}\times BF_{01}$$

**Variables:**

- left side: posterior odds of the null
- $\frac{\pi_0}{1-\pi_0}$ prior odds of the null
- $BF_{01}$ Bayes factor

**Cases:**

- (a) **Bar too high:** $\pi_0=0.95$ → prior odds 19:1; reaching posterior odds 1:10 needs $BF_{01}\le1/190$ ($t\gg3$) → real effects missed (Type II).
- (b) **Infinite data washes out the prior** (if $0<\pi_0<1$), but return samples are finite.
- (c) **Dogmatic priors** ($\pi_0=1$) = faith, not analysis.
- **Mitigation:** sensitivity analysis over $\pi_0\in\{0.25,0.5,0.75,0.9\}$.

### Equivalent π₀ for a frequentist p-value

$$\pi_0^{\text{equiv}}=\frac{p}{MBF\cdot(1-p)+p}$$

**Variables:**

- $\pi_0^{\text{equiv}}$ prior that would make the posterior $P(H_0\mid\text{data})$ equal to $p$
- $p$ p-value
- $MBF$ minimum Bayes factor at that $p$

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

$$p=P\big(T(\text{data})\ge T(\text{observed})\mid H_0\big)\qquad\text{vs.}\qquad P(\text{data}\mid H_0)$$

**Variables:**

- $T(\cdot)$ test statistic (e.g. t-stat)
- $p$ tail probability under the null
- $P(\text{data}\mid H_0)$ likelihood (point density) under the null

| | p-value | Likelihood in Bayes |
|---|---|---|
| Object | Tail probability (integral) | Point density |
| Data considered | Observed **+ more extreme** | Only observed |

**Chain:** $p\longrightarrow MBF\longrightarrow$ posterior odds $\longrightarrow$ posterior probability of $H_0$.

### Worked example: t = 2.5, p = 0.012, π₀ = 0.66

1. $MBF=-2.718\times0.012\times\ln(0.012)\approx0.144$ (the data are only ~6.9× more likely under $H_1$ at best).
2. Prior odds $0.66/0.34\approx1.94$.
3. Posterior odds $1.94\times0.144\approx0.279$.
4. $P(H_0\mid\text{data})=0.279/1.279\approx$ **21.8%**, 18× the p-value.

| Misconception | Reality |
|---|---|
| p = P(data \| H₀) | No: a tail integral, not a density |
| p = P(H₀ \| data) | No: that's the posterior (**prosecutor's fallacy**) |
| Bayes uses p as the likelihood | No: MBF is a transformation approximating the likelihood ratio |

**Why MBF?** A real Bayes factor needs a full alternative (a prior on the size of alpha). MBF gives $H_1$ its best shot → conservative toward $H_0$, desirable for a factor zoo. It breaks down for $p\ge1/e$ or tiny samples.

### Connections
- **Builds on:** [[conditional-probability-bayes]] (posterior odds = prior odds × likelihood ratio), [[hypothesis-testing]].
- **Frequentist counterpart:** [[multiple-testing]]. **Model-checking cousin:** [[bayesian-p-value]].

<a id="bayesian-p-value"></a>

## Bayesian (Posterior Predictive) p-value
<!-- section: bayesian-p-value | prerequisites: [conditional-probability-bayes, hypothesis-testing] | related: [bayesianized-p-value, monte-carlo-pricing] | sources: [src-quant-finance-study-notes] | tags: [posterior-predictive, model-checking, mcmc] -->

A model-checking tool, not a test of a null: *"If my model is correct, how unusual is the data I actually saw?"*

### Formula
$$p_B=\Pr\big(T(y_{\text{rep}},\theta)\ge T(y_{\text{obs}},\theta)\ \big|\ y_{\text{obs}}\big),\qquad \hat p_B=\frac1S\sum_{s=1}^S\mathbb 1\big\{T(y_{\text{rep}}^{(s)},\theta^{(s)})\ge T(y_{\text{obs}},\theta^{(s)})\big\}$$

**Variables:**

- $p_B$ posterior predictive p-value; $\hat p_B$ its simulation estimate
- $y_{\text{obs}}$ observed data
- $y_{\text{rep}}$ replicated data drawn from the posterior predictive $p(y_{\text{rep}}\mid y_{\text{obs}})$
- $\theta$ parameters drawn from the posterior $p(\theta\mid y_{\text{obs}})$
- $T(\cdot,\cdot)$ discrepancy measure (max, variance, tail, autocorrelation…)
- $S$ number of posterior draws, indexed by $s$
- $\mathbb 1\{\cdot\}$ indicator

**MCMC recipe:** draw $\theta^{(s)}$ → simulate $y_{\text{rep}}^{(s)}$ → compare $T$ → average the indicator.

### Key points
- $p_B\approx0.5$ = typical (good fit); near 0 or 1 = the model fails to reproduce that feature. It is a diagnostic, not a test (no Type I error rate).

| Aspect | Frequentist p-value | Bayesian (PPP) p-value |
|---|---|---|
| Null distribution | Fixed θ (point null) | Marginalised over the posterior |
| Replication | Resampling under $H_0$ | Posterior predictive draws |
| Statistic | $T(y)$ | Can be $T(y,\theta)$ |
| Purpose | Reject/accept | Diagnose fit |
| Uniform under truth? | Yes | **No**: conservative (pulled toward 0.5) |

- **Weakness:** "double use" of the data (Bayarri & Berger 2000) → low power. Fixes: partial / conditional predictive p-values.
- **Why not uniform?** The posterior conditions on $y_{\text{obs}}$, so $y_{\text{rep}}$ is pulled toward $y_{\text{obs}}$.
- **How to choose T?** A feature the model is **not** fitted to (e.g. skewness or the maximum for a Gaussian fitted by mean and variance).
- **PPP vs Bayes factor:** PPP measures the absolute fit of one model; a Bayes factor measures relative fit between models.

### Connections
- **Contrast:** [[hypothesis-testing]] (frequentist p-value), [[bayesianized-p-value]] (posterior probability of $H_0$).
