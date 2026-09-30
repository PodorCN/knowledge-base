---
id: signals-research-process
title: "Alpha, Signals & the Information Coefficient"
type: topic
domain: signal-research
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Alpha, Signals & the Information Coefficient

This chapter goes from "what is alpha" to "how big a return should I forecast". It defines excess return, alpha and beta, builds a simple time-series signal, measures a signal's skill with the information coefficient, attributes a composite signal's skill to its components, and converts a signal score into an expected-return forecast that a portfolio optimiser can use.

**Prerequisites:** [[ols-regression]], [[returns-simple-log]], [[variance-covariance-correlation]], [[time-series-validation]].

**Leads to:** [[signal-to-weight]], [[mean-variance-optimization]], [[black-litterman]], [[multi-asset-signals]].

**Sections:** [[capm-alpha-beta]] · [[time-series-momentum]] · [[information-coefficient]] · [[ic-contribution]] · [[grinold-alpha]]

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
<!-- section: time-series-momentum | prerequisites: [returns-simple-log] | related: [signal-to-weight, cross-validation-leakage, backtest-pitfalls] | sources: [src-signal-to-weight] | tags: [momentum, signal, z-score] -->

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

### Connections
- **Builds on:** [[returns-simple-log]].
- **Feeds:** [[signal-to-weight]] → [[risk-budgeting]]; the momentum leg of [[fx-carry-spot-slide]].

<a id="information-coefficient"></a>

## Information Coefficient (IC, Rank IC, ICIR) & the Fundamental Law
<!-- section: information-coefficient | prerequisites: [variance-covariance-correlation, time-series-momentum] | related: [ic-contribution, grinold-alpha, multiple-testing, multicollinearity, sharpe-ratio, cross-validation-leakage] | sources: [src-quant-finance-study-notes] | tags: [ic, rank-ic, icir, breadth, fundamental-law] -->

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
