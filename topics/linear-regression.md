---
id: linear-regression
title: "Linear Regression"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook]
---
# Linear Regression

**Sections:** [[ols-regression]] · [[r-squared]] · [[gauss-markov-assumptions]] · [[robust-standard-errors]] · [[omitted-variable-bias]] · [[multicollinearity]] · [[regression-invariances]] · [[prediction-vs-confidence-interval]]

<a id="ols-regression"></a>

## OLS Linear Regression (derivation & geometry)
<!-- section: ols-regression | prerequisites: [variance-covariance-correlation] | related: [r-squared, gauss-markov-assumptions, conditional-expectation-best-predictor, implied-forward-regression, capm-alpha-beta, ridge-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [ols, normal-equations, projection, fwl] -->

### Simple regression (with intercept)
$$\hat\beta_1=\frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2}=r_{xy}\frac{s_y}{s_x},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x$$

**Reverse regressions:** $\hat\beta_{Y|X}\hat\beta_{X|Y}=r^2$ (reciprocals only if $|r|=1$). E.g. $s_x=2,s_y=3,r=0.6$ → 0.9 and 0.4.

**No intercept:** $\hat\beta=\sum x_iy_i/\sum x_i^2$; product of the two slopes = squared raw cosine, not $r^2$.

### Multiple regression
$$X^\top X\hat\beta=X^\top y\ \Rightarrow\ \hat\beta=(X^\top X)^{-1}X^\top y,\qquad H=X(X^\top X)^{-1}X^\top,\ \hat y=Hy,\ X^\top e=0$$

**Variables:**

- $x_i,y_i$ observations
- $r_{xy}$ sample correlation
- $s_x,s_y$ sample std devs
- $X$ $n\times p$ design matrix (column of 1s = intercept)
- $y$ response
- $\hat\beta$ coefficients
- $H$ hat (projection) matrix, symmetric & idempotent
- $e$ residuals

### Key points
- Line passes through $(\bar x,\bar y)$; with intercept $\sum e_i=0$.
- Compute with **QR/SVD**, not an explicit inverse.
- **Frisch–Waugh–Lovell:** coefficient on $x_j$ = regress residualised $y$ on residualised $x_j$ → why signs change when controls are added.
- Slope is association, not causation, without extra assumptions.

### Connections
- **Builds on:** [[variance-covariance-correlation]]; approximates [[conditional-expectation-best-predictor]].
- **Assumptions / inference:** [[gauss-markov-assumptions]], [[robust-standard-errors]], [[r-squared]].
- **Failure modes:** [[omitted-variable-bias]], [[multicollinearity]] → [[ridge-regression]].
- **Finance applications:** [[capm-alpha-beta]] (beta = slope), [[implied-forward-regression]] (regress $C-P$ on $K$).

<a id="r-squared"></a>

## R² and Adjusted R²
<!-- section: r-squared | prerequisites: [ols-regression] | related: [bias-variance-tradeoff, cross-validation-leakage] | sources: [src-squarepoint-dqa-workbook] | tags: [goodness-of-fit] -->

### Formulas
$$R^2=1-\frac{SSE}{SST},\qquad \bar R^2=1-\frac{SSE/(n-p)}{SST/(n-1)}$$

**Variables:**

- $SSE=\sum e_i^2$
- $SST=\sum(y_i-\bar y)^2$
- $n$ observations
- $p$ coefficients incl. intercept

### Key points
- Simple OLS with intercept: $R^2=r_{xy}^2$.
- Adding regressors can't lower training $R^2$ (nested model still feasible) — adjusted $R^2$ and **test** performance can fall.
- Test $R^2$ can be **negative** (worse than predicting the mean).

### Connections
- **Why training R² misleads:** [[bias-variance-tradeoff]], [[cross-validation-leakage]].

<a id="gauss-markov-assumptions"></a>

## Regression Assumptions (Gauss–Markov) & Inference
<!-- section: gauss-markov-assumptions | prerequisites: [ols-regression, hypothesis-testing] | related: [robust-standard-errors, omitted-variable-bias, multicollinearity] | sources: [src-squarepoint-dqa-workbook] | tags: [blue, unbiasedness, t-test, f-test] -->

| Claim | Needs |
|---|---|
| Unique $\hat\beta$ exists | $X$ full column rank |
| Unbiased | correct linear mean + $E[\varepsilon\mid X]=0$ |
| Classical SE formula valid | also $\mathrm{Var}(\varepsilon\mid X)=\sigma^2I$ |
| BLUE | Gauss–Markov conditions |
| Exact finite-sample t/F | also $\varepsilon\mid X\sim N(0,\sigma^2I)$ |

### Formulas
$$\hat\beta=\beta+(X^\top X)^{-1}X^\top\varepsilon,\quad \mathrm{Var}(\hat\beta\mid X)=\sigma^2(X^\top X)^{-1},\quad \hat\sigma^2=\frac{SSE}{n-p},\quad SE(\hat\beta_1)=\frac{\hat\sigma}{\sqrt{\sum(x_i-\bar x)^2}}$$
$$t_j=\frac{\hat\beta_j-b_0}{SE(\hat\beta_j)}\sim t_{n-p},\qquad F=\frac{(SSE_R-SSE_U)/q}{SSE_U/(n-p_U)}\sim F_{q,n-p_U}$$

**Variables:**

- $\beta$ true coefficients
- $\varepsilon$ errors
- $b_0$ null value
- $q$ number of restrictions
- $R/U$ restricted/unrestricted

### Key points
- **Normality is NOT needed for unbiasedness** (classic trap).
- More spread in $x$ → smaller slope SE.
- All individual t-stats weak but joint F significant: possible with correlated regressors.

### Connections
- **Violations:** [[robust-standard-errors]] (heteroskedasticity / autocorrelation), [[omitted-variable-bias]] (endogeneity), [[multicollinearity]].

<a id="robust-standard-errors"></a>

## Heteroskedasticity, Serial Correlation & Robust SEs
<!-- section: robust-standard-errors | prerequisites: [gauss-markov-assumptions] | related: [effective-sample-size, stationarity-ar1] | sources: [src-squarepoint-dqa-workbook] | tags: [hc0, hac, newey-west] -->

### Formulas
$$\mathrm{Var}(\hat\beta\mid X)=(X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1},\qquad \text{HC0: }(X^\top X)^{-1}\Big(\sum_i e_i^2x_ix_i^\top\Big)(X^\top X)^{-1}$$

**Variables:**

- $\Omega$ error covariance
- $e_i$ residual
- $x_i$ regressor vector for row $i$

### Key points
- Heteroskedasticity **doesn't bias** $\hat\beta$ (if $E[\varepsilon|X]=0$) but breaks the classical SE.
- Serial correlation → HAC (Newey–West) or clustering; "robust" SEs don't fix endogeneity or every dependence.

### Connections
- **Time-series cause:** [[stationarity-ar1]]; quantified by [[effective-sample-size]].

<a id="omitted-variable-bias"></a>

## Omitted-Variable Bias
<!-- section: omitted-variable-bias | prerequisites: [ols-regression] | related: [gauss-markov-assumptions, capm-alpha-beta] | sources: [src-squarepoint-dqa-workbook] | tags: [endogeneity, confounding] -->

### Formula
True $Y=\beta_0+\beta_1X+\beta_2Z+\varepsilon$; regress $Y$ on $X$ only:
$$\tilde\beta_1=\beta_1+\beta_2\frac{\mathrm{Cov}(X,Z)}{\mathrm{Var}(X)}$$

**Variables:**

- $Z$ omitted variable
- $\beta_2$ its effect on $Y$

### Key points
- Bias needs **both** $\beta_2\ne0$ and $\mathrm{Cov}(X,Z)\ne0$.
- Explains coefficient sign flips when adding controls (also via FWL).
- Finance: "alpha" can be an omitted risk factor ([[capm-alpha-beta]]).

<a id="multicollinearity"></a>

## Multicollinearity & VIF
<!-- section: multicollinearity | prerequisites: [ols-regression, eigen-svd-psd] | related: [ridge-regression, pca, regression-invariances] | sources: [src-squarepoint-dqa-workbook] | tags: [vif, ill-conditioning] -->

### Formula
$$VIF_j=\frac{1}{1-R_j^2}$$

**Variables:** $R_j^2$ from regressing regressor $j$ on the other regressors.

### Key points
- Perfect collinearity → coefficients non-unique (fitted values still unique = projection).
- Near-collinearity → small singular values → coefficients unstable; prediction may still be fine.
- Remedies: drop/combine variables, more data, [[ridge-regression]], [[pca]] regression — choose by goal.

### Connections
- **Diagnosed by:** [[eigen-svd-psd]] (small eigenvalues of $X^\top X$). **Fixed by:** [[ridge-regression]].

<a id="regression-invariances"></a>

## Regression Invariances (duplication, scaling)
<!-- section: regression-invariances | prerequisites: [gauss-markov-assumptions] | related: [ridge-regression, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [interview-variations] -->

### Duplicate every row
$X^\top X$, $X^\top y$ double → **coefficients unchanged**. SSE doubles; naive software uses $2n-p$ dof:
$$\text{SE}_{new}=\text{SE}_{old}\sqrt{\frac{n-p}{2n-p}}\approx\frac{\text{SE}_{old}}{\sqrt2}$$
The shrink is **fictitious** — no new information. (Ridge with fixed λ on an unnormalised SSE *does* change: effective λ halves.)

### Other variations
- $y\to cy$: coefficients & residuals ×$c$, SEs ×$|c|$, $R^2$ unchanged.
- $x_j\to cx_j$: its coefficient ÷$c$; fits unchanged.
- Add a constant to $x_j$ (with intercept): slope unchanged.
- Exact duplicate column: OLS non-unique; ridge splits the weight equally.
- Add noise feature: training fit can't worsen; test may.

**Variables:** $n$ rows, $p$ coefficients, $c$ nonzero constant.

### Connections
- **Related:** [[effective-sample-size]] (correlated rows ≈ fewer real observations), [[ridge-regression]].

<a id="prediction-vs-confidence-interval"></a>

## Prediction Interval vs Confidence Interval
<!-- section: prediction-vs-confidence-interval | prerequisites: [gauss-markov-assumptions, confidence-intervals] | related: [] | sources: [src-squarepoint-dqa-workbook] | tags: [intervals] -->

$$SE(\text{mean at }x_0)=\hat\sigma\sqrt{\tfrac1n+\tfrac{(x_0-\bar x)^2}{S_{xx}}},\qquad SE(\text{new obs})=\hat\sigma\sqrt{1+\tfrac1n+\tfrac{(x_0-\bar x)^2}{S_{xx}}}$$

**Variables:**

- $x_0$ query point
- $S_{xx}=\sum(x_i-\bar x)^2$
- $\hat\sigma$ residual std error

The extra "1" = irreducible noise of a new observation → prediction intervals are always wider.
