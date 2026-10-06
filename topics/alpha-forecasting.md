---
id: alpha-forecasting
title: "Alpha & Return Forecasts"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Alpha & Return Forecasts

This chapter defines excess return, alpha and beta, and converts a signal score into an expected-return forecast that a portfolio optimiser can use.

**Prerequisites:** [[ols-regression]], [[returns-simple-log]], [[information-coefficient]], [[ic-contribution]].

**Leads to:** [[exposure-neutrality]], [[structural-risk-premia]], [[relative-value-long-short]], [[mean-variance-optimization]], [[black-litterman]], [[signal-to-weight]].

**Sections:** [[capm-alpha-beta]] · [[grinold-alpha]]

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
