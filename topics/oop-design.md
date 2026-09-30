---
id: oop-design
title: "OOP & Design"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep, src-rbc-gam-quantdev-notes]
---
# OOP & Design

A pricing application has to absorb new products, new models and monthly library releases without being rewritten. This chapter covers the object-oriented principles and design patterns that make that possible, illustrated on a pricing app, and the resulting architecture: separate the instrument, the market data and the model. It then covers running that code in production (integrating a new model-library release safely, reconciling prices that disagree between two systems) and a classic coding-interview algorithm.

**Prerequisites:** none in code; the finance examples use [[option-payoffs-moneyness]], [[forward-pricing]] and [[volatility-surface]]; the release and reconciliation sections use [[put-call-parity]] and [[greeks-conventions-bumping]].

**Leads to:** [[csharp-dotnet]] (the language); back to [[model-risk-governance]] (the controls the release and reconciliation procedures implement).

**Sections:** [[oop-pillars]] · [[solid-principles]] · [[design-patterns-pricing]] · [[pricing-app-architecture]] · [[model-release-regression-testing]] · [[price-reconciliation]] · [[floyd-cycle-detection]]

<a id="oop-pillars"></a>

## OOP Pillars (with a pricing example)
<!-- section: oop-pillars | prerequisites: [] | related: [solid-principles, design-patterns-pricing, pricing-app-architecture, csharp-essentials] | sources: [src-rbc-quantdev-prep] | tags: [oop, encapsulation, polymorphism] -->

The four pillars of object-oriented design, each with its role in a pricing library.

### Definitions

| Pillar | Meaning | Pricing example |
|---|---|---|
| Encapsulation | hide state, expose behaviour | `VolSurface` hides its grid, exposes `GetVol(K, T)` |
| Abstraction | model the essential interface | `IPricingModel.Price(instrument, market)` |
| Inheritance | reuse via "is-a" | `EuropeanCall : VanillaOption : Instrument` |
| Polymorphism | same call, different behaviour | `model.Price(trade)` runs BS, MC or PDE |

### Key points
- **Composition over inheritance:** a barrier option isn't "a vanilla with a flag" — compose `Option { Payoff, ExerciseSchedule, Barrier? }` to avoid fragile deep hierarchies as exotic variations multiply.

### Connections
- **Used by:** [[solid-principles]], [[design-patterns-pricing]], [[csharp-abstract-classes]].

<a id="solid-principles"></a>

## SOLID (desk-app examples)
<!-- section: solid-principles | prerequisites: [oop-pillars] | related: [design-patterns-pricing, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [solid, design] -->

Five design rules that keep a codebase open to extension, each shown on a desk application.

### Definitions
- **S**ingle responsibility: the pricer doesn't also format the UI.
- **O**pen/closed: add a model by adding a class implementing `IPricingModel`, not by editing a switch.
- **L**iskov substitution: every `IPricingModel` honours the contract (e.g. Greeks in the same units, [[greeks-conventions-bumping]]).
- **I**nterface segregation: `IGreeksProvider` separate from `IPricer`, so simple models don't fake Greeks.
- **D**ependency inversion: ViewModels depend on an injected `IPricingService` → mockable in tests.

### Connections
- **Builds on:** [[oop-pillars]]. **Applied in:** [[pricing-app-architecture]].

<a id="design-patterns-pricing"></a>

## Design Patterns in a Pricing App
<!-- section: design-patterns-pricing | prerequisites: [oop-pillars] | related: [solid-principles, pricing-app-architecture, model-release-regression-testing] | sources: [src-rbc-quantdev-prep] | tags: [patterns, strategy, adapter, observer] -->

Standard design patterns and where each appears in a pricing application.

### Definitions

| Pattern | Use |
|---|---|
| Strategy | swap the pricing model / numerical method |
| Factory / Registry | create the right model per product + library version |
| **Adapter** | wrap the quant library's API behind your own interface → isolates monthly changes |
| Observer | market-data tick → reprice → UI refresh (events, `IObservable`, `INotifyPropertyChanged`) |
| Decorator | caching, logging, timing around a pricer |
| Builder | construct structured-product term sheets |
| Command | undo/redo, scenario actions, bumps |
| Visitor | price / risk / cash-flow report over an instrument tree |

### Connections
- **Builds on:** [[oop-pillars]].
- **Adapter is key for:** [[model-release-regression-testing]]. **Strategy in code:** swappable engines in [[csharp-pricing-library-example]].

<a id="pricing-app-architecture"></a>

## Pricing App Architecture (instrument / market data / model)
<!-- section: pricing-app-architecture | prerequisites: [oop-pillars, solid-principles] | related: [csharp-essentials, design-patterns-pricing, forward-pricing, volatility-surface, scenario-risk-grids, model-risk-governance] | sources: [src-rbc-quantdev-prep] | tags: [architecture, market-data, immutability] -->

**Separate what (the instrument, immutable) / with what (a market-data snapshot) / how (the model)** → models from the monthly library release can be swapped without touching instruments or the UI.

### Core interfaces
```csharp
public interface IMarketData { double Spot(string ul); double Discount(DateTime t); double Vol(string ul, double k, DateTime t); }
public interface IPricingModel { bool Supports(Instrument i); PricingResult Price(Instrument i, IMarketData md, PricingSettings s); }
public record PricingResult(double Pv, IReadOnlyDictionary<string,double> Greeks, double? StdError);
```

### Market data an equity option needs
Spot; a discount curve per currency; the dividend schedule (cash + yield, ex-dates); the borrow/repo curve; the implied vol surface (strike/delta × expiry); for quantos, FX vol + correlation ([[quanto-options]]); for baskets, a correlation matrix; calendars and settlement conventions. See [[forward-pricing]] and [[volatility-surface]] for why each input matters.

### Product-thinking features (structured-products desk)
Term-sheet templates (autocallable, reverse convertible, PPN); **solve-for** coupon/barrier/participation; scenario and Greek ladders ([[scenario-risk-grids]]); correlation and dividend sensitivity; lifecycle events (fixings, autocall triggers, knock-ins); a pricing audit trail ([[model-risk-governance]]).

### Connections
- **Builds on:** [[oop-pillars]], [[solid-principles]].
- **Inputs explained in:** [[forward-pricing]], [[volatility-surface]]. **Language details:** [[csharp-essentials]].

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
<!-- section: floyd-cycle-detection | prerequisites: [] | related: [] | sources: [src-rbc-quantdev-prep, src-rbc-gam-quantdev-notes] | tags: [algorithms, linked-list] -->

Detect whether a linked list contains a cycle using two pointers moving at different speeds.

### Key points
- Slow pointer +1, fast pointer +2 per step; if they meet → there is a cycle.
- **O(n) time, O(1) space.**
- Cycle start: reset one pointer to the head, move both +1 until they meet.
- (Glassdoor-reported RBC quant-dev question, alongside "explain basic OO concepts".)

### Code (Python)
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True
    return False
```
