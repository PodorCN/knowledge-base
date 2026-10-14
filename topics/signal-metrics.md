---
id: signal-metrics
title: "Signal Metrics"
type: topic
domain: signal-research
sources: [src-quant-finance-study-notes, src-carry-course-notes, src-signal-to-weight]
---
# Signal Metrics

This chapter introduces the fundamental mathematical metrics used to evaluate and compare predictive signals before portfolio construction: measuring skill via the Information Coefficient (Pearson vs Rank IC, time-series vs cross-sectional, and composite IC contribution), testing statistical significance under overlapping returns, tracking stability with ICIR and hit rate, relating skill, independent breadth and implementation with the Fundamental Law of Active Management, and mapping scores into positions to measure timing curves, drawdowns, turnover, and transaction costs.

**Prerequisites:** [[returns-simple-log]], [[variance-covariance-correlation]], [[effective-sample-size]], [[time-series-validation]].

**Leads to:** [[timing-signal-evaluation]], [[grinold-alpha]], [[signal-to-weight]], [[black-litterman]], [[multi-asset-signals]].

**Sections:** [[information-coefficient]] · [[ic-contribution]] · [[ic-significance]] · [[icir-stability]] · [[hit-rate]] · [[fundamental-law-active-management]] · [[signal-position-construction]] · [[timing-curve-metrics]] · [[turnover-cost-drag]]

<a id="information-coefficient"></a>

## Information Coefficient
<!-- section: information-coefficient | prerequisites: [variance-covariance-correlation, effective-sample-size] | related: [ic-significance, icir-stability, hit-rate, timing-signal-evaluation] | sources: [src-quant-finance-study-notes, src-carry-course-notes] | tags: [ic, rank-ic, pearson, spearman, ic-contribution] -->

The information coefficient measures association between an available signal and a specified subsequent return. Define the comparison axis and horizon before computing it: asset selection compares assets at a date; timing compares dates for an asset or spread.

### Formula

$$IC_t^{\mathrm{CS}}=\operatorname{corr}_{i}(s_{i,t},R_{i,t\to t+h}),\qquad IC^{\mathrm{TS}}=\operatorname{corr}_{t}(s_t,R_{t\to t+h})$$

**Variables:**

- $IC_t^{\mathrm{CS}}$ cross-sectional Pearson IC on date $t$, in $[-1,1]$
- $IC^{\mathrm{TS}}$ time-series Pearson IC over the evaluation dates, in $[-1,1]$
- $i$ asset index within the eligible universe at date $t$
- $t$ trading date; the correlation subscript specifies the comparison axis
- $s_{i,t}$ score of asset $i$ available at the decision time on date $t$
- $s_t$ available score for the single asset or spread being timed
- $h$ target horizon in trading days
- $R_{i,t\to t+h}$ asset's realised forward simple return, in decimals
- $R_{t\to t+h}$ realised forward simple return of the timed asset or spread
- $\operatorname{corr}_{i}$ Pearson correlation across assets on one date
- $\operatorname{corr}_{t}$ Pearson correlation across dates in one sample

### Key points

- **Pearson IC** measures linear association, not exact proportionality. It is affected by return magnitudes and can be sensitive to outliers.
- **Rank IC** is Pearson correlation after separately ranking scores and returns on the same axis. It measures ordering and is invariant to strictly increasing transformations of either variable. Outliers still influence their ranks; their monetary magnitude no longer enters directly.
- Assign average ranks to ties. The shortcut based on squared rank differences below assumes no ties. Constant scores or returns give undefined correlation, not zero skill.
- A positive IC supports the specified orientation, subject to uncertainty. A negative IC may indicate reversal or noise. Changing orientation after observing it is another selection step.
- IC levels depend on universe, horizon, target and preprocessing. The notes' 0.01–0.03, 0.03–0.05 and 0.05–0.10 ranges are contextual heuristics; IC above 0.10 warrants investigation but does not prove leakage.

### Rank correlation calculation

$$IC^{\mathrm{rank}}=\operatorname{corr}(\operatorname{rk}(s),\operatorname{rk}(R))=1-\frac{6\sum_{j=1}^{n}d_j^2}{n(n^2-1)}$$

**Variables:**

- $IC^{\mathrm{rank}}$ Spearman correlation, in $[-1,1]$
- $s$ vector of scores in the chosen cross section or time sample
- $R$ matching vector of forward returns
- $\operatorname{rk}$ ascending rank operator, using average ranks for ties
- $\operatorname{corr}$ Pearson correlation of the two rank vectors
- $n$ number of matched observations; the shortcut requires no ties
- $j$ observation index, running from 1 to $n$
- $d_j$ score rank minus return rank for observation $j$

### Worked example

| Asset | Score | Score rank | Weekly return | Return rank | Rank difference | Squared difference |
|---|---|---|---|---|---|---|
| A | +1.2 | 4 | +0.8% | 4 | 0 | 0 |
| B | −0.5 | 2 | −0.2% | 2 | 0 | 0 |
| C | +0.3 | 3 | +1.5% | 5 | −2 | 4 |
| D | +2.0 | 5 | +0.4% | 3 | +2 | 4 |
| E | −1.1 | 1 | −0.6% | 1 | 0 | 0 |

The squared differences sum to 8, giving Rank IC $1-6\times8/(5\times24)=0.60$. Pearson IC is approximately 0.5436. Replacing E's return with −10.0% leaves all ranks unchanged, so Rank IC stays 0.60; Pearson IC rises to approximately 0.6735. The example demonstrates sensitivity to magnitudes, not that rank correlation is always the appropriate trading objective.

### Connections

- **Builds on:** [[variance-covariance-correlation]], [[effective-sample-size]].
- **Used by:** [[ic-contribution]], [[ic-significance]], [[icir-stability]], [[fundamental-law-active-management]], [[eval-directional-prediction]].

<a id="ic-contribution"></a>

## IC Contribution of a Composite Score
<!-- section: ic-contribution | prerequisites: [information-coefficient] | related: [grinold-alpha, eval-correlation-redundancy] | sources: [src-quant-finance-study-notes] | tags: [ic-contribution, composite, correlation] -->

A composite combines component scores; its predictive correlation depends on both their skills and their covariance. For Pearson IC against a common target on the same observations, covariance linearity gives an additive decomposition.

### Formula

$$S=\sum_{k=1}^{K}a_k s_k,\qquad IC_S=\sum_{k=1}^{K}\phi_k IC_k,\qquad \phi_k=\frac{a_k\sigma_k}{\sigma_S}$$

**Variables:**

- $S$ composite score vector
- $K$ number of component signals
- $k$ component index, running from 1 to $K$
- $a_k$ fixed component combination weight
- $s_k$ component score vector over the same observations
- $IC_S$ Pearson correlation of the composite with the common forward-return target
- $IC_k$ Pearson correlation of component $k$ with that target
- $\phi_k$ component's correlation scaling coefficient; not generally a risk-budget share
- $\sigma_k$ sample standard deviation of component $k$
- $\sigma_S$ sample standard deviation of the composite, required positive

### Key points

The coefficients need not sum to one. This identity does not apply directly to the Rank IC of a raw-score composite, because ranking the composite is nonlinear.

### Worked example

Equal weights on unit-variance Value, Momentum and Quality, with pairwise correlations 0.10, 0.30 and 0.00, give composite standard deviation 0.6498 and each coefficient 0.5130. Standalone ICs 0.040, 0.050 and 0.030 contribute approximately 0.0205, 0.0256 and 0.0154; composite Pearson IC is 0.0616. The decomposition is:

| Component | Standalone Pearson IC | IC contribution | Share of composite IC |
|---|---|---|---|
| Value | 0.040 | 0.0205 | 33.3% |
| Momentum | 0.050 | 0.0256 | 41.7% |
| Quality | 0.030 | 0.0154 | 25.0% |
| Composite | — | 0.0616 | 100.0% |

Low correlation can improve the composite, but does not guarantee improvement for arbitrary weights and skills.

### Connections

- **Builds on:** [[information-coefficient]].
- **Used by:** [[grinold-alpha]].
- **Related:** [[eval-correlation-redundancy]].

<a id="ic-significance"></a>

## Statistical Uncertainty of IC
<!-- section: ic-significance | prerequisites: [information-coefficient, effective-sample-size] | related: [icir-stability, eval-statistical-significance, multiple-testing] | sources: [src-carry-course-notes, src-quant-finance-study-notes] | tags: [t-stat, significance, overlap-adjustment, newey-west] -->

An estimated IC needs an uncertainty assessment. Distinguish testing a predictive correlation from testing a strategy's mean return: they measure different objects, before and after position construction respectively.

### Formula

For independent bivariate-normal pairs, the Pearson correlation statistic has an exact null Student distribution. The carry notes use an effective-sample substitution as a rough screening approximation:

$$t_{IC}\approx\frac{\widehat{IC}\sqrt{n_{\mathrm{eff}}-2}}{\sqrt{1-\widehat{IC}^{\,2}}},\qquad m=\frac{h}{\Delta},\qquad n_{\mathrm{eff}}\approx\frac{n}{m}$$

**Variables:**

- $t_{IC}$ approximate correlation screening statistic; not the time index
- $\widehat{IC}$ estimated correlation, with absolute value less than one
- $n_{\mathrm{eff}}$ assumed independent-equivalent sample size, required greater than two
- $n$ number of matched signal/forward-return observations
- $m$ overlap ratio; this approximation concerns overlapping horizons with $h\ge\Delta$
- $h$ forward-return horizon in trading days
- $\Delta$ sampling interval in trading days; approximately five for weekly sampling

### Key points

- Under independent bivariate-normal pairs, use the actual sample size and null degrees of freedom equal to sample size minus two. Spearman inference is different; the formula with an estimated effective sample size is not an exact dependent-data test.
- The overlap approximation comes from summed independent return increments. Persistent scores, nonlinear statistics and additional serial dependence can change the relevant sampling uncertainty.
- For cross-sectional IC, inference on the mean periodic IC uses the time series of IC estimates and its dependence. Stacking all asset-date pairs is a different estimator and does not make them independent.
- Dependence-aware bootstrap methods or HAC inference for a specified regression require explicit assumptions. Ordinary independent shuffling is not a general solution for dependent observations.
- The return-mean statistic equals period Sharpe times square root of observation count under the corresponding independent-return standard-error calculation ([[sharpe-ratio]]). It does not test IC.
- Carry's 1.5 hurdle is a screening choice. A statistic near 2 is a large-sample two-sided 5% approximation, and 3 is a context-dependent multiple-testing benchmark. None replaces specifying the test and candidate family.
- Failure to reject zero indicates insufficient evidence, not proof of no effect or proof that profits were luck.

### Worked example

Weekly sampling of 21-day forwards has overlap ratio $21/5=4.2$ and adjacent windows share about 16 trading days. With 574 observations, the approximation gives 136.67 effective observations; IC 0.0423 gives statistic about 0.49. With 520 observations it gives 123.81. These are approximations, not counts of independent economic cycles.

**Reference:** [SciPy's Spearman documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) discusses limitations of asymptotic p-values; [statsmodels HAC documentation](https://www.statsmodels.org/stable/generated/statsmodels.stats.sandwich_covariance.cov_hac.html) describes regression covariance estimation under time dependence.

### Connections

- **Builds on:** [[information-coefficient]], [[effective-sample-size]].
- **Used by:** [[eval-statistical-significance]].
- **Related:** [[multiple-testing]], [[robust-standard-errors]].

<a id="icir-stability"></a>

## ICIR: Stability of Signal Over Time
<!-- section: icir-stability | prerequisites: [information-coefficient] | related: [ic-significance, timing-signal-evaluation] | sources: [src-quant-finance-study-notes] | tags: [icir, stability, sharpe-of-ic] -->

ICIR is the mean periodic IC divided by its sample standard deviation. It describes the IC series across time; it is distinct from the portfolio information ratio (IR), which uses active returns and tracking error.

### Formula
$$\text{ICIR}=\frac{\overline{IC}}{\sigma_{IC}},\qquad \overline{IC}=\frac1T\sum_{t=1}^TIC_t,\qquad \sigma_{IC}=\sqrt{\frac{1}{T-1}\sum_{t=1}^T(IC_t-\overline{IC})^2}$$

**Variables:**

- $\text{ICIR}$ information coefficient information ratio (signal stability across time)
- $\overline{IC}$ average information coefficient over the evaluation period
- $\sigma_{IC}$ sample standard deviation of periodic information coefficients over time
- $IC_t$ information coefficient at period $t$
- $T$ number of periodic IC observations, required greater than one
- $t$ periodic IC index; specify whether each observation is cross-sectional IC or a time-window estimate

### Why ICIR matters: consistency beats peak IC
Consider two competing signals evaluated over 3 years:
- **Signal A (Volatile Gambler):** Mean IC is $+0.06$, but standard deviation is $0.20$ ($\text{ICIR} = 0.30$). Some months it hits $+0.30$, but other months it falls to $-0.25$. These describe unstable measured association, not a calculation of portfolio drawdown.
- **Signal B (Steady Engine):** Mean IC is $+0.04$, but standard deviation is only $0.05$ ($\text{ICIR} = 0.80$). The mean and standard deviation alone do not determine the range of individual monthly ICs.

Signal B has higher estimated ICIR (0.80 versus 0.30), indicating a larger mean relative to the variation in its periodic IC. This does not establish a smoother live profit curve: positions, return magnitudes, costs and tail exposures still matter.
- State the IC sampling frequency, forecast horizon and any annualisation. The notes' 0.5 and 1.0 benchmarks are contextual heuristics. Overlapping rolling ICs are dependent; their smoothness does not establish independent evidence. ICIR is undefined if its denominator is zero.

### Connections
- **Builds on:** [[information-coefficient]].
- **Used by:** [[timing-signal-evaluation]].

<a id="hit-rate"></a>

## Directional Hit Rate
<!-- section: hit-rate | prerequisites: [information-coefficient] | related: [ic-significance, timing-signal-evaluation] | sources: [src-carry-course-notes] | tags: [hit-rate, win-rate, direction] -->

The directional hit rate is the simplest intuitive diagnostic: what percentage of the time did the signal point in the correct direction?

### Formula
$$HR=\frac1T\sum_{t=1}^T\mathbf{1}_{\{\mathrm{sign}(s_t)=\mathrm{sign}(R_{t\to t+h})\}}$$

**Variables:**

- $HR$ directional hit rate (percentage of periods where signal and return agree in sign)
- $T$ number of evaluation dates retained under the stated zero-signal and zero-return policy
- $s_t$ directional score available at date $t$, with zero defined as neutral
- $t$ evaluation date index
- $h$ forecast horizon in trading days
- $R_{t\to t+h}$ realised forward simple return over horizon $h$
- $\mathrm{sign}$ sign operator, taking values minus one, zero or plus one
- $\mathbf{1}_{\{\cdot\}}$ indicator function taking value 1 if the condition holds, 0 otherwise

**Notes:** specify whether abstentions and zero returns are excluded or counted. Fifty percent is the baseline for symmetric guessing, not automatically for an imbalanced return-sign distribution.

### Why hit rate alone is deceptive
A 58% hit rate sounds great to novice traders, but **hit rate ignores magnitude**:
- If you are right 58% of the time on tiny $+0.2\%$ market drifts, but wrong 42% of the time during sudden $-3.0\%$ market plunges, you will lose massive amounts of money despite a "high hit rate".
- Hit rate is a directional sanity check, never a sufficient condition for a strategy. Interpret it alongside predictive association and net trading returns; there is no universal requirement that all three measures agree in every strategy.

### Connections
- **Builds on:** [[information-coefficient]].
- **Used by:** [[timing-signal-evaluation]].

<a id="fundamental-law-active-management"></a>

## The Fundamental Law of Active Management
<!-- section: fundamental-law-active-management | prerequisites: [information-coefficient] | related: [grinold-alpha, eval-correlation-redundancy] | sources: [src-quant-finance-study-notes] | tags: [fundamental-law, information-ratio, breadth, transfer-coefficient] -->

The fundamental law connects predictive skill with expected portfolio performance under an idealised model. Skill matters, independent opportunities provide breadth, and portfolio constraints affect how much of the forecast can be implemented. It is a planning relationship, not a guarantee of realised profit or a measure of trading capacity.

### Formula

$$IR=\frac{E[A]}{\sigma_A},\qquad IR\approx IC\sqrt{BR}\,TC$$

**Variables:**

- $IR$ information ratio: expected active return per unit of tracking error, over a stated horizon
- $A$ portfolio return minus benchmark return over that horizon, in decimals
- $E[A]$ expected active return over that horizon
- $\sigma_A$ standard deviation of active return (tracking error), required positive
- $IC$ forecast skill per independent opportunity under the model's risk adjustment; a historical Rank IC is a proxy rather than an automatic exact substitute
- $BR$ number of independent opportunities per year when the relationship is used for annual performance
- $TC$ transfer coefficient, measuring alignment between forecasts and implemented active positions; one represents ideal unconstrained alignment

### Key points

- **IC versus IR:** IC describes predictive association; IR describes portfolio active return relative to its variability. Neither is the directional hit rate. Match horizons and distinguish expected quantities from sample estimates.
- **Breadth:** 500 correlated stocks are not automatically 500 independent bets. Repeated observations of the same slow-moving signal are not automatically new independent opportunities either.
- **TC:** long-only restrictions, position limits and turnover constraints may prevent the desired active positions. A smaller positive TC means less of the model's forecast is expressed for the same active risk.
- **Interpretation:** increasing independent breadth helps only if skill and implementation remain comparable. Turnover, correlated opportunities and deteriorating skill can undermine the apparent gain.
- **Costs:** incorporate costs consistently into the optimisation and return forecasts. A high TC does not independently prove net profitability, liquidity or capacity.

### Worked example

With skill 0.04, 100 independent opportunities per year and TC 0.5, the planning relationship gives annual IR approximately $0.04\times\sqrt{100}\times0.5=0.20$. With ideal alignment (TC 1), the same model gives 0.40. These are illustrative model outputs, not backtest evidence.

<details>
<summary>Interpreting the transfer coefficient</summary>

For a positive-definite risk covariance matrix, the transfer coefficient can be defined as the cosine between the risk-adjusted forecast vector and the risk-adjusted active-weight vector. It lies between minus one and plus one; negative values mean the positions oppose the forecast. In the usual intended implementation, attention centres on values from zero to one. TC zero means no alignment under this risk model; a negative TC means the implemented portfolio takes the opposite side of the forecast. The unconstrained mean–variance portfolio has TC one when weights align with the model's optimal direction.

The original hedge-fund range 0.9–1.0 and mutual-fund range 0.3–0.5 are illustrative, not classifications that determine a fund's TC. A tracking-error budget alone can scale an otherwise unconstrained portfolio without reducing its alignment.

</details>

### Correlation and effective counts

An equal-weight average of equal-variance observations with a common pairwise correlation has the following independent-equivalent count for the variance of its mean:

$$N_{\mathrm{eff}}=\frac{N}{1+(N-1)\bar\rho}$$

**Variables:**

- $N_{\mathrm{eff}}$ independent-equivalent observation count for this equal-weight averaging model
- $N$ number of equal-variance observations
- $\bar\rho$ common pairwise correlation; the covariance must be valid and the denominator positive

**Notes:** at $N=500$ and $\bar\rho=0.20$, this gives about 4.96. It illustrates how dependence affects an average; it is not a general estimator of active-management breadth. The original casino analogy conveys repeated independent opportunities, but a 2.7% house edge is not an IC of 0.02 and cannot be substituted as one. Even many favourable independent bets do not guarantee a profit over a finite horizon.

**Reference:** [CFA Institute: Analysis of Active Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/analysis-active-portfolio-management).

### Connections

- **Builds on:** [[information-coefficient]].
- **Used by:** [[grinold-alpha]], [[eval-correlation-redundancy]].
- **Related:** [[measuring-performance]].

<a id="signal-position-construction"></a>

## Signal Position Construction (Score to Weight)
<!-- section: signal-position-construction | prerequisites: [information-coefficient] | related: [timing-curve-metrics, turnover-cost-drag, signal-to-weight] | sources: [src-carry-course-notes, src-signal-to-weight] -->

Before a signal can generate a backtest or trade live, its raw indicator must be converted into an active portfolio position without lookahead bias.

### Formula
The carry example standardises using an expanding historical window and maps linearly to a diagnostic spread exposure. Inputs at date $t$ must be available before the assumed execution; use a minimum history and handle zero estimated variance explicitly:

$$z_t=\frac{x_t-\bar x_{\le t}}{\hat\sigma_{\le t}},\qquad s_t=\mathrm{clip}(z_t,-2,+2),\qquad w_t=\mathrm{clip}\left(\frac{s_t}{2},-1,+1\right)$$

**Variables:**

- $x_t$ raw signal indicator at date $t$
- $\bar x_{\le t}$ historical expanding mean of $x$ up to date $t$
- $\hat\sigma_{\le t}$ historical expanding standard deviation of $x$ up to date $t$
- $z_t$ standardised expanding z-score at date $t$
- $s_t$ signal score clipped to $[-2,+2]$
- $w_t$ diagnostic spread exposure in $[-1,1]$; positive means long the first leg and short the second, negative reverses both, zero is flat
- $t$ decision date, after input availability and before execution
- $\mathrm{clip}$ operator limiting its input to the stated lower and upper bounds

### Key points
1. **Expanding vs rolling:** rolling windows require picking an arbitrary lookback (e.g. 1 year or 3 years), creating an extra parameter to overfit. Expanding windows use all available history but may adapt slowly to structural changes. Rolling windows can also be point-in-time; window length is a design choice to evaluate, not evidence of leakage by itself.
2. **Capping at $\pm 2$:** a z-score above $+2$ occurs only $\sim 2.5\%$ of the time under normality. The cap limits this rule's exposure. The normal-tail calculation is illustrative, not an empirical guarantee about financial signal scores.
3. **Linear mapping:** $s_t = 0 \implies w_t = 0$ (neutral). $s_t = +1.0 \implies w_t = +0.50$ (half position). $s_t = +2.0 \implies w_t = +1.00$ (full position).

### Connections
- **Builds on:** [[information-coefficient]].
- **Used by:** [[timing-curve-metrics]], [[turnover-cost-drag]], [[signal-to-weight]].

<a id="timing-curve-metrics"></a>

## Timing Curve & Underwater Drawdown
<!-- section: timing-curve-metrics | prerequisites: [signal-position-construction, returns-simple-log] | related: [turnover-cost-drag, timing-signal-evaluation] | sources: [src-carry-course-notes] | tags: [timing-curve, equity-curve, drawdown, compounding] -->

A timing curve simulates holding the signal position over time, compounding a unit of initial capital to evaluate gross profitability and peak-to-trough drawdowns.

### Formula
$$V_{t+1}=V_t\big(1+w_t\,R_{t\to t+1}\big),\qquad V_0=1,\qquad AR=V_T^{\,52/T}-1$$

**Variables:**

- $V_t$ portfolio value at week $t$ starting from $V_0=1$
- $w_t$ position held from week $t$ to $t+1$
- $R_{t\to t+1}$ realised spread return over week $t$ to $t+1$
- $V_0$ initial strategy capital, normalized to 1
- $AR$ annualised geometric compound return
- $V_T$ final strategy value after $T$ weeks
- $T$ total number of weekly rebalance intervals, required positive
- $t$ weekly index
- $52$ assumed number of weekly intervals per year

**Notes:** this is a simplified spread sleeve, not automatically a full stock/bond portfolio. Here $t$ counts weekly rebalance intervals rather than trading days; the return is one holding-interval return, not an overlapping 21-day label. Financing and baseline holdings must be specified for a complete strategy.

### Underwater drawdown curve
$$DD_t=\frac{V_t}{\max_{u\le t}V_u}-1,\qquad \text{Max }DD=\min_{1\le t\le T}DD_t$$

**Variables:**

- $DD_t$ drawdown at week $t$ ($DD_t\le0$, 0 at peak)
- $V_t$ portfolio value at week $t$
- $\text{Max }DD$ maximum drawdown over the entire backtest period
- $T$ total number of weekly rebalance intervals
- $t$ current weekly index
- $u$ historical weekly index, including zero so the initial value enters the running peak
- $\max$ running maximum operator
- $\min$ minimum over the evaluation period

**Reading the underwater chart:**
Read the underwater chart alongside the return curve:
- How deep is the worst loss ($\text{Max }DD$)?
- How long does the strategy stay underwater before recovering to a new high (drawdown duration)?
- A strategy earning 10% a year with a three-year underwater period and a 25% peak loss may be unsuitable for a mandate; investor responses are not mechanically determined by these numbers.

### Connections
- **Builds on:** [[signal-position-construction]], [[returns-simple-log]].
- **Used by:** [[turnover-cost-drag]], [[timing-signal-evaluation]].

<a id="turnover-cost-drag"></a>

## Turnover & Transaction Cost Drag
<!-- section: turnover-cost-drag | prerequisites: [timing-curve-metrics] | related: [timing-signal-evaluation] | sources: [src-carry-course-notes] | tags: [turnover, transaction-costs, net-return, autocorrelation] -->

Paper backtests assume frictionless trading. In live execution, brokerage commissions, bid-ask spreads, and market impact take an immediate bite out of returns on every trade.

### Formula
$$TO=\frac1T\sum_{t=1}^T|w_t-w_{t-1}|,\qquad \text{Cost}=c\cdot TO\cdot52,\qquad AR_{\text{net}}\approx AR-\text{Cost}$$

**Variables:**

- $TO$ average weekly turnover (absolute position change per week)
- $w_t, w_{t-1}$ position weights at weeks $t$ and $t-1$
- $T$ number of weekly rebalance intervals
- $t$ weekly index
- $52$ assumed number of weekly intervals per year
- $c$ one-way transaction cost per unit traded (e.g. 5 bps = 0.0005)
- $\text{Cost}$ annual transaction cost drag
- $AR$ annualised gross return
- $AR_{\text{net}}$ annualised net return after transaction costs

**Notes:** this toy turnover measures target-weight changes. Actual turnover uses pretrade holdings and counts both legs consistently. The cost parameter must specify whether it covers one leg or the entire spread. Annual drag and subtraction from geometric gross return are approximations; exact net CAGR compounds net period returns.

### Persistence and turnover
Persistence can reduce trading under a fixed mapping, but these autocorrelation/turnover pairs are illustrative. Scale, clipping, sizing and price-driven rebalancing also matter:
- **Slow Macro Signal (e.g. Carry, Dividend Yield):**
  Weekly autocorrelation $\rho \approx 0.95$. The score moves sluggishly, so weekly turnover is minimal ($TO \approx 0.08$). Total annual cost at 5 bps is only $0.0005 \times 0.08 \times 52 \approx 0.21\% / \text{year}$. This drag must be compared with gross return and other implementation costs.
- **Fast Noisy Signal (e.g. Short-term Sentiment):**
  Weekly autocorrelation $\rho \approx 0.30$. The score flips direction constantly, causing turnover to spike ($TO \approx 0.60$). Annual transaction drag is $0.0005 \times 0.60 \times 52 \approx 1.56\% / \text{year}$. If gross annual return was $2.0\%$, net return is approximately $0.44\%$ before other frictions and compounding effects.

### Connections
- **Builds on:** [[timing-curve-metrics]].
- **Used by:** [[timing-signal-evaluation]], [[carry-stock-bond-timing]].
