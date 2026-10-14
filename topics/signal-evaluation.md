---
id: signal-evaluation
title: "Signal Evaluation"
type: topic
domain: signal-research
sources: [src-signal-to-weight, src-squarepoint-dqa-workbook, src-quant-finance-study-notes, src-carry-course-notes]
---
# Signal Evaluation

Evaluate a signal in three steps: check what it predicts, test whether a fixed trading rule earns money after costs, and assess its contribution to the portfolio. Start with the simulated curves below, then follow the matching scatter, bucket, drawdown and cost plots through the chapter. Here $i$ indexes assets, $t$ denotes a decision date, $h$ is a forecast horizon in trading days and $\Delta$ is the sampling interval in trading days; returns are simple decimals.

**Prerequisites:** [[information-coefficient]], [[cross-validation-leakage]], [[timing-curve-metrics]], [[turnover-cost-drag]].

**Leads to:** [[signal-to-weight]], [[carry-stock-bond-timing]], [[marginal-sharpe-improvement]].

**Sections:** [[timing-signal-evaluation]] · [[broker-research-replication]] · [[eval-three-stage-protocol]] · [[eval-directional-prediction]] · [[eval-statistical-significance]] · [[eval-directional-hit-rate]] · [[eval-sizing-monotonicity]] · [[eval-tradable-profitability]] · [[eval-turnover-costs]] · [[eval-temporal-stability]] · [[eval-correlation-redundancy]] · [[research-workflow]] · [[backtest-pitfalls]]


![Three net equity curves on the same simulated market: predictive at 5 bps, noise at 5 bps, and the same predictive signal at 50 bps.](../assets/figures/signal-evaluation/equity-curves.svg)

**Read the curves:** blue turns 1 into **2.37**; grey noise ends at **0.80**. Orange uses exactly the same predictive score as blue but pays higher costs and ends at **0.63**. Prediction and profitable implementation are separate questions.

<details>
<summary>Simulation setup, assumptions and reproducibility</summary>

**Illustrative simulation (自己推理):** 520 weekly decisions, fixed seed 20261014. These are synthetic outcomes, not market evidence. Each score is available before the next return is realised. Scores and rules are fixed in advance; no model is fitted or selected from these outcomes. All plots below use this same sample.

$$R_{t\to t+1}=0.025\left(0.18s_t+\sqrt{1-0.18^2}\,\varepsilon_{t+1}\right),\qquad w_t^{g}=\mathrm{clip}(s_t/2,-1,1),\qquad w_t^{n}=\mathrm{clip}(u_t/2,-1,1)$$

**Variables:**

- $t$ weekly decision index in this simulation, rather than a trading-day index
- $R_{t\to t+1}$ next-week simple return of the simulated spread
- $s_t$ predictive score known at the decision time, drawn from a standard normal distribution
- $u_t$ standard normal noise score known at the decision time, independent of the predictive scores and returns
- $\varepsilon_{t+1}$ new standard normal shock realised after the decision; all scores and shocks are independent across weeks
- $w_t^{g}$ predictive strategy's spread exposure during the next week
- $w_t^{n}$ noise strategy's spread exposure during the next week
- $\mathrm{clip}$ operator imposing the lower and upper exposure limits

**Notes:** the loading 0.18 creates a modest positive population correlation in this illustrative model; 0.025 is the weekly target-return standard deviation. Both score series have unit variance. The realised Rank ICs are +0.166 and −0.007. These values are outcomes of the simulation, not acceptance thresholds.

$$\Pi_{t+1}^{\mathrm{net}}=w_tR_{t\to t+1}-c|w_t-w_{t-1}|$$

**Variables:**

- $\Pi_{t+1}^{\mathrm{net}}$ net strategy return for the weekly holding interval
- $w_t$ chosen strategy's exposure at decision $t$
- $w_{t-1}$ previous target exposure, with zero exposure before the first trade
- $t$ weekly decision index
- $R_{t\to t+1}$ realised spread return over the following week
- $c$ all-in cost per unit of absolute spread exposure traded: 0.0005 for 5 bps or 0.005 for 50 bps

**Limitations:** this is a diagnostic spread sleeve. It charges the initial entry and each target-weight change, without separate final liquidation, financing, borrow, market impact or price-driven weight drift. One simulated path is not a guarantee: noise can temporarily profit and a useful signal can temporarily lose. Regenerate with `python scripts/generate_signal_figures.py` (NumPy and Matplotlib).

</details>

<a id="timing-signal-evaluation"></a>

## Specify the Experiment Before Reading Results
<!-- section: timing-signal-evaluation | prerequisites: [information-coefficient, cross-validation-leakage, signal-position-construction, timing-curve-metrics] | related: [eval-three-stage-protocol, eval-directional-prediction, research-workflow, stock-bond-carry-case-study] | sources: [src-carry-course-notes, src-squarepoint-dqa-workbook] | tags: [checklist, signal-testing, diagnostics] -->

Begin with a testable claim: which return should the signal predict, using which information, and through which trading rule? Fixing these choices before inspecting results makes the backtest an experiment rather than a search for an attractive curve.

### Definition

Record the economic hypothesis, universe, signal orientation, return target, information availability, forecast horizon, rebalance frequency, execution assumptions, benchmark, costs, sample partitions and pass/stop rules. A positive score must have an explicit meaning: higher expected asset return, greater relative attractiveness, or a tilt toward one leg of a spread.

### Key points

**Reading order:** audit data → isolate samples → measure prediction → simulate trades and costs → check stability and portfolio value.

<details>
<summary>Detailed checklist and interpretation</summary>

| Stage | Evidence | Question answered |
|---|---|---|
| Data audit | Formula, universe history, publication dates, price adjustments | Could the signal have been computed and traded then? |
| Sample isolation | Chronological splits and complete forward windows | Which data may influence design, and which evaluate it? |
| Prediction | IC, uncertainty, hit rate, quantile returns | Does the score contain information about its stated target? |
| Trading | Fixed sizing, return curve, drawdown, costs | Does that information survive conversion into positions? |
| Robustness | Subperiods, rolling diagnostics, out-of-sample results | How concentrated and reproducible is the evidence? |
| Portfolio contribution | Existing exposures and incremental performance | Is the candidate useful alongside existing holdings? |
| Decision | Evidence, limitations, rejected alternatives | Proceed, stop, or register a new experiment? |

**Reading it:** ranking assets correctly, earning net trading profits and improving an existing portfolio are distinct claims. No single IC, hit rate, Sharpe ratio or correlation cutoff establishes all three.

<details>
<summary>Predictive ordering, directional accuracy and profit</summary>

A signal can rank two assets correctly while both lose money. A directional rule can be right often but lose more on its few mistakes than it gains on its successes. A profitable standalone strategy can repeat exposures already held in the portfolio. The separate diagnostics distinguish these possibilities.

</details>

**Notes:** the carry experiment used weekly observations, 21-trading-day forward returns, and a selection hurdle of positive IC with an approximate IC statistic of at least 1.5. These are recorded experiment choices, not universal standards.

</details>

### Connections

- **Builds on:** [[information-coefficient]], [[cross-validation-leakage]], [[signal-position-construction]].
- **Used by:** [[eval-three-stage-protocol]], [[research-workflow]], [[carry-measurement-protocol]].

<a id="broker-research-replication"></a>

## Audit the Data and Reproduce the Signal
<!-- section: broker-research-replication | prerequisites: [timing-signal-evaluation, cross-validation-leakage] | related: [eval-three-stage-protocol, backtest-pitfalls, carry-measurement-protocol] | sources: [src-carry-course-notes, src-squarepoint-dqa-workbook] | tags: [broker-research, replication, point-in-time] -->

Before testing predictive power, establish that the historical signal matches its definition and uses information available at the decision time. Replicating published research requires reproducing its calculations and auditing its trading assumptions.

### Definition

Point-in-time data are indexed by when an input became available, not merely by the economic period it describes. The trade follows the decision and the assumed execution opportunity; a price observed after the close cannot support an earlier fill at that close.

### Key points

- Use only data available at the decision time.
- Match formulas, units, universe history and executable prices before testing performance.

<details>
<summary>Detailed checklist and interpretation</summary>

| Audit | Why it matters | Naive version to reject |
|---|---|---|
| Formula and units | Inputs must measure the intended quantity | Mixing percentages and decimals or incompatible horizons |
| Price adjustments | Total-return prices and valuation denominators serve different purposes | Dividing cash dividends by retrospectively dividend-adjusted prices |
| Publication and revisions | A period date is not an availability date | Using revised macro history as if it were known then |
| Calendar alignment | Values may flow forward after availability | Interpolating toward a future month-end observation |
| Universe history | The tradable universe changes | Testing only today's surviving constituents |
| Normalisation | Calibration must use available history | Full-sample means, standard deviations or transformations |
| Execution | Delay, spread, fees, borrow and financing affect feasibility | Immediate fills without friction or capacity limits |

**Replication checks:** align dates, units, missing values and formula versions, then compare raw values and correlations. The notes' correlation benchmark of 0.60 is a screening heuristic, not proof of correct replication: even perfect correlation can coexist with an incorrect scale or offset.

</details>

### Worked example

The carry notes report that a dividend-adjusted denominator overstated the 2006 SPY dividend yield as 2.48% rather than 1.73%. That is a discrepancy of 0.75 percentage points, about 43.4% of the stated correct yield. An input error changes the signal before any predictive test.

**Notes:** the original one-business-day lag for BAA10Y and seven-day lag for ICSA are assumptions to verify against actual availability records. Date labels alone do not establish release timing. Applying an annual valuation measure to weekly timing also requires an explicit economic rationale.

### Connections

- **Builds on:** [[timing-signal-evaluation]], [[cross-validation-leakage]].
- **Used by:** [[eval-three-stage-protocol]], [[backtest-pitfalls]].
- **Related:** [[carry-measurement-protocol]].

<a id="eval-three-stage-protocol"></a>

## Isolate Selection, Validation and Test Samples
<!-- section: eval-three-stage-protocol | prerequisites: [timing-signal-evaluation, cross-validation-leakage] | related: [eval-statistical-significance, research-workflow, stock-bond-carry-case-study] | sources: [src-carry-course-notes] | tags: [select-validate-test, protocol, purging] -->

Partition history before inspecting performance. Separate the evidence used to design a signal from the evidence used to evaluate the frozen design.

### Definition

| Sample | Permitted use | Carry experiment dates |
|---|---|---|
| Select | Develop and screen; record all variants tried | Inception through 2017-12-31 |
| Validate | Check persistence under the frozen protocol | 2018-01-01 through 2023-09-27 |
| Test | Evaluate a design fixed without this sample | From 2023-09-28 to the experiment's stated data cutoff |

### Key points

- **Purge boundary crossings:** this protocol retains a label only when its entire forward window lies inside the partition. A crossing 21-day label is excluded. The purpose is to prevent earlier selection from using later outcomes ([[cross-validation-leakage]]).
- **Distinguish protocols:** ordinary model validation may select hyperparameters before a final test. This carry protocol used validation as a one-time check of a frozen candidate. If its results influence redesign, it becomes development evidence and a new untouched evaluation is needed.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- **Preserve available history:** past inputs may construct a later signal if they would have been available live. Later forward returns must not influence earlier calibration.
- **Record repeated trials:** changing sign, horizon, data source, clipping or sizing after seeing results is another experiment. Sealing a final sample does not eliminate selection bias within development.
- **Separate testing and monitoring:** a final historical test is evaluated once. Live monitoring continues, but observed live data cease to be untouched evidence for subsequent redesigns.

</details>

### Worked example

Carry selection had 574 weeks, Rank IC +0.0423 and approximate overlap-adjusted statistic +0.49. It failed the registered 1.5 hurdle. Gross annualised return +2.3% and hit rate 60% did not override that decision.

The later disclosed demonstration had 295 validation weeks: IC +0.1220, approximate statistic +1.02, hit rate 55% and gross annualised return +1.5%. This does not mean the failed candidate passed the original protocol. The complete case belongs in [[stock-bond-carry-case-study]].

### Connections

- **Builds on:** [[timing-signal-evaluation]], [[cross-validation-leakage]].
- **Used by:** [[eval-statistical-significance]], [[research-workflow]], [[carry-measurement-protocol]].
- **Related:** [[stock-bond-carry-case-study]].

<a id="eval-directional-prediction"></a>

## Test Predictive Ordering at the Intended Horizon
<!-- section: eval-directional-prediction | prerequisites: [information-coefficient, eval-three-stage-protocol] | related: [eval-statistical-significance, eval-directional-hit-rate, eval-sizing-monotonicity] | sources: [src-carry-course-notes, src-quant-finance-study-notes] | tags: [rank-ic, prediction, evaluation] -->

IC tests whether higher scores correspond to higher subsequent returns. Choose the comparison axis first: assets on a given date for selection, or historical dates for timing an asset or spread.

### Definition

Use [[information-coefficient]] for Pearson and Rank IC formulas. Cross-sectional IC gives one coefficient per date by comparing assets; time-series IC compares dated score/forward-return pairs across the sample. State the target, horizon, ranking direction, ties and missing-value treatment.

### Key points

- Positive IC supports the registered orientation, subject to uncertainty. Negative IC may indicate an inverted relationship or noise; reversing the sign after inspection is a new design choice.
- Near-zero IC provides little evidence for the measured association. It does not rule out every nonlinear or conditional relationship.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Pearson measures linear association in levels; Rank IC measures association in ordering. Rank IC is neither a directional success percentage nor a profit measure.
- A large IC motivates an audit but does not establish leakage. The earlier 0.04–0.08 range and 0.10 warning level are contextual heuristics, not universal pass/fail rules.
- A 21-day IC evaluates a 21-day target. It does not establish that a weekly position earns money; that requires [[eval-tradable-profitability]].

</details>

### Worked example

![A predictive score has a positive fitted relationship; a noise score has almost none. Both scatter plots remain noisy.](../assets/figures/signal-evaluation/predictive-scatter.svg)

**Read the plot:** blue slopes upward: higher scores tend to precede higher returns. Grey is nearly flat. The large scatter explains why even a useful score is wrong on many individual weeks.

### Connections

- **Builds on:** [[information-coefficient]], [[eval-three-stage-protocol]].
- **Used by:** [[eval-statistical-significance]], [[eval-directional-hit-rate]], [[eval-sizing-monotonicity]].

<a id="eval-statistical-significance"></a>

## Measure Uncertainty and Account for Repeated Trials
<!-- section: eval-statistical-significance | prerequisites: [ic-significance, effective-sample-size, multiple-testing, eval-directional-prediction] | related: [eval-three-stage-protocol, eval-temporal-stability] | sources: [src-carry-course-notes] | tags: [t-stat, overlap, sample-size] -->

After estimating association, ask how precisely it is estimated and how much searching preceded it. A small positive estimate with wide uncertainty is weaker evidence than the same effect supported by an appropriate independent evaluation.

### Definition

Report the estimate, sample length, horizon, sampling interval, dependence treatment, test direction and candidate family. The approximate statistic in [[ic-significance]] is a screening calculation; replacing sample size with an overlap approximation does not give an exact test for dependent Rank IC observations.

### Key points

- **Overlap:** weekly 21-day returns share approximately 16 days. Carry used overlap ratio 4.2 and effective sample size near 137 rather than 574. This is a simplifying approximation, not a count of independent economic cycles.
- **Additional dependence:** persistent signals, clustered shocks and changing volatility may defeat a correction based only on window length. Use suitable dependence-aware resampling or, for a specified predictive regression, HAC inference ([[robust-standard-errors]]).

<details>
<summary>Assumptions, edge cases and further checks</summary>

- **Cross-sectional dependence:** 500 stocks over 52 weeks produce 26,000 rows, not necessarily independent observations. Shared factors and repeated asset observations matter.
- **Low power:** fewer observations make small effects hard to detect. Lowering a hurdle changes the error tradeoff; it does not restore missing information.
- **Repeated testing:** a statistic near 3 is a literature benchmark under particular setups, not protection against every search. Define a correction for the actual family ([[multiple-testing]]).
- **Failure:** not rejecting zero means insufficient evidence under the method. It does not prove no effect exists or that every realised profit was luck.

**Reading it:** a statistic of 1.5 has a one-sided normal tail probability about 0.067 and two-sided about 0.134. It is not a conventional two-sided 5% result. These approximations require valid inference; carry used 1.5 as a registered screening choice.

</details>

### Connections

- **Builds on:** [[ic-significance]], [[effective-sample-size]], [[multiple-testing]], [[eval-directional-prediction]].
- **Used by:** [[eval-temporal-stability]], [[research-workflow]].
- **Related:** [[robust-standard-errors]].

<a id="eval-directional-hit-rate"></a>

## Check Directional Accuracy Without Confusing It with Profit
<!-- section: eval-directional-hit-rate | prerequisites: [hit-rate, eval-directional-prediction] | related: [eval-tradable-profitability, win-rate-expectancy] | sources: [src-carry-course-notes] | tags: [hit-rate, win-rate] -->

Hit rate checks whether the signal sign agrees with the subsequent return sign. It is meaningful only when zero is a defined directional boundary for both score and target.

### Definition

Use [[hit-rate]] for the formula. State how zero signals, zero returns and abstentions enter the denominator. A cross-sectional score can rank assets usefully without predicting each asset's absolute return sign.

### Key points

- Compare with a relevant baseline. Fifty percent applies to symmetric guessing, not automatically to a target with positive drift or imbalanced signs.
- The original 52–55% screening range and 65% warning level require context; neither proves tradability or overfitting.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Directional hit rate and trade win rate can differ because of overlapping positions, exits and costs.
- Inspect gain and loss magnitudes ([[win-rate-expectancy]]).

</details>

### Worked example

The notes describe correct predictions on 58% of dates with +0.2% outcomes and incorrect predictions on 42% with −3.0% outcomes. At equal exposure and without costs, the mean signed outcome is $0.58\times0.2\%-0.42\times3.0\%=-1.144\%$. High accuracy does not establish profitability.

### Connections

- **Builds on:** [[hit-rate]], [[eval-directional-prediction]].
- **Used by:** [[eval-tradable-profitability]].
- **Related:** [[win-rate-expectancy]].

<a id="eval-sizing-monotonicity"></a>

## Inspect Score Strength and Conditional Returns
<!-- section: eval-sizing-monotonicity | prerequisites: [eval-directional-prediction] | related: [eval-tradable-profitability, stock-bond-carry-case-study] | sources: [src-carry-course-notes] | tags: [quantile-sort, monotonicity, bucket-returns] -->

A quantile sort shows whether stronger scores correspond to higher average forward returns. It diagnoses a proposed sizing rule but does not establish an optimal rule by itself.

### Formula

$$\bar R_q=\frac{1}{|B_q|}\sum_{t\in B_q}R_{t\to t+h},\qquad q=1,\ldots,Q$$

**Variables:**

- $\bar R_q$ mean forward simple return in bucket $q$, in decimals
- $q$ bucket index, ordered from lowest to highest score
- $Q$ number of buckets; five in the carry experiment
- $B_q$ set of evaluation dates assigned to bucket $q$
- $|B_q|$ number of dates in that bucket
- $t$ evaluation date
- $h$ forecast horizon in trading days
- $R_{t\to t+h}$ realised target return over that horizon

### Key points

- Timing buckets historical dates; cross-sectional selection sorts assets within each date before aggregating.
- Report bucket counts and uncertainty. Overlapping labels reduce the information behind apparent differences.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Increasing means support monotonicity, not constant slope or optimal linear sizing. Risk and costs also determine weights.
- Full-sample buckets may describe a sample. If their boundaries determine trades, estimate them from information available at the decision time.
- A hump warrants investigation. A nonlinear rule invented after inspecting it needs a fresh evaluation.

</details>

### Worked example

![Mean next-week returns by score quintile for the predictive and noise scores, with approximate confidence intervals.](../assets/figures/signal-evaluation/quantile-returns.svg)

**Read the bars:** blue rises from low-score Q1 to high-score Q5; grey has no consistent ordering. Thin lines are approximate 95% intervals for group means in this independent-week simulation. They show uncertainty, not guaranteed future ranges.

<details>
<summary>Carry results and alternative rule</summary>

Carry selection quintiles were −0.10%, +0.41%, +0.95%, +0.72%, −0.09%. Q5 underperformed Q3, challenging the proposed monotonic relationship. Validation quintiles were +0.60%, +0.15%, +1.14%, +0.99%, +1.17%; neither sample forms an exact staircase.

The hindsight-inspired alternative was $z_{\mathrm{hump}}=-|z|$: buy equities near normal carry and bonds at extremes. **(自己推理)**: this was the original alternative interpretation. Its validation IC +0.007 and approximate statistic +0.06 did not support the alternative. They do not prove that the original hump was purely noise.

</details>

### Connections

- **Builds on:** [[eval-directional-prediction]].
- **Used by:** [[eval-tradable-profitability]].
- **Related:** [[stock-bond-carry-case-study]].

<a id="eval-tradable-profitability"></a>

## Simulate Positions, Returns and Drawdowns
<!-- section: eval-tradable-profitability | prerequisites: [timing-curve-metrics, signal-position-construction, eval-sizing-monotonicity] | related: [eval-turnover-costs, eval-temporal-stability, sharpe-ratio] | sources: [src-carry-course-notes] | tags: [timing-curve, drawdown, equity-curve] -->

The trading backtest evaluates a fixed, executable score-to-position rule. Simulate actual holding intervals instead of compounding overlapping forecast labels as if they were sequential profits.

### Definition

Use [[signal-position-construction]] for sizing and [[timing-curve-metrics]] for compounding and drawdown. Carry predicts 21 trading days ahead but holds each diagnostic position for one weekly rebalance interval. Each realised weekly return enters the curve once.

### Key points

- Specify signal availability, order time, fill time and the return earned after execution.
- Define the weight: a unit stock-minus-bond spread has two legs and differs from a fully invested stock/bond allocator in exposure and costs.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Label a spread curve as a diagnostic sleeve unless baseline holdings, cash and financing are included in the complete portfolio simulation.
- Compare gross and net return, annualised geometric return, [[sharpe-ratio]], drawdown and recovery duration with the intended benchmark at comparable risk.
- Drawdown in [[timing-curve-metrics]] is nonpositive. If reporting a positive loss magnitude, label that convention.
- A positive curve with years underwater may fail the mandate. Drawdown tolerances are mandate-specific rather than universal.

**Reading it:** IC is evidence about a score; simulated net return is evidence about one implementation. Neither substitutes for the other.

<details>
<summary>Forecast horizon versus rebalance interval</summary>

A weekly decision can use a forecast about the next 21 trading days. If the rule rebalances every week, simulate each week's realised return on the position actually held. The 21-day forward returns serve as prediction labels and overlap; multiplying them together would count shared market moves repeatedly. A rule that holds each new trade for the full 21 days instead needs an explicit simulation of its overlapping positions and capital allocation.

</details>

</details>

### Worked example

![Weekly peak-to-trough drawdowns for the three simulated implementations.](../assets/figures/signal-evaluation/drawdowns.svg)

**Read the drawdown:** zero means a new capital peak. Blue still falls about **15%** below its previous peak; grey reaches about **36%** and orange **50%**. A profitable long-run curve can still involve a difficult recovery.

### Connections

- **Builds on:** [[timing-curve-metrics]], [[signal-position-construction]], [[eval-sizing-monotonicity]].
- **Used by:** [[eval-turnover-costs]], [[eval-temporal-stability]].
- **Related:** [[sharpe-ratio]], [[signal-to-weight]].

<a id="eval-turnover-costs"></a>

## Deduct Frictions at Each Rebalance
<!-- section: eval-turnover-costs | prerequisites: [turnover-cost-drag, eval-tradable-profitability] | related: [eval-correlation-redundancy, portfolio-construction-process] | sources: [src-carry-course-notes] | tags: [turnover, transaction-costs, net-return] -->

Charge costs to the actual trades produced by the frozen rule. Persistence may influence turnover, but signal autocorrelation alone does not determine cost survival.

### Definition

[[turnover-cost-drag]] gives the simplified weekly convention. For a portfolio, measure changes from pretrade holdings to target holdings, charge each leg consistently and compound net period returns. Specify whether costs are per leg, one-way, round-trip or all-in for a spread.

### Key points

- Include applicable spread, slippage, commissions, borrow and financing. Impact and capacity depend on liquidity and trade size; 5 bps is illustrative.
- A scalar spread-weight change is not automatically the sum of traded asset notionals. Account for both legs and reversals.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Price changes can create rebalancing trades even with an unchanged signal.
- Annual drag based on average turnover is an approximation. Subtracting it from geometric gross return is not exact net CAGR.
- Recompute under plausible, documented costs. If net return becomes negative, the tested implementation fails under those assumptions.

</details>

### Worked example

![Identical predictive strategy: gross mean return less annualised trading costs at zero, five and fifty basis points.](../assets/figures/signal-evaluation/cost-drag.svg)

**Read the cost bars:** the score and positions stay unchanged. Annualised arithmetic gross mean return is **10.4%**; trading drag is about **1.5%** at 5 bps and **14.6%** at 50 bps. Black dots mark net mean return. These arithmetic means differ from the geometric returns of the compounded curves.

<details>
<summary>Turnover calculation with small numbers</summary>

At a one-way all-in cost of 5 bps per unit of the stated turnover convention, weekly turnover 0.08 gives annual arithmetic drag $0.0005\times0.08\times52=0.208\%$. Turnover 0.60 gives 1.56%; subtracting from 2.0% gross return gives approximately 0.44%, before other frictions and compounding effects.

**Notes:** the original examples pair these turnover levels with autocorrelations 0.95 and 0.30. These are illustrative pairings, not a mapping from autocorrelation to turnover. Carry's selection/validation autocorrelations were 0.95/0.94.

</details>

### Connections

- **Builds on:** [[turnover-cost-drag]], [[eval-tradable-profitability]].
- **Used by:** [[eval-correlation-redundancy]].
- **Related:** [[portfolio-construction-process]].

<a id="eval-temporal-stability"></a>

## Check Stability Across Time and Conditions
<!-- section: eval-temporal-stability | prerequisites: [icir-stability, eval-statistical-significance, eval-tradable-profitability] | related: [eval-three-stage-protocol, eval-correlation-redundancy] | sources: [src-carry-course-notes] | tags: [rolling-ic, yearly-ic, regime-stability] -->

Compare predictive and trading evidence across subperiods to understand where the effect occurs. Stability does not require every noisy yearly IC estimate to be positive.

### Definition

Inspect rolling and yearly IC alongside net return, drawdown, turnover and exposure. [[icir-stability]] defines ICIR for a specified periodic IC series; it is not portfolio IR and does not guarantee smooth profits.

### Key points

- Carry used rolling 52-week IC and yearly IC with at least ten observations. Ten weeks is a display threshold, not reliable inference for overlapping 21-day labels.
- Rolling windows share data. Successive estimates are not independent confirmations; smoothness can arise from overlap.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Sign changes may reflect noise, changing economics or input problems. Investigate rather than declaring pure noise.
- Inspect profit concentration separately from IC concentration. Crisis performance may be meaningful, but its repeatability and mandate fit need explanation.
- The earlier 70%-positive-years criterion is a possible registered diagnostic, not a universal standard. Report counts, sample lengths and uncertainty.
- Define regimes before using them for model selection. Post-hoc subperiod analysis is exploratory.

</details>

### Connections

- **Builds on:** [[icir-stability]], [[eval-statistical-significance]], [[eval-tradable-profitability]].
- **Used by:** [[eval-correlation-redundancy]], [[research-workflow]].
- **Related:** [[eval-three-stage-protocol]].

<a id="eval-correlation-redundancy"></a>

## Assess Incremental Portfolio Value
<!-- section: eval-correlation-redundancy | prerequisites: [information-coefficient, eval-turnover-costs, eval-temporal-stability] | related: [marginal-sharpe-improvement, fundamental-law-active-management, research-workflow] | sources: [src-carry-course-notes, src-quant-finance-study-notes] | tags: [correlation, redundancy, diversification] -->

Ask whether adding the candidate improves the existing portfolio under its costs and constraints. Similarity is a diagnostic, not a complete decision rule.

### Definition

Distinguish score correlation, strategy-return correlation and common risk exposures. Similar scores can produce different returns through sizing or execution; low score correlation can conceal common factor exposure.

### Key points

- Compare aligned samples, net strategy returns and exposures. A score correlation above 0.60 flags similarity under the contextual screening heuristic, not zero incremental information; a lower value does not establish usefulness.
- Choosing the higher in-sample statistic among correlated signals adds selection bias. Evaluate the chosen design independently.

<details>
<summary>Assumptions, edge cases and further checks</summary>

- Recompute the combined portfolio at feasible allocations under its risk budget, turnover and capacity constraints.
- [[marginal-sharpe-improvement]] derives a local frictionless addition condition using return correlation and Sharpe ratios. It is not a condition on signal-score correlation.
- Square-root formulas for optimal Sharpe improvement require an optimally combined, uncorrelated incremental return component. An ordinary benchmark-relative IR cannot be substituted without establishing that decomposition.
- [[fundamental-law-active-management]] links skill, independent breadth and implementation. It explains possible sources of portfolio value, but does not certify this candidate's realised contribution.

</details>

### Connections

- **Builds on:** [[information-coefficient]], [[eval-turnover-costs]], [[eval-temporal-stability]].
- **Used by:** [[research-workflow]], [[signal-to-weight]].
- **Related:** [[marginal-sharpe-improvement]], [[fundamental-law-active-management]].

<a id="research-workflow"></a>

## Record the Decision and Research Trail
<!-- section: research-workflow | prerequisites: [eval-three-stage-protocol, eval-statistical-significance, eval-correlation-redundancy] | related: [backtest-pitfalls, multiple-testing] | sources: [src-squarepoint-dqa-workbook] | tags: [research, communication, workflow] -->

Conclude with a decision tied to the registered objective and evidence. Documenting a failed candidate preserves what was learned and prevents repeated searches from losing their history.

### Definition

Record the hypothesis, availability rules, baseline, implementation, partitions, variants, results, rejected alternatives, limitations and decision. Future modifications start from this record.

### Key points

- End with a recorded decision: proceed, stop, or register another experiment.
- Separate measured evidence from explanations that remain hypotheses.

<details>
<summary>Detailed checklist and interpretation</summary>

| Decision | Meaning | Next step |
|---|---|---|
| Proceed under the protocol | The stated criteria were met | Evaluate the frozen design on the next reserved sample or monitor an authorised deployment |
| Stop under the protocol | A required criterion failed | Record the failure without claiming the economic theory was disproved |
| Register another experiment | A specific measurement or design hypothesis merits testing | Document the change, accumulated trials and remaining independent data |

**Carry decision:** IC +0.0423 and approximate statistic +0.49 did not meet the selection criterion. This tested proxy failed the registered screen; it does not establish that carry cannot predict returns elsewhere.

**Communication:** the original project notes use 30 seconds for hypothesis and decision, two minutes for data, baseline, implementation, validation and limitations, and ten minutes for assumptions, diagnostics, rejected alternatives, costs and risks. At each depth distinguish measured results from untested explanations.

**Monitoring:** establish review/stop criteria before deployment. Compare actual signals, orders, fills and costs with the historical implementation. Record any redesign informed by those observations.

</details>

### Connections

- **Builds on:** [[eval-three-stage-protocol]], [[eval-statistical-significance]], [[eval-correlation-redundancy]].
- **Used by:** [[backtest-pitfalls]].
- **Related:** [[multiple-testing]], [[carry-case-diagnosis]].

<a id="backtest-pitfalls"></a>

## Diagnose Backtest and Live Performance Gaps
<!-- section: backtest-pitfalls | prerequisites: [research-workflow, multiple-testing] | related: [cross-validation-leakage, price-reconciliation, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [backtest, overfitting, survivorship, debugging] -->

Start by checking whether both systems implement the same decisions on the same information. Then assess execution, uncertainty, selection and market changes.

### Definition

Separate an implementation discrepancy from a disappointing realisation of a correctly implemented strategy. A short loss sequence can occur under positive expectation; the loss itself does not identify the cause.

### Key points

- First compare signals, orders and fills at identical timestamps.
- Then investigate costs, selection bias and market changes.

<details>
<summary>Detailed checklist and interpretation</summary>

| Investigation | Checks | Purpose |
|---|---|---|
| Implementation and data | Same timestamps; signals, orders, dividends, splits, duplicates, future-shifted features, universes, revisions | Establish that the comparison is valid |
| Execution and accounting | Assumed versus actual fills, costs, borrow, financing, volumes | Establish whether frictions consume the paper edge |
| Uncertainty and selection | Sample length, dependence, all variants tried, reused evaluation samples | Assess inflated performance expectations |
| Regime and capacity | Exposure changes, volatility, structure, crowding | Test market explanations after operational checks |

**Notes:** the original 5%-of-daily-volume check is a capacity diagnostic, not a universal safe limit. A backtest Sharpe of 4 motivates an audit, but proves neither an edge nor a bug. Record supported explanations separately from unresolved hypotheses.

</details>

### Connections

- **Builds on:** [[research-workflow]], [[multiple-testing]].
- **Related:** [[cross-validation-leakage]], [[price-reconciliation]], [[sharpe-ratio]].
