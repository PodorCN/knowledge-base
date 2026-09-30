---
id: production-coding
title: "Production & Coding"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep]
---
# Production & Coding

The final chapter covers running pricing code in production: integrating a new model-library release safely, reconciling prices that disagree between two systems, and a classic coding-interview algorithm.

**Prerequisites:** [[pricing-app-architecture]], [[put-call-parity]], [[greeks-conventions-bumping]].

**Leads to:** back to [[model-risk-governance]] (the controls these procedures implement).

**Sections:** [[model-release-regression-testing]] · [[price-reconciliation]] · [[floyd-cycle-detection]]

<a id="model-release-regression-testing"></a>

## Integrating Model-Library Releases (regression harness)
<!-- section: model-release-regression-testing | prerequisites: [pricing-app-architecture] | related: [price-reconciliation, model-risk-governance, put-call-parity, design-patterns-pricing] | sources: [src-rbc-quantdev-prep] | tags: [release, regression-test, versioning] -->

A new quant-library release must be proven not to change prices unexpectedly before traders use it. The procedure is a regression harness: price a fixed book on frozen market data with the old and new versions and explain every difference.

### Procedure
1. Read the release notes; classify each change (new model, parameter change, bug fix, API change).
2. **Regression harness:** a frozen market-data snapshot + representative trades (vanillas, each exotic family, edge cases: near-barrier, short-dated, zero-vol).
3. Run old vs new; report price and Greek differences with **per-product tolerances**.
4. Every difference above tolerance is explained by the release notes or escalated to the quants.
5. Update adapters/UI for new models and parameters ([[design-patterns-pricing]]).
6. UAT → trader sign-off on known trades → release with a rollback ready.
7. Keep the **model version visible** in the app and in saved pricings (audit, [[model-risk-governance]]).

### Key points
- **Invariant checks:** [[put-call-parity]] on European vanillas — a break is a bug.

### Connections
- **Builds on:** [[pricing-app-architecture]]. **Related:** [[price-reconciliation]].

<a id="price-reconciliation"></a>

## Price Reconciliation ("app ≠ risk system")
<!-- section: price-reconciliation | prerequisites: [pricing-app-architecture] | related: [greeks-conventions-bumping, model-release-regression-testing, forward-pricing, backtest-pitfalls] | sources: [src-rbc-quantdev-prep] | tags: [debugging, reconciliation] -->

When two systems price the same trade differently, isolate the cause before touching model code: diff the inputs **field by field**.

### Checklist
1. Same trade terms?
2. Same market-data snapshot (time, dividends, borrow, surface)?
3. Same model and model version?
4. Same conventions (day count, settlement lag, vol by strike vs moneyness, Greek units — [[greeks-conventions-bumping]])?
5. Same numerical settings (paths, grid)?

### Key points
- **Most breaks are data or conventions, not maths** (forward/dividend issues top the list, [[forward-pricing]]).

### Connections
- **Builds on:** [[pricing-app-architecture]].
- **Same mindset as:** [[backtest-pitfalls]] (check the implementation before theorising).

<a id="floyd-cycle-detection"></a>

## Floyd's Cycle Detection (tortoise & hare)
<!-- section: floyd-cycle-detection | prerequisites: [] | related: [] | sources: [src-rbc-quantdev-prep] | tags: [algorithms, linked-list] -->

Detect whether a linked list contains a cycle using two pointers moving at different speeds.

### Key points
- Slow pointer +1, fast pointer +2 per step; if they meet → there is a cycle.
- **O(n) time, O(1) space.**
- Cycle start: reset one pointer to the head, move both +1 until they meet.
- (Glassdoor-reported RBC quant-dev question, alongside "explain basic OO concepts".)
