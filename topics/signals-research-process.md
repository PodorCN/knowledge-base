---
id: signals-research-process
title: "Signals & Research Process"
type: topic
domain: signal-research
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Signals & Research Process

**Sections:** [[time-series-momentum]] · [[capm-alpha-beta]] · [[information-coefficient]] · [[ic-contribution]] · [[grinold-alpha]] · [[win-rate-expectancy]] · [[research-workflow]] · [[backtest-pitfalls]]

<a id="time-series-momentum"></a>

## Time-Series Momentum Signal ("Is the trend still up?")
<!-- section: time-series-momentum | prerequisites: [returns-simple-log] | related: [signal-to-weight, cross-validation-leakage, backtest-pitfalls] | sources: [src-signal-to-weight] | tags: [momentum, signal, z-score] -->

$$raw_t=\frac{P_t}{P_{t-12}}-1,\qquad z_t=\frac{raw_t-\mu_{raw}}{\sigma_{raw}},\qquad s_t=\mathrm{clip}(z_t,-2,+2)$$

**Variables:**

- $P_t$ price/index level at month $t$
- $P_{t-12}$ price 12 months ago
- $\mu_{raw},\sigma_{raw}$ mean/std of raw over a look-back window (window TBD)
- $s_t$ signal

### Reading the signal
- $s=0$: momentum at its historical average → no conviction, no position.
- $s=+1.5$: 1.5σ above average → moderately strong uptrend. $s=-2$: clipped floor (max bearish).
- **Sign = direction, magnitude = conviction**, unitless → different raw signals are comparable.

### Connections
- **Feeds:** [[signal-to-weight]] → [[risk-budgeting]].

<a id="capm-alpha-beta"></a>

## Excess Return, Alpha, Beta & CAPM
<!-- section: capm-alpha-beta | prerequisites: [ols-regression, returns-simple-log] | related: [omitted-variable-bias, exposure-neutrality, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [beta, alpha, factor] -->

$$R_i-r_f=\alpha_i+\beta_i(R_m-r_f)+\varepsilon_i,\qquad \beta_i=\frac{\mathrm{Cov}(R_i,R_m)}{\mathrm{Var}(R_m)},\qquad \text{CAPM: }E[R_i]-r_f=\beta_i(E[R_m]-r_f)$$

**Variables:**

- $R_i$ asset return
- $R_m$ market return
- $r_f$ same-period risk-free return
- $\alpha_i$ intercept
- $\varepsilon_i$ residual

- Beta = OLS slope. Positive alpha may be noise, an omitted factor ([[omitted-variable-bias]]) or selection bias.
- CAPM is an equilibrium model, not a definition of realised returns.

<a id="information-coefficient"></a>

## Information Coefficient (IC, Rank IC, ICIR) & the Fundamental Law
<!-- section: information-coefficient | prerequisites: [variance-covariance-correlation, time-series-momentum] | related: [ic-contribution, grinold-alpha, multiple-testing, multicollinearity, sharpe-ratio, cross-validation-leakage] | sources: [src-quant-finance-study-notes] | tags: [ic, rank-ic, icir, breadth, fundamental-law] -->

### Formula
$$IC_t=\frac{\sum_i(s_{i,t}-\bar s_t)(r_{i,t+1}-\bar r_{t+1})}{\sqrt{\sum_i(s_{i,t}-\bar s_t)^2}\sqrt{\sum_i(r_{i,t+1}-\bar r_{t+1})^2}}$$

**Variables:**

- $IC_t\in[-1,1]$ IC at period $t$
- $i=1..N$ assets in the cross-section
- $s_{i,t}$ signal at $t$
- $r_{i,t+1}$ realised forward return $t\to t+1$
- $\bar s_t,\bar r_{t+1}$ cross-sectional means

Timing: signal at $t$ vs returns from $t$ to $t+1$ (else look-ahead bias, [[cross-validation-leakage]]).

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
| Outliers | Sensitive (winsorise 1/99%) | Robust: industry default |

### ICIR
$$\overline{IC}=\frac1T\sum_tIC_t,\qquad \sigma_{IC}=\sqrt{\tfrac{1}{T-1}\textstyle\sum_t(IC_t-\overline{IC})^2},\qquad \text{ICIR}=\frac{\overline{IC}}{\sigma_{IC}},\qquad t\approx\text{ICIR}\sqrt T$$

**Variables:**

- $T$ number of periods

Mean IC 0.04 / σ 0.05 (ICIR 0.8) beats mean 0.06 / σ 0.15 (ICIR 0.4).

### Fundamental Law of Active Management
$$\text{IR}\approx IC\cdot\sqrt{BR}\cdot TC$$

**Variables:**

- IR portfolio information ratio
- $BR$ breadth (independent bets per year)
- $TC\in[0,1]$ transfer coefficient (Clarke–de Silva–Thorley): how much survives constraints

IC = 0.03, BR = 1000 → IR ≈ 0.95. **Low IC is fine if breadth compensates.**

### Key points
- Cross-sectional (not time-series); report the universe; tradable forward returns; point-in-time universe (survivorship); IC decay by horizon; hit rate ≠ IC.
- IC is implementation-agnostic and enables signal blending ([[ic-contribution]]).
- Correlated factors reduce effective breadth ([[multicollinearity]]).

### Connections
- **Used by:** [[ic-contribution]], [[grinold-alpha]], [[black-litterman]] (view confidence).

<a id="ic-contribution"></a>

## IC Contribution of a Composite Signal
<!-- section: ic-contribution | prerequisites: [information-coefficient, variance-covariance-correlation] | related: [grinold-alpha, risk-contribution, multicollinearity] | sources: [src-quant-finance-study-notes] | tags: [composite-signal, attribution, signal-redundancy] -->

### Formula
$$S_{i,t}=\sum_{k=1}^Kw_k\,s_{k,i,t},\qquad IC_t=\sum_{k=1}^K\underbrace{\frac{w_k\,\mathrm{Cov}(s_{k,i,t},r_{i,t+1})}{\sigma_{S_t}\,\sigma_{r_{t+1}}}}_{IC^{(k)}_t},\qquad IC^{(k)}_t=\underbrace{\frac{w_k\,\sigma_{s_{k,t}}}{\sigma_{S_t}}}_{\phi_{k,t}:\ \text{effective weight}}\times\underbrace{\mathrm{corr}(s_{k,i,t},r_{i,t+1})}_{\text{stand-alone IC}}$$

**Variables:**

- $S_{i,t}$ composite signal
- $s_{k,i,t}$ component $k$ (z-scored)
- $w_k$ weight; $K$ number of components
- $\sigma_{S_t}$ cross-sectional std of the composite
- $\sigma_{r_{t+1}}$ std of returns
- $\sigma_{s_{k,t}}$ std of component $k$

**Why additive:** covariance is linear and the denominator is common to all components (same idea as Euler risk decomposition, [[risk-contribution]]).

### Steps (per period)
1. Z-score each signal → 2. build composite → 3. composite IC → 4. stand-alone ICs → 5. $\phi_k=w_k/\sigma_{S_t}$ (z-scored) → 6. $IC^{(k)}=\phi_k\times IC^{solo}_k$ → 7. check $\sum_kIC^{(k)}=IC_t$ → average over time and report the t-stat.

### Worked example
Equal weights 1/3; corr(V,M) = 0.1, corr(V,Q) = 0.3, corr(M,Q) = 0:

$$\sigma_S^2=3(1/3)^2+2(1/3)^2(0.1+0.3+0)=0.422\Rightarrow\sigma_S=0.650,\ \ \phi_k=0.513$$

| Signal | Stand-alone IC | Contribution | Share |
|---|---|---|---|
| Value | 0.04 | 0.0205 | 33% |
| Momentum | 0.05 | 0.0256 | 42% |
| Quality | 0.03 | 0.0154 | 25% |
| **Composite** | | **0.0615** | |

### Key points
- Depends on correlation structure and weights (a property within a composite, not of the signal); can be negative; Rank IC is not additive (use the Pearson approximation, Shapley or leave-one-out); marginal contribution ≠ $IC^{(k)}$.
- **Weighting schemes:** equal · IC-weighted · ICIR-weighted · full mean–variance on the IC covariance.

<a id="grinold-alpha"></a>

## Grinold: Alpha Score → Return Forecast
<!-- section: grinold-alpha | prerequisites: [information-coefficient, ols-regression] | related: [mean-variance-optimization, black-litterman, signal-to-weight, ic-contribution] | sources: [src-quant-finance-study-notes] | tags: [alpha, forecasting, grinold, mvo-inputs] -->

### Formula
$$\alpha_i=\text{IC}\cdot\sigma_i\cdot z_i$$

**Variables:**

- $\alpha_i$ expected excess return of asset $i$
- IC signal skill
- $\sigma_i$ **residual** (idiosyncratic) volatility: the opportunity
- $z_i$ cross-sectional z-score: the signal strength

### Derivation
$$r_{i,t+1}=a+b\,z_{i,t}+\varepsilon,\qquad b=\frac{\mathrm{Cov}(z,r)}{\mathrm{Var}(z)}=\mathrm{corr}(z,r)\,\sigma_r=\text{IC}\cdot\sigma_r$$

Replace $\sigma_r$ with the asset's own $\sigma_i$ → $\alpha_i=\text{IC}\,\sigma_i\,z_i$.

**Example** (IC = 0.04, z = +1.2): AAPL, σ = 22%: $0.04\times0.22\times1.2=$ **106 bps/yr**; biotech, σ = 55%: $0.04\times0.55\times1.2=$ **264 bps/yr**.

### Feeding MVO
$$\max_{\mathbf w}\ \mathbf w^\top\boldsymbol\alpha-\frac\lambda2\mathbf w^\top\boldsymbol\Sigma\mathbf w,\qquad w_i^*\propto\frac{\alpha_i}{\lambda\sigma_i^2}=\frac{\text{IC}\cdot z_i}{\lambda\,\sigma_i}$$

**Variables:**

- $\mathbf w$ weights
- $\boldsymbol\Sigma$ covariance
- $\lambda$ risk aversion

→ the optimal weight is **inversely** proportional to vol (alpha ∝ σ, risk ∝ σ²); same shape as $w\propto s/\sigma$ in [[signal-to-weight]].

### Which IC?
Historical mean (simple) · **shrunk toward 0 by 30–50% (standard)** · rolling · forward-looking · ICIR-based. Use an IC estimated on a strictly prior window.

### Multi-signal
$$\alpha_i=\text{IC}_{\text{comp}}\,\sigma_i\,z_{\text{comp},i}\ \ \text{(preferred, captures correlation)}\qquad\text{vs.}\qquad \alpha_i=\sigma_i\sum_k\text{IC}_k\,w_k\,z_{k,i}\ \ \text{(assumes orthogonal signals)}$$

### Key points
- **Caveats:** residual not total vol; match IC horizon to alpha horizon; z-score within the cross-section; robust z (median/MAD, winsorise); assumes a linear conditional mean; conditional ICs by segment.
- **Properties:** alphas sum to ≈ 0 (long-short by construction); dispersion ≈ IC·σ̄; aggregating recovers IR ≈ IC√BR.
- Don't believe the signal? Shrink IC → 0.
- **Relation to BL:** Grinold = front end (signal → alpha / view $Q$); BL = back end (views + prior → portfolio) → [[black-litterman]].

### Connections
- **Builds on:** [[information-coefficient]], [[ols-regression]]. **Feeds:** [[mean-variance-optimization]], [[black-litterman]].

<a id="win-rate-expectancy"></a>

## Win Rate vs Expected Value
<!-- section: win-rate-expectancy | prerequisites: [expectation-linearity-indicators] | related: [risk-measures, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [expectancy] -->

$$E[\Pi]=pg-(1-p)\ell-c$$

**Variables:**

- $p$ win probability
- $g$ gain on win
- $\ell$ loss on loss
- $c$ cost per trade

- 90% win rate, +1 / −20 → $0.9-2=-1.1$ per trade.
- High win rate ≠ positive expectation (typical of short-option strategies).

<a id="research-workflow"></a>

## Research Workflow & Project Storytelling
<!-- section: research-workflow | prerequisites: [] | related: [backtest-pitfalls, cross-validation-leakage, multiple-testing] | sources: [src-squarepoint-dqa-workbook] | tags: [research, communication] -->

1. Hypothesis + economic/operational reason.
2. What information is available **at decision time**.
3. Simple baseline.
4. Chronological validation + uncertainty ([[cross-validation-leakage]]).
5. Costs & feasibility.
6. Stability across periods, instruments, parameters.
7. Document failure modes; monitor deployment.

### One project at three depths

- **30 s:** problem, your contribution, result.
- **2 min:** data, baseline, method, validation, result, limitation.
- **10 min:** assumptions, features, model choice, failed experiments, uncertainty, debugging, improvements.
- Be ready to explain every technical noun on your résumé.

### Answering technique
1. Clarify setup
2. Define variables
3. Name principle
4. Write the first equation
5. Solve & check a limiting case
6. Interpret and state when it breaks

If stuck: say what you know, simplify (equal-vol case first).

<a id="backtest-pitfalls"></a>

## Backtest Pitfalls & Live Underperformance
<!-- section: backtest-pitfalls | prerequisites: [research-workflow] | related: [multiple-testing, cross-validation-leakage, sharpe-ratio, price-reconciliation, conditional-probability-bayes] | sources: [src-squarepoint-dqa-workbook] | tags: [backtest, overfitting, survivorship] -->

### "Sharpe 4 in backtest, loses immediately live" — investigation order
1. **Reconcile implementation:** inputs, signal timing, target positions, fills, costs, PnL accounting; timestamps, corporate actions, duplicates, look-ahead data.
2. **Execution realism:** spread, slippage, delay, participation limits, borrow, financing.
3. **Research process:** selection across many trials ([[multiple-testing]]), out-of-sample evidence.
4. **Is the loss surprising** given sample length, exposures, return distribution? Regime/liquidity/crowding change?

- Don't explain a bug as a regime change.
- A bad first week alone doesn't prove failure.

### Usual suspects
Future information / leakage, bad corporate-action adjustment, unrealistic execution, duplicated rows, survivorship bias, strategy selection, stale prices, ignored costs.

### Connections
- [[cross-validation-leakage]], [[sharpe-ratio]] (why high SR misleads), [[price-reconciliation]] (same "diff the inputs first" discipline).
