---
id: csharp-dotnet
title: "C# & .NET"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep, src-csharp-syntax-notes]
---
# C# & .NET

**Sections:** [[csharp-abstract-classes]] · [[csharp-arrow-syntax]] · [[csharp-constructors-base]] · [[csharp-ternary-operator]] · [[csharp-syntax-cheatsheet]] · [[csharp-essentials]] · [[dotnet-concurrency-wpf]]

<a id="csharp-abstract-classes"></a>

## Abstract Classes & Abstract Methods
<!-- section: csharp-abstract-classes | prerequisites: [oop-pillars] | related: [csharp-essentials, pricing-app-architecture, csharp-constructors-base] | sources: [src-csharp-syntax-notes] | tags: [csharp, abstract, polymorphism, override] -->

Examples come from equity-derivative pricing class design (Payoff / Exercise / Option / PricingEngine).

```csharp
public abstract class Instrument { public abstract double NPV(); }
```

| Part | Meaning |
|---|---|
| `abstract class` | Abstract class: you **cannot** `new Instrument()`; it can only be inherited |
| `public abstract double NPV();` | Abstract method: declaration only, **no implementation** (no `{ }`) |
| `NPV` | Net Present Value, the product's value today |

**Rule:** a non-abstract subclass **must** implement every abstract method with `override`, otherwise it doesn't compile.

```csharp
public abstract class Option : Instrument { ... }            // still abstract, may leave NPV unimplemented

public abstract class OneAssetOption<TSelf> : Option
{
    public override double NPV() => _engine.Calculate((TSelf)this);   // actually implemented here
}
```

**Why this design:** one common interface, so different products can be handled polymorphically.

```csharp
var portfolio = new List<Instrument> { euCall, amPut, asian /*, bond, swap */ };
double total = 0;
foreach (var inst in portfolio)
    total += inst.NPV();      // no need to know the concrete product; each calls its own implementation
```

- Abstract class vs interface: see [[csharp-essentials]].

### C++ equivalent

```cpp
class Instrument {
public:
    virtual ~Instrument() = default;   // a polymorphic base class must have a virtual destructor
    virtual double NPV() const = 0;    // pure virtual function = C# abstract
};
```

### Connections
- **Builds on:** [[oop-pillars]] (abstraction, polymorphism).
- **Used in:** [[pricing-app-architecture]].

<a id="csharp-arrow-syntax"></a>

## The Two Uses of `=>`
<!-- section: csharp-arrow-syntax | prerequisites: [csharp-abstract-classes] | related: [csharp-essentials, csharp-constructors-base] | sources: [src-csharp-syntax-notes] | tags: [csharp, lambda, expression-bodied, linq] -->

### Use 1: expression-bodied member

`=>` means **"the method body is this one expression"**.

| Member's return type | `=> expression` is equivalent to |
|---|---|
| **Returns a value** (e.g. `double`) | `{ return expression; }` |
| **No return value** (`void`, constructor) | `{ expression; }`: executes only, **no return** |

**Returns a value, same as `return`:**

```csharp
public override double Value(double s) => Math.Max(s - Strike, 0.0);
// equivalent to
public override double Value(double s) { return Math.Max(s - Strike, 0.0); }
```

**No return value, executes only:**

```csharp
public void SetPricingEngine(IPricingEngine<TSelf> engine) => _engine = engine;
// equivalent to
public void SetPricingEngine(IPricingEngine<TSelf> engine) { _engine = engine; }
```

**Read-only property:**

```csharp
public double Moneyness => Spot / Strike;   // same as get { return Spot / Strike; }
```

**Rules:**

- Only **one expression** can follow `=>`.
- An assignment `_cash = cash` is also an expression in C#, so it can follow `=>`.

### Use 2: lambda expression (anonymous function)

Left of `=>` are the parameters, right of it is the function body.

```csharp
Func<double, double> callPayoff = s => Math.Max(s - 100, 0);
callPayoff(120);                                     // 20

var itm   = portfolio.Where(opt => opt.NPV() > 1.0); // LINQ filter
var total = portfolio.Sum(inst => inst.NPV());       // aggregate
```

| Form | Meaning |
|---|---|
| `x => x * 2` | one parameter |
| `(x, y) => x + y` | several parameters |
| `() => 42` | no parameters |
| `x => { var y = x * 2; return y + 1; }` | several statements need `{ }` and `return` |

### Telling the two uses apart

| Where `=>` appears | Which use |
|---|---|
| After the **declaration** of a method, property or constructor | expression-bodied member |
| Passed as an **argument**, or assigned to a `Func` / `Action` | lambda |

**Lambdas in other languages:**

- Python: `lambda s: max(s - 100, 0)`
- C++: `[](double s) { return std::max(s - 100.0, 0.0); }`

### Connections
- **Used with:** LINQ and `Func` in [[csharp-essentials]].
- **In constructors:** [[csharp-constructors-base]].

<a id="csharp-constructors-base"></a>

## Constructors & `: base(...)`
<!-- section: csharp-constructors-base | prerequisites: [csharp-abstract-classes, csharp-arrow-syntax] | related: [oop-pillars] | sources: [src-csharp-syntax-notes] | tags: [csharp, constructor, inheritance, initialization-order] -->

```csharp
public CashOrNothingPayoff(OptionType type, double strike, double cash) : base(type, strike) => _cash = cash;
//     ①                   ②                                            ③                      ④
```

| Part | Meaning |
|---|---|
| ① `public CashOrNothingPayoff` | Same name as the class, no return type → **constructor** (runs on `new`) |
| ② `(OptionType type, double strike, double cash)` | Arguments passed when the object is created |
| ③ `: base(type, strike)` | **First calls the base class** `StrikedPayoff` constructor, handing type and strike to the base class to store |
| ④ `=> _cash = cash;` | Then runs its own code: stores `_cash`. A constructor has no return value, so this `=>` only executes, no return |

### Full form (equivalent to the line above)

```csharp
public CashOrNothingPayoff(OptionType type, double strike, double cash)
    : base(type, strike)      // step 1: the base class stores Type and Strike
{
    _cash = cash;             // step 2: the subclass stores its own _cash
}
```

### Why two steps

Each class initialises only the data **it** defines:

```
StrikedPayoff (base)       defines Type, Strike  → base constructor assigns them
  └─ CashOrNothingPayoff   defines _cash         → subclass assigns it itself
```

`Type` and `Strike` are read-only properties (`{ get; }`) of the base class. They can only be assigned in the base class's own constructor; the subclass cannot write `Strike = strike` directly.

### Execution order

For `new CashOrNothingPayoff(OptionType.Call, 100, 1.0)`:

1. Enter the subclass constructor and receive the arguments.
2. Run `: base(type, strike)` → base class: `Type = Call; Strike = 100;`.
3. Back in the subclass: `_cash = 1.0;`.
4. Object creation complete.

**Rule: the base class is constructed first, then the subclass.**

### Comparison

**Python:**

```python
class CashOrNothingPayoff(StrikedPayoff):
    def __init__(self, type, strike, cash):
        super().__init__(type, strike)   # ← : base(type, strike)
        self._cash = cash                # ← => _cash = cash
```

**C++:**

```cpp
CashOrNothingPayoff(OptionType t, double K, double cash)
    : StrikedPayoff(t, K), cash_(cash) {}   // done in the initializer list
```

### Connections
- **Builds on:** [[csharp-abstract-classes]], [[csharp-arrow-syntax]].

<a id="csharp-ternary-operator"></a>

## The Ternary Operator `? :`
<!-- section: csharp-ternary-operator | prerequisites: [] | related: [csharp-constructors-base] | sources: [src-csharp-syntax-notes] | tags: [csharp, operators, control-flow] -->

**Format:**

```
condition ? value if true : value if false
```

It compresses if-else into one line, to pick one of two values.

```csharp
public override double Value(double s)
{
    bool itm = Type == OptionType.Call ? s > Strike : s < Strike;   // a call checks S>K, a put checks S<K
    return itm ? _cash : 0.0;                                       // pays cash if in the money, else 0
}
```

**`return itm ? _cash : 0.0;` is equivalent to:**

```csharp
if (itm)
    return _cash;
else
    return 0.0;
```

**Example:** call, Strike = 100, cash = 1.0:

| Price at expiry s | itm | Returns |
|---|---|---|
| 120 | `120 > 100` → true | 1.0 |
| 90 | `90 > 100` → false | 0.0 |

**Other languages:**

| Language | Syntax |
|---|---|
| C# / C++ / Java | `itm ? cash : 0.0` |
| Python | `cash if itm else 0.0` (value first, condition in the middle) |

- Once the logic gets complicated, switch to if-else for readability.

### Connections
- **Payoff example:** cash-or-nothing digital, see [[digital-options]].

<a id="csharp-syntax-cheatsheet"></a>

## C# Syntax Cheat Sheet
<!-- section: csharp-syntax-cheatsheet | prerequisites: [csharp-abstract-classes] | related: [csharp-essentials, csharp-arrow-syntax, csharp-constructors-base] | sources: [src-csharp-syntax-notes] | tags: [csharp, syntax, reference] -->

| Syntax | Example | Meaning |
|---|---|---|
| `: BaseClass` | `class PlainVanillaPayoff : StrikedPayoff` | inheritance |
| `: Interface` | `class MCEuropeanEngine : IPricingEngine<VanillaOption>` | implements an interface |
| `override` | `public override double Value(...)` | implements or overrides a base-class abstract / virtual method |
| `sealed` | `public sealed class PlainVanillaPayoff` | cannot be inherited further |
| `protected` | `protected StrikedPayoff(...)` | accessible only to the class itself and subclasses |
| `internal` | `internal static class Normal` | visible only inside the current project (assembly) |
| `static class` | `Normal.Cdf(x)` | cannot be `new`ed, all static methods, like a utility-function module |
| `{ get; }` | `public double Strike { get; }` | read-only auto-property, assignable only in the constructor |
| `readonly` | `private readonly double _cash;` | read-only field, assignable only in the constructor |
| `enum` | `enum OptionType { Call, Put }` | a set of named constants, safer than strings |
| generics `<T>` | `IPricingEngine<TOption>` | type parameter, specified when used |
| `where T : X` | `where TOption : Option` | generic constraint: T must be X or a subclass of X |
| `?` (after a type) | `IPricingEngine<TSelf>? _engine` | may be null |
| `??` | `_engine ?? throw new ...` | use the left side if not null, otherwise evaluate the right side |
| `throw` expression | `x ?? throw new InvalidOperationException(...)` | throw can appear inside an expression (C# 7+) |
| `is not T x` | `if (opt.Payoff is not PlainVanillaPayoff pay) throw ...;` | pattern matching: checks the type, and casts and assigns to `pay` at the same time |
| `(T)x` | `(TSelf)this` | explicit cast |
| `record` | `record BlackScholesProcess(double Spot, ...)` | immutable data class; constructor, properties and equality generated automatically |
| `with` | `process with { Spot = 101 }` | copies a record with some fields changed; the original is unchanged |
| `var` | `var v = new double[n + 1];` | let the compiler infer the type |
| optional parameter | `int seed = 42` | uses the default if not passed |
| named argument | `new BlackScholesProcess(Spot: 100, ...)` | write parameter names at the call site for readability |
| `$"..."` | `$"NPV: {npv:F4}"` | string interpolation; `:F4` means 4 decimal places |
| `200_000` | `new MCEuropeanEngine(process, 200_000)` | digit separator, equals 200000 |
| `*=` / `+=` | `s *= Math.Exp(...)` | `s = s * ...` / `s = s + ...` |
| `try / catch` | `try { ... } catch (ArgumentException e) { ... }` | catch exceptions |

*All of the above is standard C# / C++ syntax. The `Instrument` / `NPV()` / `PricingEngine` naming follows QuantLib conventions.*

### Connections
- **Details:** [[csharp-abstract-classes]], [[csharp-arrow-syntax]], [[csharp-constructors-base]], [[csharp-ternary-operator]]. **Records & `with`:** [[csharp-essentials]].

<a id="csharp-essentials"></a>

## C# / .NET Essentials for Quant Dev
<!-- section: csharp-essentials | prerequisites: [oop-pillars] | related: [dotnet-concurrency-wpf, pricing-app-architecture, monte-carlo-pricing, csharp-abstract-classes, csharp-syntax-cheatsheet] | sources: [src-rbc-quantdev-prep, src-csharp-syntax-notes] | tags: [csharp, dotnet, gc, interop] -->

- **Interface vs abstract class:** interface = contract, multiple implementation, no state (default methods since C# 8) → pluggable things (models, data sources). Abstract class = shared state + partial implementation, single inheritance → shared instrument behaviour.

| | `abstract class` | `interface` |
|---|---|---|
| Can it have implementation? | Can mix: some methods implemented, some abstract | Usually not (C# 8+ allows default implementations) |
| Can it have fields? | Yes | No instance fields |
| How many? | A class can inherit only **one** class | A class can implement **many** interfaces |

- **struct / class / record:** struct = value type, copied (small immutable data like a tenor); class = reference, identity; **record** = reference type with value equality + `with` → ideal for immutable trades / market snapshots.
- **Immutability:** lock-free concurrent pricing, reproducible results, scenarios = `md with { Spot = 105 }`.
- **GC:** generational (Gen 0/1/2, LOH > 85 KB). In MC hot loops reuse arrays, `Span<T>`, `ArrayPool<T>`. Unsubscribed event handlers leak memory in long-running desktop apps.
- **Errors:** validate inputs up front (negative vol, past expiry, missing dividend); clear trader-readable error; never silently return 0/NaN; log trade ID + model version.
- **Generics/LINQ:** `Dictionary<string, Func<Instrument, IPricingModel>>` registry; `trades.GroupBy(t => t.Underlying).Select(g => new { g.Key, Delta = g.Sum(t => t.Delta) })`.
- **C++ interop:** P/Invoke to a C API, C++/CLI wrapper, COM, or out-of-process service (gRPC/REST). Watch marshalling cost, memory ownership, version pinning.
- **Python → C#:** ABCs ≈ interfaces, dataclasses ≈ records; add static typing and explicit threading.

<a id="dotnet-concurrency-wpf"></a>

## .NET Concurrency, WPF & MVVM
<!-- section: dotnet-concurrency-wpf | prerequisites: [csharp-essentials] | related: [pricing-app-architecture, scenario-risk-grids] | sources: [src-rbc-quantdev-prep] | tags: [async, wpf, mvvm, threading] -->

- **async/await** → I/O-bound (fetch market data, call a pricing service); frees the UI thread.
- **Parallel.For / PLINQ / Task.Run** → CPU-bound (MC paths, scenario grids).
- Never `.Result` / `.Wait()` on the UI thread → deadlock with WPF sync context.
- **500 scenarios, responsive UI:** `await Task.Run(...)`, `IProgress<T>`, `CancellationToken`, batch `ObservableCollection` updates on the Dispatcher, virtualise grids.
- **MVVM:** Model = domain (trades, pricers); View = XAML; ViewModel = state + commands (`INotifyPropertyChanged`, `ICommand`) → testable without UI. Toolkits: CommunityToolkit.Mvvm, Prism, ReactiveUI.
