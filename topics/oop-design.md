---
id: oop-design
title: "OOP & Design"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep]
---
# OOP & Design

**Sections:** [[oop-pillars]] · [[solid-principles]] · [[design-patterns-pricing]] · [[pricing-app-architecture]]

<a id="oop-pillars"></a>

## OOP Pillars (with a pricing example)
<!-- section: oop-pillars | prerequisites: [] | related: [solid-principles, design-patterns-pricing, pricing-app-architecture, csharp-essentials] | sources: [src-rbc-quantdev-prep] | tags: [oop, encapsulation, polymorphism] -->

| Pillar | Meaning | Pricing example |
|---|---|---|
| Encapsulation | hide state, expose behaviour | `VolSurface` hides its grid, exposes `GetVol(K, T)` |
| Abstraction | model the essential interface | `IPricingModel.Price(instrument, market)` |
| Inheritance | reuse via "is-a" | `EuropeanCall : VanillaOption : Instrument` |
| Polymorphism | same call, different behaviour | `model.Price(trade)` runs BS, MC or PDE |

**Composition over inheritance:** a barrier option isn't "a vanilla with a flag" — compose `Option { Payoff, ExerciseSchedule, Barrier? }` to avoid fragile deep hierarchies as exotic variations multiply.

<a id="solid-principles"></a>

## SOLID (desk-app examples)
<!-- section: solid-principles | prerequisites: [oop-pillars] | related: [design-patterns-pricing, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [solid, design] -->

- **S**ingle responsibility: the pricer doesn't also format the UI.
- **O**pen/closed: add a model by adding a class implementing `IPricingModel`, not editing a switch.
- **L**iskov: every `IPricingModel` honours the contract (e.g. Greeks in the same units).
- **I**nterface segregation: `IGreeksProvider` separate from `IPricer` so simple models don't fake Greeks.
- **D**ependency inversion: ViewModels depend on an injected `IPricingService` → mockable in tests.

<a id="design-patterns-pricing"></a>

## Design Patterns in a Pricing App
<!-- section: design-patterns-pricing | prerequisites: [oop-pillars] | related: [solid-principles, pricing-app-architecture, model-release-regression-testing] | sources: [src-rbc-quantdev-prep] | tags: [patterns, strategy, adapter, observer] -->

| Pattern | Use |
|---|---|
| Strategy | swap pricing model / numerical method |
| Factory / Registry | create the right model per product + library version |
| **Adapter** | wrap the quant library's API behind your own interface → isolates monthly changes |
| Observer | market-data tick → reprice → UI refresh (events, `IObservable`, `INotifyPropertyChanged`) |
| Decorator | caching, logging, timing around a pricer |
| Builder | construct structured-product term sheets |
| Command | undo/redo, scenario actions, bumps |
| Visitor | price / risk / cash-flow report over an instrument tree |

### Connections
- **Adapter is key for:** [[model-release-regression-testing]].

<a id="pricing-app-architecture"></a>

## Pricing App Architecture (instrument / market data / model)
<!-- section: pricing-app-architecture | prerequisites: [oop-pillars] | related: [csharp-essentials, design-patterns-pricing, forward-pricing, volatility-surface, scenario-risk-grids] | sources: [src-rbc-quantdev-prep] | tags: [architecture, market-data, immutability] -->

**Separate what (instrument, immutable) / with what (market-data snapshot) / how (model)** → swap models from the monthly library release without touching instruments or UI.

```csharp
public interface IMarketData { double Spot(string ul); double Discount(DateTime t); double Vol(string ul, double k, DateTime t); }
public interface IPricingModel { bool Supports(Instrument i); PricingResult Price(Instrument i, IMarketData md, PricingSettings s); }
public record PricingResult(double Pv, IReadOnlyDictionary<string,double> Greeks, double? StdError);
```

### Market data an equity option needs
Spot; discount curve per currency; dividend schedule (cash + yield, ex-dates); borrow/repo curve; implied vol surface (strike/delta × expiry); quantos: FX vol + correlation; baskets: correlation matrix; calendars, settlement conventions.

### Product-thinking features (structured-products desk)
Term-sheet templates (autocall, RC, PPN); **solve-for** coupon/barrier/participation; scenario & Greek ladders; correlation & dividend sensitivity; lifecycle events (fixings, autocall triggers, knock-ins); pricing audit trail.

### Connections
- **Inputs explained in:** [[forward-pricing]], [[volatility-surface]]. **Language details:** [[csharp-essentials]].
