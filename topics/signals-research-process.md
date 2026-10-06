---
id: signals-research-process
title: "Signals & Research"
type: topic
domain: signal-research
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-carry-course-notes]
---
# Signals & Research

This chapter goes from "what is alpha" to "how big a return should I forecast". It defines excess return, alpha and beta, builds a simple time-series signal, measures a signal's skill with the information coefficient, attributes a composite signal's skill to its components, and converts a signal score into an expected-return forecast that a portfolio optimiser can use. It ends with method rather than models: the sequence of steps a research project should follow, how to present it, and how to investigate a strategy whose backtest does not survive contact with live trading.

**Prerequisites:** [[ols-regression]], [[returns-simple-log]], [[variance-covariance-correlation]], [[time-series-validation]], [[cross-validation-leakage]], [[multiple-testing]].

**Leads to:** [[signal-to-weight]], [[mean-variance-optimization]], [[black-litterman]], [[multi-asset-signals]], [[sharpe-ratio]] (why a high backtest Sharpe misleads), [[price-reconciliation]] (the same debugging discipline on the sell side).

**Sections:** [[capm-alpha-beta]] · [[time-series-momentum]] · [[information-coefficient]] · [[ic-contribution]] · [[grinold-alpha]] · [[timing-signal-evaluation]] · [[research-workflow]] · [[backtest-pitfalls]]

<a id="capm-alpha-beta"></a>

## Excess Return, Alpha, Beta & CAPM
<!-- section: capm-alpha-beta | prerequisites: [ols-regression, returns-simple-log] | related: [omitted-variable-bias, exposure-neutrality, sharpe-ratio, linear-regression-assumptions] | sources: [src-squarepoint-dqa-workbook] | tags: [beta, alpha, factor] -->

Regressing an asset's excess return on the market's excess return splits it into market exposure (beta) and an intercept (alpha). CAPM is the equilibrium claim that, in expectation, the intercept is zero.

### Formulas
$$R_i-r_f=\alpha_i+\beta_i(R_m-r_f)+\varepsilon_i,\qquad \beta_i=\frac{\mathrm{Cov}(R_i,R_m)}{\mathrm{Var}(R_m)},\qquad \text{CAPM: }E[R_i]-r_f=\beta_i\big(E[R_m]-r_f\big)$$

**Variables:**

- $R_i$ return of asset $i$
- $R_m$ market return
- $r_f$ risk-free return over the same period
- $\alpha_i$ intercept (alpha)
- $\beta_i$ market beta (OLS slope)
- $\varepsilon_i$ residual (idiosyncratic return)

### Key points
- Beta is the OLS slope ([[ols-regression]]). A positive alpha may be noise, an omitted factor ([[omitted-variable-bias]]) or selection bias ([[multiple-testing]]).
- CAPM is an equilibrium model, not a definition of realised returns.

### Connections
- **Builds on:** [[ols-regression]], [[returns-simple-log]].
- **Used by:** [[exposure-neutrality]], [[structural-risk-premia]], [[relative-value-long-short]], [[grinold-alpha]] (residual volatility).

<a id="time-series-momentum"></a>

## Time-Series Momentum Signal ("Is the trend still up?")
<!-- section: time-series-momentum | prerequisites: [returns-simple-log] | related: [signal-to-weight, cross-validation-leakage, backtest-pitfalls] | sources: [src-signal-to-weight, src-carry-course-notes] | tags: [momentum, signal, z-score] -->

A worked example of turning a price history into a signal: take the 12-month return, standardise it against its own history, and clip extremes. The result is a unitless score whose sign is the direction and whose size is the conviction.

### Formula
$$raw_t=\frac{P_t}{P_{t-12}}-1,\qquad z_t=\frac{raw_t-\mu_{raw}}{\sigma_{raw}},\qquad s_t=\mathrm{clip}(z_t,-2,+2)$$

**Variables:**

- $P_t$ price or index level at month $t$
- $P_{t-12}$ price 12 months earlier
- $raw_t$ raw 12-month momentum
- $\mu_{raw},\sigma_{raw}$ mean and standard deviation of $raw$ over a look-back window (window to be decided)
- $z_t$ standardised momentum
- $s_t$ signal, $z_t$ clipped to $[-2,+2]$

### Reading the signal
- $s=0$: momentum at its historical average → no conviction, no position.
- $s=+1.5$: 1.5σ above average → moderately strong uptrend. $s=-2$: the clipped floor (maximum bearish).
- **Sign = direction, magnitude = conviction.** Being unitless, different raw signals become comparable.

### Expanding vs rolling standardisation
For timing, the look-back can be **expanding** (all history up to $t$):

$$z_t=\frac{x_t-\bar x_{\le t}}{\hat\sigma_{\le t}},\qquad s_t=\mathrm{clip}(z_t,-2,+2)$$

**Variables:**

- $x_t$ raw signal value at $t$ (e.g. 12-month momentum, relative carry)
- $\bar x_{\le t}$, $\hat\sigma_{\le t}$ mean and standard deviation of $x_u$ over all dates $u\le t$ (a minimum number of observations, e.g. 20, before the first score)
- $z_t$ expanding z-score; $s_t$ capped score

**Notes:**

- Comparing a series with its **own** history is the rule "above vs below its historical mean", in units of historical volatility.
- **Expanding vs rolling:** a rolling window is one more free parameter to overfit; expanding uses all the past and nothing else, so it stays point-in-time. In the pipeline this is a single config switch passed to the normaliser: `NORMALIZE_WINDOW = None  # None = expanding window`.
- **Cap at ±2:** so one freak observation cannot dictate a position.
- **Pitfall:** if a monthly series is forward-filled onto trading days *before* standardising, a "20-observation minimum" counts repeated daily copies, not months; the early z-scores rest on thin history and their variance is understated.

### Connections
- **Builds on:** [[returns-simple-log]].
- **Feeds:** [[signal-to-weight]] → [[risk-budgeting]]; the momentum leg of [[fx-carry-spot-slide]].

<a id="information-coefficient"></a>

## Information Coefficient (IC, Rank IC, ICIR) & the Fundamental Law
<!-- section: information-coefficient | prerequisites: [variance-covariance-correlation, time-series-momentum, effective-sample-size] | related: [ic-contribution, grinold-alpha, multiple-testing, multicollinearity, sharpe-ratio, cross-validation-leakage, timing-signal-evaluation] | sources: [src-quant-finance-study-notes, src-carry-course-notes] | tags: [ic, rank-ic, icir, breadth, fundamental-law] -->

The IC measures a signal's skill as the cross-sectional correlation between today's signal and the next period's returns. Its stability over time (ICIR) and the number of independent bets (breadth) together determine the achievable information ratio.

### Formula
$$IC_t=\frac{\sum_i(s_{i,t}-\bar s_t)(r_{i,t+1}-\bar r_{t+1})}{\sqrt{\sum_i(s_{i,t}-\bar s_t)^2}\sqrt{\sum_i(r_{i,t+1}-\bar r_{t+1})^2}}$$

**Variables:**

- $IC_t\in[-1,1]$ information coefficient at period $t$
- $i=1,\dots,N$ assets in the cross-section
- $s_{i,t}$ signal of asset $i$ at $t$
- $r_{i,t+1}$ realised forward return of asset $i$ from $t$ to $t+1$
- $\bar s_t,\bar r_{t+1}$ cross-sectional means

Timing: the signal at $t$ is compared with returns from $t$ to $t+1$ (anything else is look-ahead bias, [[cross-validation-leakage]]).

| IC | Quality |
|---|---|
| 0.01–0.03 | Weak |
| 0.03–0.05 | Decent |
| 0.05–0.10 | Strong, uncommon |
| > 0.10 | Suspicious (look-ahead / survivorship) |

| | Pearson IC | Rank (Spearman) IC |
|---|---|---|
| Inputs | Raw values | Cross-sectional ranks |
| Assumes | Linear | Monotonic |
| Outliers | Sensitive (winsorise at 1/99%) | Robust: the industry default |

### Rank IC (Spearman) step by step
Replace each value by its rank, then take the ordinary (Pearson) correlation of the ranks. With no ties this equals a closed form in the rank differences:

$$\text{Rank IC}=\mathrm{corr}\big(\mathrm{rk}(s),\mathrm{rk}(r)\big)=1-\frac{6\sum_{j=1}^{n}d_j^2}{n(n^2-1)},\qquad d_j=\mathrm{rk}(s_j)-\mathrm{rk}(r_j)$$

**Variables:**

- $j=1,\dots,n$ observations being correlated (assets on one date for the cross-sectional IC; dates for the time-series IC below)
- $n$ number of observations
- $s_j$ signal of observation $j$
- $r_j$ forward return of observation $j$
- $\mathrm{rk}(\cdot)$ rank within the sample: 1 = smallest, $n$ = largest (ties get the average rank)
- $d_j$ rank difference of observation $j$

**Reading it:** Rank IC asks only "does a higher score come with a higher return?" (monotonic, not necessarily linear). $+1$: the score orders the returns perfectly; $0$: no ordering; $-1$: perfectly reversed. Because a rank can move at most from 1 to $n$, one extreme return (a crash week) cannot dominate it, whereas it can dominate a Pearson coefficient. Whether the relation is also *linear* (which linear position sizing needs) is checked separately by a quantile sort ([[timing-signal-evaluation]]): detection first, shape second.

**Example:** five weeks of a timing score and the next-period return (%):

| Week | Score $s$ | $\mathrm{rk}(s)$ | Return $r$ | $\mathrm{rk}(r)$ | $d$ | $d^2$ |
|---|---|---|---|---|---|---|
| 1 | 1.2 | 4 | +0.8 | 4 | 0 | 0 |
| 2 | −0.5 | 2 | −0.2 | 2 | 0 | 0 |
| 3 | 0.3 | 3 | +1.5 | 5 | −2 | 4 |
| 4 | 2.0 | 5 | +0.4 | 3 | +2 | 4 |
| 5 | −1.1 | 1 | −0.6 | 1 | 0 | 0 |

$\sum d^2=8$ → Rank IC $=1-6\cdot8/(5\cdot24)=$ **0.60**; Pearson IC $=0.54$. If week 5 had been a crash ($r=-6.0$ instead of $-0.6$), its rank stays 1, so the Rank IC is still 0.60, while the Pearson IC jumps to 0.68: one outlier week moved it, not new information about the ordering.

### Time-series (timing) IC
For a single series, for example timing stocks against bonds, there is no cross-section: the IC is the correlation **across dates** between the score and the forward return that follows it.

$$IC^{\text{TS}}=\mathrm{corr}_t\big(\mathrm{rk}(s_t),\ \mathrm{rk}(R_{t\to t+h})\big)$$

**Variables:**

- $t$ sampling dates (e.g. the last trading day of each week)
- $s_t$ score known at $t$
- $h$ forecast horizon in trading days
- $R_{t\to t+h}$ return of the traded spread (e.g. equity basket minus bond basket) from $t$ to $t+h$
- $\mathrm{corr}_t$ correlation computed over the dates $t$

**Code:** the forward target is built by shifting prices **back** by $h$ days, so the row for date $t$ holds the return from $t$ to $t+h$ (`HORIZON` = 21; `eq`, `fi` are the equity and bond basket price series):

```python
fwd = (eq.shift(-HORIZON) / eq - 1) - (fi.shift(-HORIZON) / fi - 1)
```

`shift(-h)` is the only place future data enters, and only as the **target**; it must never feed the score.

**Notes:**

- Benchmarks are lower than for a cross-section: for a single stocks-vs-bonds series, 0.05 is interesting and 0.10 is rare.
- A one-year (52-week) rolling IC is the shortest window where a rank correlation is not mostly noise; an IC that keeps flipping sign around zero is the visual signature of noise.

**Code:** rolling 52-week rank IC over the weekly sample `df` (columns `z` = score, `fwd` = forward return), and the IC by calendar year with at least 10 weeks:

```python
zv, fv = df["z"].values, df["fwd"].values
rolling = pd.Series([_spearman(zv[i-52:i], fv[i-52:i]) if i >= 52 else np.nan
                     for i in range(1, len(df) + 1)], index=df.index)
yearly = df.groupby(df.index.year).apply(
    lambda g: rank_corr(g["z"], g["fwd"]) if len(g) > 10 else np.nan)
```

### Significance of an IC
$$t\approx\frac{IC\,\sqrt{n_{\text{eff}}-2}}{\sqrt{1-IC^2}}\approx IC\,\sqrt{n_{\text{eff}}-2}\quad(\text{small }IC)$$

**Variables:**

- $t$ t-statistic of the correlation under the null "true IC = 0"
- $IC$ estimated (rank) IC
- $n_{\text{eff}}$ effective number of independent observations: with overlapping forward windows it is much smaller than the number of dates ([[effective-sample-size]])

**Notes:**

- Plugging the raw number of dates into $n_{\text{eff}}$ overstates $t$ when forward windows overlap.
- **Hit rate** (share of dates where score and forward return have the same sign) is a separate, cruder statistic: `(np.sign(df["z"]) == np.sign(df["fwd"])).mean()`. A 56% hit rate can coexist with an IC near zero.
- Hurdle: $t\ge2$ is a minimum, never a triumph; a new idea needs $t\ge3$ ([[multiple-testing]], Harvey–Liu–Zhu 2016).

### ICIR
$$\overline{IC}=\frac1T\sum_{t=1}^TIC_t,\qquad \sigma_{IC}=\sqrt{\frac{1}{T-1}\sum_{t=1}^T\big(IC_t-\overline{IC}\big)^2},\qquad \text{ICIR}=\frac{\overline{IC}}{\sigma_{IC}},\qquad t\approx\text{ICIR}\,\sqrt T$$

**Variables:**

- $T$ number of periods
- $\overline{IC}$ mean IC
- $\sigma_{IC}$ standard deviation of the IC over time
- ICIR IC information ratio
- $t$ t-statistic of the mean IC

Mean IC 0.04 with σ 0.05 (ICIR 0.8) beats mean 0.06 with σ 0.15 (ICIR 0.4).

### Fundamental Law of Active Management
$$IR\approx IC\cdot\sqrt{BR}\cdot TC$$

**Variables:**

- $IR$ information ratio of the portfolio
- $IC$ signal skill
- $BR$ breadth (number of independent bets per year)
- $TC\in[0,1]$ transfer coefficient (Clarke–de Silva–Thorley): how much of the signal survives the portfolio constraints

IC = 0.03, BR = 1000 (with $TC=1$) → IR ≈ 0.95. **A low IC is fine if breadth compensates.**

### Key points
- The IC is cross-sectional (not time-series); report the universe; use tradable forward returns; use a point-in-time universe (survivorship); IC decays with horizon; hit rate ≠ IC.
- The IC is implementation-agnostic and enables signal blending ([[ic-contribution]]).
- Correlated factors reduce effective breadth ([[multicollinearity]]).

### Connections
- **Builds on:** [[variance-covariance-correlation]].
- **Used by:** [[ic-contribution]], [[grinold-alpha]], [[black-litterman]] (view confidence).

<a id="ic-contribution"></a>

## IC Contribution of a Composite Signal
<!-- section: ic-contribution | prerequisites: [information-coefficient, variance-covariance-correlation] | related: [grinold-alpha, risk-contribution, multicollinearity] | sources: [src-quant-finance-study-notes] | tags: [composite-signal, attribution, signal-redundancy] -->

When several z-scored signals are blended into a composite, the composite's IC splits exactly into one contribution per component: effective weight × stand-alone IC.

### Formula
$$S_{i,t}=\sum_{k=1}^Kw_k\,s_{k,i,t},\qquad IC_t=\sum_{k=1}^K\underbrace{\frac{w_k\,\mathrm{Cov}(s_{k,i,t},r_{i,t+1})}{\sigma_{S_t}\,\sigma_{r_{t+1}}}}_{IC^{(k)}_t},\qquad IC^{(k)}_t=\underbrace{\frac{w_k\,\sigma_{s_{k,t}}}{\sigma_{S_t}}}_{\phi_{k,t}}\times\underbrace{\mathrm{corr}(s_{k,i,t},r_{i,t+1})}_{\text{stand-alone IC}}$$

**Variables:**

- $S_{i,t}$ composite signal of asset $i$ at $t$
- $s_{k,i,t}$ component signal $k$ (z-scored)
- $w_k$ weight of component $k$; $K$ number of components
- $r_{i,t+1}$ forward return
- $\sigma_{S_t}$ cross-sectional standard deviation of the composite
- $\sigma_{r_{t+1}}$ cross-sectional standard deviation of returns
- $\sigma_{s_{k,t}}$ cross-sectional standard deviation of component $k$
- $IC^{(k)}_t$ contribution of component $k$
- $\phi_{k,t}$ effective weight of component $k$

**Why additive:** covariance is linear and the denominator is common to all components (the same idea as the Euler risk decomposition, [[risk-contribution]]).

### Steps (per period)
1. Z-score each signal.
2. Build the composite.
3. Compute the composite IC.
4. Compute the stand-alone ICs.
5. Effective weights $\phi_k=w_k/\sigma_{S_t}$ (z-scored components have $\sigma_{s_k}=1$).
6. $IC^{(k)}=\phi_k\times IC^{\text{solo}}_k$.
7. Check $\sum_kIC^{(k)}=IC_t$; average over time and report the t-stat.

### Worked example
Equal weights 1/3; corr(V,M) = 0.1, corr(V,Q) = 0.3, corr(M,Q) = 0:

$$\sigma_S^2=3\,(1/3)^2+2\,(1/3)^2\,(0.1+0.3+0)=0.422\ \Rightarrow\ \sigma_S=0.650,\qquad \phi_k=0.513$$

| Signal | Stand-alone IC | Contribution | Share |
|---|---|---|---|
| Value | 0.04 | 0.0205 | 33% |
| Momentum | 0.05 | 0.0256 | 42% |
| Quality | 0.03 | 0.0154 | 25% |
| **Composite** | | **0.0615** | |

### Key points
- A contribution depends on the correlation structure and weights (a property within a composite, not of the signal alone); it can be negative; Rank IC is not additive (use the Pearson approximation, Shapley values or leave-one-out); the marginal contribution ≠ $IC^{(k)}$.
- **Weighting schemes:** equal · IC-weighted · ICIR-weighted · full mean–variance on the IC covariance.

### Connections
- **Builds on:** [[information-coefficient]].
- **Used by:** [[grinold-alpha]] (composite IC), [[relative-value-long-short]], [[fx-carry-spot-slide]].

<a id="grinold-alpha"></a>

## Grinold: Alpha Score → Return Forecast
<!-- section: grinold-alpha | prerequisites: [information-coefficient, ols-regression] | related: [mean-variance-optimization, black-litterman, signal-to-weight, ic-contribution] | sources: [src-quant-finance-study-notes] | tags: [alpha, forecasting, grinold, mvo-inputs] -->

A signal score is not an expected return. Grinold's rule rescales it: forecast = skill × volatility × score.

### Formula
$$\alpha_i=IC\cdot\sigma_i\cdot z_i$$

**Variables:**

- $\alpha_i$ expected excess return of asset $i$
- $IC$ signal skill
- $\sigma_i$ **residual** (idiosyncratic) volatility of asset $i$: the opportunity
- $z_i$ cross-sectional z-score of the signal: the signal strength

### Derivation
$$r_{i,t+1}=a+b\,z_{i,t}+\varepsilon,\qquad b=\frac{\mathrm{Cov}(z,r)}{\mathrm{Var}(z)}=\mathrm{corr}(z,r)\,\sigma_r=IC\cdot\sigma_r$$

**Variables:**

- $a,b$ intercept and slope of the predictive regression
- $\sigma_r$ standard deviation of returns
- $\mathrm{Var}(z)=1$ for a z-score

Replacing $\sigma_r$ with the asset's own $\sigma_i$ gives $\alpha_i=IC\,\sigma_i\,z_i$.

### Worked example
IC = 0.04, $z$ = +1.2: AAPL with $\sigma$ = 22%: $0.04\times0.22\times1.2=$ **106 bps/yr**; a biotech with $\sigma$ = 55%: $0.04\times0.55\times1.2=$ **264 bps/yr**.

### Feeding mean–variance optimisation
$$\max_{w}\ w^\top\alpha-\frac\gamma2\,w^\top\Sigma w,\qquad w_i^*\propto\frac{\alpha_i}{\gamma\,\sigma_i^2}=\frac{IC\cdot z_i}{\gamma\,\sigma_i}\quad\text{(diagonal }\Sigma)$$

**Variables:**

- $w$ portfolio weights
- $\alpha$ vector of alphas
- $\Sigma$ covariance matrix (diagonal with entries $\sigma_i^2$ for the proportionality)
- $\gamma$ risk aversion

→ The optimal weight is **inversely** proportional to vol (alpha ∝ σ, risk ∝ σ²) — the same shape as $w\propto s/\sigma$ in [[signal-to-weight]].

### Which IC?
Historical mean (simple) · **shrunk toward 0 by 30–50% (standard)** · rolling · forward-looking · ICIR-based. Use an IC estimated on a strictly prior window.

### Multi-signal
$$\alpha_i=IC_{\text{comp}}\,\sigma_i\,z_{\text{comp},i}\ \ \text{(preferred: captures correlation)}\qquad\text{vs.}\qquad \alpha_i=\sigma_i\sum_kIC_k\,w_k\,z_{k,i}\ \ \text{(assumes orthogonal signals)}$$

**Variables:**

- $IC_{\text{comp}}$ IC of the composite signal
- $z_{\text{comp},i}$ z-score of the composite for asset $i$
- $IC_k,w_k,z_{k,i}$ IC, weight and z-score of component $k$

### Key points
- **Caveats:** residual, not total, vol; match the IC horizon to the alpha horizon; z-score within the cross-section; robust z (median/MAD, winsorise); assumes a linear conditional mean; conditional ICs by segment.
- **Properties:** alphas sum to ≈ 0 (long-short by construction); their dispersion ≈ IC·σ̄; aggregating recovers IR ≈ IC√BR.
- Don't believe the signal? Shrink the IC toward 0.
- **Relation to Black–Litterman:** Grinold is the front end (signal → alpha / view $Q$); BL is the back end (views + prior → portfolio) → [[black-litterman]].

### Connections
- **Builds on:** [[information-coefficient]], [[ols-regression]].
- **Feeds:** [[mean-variance-optimization]], [[black-litterman]], [[signal-to-weight]].

<a id="timing-signal-evaluation"></a>

## Evaluating a Timing Signal: Quantile Sorts, Timing Curve & Pass Rules
<!-- section: timing-signal-evaluation | prerequisites: [information-coefficient, effective-sample-size, time-series-momentum] | related: [research-workflow, backtest-pitfalls, multiple-testing, cross-validation-leakage, marginal-sharpe-improvement, risk-measures, sharpe-ratio, stock-bond-carry-case-study] | sources: [src-carry-course-notes] | tags: [timing, quantile-sort, timing-curve, drawdown, turnover, pre-registration] -->

A timing signal answers one question: does a series known today predict the return of a spread (e.g. equity minus bonds) over the next period? It is judged by a set of diagnostics, never by the IC alone: overlap-adjusted significance, the shape of returns across quantiles, a timing curve with its drawdown and turnover, independence from existing signals, and untouched later data, with pass and kill rules fixed before looking.

### The checklist

| Diagnostic | Question it answers | Pass reading |
|---|---|---|
| Rank IC ([[information-coefficient]]) | Is the direction right? | $IC>0$ |
| Overlap-adjusted $t$ ([[effective-sample-size]]) | Is it distinguishable from noise? | $t\ge2$ minimum; $t\ge3$ for a new idea |
| Quantile sort | Is the relation monotonic, so linear sizing is valid? | Bucket returns rise from Q1 to Q5 |
| Timing curve | What would positions proportional to the score have earned? | Positive return, tolerable drawdown, low turnover |
| Independence | Is it a duplicate of an existing signal? | Correlation with existing signals below ~0.7 |
| Out-of-sample / contribution | Does it survive later data and improve the portfolio? | Positive IC on sealed data; higher **net** portfolio Sharpe |

### Quantile sort
Sort the history into $Q$ buckets by score (typically $Q=5$) and average the forward return in each:

$$\bar R_q=\frac{1}{|B_q|}\sum_{t\in B_q}R_{t\to t+h},\qquad q=1,\dots,Q$$

**Variables:**

- $Q$ number of buckets (5 = quintiles)
- $B_q$ set of dates whose score falls in bucket $q$ (Q1 = lowest scores, bucket $Q$ = highest); $|B_q|$ its size
- $R_{t\to t+h}$ forward return of the spread over horizon $h$
- $\bar R_q$ average forward return in bucket $q$

**Notes:**

- Positions sized linearly in the score are valid only if $\bar R_q$ rises **monotonically**. A hump or U-shape means the sizing rule is wrong even when the IC is positive: the largest positions land where returns are worst.
- Five buckets balance resolution against stability; a decile-mean line on the scatter of score vs forward return adds finer shape.

**Code:** ranking first (`method="first"` breaks ties) makes `qcut` give five equal-size buckets even when many scores are identical (e.g. a capped z-score sitting at +2):

```python
buckets = pd.qcut(df["z"].rank(method="first"), 5,
                  labels=["Q1 low", "Q2", "Q3", "Q4", "Q5 high"])
quant = df.groupby(buckets, observed=True)["fwd"].mean()   # = R-bar_q
```

### Timing curve
Hold a position proportional to the score, compound from 1 unit and read the annualised return, the drawdown chart and the turnover:

$$w_t=\mathrm{clip}\Big(\frac{s_t}{2},-1,+1\Big),\qquad V_{t+1}=V_t\big(1+w_t\,R_{t\to t+1}\big),\ V_0=1$$

$$AR=V_T^{\,52/T}-1,\qquad DD_t=\frac{V_t}{\max_{u\le t}V_u}-1,\qquad TO=\frac1T\sum_{t=1}^{T}|w_t-w_{t-1}|$$

**Variables:**

- $s_t$ score at $t$ (capped z-score in $[-2,+2]$)
- $w_t$ position in the spread: $+1$ = 100% long equity / short bonds, $-1$ the reverse; $s_t=\pm2$ (maximum conviction) maps to a full, unlevered position, $s_t=0$ to flat
- $R_{t\to t+1}$ spread return over one rebalancing period (one week)
- $V_t$ value after $t$ weeks of 1 unit invested at $t=0$; $T$ number of weeks
- $AR$ annualised return; $52/T$ converts $T$ weeks into years
- $DD_t$ drawdown at $t$ (0 at a new high, negative below it); the worst drawdown is $\min_tDD_t$
- $TO$ turnover: average absolute weekly change in position

**Notes:**

- The curve holds one **week** (the live rebalancing clock), even when the IC is measured on a longer forward horizon: the diagnostic mimics the tradable object.
- The same sizing rule for every signal keeps the curves comparable.
- Report curves **gross**; costs are applied at the portfolio level, where a slow signal (high autocorrelation of $s_t$, e.g. 0.95) keeps nearly everything it earns.
- Read the underwater (drawdown) chart before the return chart: depth and duration of losses.

**Code:** the formulas above, one line each (`wks` = weekly dates; `_next_week(px, wks)` = each asset's return over the following week; `_ann` annualises the weekly returns):

```python
pos = (z.reindex(wks) / 2).clip(-1, 1)                              # w_t
weekly = (pos * (_next_week(eq, wks) - _next_week(fi, wks))).dropna()  # w_t * R_{t->t+1}
curve = (1 + weekly).cumprod()                                      # V_t
under = curve / curve.cummax() - 1                                  # DD_t
autocorr = z.reindex(wks).corr(z.reindex(wks).shift(1))             # slow signal -> low turnover
```

### Independence, out-of-sample and contribution
- A signal correlated above ~0.7 with an existing one is a duplicate.
- In-sample statistics never decide; only untouched later data and the **marginal improvement in net portfolio Sharpe** ([[marginal-sharpe-improvement]]) do. Fundamental law: $IR=IC\times\sqrt{BR}\times TC$ ([[information-coefficient]]).
- Robustness views: rolling 52-week IC, IC by calendar year (a minimum of 10 weeks per year so partial years cannot pose as evidence), IC by regime.

### Pre-registration: pass and kill rules
- Fix the pass rule (e.g. $IC>0$ and $t\ge1.5$) **before** looking at results, and fix kill criteria (e.g. out-of-sample IC turns negative) at the same time.
- Changing the registered design after seeing results (a new data source, a longer horizon) is a **new round** with the higher $t\ge3$ hurdle ([[multiple-testing]]): the price of peeking.
- A failed candidate with clean discipline is a result, not a waste.

**Code:** the rule is written into the test script before it is run, so the verdict is mechanical:

```python
verdict = "PASS to validate" if (ic > 0 and t >= 1.5) else "FAIL stop"
```

### Connections
- **Builds on:** [[information-coefficient]], [[effective-sample-size]], [[time-series-momentum]] (the capped z-score).
- **Used by:** [[carry-stock-bond-timing]] (full case study: [[carry-measurement-protocol]], [[stock-bond-carry-case-study]]).
- **Related:** [[research-workflow]], [[multiple-testing]], [[risk-measures]] (drawdown), [[cross-validation-leakage]] (clean splits).

<a id="research-workflow"></a>

## Research Workflow & Project Storytelling
<!-- section: research-workflow | prerequisites: [cross-validation-leakage] | related: [backtest-pitfalls, multiple-testing] | sources: [src-squarepoint-dqa-workbook] | tags: [research, communication] -->

A research project should move from a stated hypothesis to a documented, monitored deployment, checking at each step that only information available at decision time is used.

### Workflow
1. Hypothesis + an economic or operational reason.
2. What information is available **at decision time**.
3. A simple baseline.
4. Chronological validation + uncertainty ([[cross-validation-leakage]]).
5. Costs and feasibility.
6. Stability across periods, instruments and parameters.
7. Document failure modes; monitor the deployment.

### One project at three depths
- **30 s:** problem, your contribution, result.
- **2 min:** data, baseline, method, validation, result, limitation.
- **10 min:** assumptions, features, model choice, failed experiments, uncertainty, debugging, improvements.
- Be ready to explain every technical noun on your résumé.

### Answering technique
1. Clarify the setup.
2. Define the variables.
3. Name the principle.
4. Write the first equation.
5. Solve and check a limiting case.
6. Interpret, and state when it breaks.

If stuck: say what you know and simplify (e.g. solve the equal-vol case first).

### Connections
- **Builds on:** [[cross-validation-leakage]].
- **Selection risk:** [[multiple-testing]]. **When it goes wrong:** [[backtest-pitfalls]].

<a id="backtest-pitfalls"></a>

## Backtest Pitfalls & Live Underperformance
<!-- section: backtest-pitfalls | prerequisites: [research-workflow, multiple-testing] | related: [cross-validation-leakage, sharpe-ratio, price-reconciliation, conditional-probability-bayes] | sources: [src-squarepoint-dqa-workbook] | tags: [backtest, overfitting, survivorship] -->

A strategy that looked excellent in a backtest and loses money live is investigated from the most mechanical explanations to the most statistical ones: first check the implementation, then execution, then the research process, and only then ask whether the loss is actually surprising.

### "Sharpe 4 in backtest, loses immediately live" — investigation order
1. **Reconcile the implementation:** inputs, signal timing, target positions, fills, costs, P&L accounting; timestamps, corporate actions, duplicates, look-ahead data.
2. **Execution realism:** spread, slippage, delay, participation limits, borrow, financing.
3. **Research process:** selection across many trials ([[multiple-testing]]), out-of-sample evidence.
4. **Is the loss surprising** given the sample length, exposures and return distribution? Has the regime, liquidity or crowding changed?

### Key points
- Don't explain a bug as a regime change.
- A bad first week alone doesn't prove failure.
- Signal precision vs base rate: a rare true edge makes even good-looking detectors imprecise ([[conditional-probability-bayes]]).

### Usual suspects
Future information / leakage, bad corporate-action adjustment, unrealistic execution, duplicated rows, survivorship bias, strategy selection, stale prices, ignored costs.

### Connections
- **Builds on:** [[research-workflow]], [[multiple-testing]].
- **Related:** [[cross-validation-leakage]], [[sharpe-ratio]] (why a high SR misleads), [[price-reconciliation]] (the same "diff the inputs first" discipline).
