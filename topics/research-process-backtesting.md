---
id: research-process-backtesting
title: "Research Process & Backtesting"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook]
---
# Research Process & Backtesting

This chapter is about method rather than models: the sequence of steps a research project should follow, how to present it, and how to investigate a strategy whose backtest does not survive contact with live trading.

**Prerequisites:** [[cross-validation-leakage]], [[multiple-testing]], [[timing-signal-evaluation]].

**Leads to:** [[sharpe-ratio]] (why a high backtest Sharpe misleads), [[price-reconciliation]] (the same debugging discipline on the sell side).

**Sections:** [[research-workflow]] · [[backtest-pitfalls]]

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
