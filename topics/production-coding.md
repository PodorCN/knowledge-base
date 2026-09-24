---
id: production-coding
title: "Production & Coding"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep]
---
# Production & Coding

**Sections:** [[model-release-regression-testing]] · [[price-reconciliation]] · [[floyd-cycle-detection]]

<a id="model-release-regression-testing"></a>

## Integrating Model-Library Releases (regression harness)
<!-- section: model-release-regression-testing | prerequisites: [pricing-app-architecture] | related: [price-reconciliation, model-risk-governance, put-call-parity, design-patterns-pricing] | sources: [src-rbc-quantdev-prep] | tags: [release, regression-test, versioning] -->

1. Read release notes; classify (new model, parameter change, bug fix, API change).
2. **Regression harness:** frozen market-data snapshot + representative trades (vanillas, each exotic family, edge cases: near-barrier, short-dated, zero-vol).
3. Run old vs new; report price & Greek diffs with **per-product tolerances**.
4. Every diff above tolerance is explained by release notes or escalated to quants.
5. Update adapters/UI for new models/params.
6. UAT → trader sign-off on known trades → release with rollback ready.
7. Keep **model version visible** in the app and saved pricings (audit).

**Invariant checks:** [[put-call-parity]] on European vanillas — a break is a bug.

<a id="price-reconciliation"></a>

## Price Reconciliation ("app ≠ risk system")
<!-- section: price-reconciliation | prerequisites: [pricing-app-architecture] | related: [greeks-conventions-bumping, model-release-regression-testing, forward-pricing, backtest-pitfalls] | sources: [src-rbc-quantdev-prep] | tags: [debugging, reconciliation] -->

Isolate before touching model code — diff inputs **field by field**:

1. Same trade terms?
2. Same market-data snapshot (time, dividends, borrow, surface)?
3. Same model and model version?
4. Same conventions (day count, settlement lag, vol by strike vs moneyness, Greek units)?
5. Same numerical settings (paths, grid)?

**Most breaks are data or conventions, not maths** (forward/dividend issues top the list).

### Connections
- **Same mindset as:** [[backtest-pitfalls]] (check implementation before theorising).

<a id="floyd-cycle-detection"></a>

## Floyd's Cycle Detection (tortoise & hare)
<!-- section: floyd-cycle-detection | prerequisites: [] | related: [] | sources: [src-rbc-quantdev-prep] | tags: [algorithms, linked-list] -->

- Slow pointer +1, fast +2; if they meet → cycle.
- **O(n) time, O(1) space.**
- Cycle start: reset one pointer to head, move both +1 until they meet.
- (Glassdoor-reported RBC quant-dev question alongside "explain basic OO concepts".)
