---
id: signals-research-process
title: "Signals & Research Process"
type: topic
domain: signal-research
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook]
---
# Signals & Research Process

**Sections:** [[time-series-momentum]] · [[capm-alpha-beta]] · [[win-rate-expectancy]] · [[research-workflow]] · [[backtest-pitfalls]]

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

<a id="win-rate-expectancy"></a>

## Win Rate vs Expected Value
<!-- section: win-rate-expectancy | prerequisites: [expectation-linearity-indicators] | related: [risk-measures, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [expectancy] -->

$$E[\Pi]=pg-(1-p)\ell-c$$

**Variables:**

- $p$ win probability
- $g$ gain on win
- $\ell$ loss on loss
- $c$ cost per trade

90% win rate, +1 / −20 → $0.9-2=-1.1$ per trade. High win rate ≠ positive expectation (typical of short-option strategies).

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

**30 s:** problem, your contribution, result. **2 min:** data, baseline, method, validation, result, limitation. **10 min:** assumptions, features, model choice, failed experiments, uncertainty, debugging, improvements.
Be ready to explain every technical noun on your résumé.

### Answering technique
Clarify setup → define variables → name principle → write the first equation → solve & check a limiting case → interpret and state when it breaks. If stuck: say what you know, simplify (equal-vol case first).

<a id="backtest-pitfalls"></a>

## Backtest Pitfalls & Live Underperformance
<!-- section: backtest-pitfalls | prerequisites: [research-workflow] | related: [multiple-testing, cross-validation-leakage, sharpe-ratio, price-reconciliation, conditional-probability-bayes] | sources: [src-squarepoint-dqa-workbook] | tags: [backtest, overfitting, survivorship] -->

### "Sharpe 4 in backtest, loses immediately live" — investigation order
1. **Reconcile implementation:** inputs, signal timing, target positions, fills, costs, PnL accounting; timestamps, corporate actions, duplicates, look-ahead data.
2. **Execution realism:** spread, slippage, delay, participation limits, borrow, financing.
3. **Research process:** selection across many trials ([[multiple-testing]]), out-of-sample evidence.
4. **Is the loss surprising** given sample length, exposures, return distribution? Regime/liquidity/crowding change?

Don't explain a bug as a regime change. A bad first week alone doesn't prove failure.

### Usual suspects
Future information / leakage, bad corporate-action adjustment, unrealistic execution, duplicated rows, survivorship bias, strategy selection, stale prices, ignored costs.

### Connections
- [[cross-validation-leakage]], [[sharpe-ratio]] (why high SR misleads), [[price-reconciliation]] (same "diff the inputs first" discipline).
