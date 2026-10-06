---
id: linear-regression
title: "Linear Regression"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Linear Regression

Linear regression is the workhorse of signal research: betas, factor loadings, alphas and forecasts are all regression coefficients. This chapter derives OLS, measures fit, states the assumptions behind unbiasedness and valid inference, and then goes through each way the assumptions fail — heteroskedasticity and autocorrelation, omitted variables, multicollinearity — and how the answers change under simple data transformations.

**Prerequisites:** [[variance-covariance-correlation]], [[conditional-expectation-best-predictor]], [[estimator-properties]], [[hypothesis-testing]], [[eigen-svd-psd]].

**Leads to:** [[ridge-regression]], [[capm-alpha-beta]], [[grinold-alpha]], [[implied-forward-regression]].

**Sections:** [[ols-regression]] · [[r-squared]] · [[gauss-markov-assumptions]] · [[prediction-vs-confidence-interval]] · [[linear-regression-assumptions]] · [[robust-standard-errors]] · [[omitted-variable-bias]] · [[multicollinearity]] · [[regression-invariances]]

Notation for this chapter: $n$ observations, $p$ coefficients including the intercept, $y$ the $n\times1$ response, $X$ the $n\times p$ design matrix, $\beta$ true coefficients, $\varepsilon$ errors, $e$ residuals.

<a id="ols-regression"></a>

## OLS Linear Regression (derivation & geometry)
<!-- section: ols-regression | prerequisites: [variance-covariance-correlation, conditional-expectation-best-predictor] | related: [r-squared, gauss-markov-assumptions, implied-forward-regression, capm-alpha-beta, ridge-regression, maximum-likelihood] | sources: [src-squarepoint-dqa-workbook] | tags: [ols, normal-equations, projection, fwl] -->

Ordinary least squares chooses the coefficients that minimise the sum of squared residuals. Geometrically, the fitted values are the orthogonal projection of $y$ onto the columns of $X$.

### Simple regression (with intercept)
$$\hat\beta_1=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2}=r_{xy}\,\frac{s_y}{s_x},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x$$

**Variables:**

- $x_i,y_i$ observations, $i=1,\dots,n$
- $\bar x,\bar y$ sample means
- $r_{xy}$ sample correlation of $x$ and $y$
- $s_x,s_y$ sample standard deviations
- $\hat\beta_0,\hat\beta_1$ fitted intercept and slope

**Reverse regressions:** $\hat\beta_{Y|X}\,\hat\beta_{X|Y}=r_{xy}^2$ (the two slopes are reciprocals only if $|r_{xy}|=1$). E.g. $s_x=2,s_y=3,r_{xy}=0.6$ → slopes 0.9 and 0.4.

**No intercept:** $\hat\beta=\sum x_iy_i/\sum x_i^2$; the product of the two slopes is then the squared raw cosine, not $r_{xy}^2$.

### Multiple regression
$$X^\top X\hat\beta=X^\top y\ \Rightarrow\ \hat\beta=(X^\top X)^{-1}X^\top y,\qquad H=X(X^\top X)^{-1}X^\top,\qquad \hat y=Hy,\qquad X^\top e=0$$

**Variables:**

- $X$ $n\times p$ design matrix (a column of 1s gives the intercept)
- $y$ response vector
- $\hat\beta$ OLS coefficients
- $H$ hat (projection) matrix, symmetric and idempotent
- $\hat y$ fitted values
- $e=y-\hat y$ residuals

### Key points
- The fitted line passes through $(\bar x,\bar y)$; with an intercept, $\sum e_i=0$.
- Compute with **QR/SVD**, not an explicit inverse.
- **Frisch–Waugh–Lovell:** the coefficient on $x_j$ equals the slope from regressing residualised $y$ on residualised $x_j$ (both residualised on the other regressors) → why signs change when controls are added.
- The slope is association, not causation, without extra assumptions.
- OLS is the Gaussian MLE ([[maximum-likelihood]]) and the linear approximation of $E[Y\mid X]$ ([[conditional-expectation-best-predictor]]).

### Connections
- **Builds on:** [[variance-covariance-correlation]], [[conditional-expectation-best-predictor]].
- **Assumptions / inference:** [[gauss-markov-assumptions]], [[robust-standard-errors]], [[r-squared]].
- **Failure modes:** [[omitted-variable-bias]], [[multicollinearity]] → [[ridge-regression]].
- **Finance applications:** [[capm-alpha-beta]] (beta = slope), [[implied-forward-regression]] (regress $C-P$ on $K$).

<a id="r-squared"></a>

## R² and Adjusted R²
<!-- section: r-squared | prerequisites: [ols-regression] | related: [bias-variance-tradeoff, cross-validation-leakage] | sources: [src-squarepoint-dqa-workbook] | tags: [goodness-of-fit] -->

$R^2$ is the share of the variation of $y$ around its mean that the regression explains; adjusted $R^2$ penalises the number of coefficients.

### Formulas
$$R^2=1-\frac{SSE}{SST},\qquad \bar R^2=1-\frac{SSE/(n-p)}{SST/(n-1)}$$

**Variables:**

- $SSE=\sum_i e_i^2$ sum of squared residuals
- $SST=\sum_i(y_i-\bar y)^2$ total sum of squares
- $\bar R^2$ adjusted $R^2$
- $n$ number of observations
- $p$ number of coefficients including the intercept

### SST versus SSE

<figure class="r2-figure">
  <svg viewBox="0 0 720 420" role="img" aria-labelledby="r2-svg-title r2-svg-desc">
    <title id="r2-svg-title">SST and SSE in linear regression</title>
    <desc id="r2-svg-desc">A scatter plot with a fitted regression line and a mean line. For one highlighted point, the distance to the mean line is an SST component and the distance to the fitted line is an SSE residual component.</desc>
    <defs>
      <marker id="r2-arrow-total" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path class="r2-total-head" d="M0 0 L8 4 L0 8 z"></path>
      </marker>
      <marker id="r2-arrow-residual" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path class="r2-residual-head" d="M0 0 L8 4 L0 8 z"></path>
      </marker>
    </defs>
    <g class="r2-grid">
      <line x1="70" y1="110" x2="680" y2="110"></line>
      <line x1="70" y1="170" x2="680" y2="170"></line>
      <line x1="70" y1="235" x2="680" y2="235"></line>
      <line x1="70" y1="290" x2="680" y2="290"></line>
      <line x1="70" y1="350" x2="680" y2="350"></line>
    </g>
    <line class="r2-axis" x1="70" y1="70" x2="70" y2="350"></line>
    <line class="r2-axis" x1="70" y1="350" x2="680" y2="350"></line>
    <text class="r2-axis-label" x="675" y="375" text-anchor="end">x</text>
    <text class="r2-axis-label" x="52" y="78">y</text>
    <line class="r2-mean" x1="90" y1="235" x2="650" y2="235"></line>
    <text class="r2-muted" x="94" y="226">mean ȳ</text>
    <line class="r2-fit" x1="90" y1="330" x2="650" y2="140"></line>
    <text class="r2-muted" x="555" y="130">fitted line ŷ</text>
    <g aria-label="observations">
      <circle class="r2-point" cx="125" cy="300" r="5"></circle>
      <circle class="r2-point" cx="180" cy="275" r="5"></circle>
      <circle class="r2-point" cx="235" cy="305" r="5"></circle>
      <circle class="r2-point" cx="300" cy="245" r="5"></circle>
      <circle class="r2-point" cx="360" cy="265" r="5"></circle>
      <circle class="r2-point" cx="420" cy="215" r="5"></circle>
      <circle class="r2-point-focus" cx="490" cy="150" r="7"></circle>
      <circle class="r2-point" cx="550" cy="185" r="5"></circle>
      <circle class="r2-point" cx="610" cy="130" r="5"></circle>
    </g>
    <line class="r2-guide" x1="490" y1="150" x2="520" y2="150"></line>
    <line class="r2-guide" x1="490" y1="195" x2="540" y2="195"></line>
    <line class="r2-total" x1="520" y1="150" x2="520" y2="235" marker-start="url(#r2-arrow-total)" marker-end="url(#r2-arrow-total)"></line>
    <line class="r2-residual" x1="540" y1="150" x2="540" y2="195" marker-start="url(#r2-arrow-residual)" marker-end="url(#r2-arrow-residual)"></line>
    <text class="r2-label" x="532" y="220">SST</text>
    <text class="r2-label" x="552" y="178">SSE</text>
    <text class="r2-muted" x="505" y="315">highlighted observation yᵢ</text>
  </svg>
  <figcaption><strong>Reading the diagram.</strong> The dashed horizontal line is the mean response ȳ. The solid diagonal line is the fitted regression. For the highlighted point, the vertical distance to the mean line is one component of <strong>SST</strong>; the vertical distance to the fitted line is its <strong>SSE</strong> residual component. The totals sum these squared vertical distances over all observations: SST is variation around the mean, while SSE is variation left after fitting.</figcaption>
</figure>

### Key points
- Simple OLS with an intercept: $R^2=r_{xy}^2$.
- Adding regressors can't lower training $R^2$ (the nested model is still feasible) — adjusted $R^2$ and **test** performance can fall.
- Test $R^2$ can be **negative** (worse than predicting the mean).

### Connections
- **Builds on:** [[ols-regression]].
- **Why training $R^2$ misleads:** [[bias-variance-tradeoff]], [[cross-validation-leakage]].

<a id="gauss-markov-assumptions"></a>

## Regression Assumptions (Gauss–Markov) & Inference
<!-- section: gauss-markov-assumptions | prerequisites: [ols-regression, hypothesis-testing] | related: [linear-regression-assumptions, robust-standard-errors, omitted-variable-bias, multicollinearity] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [blue, unbiasedness, t-test, f-test] -->

Each property of OLS needs a specific set of assumptions. This section lists which assumption supports which claim and gives the classical standard errors and t/F tests that hold when all of them are met. The next sections treat the violations.

### What each claim needs

| Claim | Needs |
|---|---|
| Unique $\hat\beta$ exists | $X$ has full column rank |
| Unbiased | correct linear mean + $E[\varepsilon\mid X]=0$ |
| Classical SE formula valid | also $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$ |
| BLUE | Gauss–Markov conditions |
| Exact finite-sample t/F | also $\varepsilon\mid X\sim N(0,\sigma^2I)$ |

**Gauss–Markov theorem:** under linearity, independent sampling, full rank, exogeneity and $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$, OLS is **BLUE** (Best Linear Unbiased Estimator; "best" = minimum variance among linear unbiased estimators).

### Formulas
$$y=X\beta+\varepsilon,\qquad \hat\beta=\beta+(X^\top X)^{-1}X^\top\varepsilon,\qquad \mathrm{Var}(\hat\beta\mid X)=\sigma^2(X^\top X)^{-1}$$
$$\hat\sigma^2=\frac{SSE}{n-p},\qquad SE(\hat\beta_1)=\frac{\hat\sigma}{\sqrt{\sum_i(x_i-\bar x)^2}}\ \ \text{(simple regression)}$$
$$t_j=\frac{\hat\beta_j-b_0}{SE(\hat\beta_j)}\sim t_{n-p},\qquad F=\frac{(SSE_R-SSE_U)/J}{SSE_U/(n-p_U)}\sim F_{J,\,n-p_U}$$

**Variables:**

- $\beta$ true coefficients; $\hat\beta$ OLS estimate
- $\varepsilon$ errors, with variance $\sigma^2$ under homoskedasticity
- $\hat\sigma^2$ estimated error variance ($\hat\sigma$: residual standard error)
- $SE(\cdot)$ standard error
- $t_j$ t-statistic for coefficient $j$
- $b_0$ value of $\beta_j$ under the null
- $SSE_R,SSE_U$ residual sums of squares of the restricted and unrestricted models
- $J$ number of restrictions tested
- $p_U$ number of coefficients in the unrestricted model

### Key points
- **Normality is NOT needed for unbiasedness or for BLUE** (classic trap); with large $n$ the CLT makes t-tests approximately valid.
- More spread in $x$ → smaller slope SE.
- All individual t-stats weak but joint F significant: possible with correlated regressors ([[multicollinearity]]).

### Connections
- **Builds on:** [[ols-regression]], [[hypothesis-testing]].
- **Violations:** [[linear-regression-assumptions]] (overview), [[robust-standard-errors]] (heteroskedasticity / autocorrelation), [[omitted-variable-bias]] (endogeneity), [[multicollinearity]].

<a id="prediction-vs-confidence-interval"></a>

## Prediction Interval vs Confidence Interval
<!-- section: prediction-vs-confidence-interval | prerequisites: [gauss-markov-assumptions, confidence-intervals] | related: [] | sources: [src-squarepoint-dqa-workbook] | tags: [intervals] -->

At a new point $x_0$, a confidence interval covers the *mean* response, while a prediction interval covers a *new observation*, which also carries its own noise.

### Formulas
$$SE(\text{mean at }x_0)=\hat\sigma\sqrt{\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}},\qquad SE(\text{new obs})=\hat\sigma\sqrt{1+\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}}$$

**Variables:**

- $x_0$ query point
- $\bar x$ sample mean of $x$
- $S_{xx}=\sum_i(x_i-\bar x)^2$
- $\hat\sigma$ residual standard error
- $n$ number of observations

### Key points
- The extra "1" is the irreducible noise of a new observation → prediction intervals are always wider.
- Both widen as $x_0$ moves away from $\bar x$.

### Connections
- **Builds on:** [[gauss-markov-assumptions]], [[confidence-intervals]].

<a id="linear-regression-assumptions"></a>

## Assumption Violations: Diagnosis & Fixes
<!-- section: linear-regression-assumptions | prerequisites: [gauss-markov-assumptions, estimator-properties] | related: [robust-standard-errors, omitted-variable-bias, multicollinearity, regression-invariances, stationarity-ar1, effective-sample-size, cross-validation-leakage] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [linear-regression, assumptions, gauss-markov, violations] -->

For the model $y=X\beta+\varepsilon$ with $\hat\beta=\beta+(X^\top X)^{-1}X^\top\varepsilon$ ([[gauss-markov-assumptions]]), this section maps each assumption to what breaks when it fails, how to detect it, and how to fix it. The central distinction: some violations bias the coefficients, others only break the standard errors.

### Assumption map

| Assumption | What it supports | If it is violated |
|---|---|---|
| **Correct linear mean / functional form** | $\beta_j$ is the conditional change in $y$ for a one-unit change in $x_j$ | Misspecified fit; coefficients can be biased or lose their economic interpretation, and out-of-sample prediction can fail. |
| **Zero conditional mean / exogeneity:** $E[\varepsilon\mid X]=0$ | OLS is unbiased and consistent under the linear model | Omitted variables, reverse causality, selection, or measurement error correlated with $X$ bias $\hat\beta$ and can make it inconsistent. Robust SEs do not fix this. |
| **Full column rank** | A unique coefficient vector exists | Perfect collinearity makes coefficients non-unique; near-collinearity makes them unstable and high-variance. |
| **Homoskedasticity:** $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$ | Classical standard errors and t/F inference | Coefficients can remain unbiased if exogeneity holds, but classical SEs, p-values and confidence intervals are wrong; use heteroskedasticity-robust or clustered SEs. |
| **Independent errors** | Classical iid standard errors and inference | Serial correlation, clustering or duplicated rows make SEs unreliable and reduce the effective sample size; use HAC/clustered SEs and account for dependence. |
| **Normal errors** | Exact finite-sample t/F tests and normal-theory intervals | Non-normal errors can make finite-sample p-values and intervals inaccurate; unbiasedness does not require normality. Large samples or robust/asymptotic methods are alternatives. |
| **No influential outliers / leverage points** | A stable fitted line and stable inference | A small number of points can move coefficients, fitted values and SEs; inspect diagnostics and decide whether the data or the model needs attention. |

### Key points interviewers look for
- **Only endogeneity causes bias.** Heteroskedasticity and autocorrelation break the SEs, not the coefficients.
- Linearity is in **β**, not in $x$: using $x^2$ or $\ln x$ as a regressor is still linear regression.
- **Sources of endogeneity:** omitted variables, measurement error in $X$, simultaneity / reverse causality.

### Diagnostics and fixes

| Problem | Test | Fix |
|---|---|---|
| Heteroskedasticity | Breusch–Pagan, White; fan-shaped residual plot | White/HC robust SE, WLS |
| Autocorrelation | Durbin–Watson, Breusch–Godfrey, Ljung–Box | Newey–West (HAC) SE, GLS |
| Multicollinearity (imperfect) | VIF > 10, condition number | Drop/combine, ridge, PCA |
| Endogeneity | Hausman test | IV / 2SLS |
| Non-normality | Jarque–Bera, QQ plot | Large $n$, bootstrap |

### Finance and time-series failure modes
- **Autocorrelated or duplicated rows:** the apparent sample size is too large; naive annualisation and standard errors overstate precision. See [[effective-sample-size]] and [[regression-invariances]].
- **Non-stationary levels:** a regression can be highly significant but spurious; stationarity must be checked before interpreting the slope. See [[stationarity-ar1]].
- **Look-ahead or post-decision data:** OLS can fit an impossible information set and produce an inflated fit or backtest; this is a data-construction failure, not something robust SEs repair. See [[cross-validation-leakage]].

### Factor-regression angle (自己推理)

In factor regressions $R_{p,t}-R_{f,t}=\alpha+\beta^\top F_t+\varepsilon_t$:

**Variables:**

- $R_{p,t}$ portfolio (fund) return in period $t$
- $R_{f,t}$ risk-free return in period $t$
- $\alpha$ intercept (alpha)
- $\beta$ vector of factor loadings
- $F_t$ vector of factor returns in period $t$
- $\varepsilon_t$ residual

**Typical issues:**

- **Overlapping returns** (monthly data, 12-month windows) → autocorrelation by construction → Newey–West SEs.
- **Volatility clustering** → heteroskedasticity almost always present → HAC SEs.
- **Correlated factors** (Value vs Profitability) → unstable betas, overall fit unaffected ([[multicollinearity]]).
- **Omitted factor** → shows up as spurious **alpha** ([[omitted-variable-bias]]).

**Interview answer:** "Only exogeneity threatens unbiasedness. Heteroskedasticity and autocorrelation only affect inference, so in finance we almost always use robust or HAC standard errors."

### Quick diagnosis
- **Coefficients biased or unstable:** inspect functional form, omitted variables, endogeneity and multicollinearity.
- **Coefficients stable but p-values wrong:** inspect heteroskedasticity, serial correlation, clustering and influential points.
- **A clean-looking fit but bad out-of-sample behaviour:** check leakage, time ordering, and whether the model is evaluated on data unavailable at decision time.

### Connections
- **Builds on:** [[gauss-markov-assumptions]].
- **Bias:** [[omitted-variable-bias]]. **Variance / inference:** [[robust-standard-errors]], [[multicollinearity]].
- **Signal-research implementation:** [[regression-invariances]], [[cross-validation-leakage]].

<a id="robust-standard-errors"></a>

## Heteroskedasticity, Serial Correlation & Robust SEs
<!-- section: robust-standard-errors | prerequisites: [linear-regression-assumptions] | related: [effective-sample-size, stationarity-ar1] | sources: [src-squarepoint-dqa-workbook] | tags: [hc0, hac, newey-west] -->

When the errors do not have constant, uncorrelated variance, OLS coefficients stay unbiased (given exogeneity) but the classical variance formula is wrong. The "sandwich" formula replaces it.

### Formulas
$$\mathrm{Var}(\hat\beta\mid X)=(X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1},\qquad \text{HC0: }(X^\top X)^{-1}\Big(\sum_i e_i^2\,x_ix_i^\top\Big)(X^\top X)^{-1}$$

**Variables:**

- $\Omega=\mathrm{Var}(\varepsilon\mid X)$ error covariance matrix
- $e_i$ residual of row $i$
- $x_i$ regressor vector of row $i$ (as a column)

### Key points
- Heteroskedasticity **doesn't bias** $\hat\beta$ (if $E[\varepsilon\mid X]=0$) but breaks the classical SE.
- Serial correlation → HAC (Newey–West) or clustered SEs; "robust" SEs don't fix endogeneity or every form of dependence.

### Connections
- **Builds on:** [[linear-regression-assumptions]].
- **Time-series cause:** [[stationarity-ar1]]; quantified by [[effective-sample-size]].

<a id="omitted-variable-bias"></a>

## Omitted-Variable Bias
<!-- section: omitted-variable-bias | prerequisites: [ols-regression, linear-regression-assumptions] | related: [capm-alpha-beta] | sources: [src-squarepoint-dqa-workbook] | tags: [endogeneity, confounding] -->

Leaving out a relevant variable that is correlated with an included regressor makes the included coefficient absorb part of the omitted effect — the most common source of endogeneity.

### Formula
True model $y=\beta_0+\beta_1x+\beta_2z+\varepsilon$; regress $y$ on $x$ only:

$$\tilde\beta_1\ \to\ \beta_1+\beta_2\,\frac{\mathrm{Cov}(x,z)}{\mathrm{Var}(x)}$$

**Variables:**

- $x$ included regressor
- $z$ omitted variable
- $\beta_1$ true effect of $x$; $\beta_2$ true effect of $z$ on $y$
- $\tilde\beta_1$ slope from the short regression (its probability limit shown)

### Key points
- The bias needs **both** $\beta_2\ne0$ and $\mathrm{Cov}(x,z)\ne0$.
- It explains coefficient sign flips when adding controls (also via Frisch–Waugh–Lovell, [[ols-regression]]).
- Finance: "alpha" can be an omitted risk factor ([[capm-alpha-beta]]).

### Connections
- **Builds on:** [[ols-regression]], [[linear-regression-assumptions]].

<a id="multicollinearity"></a>

## Multicollinearity & VIF
<!-- section: multicollinearity | prerequisites: [ols-regression, eigen-svd-psd] | related: [ridge-regression, pca, regression-invariances, information-coefficient] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [vif, ill-conditioning, factor-redundancy] -->

When regressors are strongly correlated with each other, the data cannot separate their individual effects: coefficients become imprecise and unstable although the overall fit is fine.

### Formula
$$\text{VIF}_j=\frac{1}{1-R_j^2},\qquad x_j=\alpha+\sum_{k\ne j}\beta_kx_k+\varepsilon\ \ \text{(auxiliary regression)},\qquad \mathrm{Var}(\hat\beta_j)=\frac{\sigma^2}{(n-1)\,\mathrm{Var}(x_j)}\cdot\text{VIF}_j$$

**Variables:**

- $\text{VIF}_j$ variance inflation factor of regressor $j$
- $R_j^2$ $R^2$ of the auxiliary regression of regressor $x_j$ on all the other regressors $x_k$
- $\sigma^2$ error variance of the main regression
- $n$ number of observations
- $\mathrm{Var}(x_j)$ sample variance of regressor $j$

VIF = 5 → SE × $\sqrt5\approx2.24$ → t-stat ÷ 2.24. Tolerance $=1/\text{VIF}$.

### Worked example (factor regressors)

| Factor | Auxiliary $R^2$ | VIF |
|---|---|---|
| Value | 0.15 | 1.18 |
| Quality | 0.82 | 5.56 |
| Profitability | 0.79 | 4.76 |
| Momentum | 0.08 | 1.09 |

→ Quality and Profitability double-count "company quality".

| VIF | Meaning |
|---|---|
| 1–2 | Fine |
| 2–5 | Moderate (common in factor work) |
| 5–10 | Unreliable |
| > 10 | Severe; drop or combine |

### Key points
- Perfect collinearity → coefficients non-unique (fitted values are still unique: they are a projection).
- Near-collinearity → small singular values of $X$ → unstable coefficients; prediction may still be fine ([[eigen-svd-psd]]).
- **Consequences:** inflated SEs, unstable or sign-flipping betas, confounded attribution. **Not a bias**: overall $R^2$ and the joint F-test are unaffected.
- **Remedies:** drop · composite · residualise (changes the meaning) · PCA · ridge/LASSO · more data; choose by goal.
- **Subtleties:** unit-free; misses nonlinear redundancy; a within-model property; catches multi-way collinearity that pairwise correlations miss; a condition number > 30 is an alternative diagnostic; correlated factors reduce effective **breadth** ([[information-coefficient]]).

### Connections
- **Builds on:** [[ols-regression]]; **diagnosed by:** [[eigen-svd-psd]] (small eigenvalues of $X^\top X$).
- **Fixed by:** [[ridge-regression]], [[pca]].

<a id="regression-invariances"></a>

## Regression Invariances (duplication, scaling)
<!-- section: regression-invariances | prerequisites: [gauss-markov-assumptions] | related: [ridge-regression, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [interview-variations] -->

Interviewers test understanding by transforming the data and asking what changes. The answers follow from the normal equations and the SE formula.

### Duplicate every row
$X^\top X$ and $X^\top y$ both double → **coefficients unchanged**. SSE doubles, and naive software uses $2n-p$ degrees of freedom:

$$\text{SE}_{\text{new}}=\text{SE}_{\text{old}}\sqrt{\frac{n-p}{2n-p}}\approx\frac{\text{SE}_{\text{old}}}{\sqrt2}$$

**Variables:**

- $n$ number of original rows
- $p$ number of coefficients
- $\text{SE}_{\text{old}},\text{SE}_{\text{new}}$ standard errors before and after duplication

The shrink is **fictitious** — no new information. (Ridge with a fixed λ on an unnormalised SSE *does* change: the effective λ halves.)

### Other variations
- $y\to cy$: coefficients and residuals × $c$, SEs × $|c|$, $R^2$ unchanged.
- $x_j\to cx_j$: its coefficient ÷ $c$; fitted values unchanged.
- Add a constant to $x_j$ (with an intercept): slope unchanged.
- Exact duplicate column: OLS non-unique; ridge splits the weight equally.
- Add a noise feature: training fit can't worsen; test fit may.

Here $c$ is any nonzero constant.

### Connections
- **Builds on:** [[gauss-markov-assumptions]].
- **Related:** [[effective-sample-size]] (correlated rows ≈ fewer real observations), [[ridge-regression]].
