---
id: csharp-dotnet
title: "C# & .NET"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep, src-csharp-syntax-notes]
---
# C# & .NET

**Sections:** [[csharp-abstract-classes]] · [[csharp-arrow-syntax]] · [[csharp-constructors-base]] · [[csharp-ternary-operator]] · [[csharp-syntax-cheatsheet]] · [[csharp-pricing-library-example]] · [[csharp-essentials]] · [[dotnet-concurrency-wpf]]

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

<a id="csharp-pricing-library-example"></a>

## Complete Example: A Pricing Library in C# (annotated line by line)
<!-- section: csharp-pricing-library-example | prerequisites: [csharp-abstract-classes, csharp-arrow-syntax, csharp-constructors-base, csharp-ternary-operator] | related: [pricing-app-architecture, design-patterns-pricing, black-scholes-formula, binomial-replication, monte-carlo-pricing, asian-options, digital-options, american-early-exercise] | sources: [src-csharp-syntax-notes] | tags: [csharp, pricing-library, composition, generics, crtp] -->

- The complete pricing example: Payoff → Exercise → Process → Instrument/Option → Engines → Main. Concatenating all code blocks in order gives one complete `.cs` file (.NET 6+).
- A C++ version of the same design has been compiled and run, with these results:

| Product | Engine | Price |
|---|---|---|
| EU call | analytic | 10.4506 |
| EU call | binomial | 10.4466 |
| EU call | MC | 10.5167 |
| EU put | analytic | 5.5735 |
| AM put | binomial | 6.0888 |
| Digital | MC | 0.5330 |
| Asian | MC | 6.1473 |

- This C# version has not been compiled here; MC results will differ slightly because the random number generator differs.

### Overall structure

Four independent parts, combined at the end by composition:

| Part | Responsible for | Examples |
|---|---|---|
| **Payoff** | how much is paid at expiry | Call / Put / Digital |
| **Exercise** | when it can be exercised | European / American |
| **Process** | market data + model | spot, r, q, vol (GBM) |
| **Engine** | which method computes the price | analytic formula / binomial tree / Monte Carlo |

`Instrument` / `Option` packages Payoff + Exercise together, then "attaches" an Engine to compute the NPV.

### 0. Setup: namespace and enums

```csharp
using System;   // imports the System namespace: Math, Random, Console, exception classes, etc. Without it you'd write System.Math.Max(...)


// [enum] a set of named constants. OptionType can only be Call or Put, safer than a string "call" (a typo is a compile error)
public enum OptionType { Call, Put }

// Exercise type: European (exercise only at expiry) or American (exercise any time before expiry)
public enum ExerciseType { European, American }
```

### 1. PAYOFF: how much is paid at expiry; essentially a function S -> cash

```csharp
// [abstract class] cannot new Payoff() directly, only inherit. It defines "what every payoff must have"
public abstract class Payoff
{
    // [abstract method] declaration only, no implementation (no { }). Subclasses must implement it with override
    // Meaning: given an underlying price s, return how much is paid at that price
    public abstract double Value(double s);
}

// Middle layer: common parent of all "payoffs with a strike" (call, put, digital all have a strike)
// It inherits Payoff (": Payoff" means "inherits from Payoff") but is still abstract, because it doesn't yet know how to compute Value
public abstract class StrikedPayoff : Payoff
{
    // [protected constructor] only subclasses can call it (outside code can't new StrikedPayoff)
    // Purpose: store the passed-in type and strike in the two properties below
    protected StrikedPayoff(OptionType type, double strike) { Type = type; Strike = strike; }

    // [read-only auto-property { get; }] outside code can read but not change; assigned once in the constructor → immutable after creation, safe
    public OptionType Type { get; }   // Call or Put
    public double Strike { get; }     // strike K
}

// [sealed] this class cannot be inherited further (bottom-level concrete class, prevents arbitrary inheritance)
// Plain vanilla payoff: call = max(S-K, 0), put = max(K-S, 0)
public sealed class PlainVanillaPayoff : StrikedPayoff
{
    // ": base(type, strike)" first calls the base StrikedPayoff constructor, passing the arguments up
    // The { } after it is empty: this class has no extra data of its own to store
    public PlainVanillaPayoff(OptionType type, double strike) : base(type, strike) { }

    // [override] implements the abstract method Value from the base class Payoff
    // [=>] expression-bodied member: shorthand when the body is a single expression, equivalent to { return ...; }
    // [? :] ternary operator: condition ? value if true : value if false
    public override double Value(double s) =>
        Type == OptionType.Call ? Math.Max(s - Strike, 0.0)   // Call: max(S - K, 0)
                                : Math.Max(Strike - s, 0.0);  // Put : max(K - S, 0)
}

// Digital option (cash-or-nothing digital): pays a fixed cash amount if in the money at expiry, otherwise 0
public sealed class CashOrNothingPayoff : StrikedPayoff
{
    // [readonly field] can only be assigned in the constructor; the _ prefix is the C# naming convention for private fields
    private readonly double _cash;

    // First call the base constructor to store type/strike, then use => to store cash in _cash (only one statement after =>, so the shorthand works)
    public CashOrNothingPayoff(OptionType type, double strike, double cash) : base(type, strike) => _cash = cash;

    // The body has two lines here, so it can't use the => shorthand; use normal { }
    public override double Value(double s)
    {
        bool itm = Type == OptionType.Call ? s > Strike : s < Strike;   // itm = in the money: a call needs S>K, a put needs S<K
        return itm ? _cash : 0.0;                                       // pays cash if in the money, else 0
    }
}
```

### 2. EXERCISE: exercise style, put into the option by composition rather than subclasses like AmericanCall / EuropeanPut

```csharp
public abstract class Exercise
{
    // protected constructor: only subclasses (EuropeanExercise / AmericanExercise) can call it
    protected Exercise(ExerciseType type, double expiry) { Type = type; Expiry = expiry; }

    public ExerciseType Type { get; }   // exercise type
    public double Expiry { get; }       // time to expiry T (years)
}

// The two concrete subclasses do one thing only: pass the right ExerciseType to the base class. So usage reads naturally: new EuropeanExercise(1.0)
public sealed class EuropeanExercise : Exercise { public EuropeanExercise(double expiry) : base(ExerciseType.European, expiry) { } }
public sealed class AmericanExercise : Exercise { public AmericanExercise(double expiry) : base(ExerciseType.American, expiry) { } }
```

### 3. MARKET + MODEL: all the market data needed under Black-Scholes (geometric Brownian motion, GBM)

```csharp
// [record] the "data class" introduced in C# 9: one line auto-generates the constructor, read-only properties, equality and ToString
// It is immutable: can't be changed after creation → pricing is a pure function, thread-safe and reproducible
// For scenario analysis / Greeks, copy it with "with" and change one value: process with { Spot = 101 }
public sealed record BlackScholesProcess(double Spot, double Rate, double DivYield, double Vol);
//                                        S0 spot      r risk-free   q continuous      σ volatility
//                                                     rate          dividend yield
```

### 4. INSTRUMENT / ENGINE: the "interface contract" between product and pricing method

```csharp
// Top-level base class of all financial products: the only contract is "you must be able to tell me what you're worth (NPV = net present value)"
// So a portfolio can be a List<Instrument>, summing NPV() in a loop without caring which product it is (polymorphism)
public abstract class Instrument
{
    public abstract double NPV();
}

// [interface] only specifies "which methods must exist", no implementation. Every pricing engine must implement Calculate
// [generic <TOption>] TOption is a "type parameter"; which option type it is gets decided when used.
//    e.g. IPricingEngine<VanillaOption> = "an engine dedicated to pricing VanillaOption"
// [where TOption : Option] generic constraint: TOption must be Option or a subclass (you can't pass in a string)
public interface IPricingEngine<TOption> where TOption : Option
{
    double Calculate(TOption option);   // takes an option, returns the price. Interface methods are public by default
}

// Common base class of all options: every option "has a" Payoff and "has an" Exercise (composition has-a, not inheritance is-a)
// It inherits Instrument but is still abstract: it doesn't yet know how to compute NPV (that's delegated to the engine)
public abstract class Option : Instrument
{
    protected Option(Payoff payoff, Exercise exercise) { Payoff = payoff; Exercise = exercise; }

    // Note: the property has the same name as the class (Payoff Payoff); C# allows this, the first is the type, the second the property name
    public Payoff Payoff { get; }
    public Exercise Exercise { get; }
}

// [The hardest part] "self-referencing generic" (C#'s version of the CRTP trick)
//   TSelf stands for "the subclass that inherits me". e.g. VanillaOption : OneAssetOption<VanillaOption>, so TSelf is VanillaOption
//   Goal: VanillaOption can only attach IPricingEngine<VanillaOption>, AsianOption only IPricingEngine<AsianOption>
//         — attaching the wrong engine (e.g. a binomial engine on an Asian) fails at "compile time", not by computing a wrong price at run time
//   where TSelf : OneAssetOption<TSelf>: constrains TSelf to really be my subclass
public abstract class OneAssetOption<TSelf> : Option where TSelf : OneAssetOption<TSelf>
{
    // The currently attached pricing engine. [?] means it may be null (no engine set yet)
    private IPricingEngine<TSelf>? _engine;

    // Does nothing except pass payoff and exercise to the base Option to store
    protected OneAssetOption(Payoff payoff, Exercise exercise) : base(payoff, exercise) { }

    // Set / replace the pricing engine. The parameter type is IPricingEngine<TSelf> → an engine of the wrong type can't even be passed in
    public void SetPricingEngine(IPricingEngine<TSelf> engine) => _engine = engine;

    // Implements the NPV() required by Instrument: hand "itself" to the engine to compute
    //   [??] null-coalescing operator: use the left side if not null, otherwise evaluate the right side → here the right side throws
    //   [throw expression] since C# 7, throw can appear inside an expression
    //   [(TSelf)this] casts this (type OneAssetOption<TSelf>) to the real subclass type so it can be passed to Calculate(TSelf)
    public override double NPV() =>
        (_engine ?? throw new InvalidOperationException("no pricing engine set")).Calculate((TSelf)this);
}

// Vanilla option: European or American call/put/digital are all this class; they differ only in the Payoff and Exercise passed in
// It passes itself as TSelf to the base class: OneAssetOption<VanillaOption>
public sealed class VanillaOption : OneAssetOption<VanillaOption>
{
    public VanillaOption(Payoff payoff, Exercise exercise) : base(payoff, exercise) { }
}

// Asian option: the payoff applies to the "average price", so one extra parameter: how many price observations (fixings)
public sealed class AsianOption : OneAssetOption<AsianOption>
{
    // First hand payoff/exercise to the base class, then use => to store fixings in the property
    public AsianOption(Payoff payoff, Exercise exercise, int fixings) : base(payoff, exercise) => Fixings = fixings;

    public int Fixings { get; }   // number of averaging observations, e.g. 12 = observe once a month
}
```

### Math utilities

```csharp
// [static class] cannot be new-ed, all static methods, called directly as Normal.Cdf(x). Like a Python utility-function module
// [internal] visible only inside the current project (assembly), invisible from outside
internal static class Normal
{
    // Standard normal CDF N(x). .NET has no built-in erf, so use the Abramowitz & Stegun 26.2.17 approximation (error < 7.5e-8)
    public static double Cdf(double x)
    {
        if (x < 0) return 1.0 - Cdf(-x);                        // symmetry: N(-x) = 1 - N(x); the formula only handles x >= 0
        double t = 1.0 / (1.0 + 0.2316419 * x);                  // intermediate variable of the A&S approximation
        double poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
        //            ↑ degree-5 polynomial written nested (Horner's method): fewer multiplications, numerically more stable
        return 1.0 - Math.Exp(-0.5 * x * x) / Math.Sqrt(2.0 * Math.PI) * poly;   // 1 - φ(x)·poly, φ is the normal density
    }

    // Generate a standard normal random number Z ~ N(0,1). Box-Muller transform: two uniform random numbers → one normal
    public static double Sample(Random rng)
    {
        double u1 = 1.0 - rng.NextDouble(), u2 = rng.NextDouble();   // NextDouble() ∈ [0,1); using 1-u1 guarantees u1 > 0, avoiding log(0)
        return Math.Sqrt(-2.0 * Math.Log(u1)) * Math.Cos(2.0 * Math.PI * u2);
    }
}
```

### ENGINES: concrete pricing methods; each engine implements IPricingEngine<some option type>

```csharp
// ---------- Engine 1: Black-Scholes analytic formula (European + plain call/put only) ----------
public sealed class AnalyticEuropeanEngine : IPricingEngine<VanillaOption>   // ": interface" = implements this interface
{
    private readonly BlackScholesProcess _p;                        // the engine holds the market data / model

    public AnalyticEuropeanEngine(BlackScholesProcess p) => _p = p; // constructor: store the process

    public double Calculate(VanillaOption opt)                      // implements the method the interface requires
    {
        // Check 1: the analytic formula only applies to European. If not, fail early (fail fast); don't silently compute a wrong number
        if (opt.Exercise.Type != ExerciseType.European)
            throw new ArgumentException("AnalyticEuropeanEngine: European exercise only");

        // Check 2: [is not ... pay] pattern matching. If opt.Payoff is not a PlainVanillaPayoff, throw;
        //          if it is, it's cast and assigned to a new variable pay at the same time (pay.Strike, pay.Type usable below)
        if (opt.Payoff is not PlainVanillaPayoff pay)
            throw new ArgumentException("AnalyticEuropeanEngine: plain vanilla payoff only");

        // Pull out the variables the formula needs, with short names, to match the formula
        double s = _p.Spot, k = pay.Strike, t = opt.Exercise.Expiry;   // S, K, T
        double r = _p.Rate, q = _p.DivYield, v = _p.Vol;               // r, q, σ
        double sT = v * Math.Sqrt(t);                                  // σ√T
        double d1 = (Math.Log(s / k) + (r - q + 0.5 * v * v) * t) / sT; // d1 = [ln(S/K) + (r - q + σ²/2)T] / (σ√T)
        double d2 = d1 - sT;                                           // d2 = d1 - σ√T
        double dfR = Math.Exp(-r * t), dfQ = Math.Exp(-q * t);         // discount factor e^{-rT} and dividend discount e^{-qT}

        return pay.Type == OptionType.Call
            ? s * dfQ * Normal.Cdf(d1) - k * dfR * Normal.Cdf(d2)      // Call = S e^{-qT} N(d1) - K e^{-rT} N(d2)
            : k * dfR * Normal.Cdf(-d2) - s * dfQ * Normal.Cdf(-d1);   // Put  = K e^{-rT} N(-d2) - S e^{-qT} N(-d1)
    }
}

// ---------- Engine 2: CRR binomial tree (European and American, any payoff) ----------
public sealed class BinomialVanillaEngine : IPricingEngine<VanillaOption>
{
    private readonly BlackScholesProcess _p;
    private readonly int _n;                                         // number of tree steps: more is more accurate and slower

    public BinomialVanillaEngine(BlackScholesProcess p, int steps) { _p = p; _n = steps; }

    public double Calculate(VanillaOption opt)
    {
        double t = opt.Exercise.Expiry, dt = t / _n;                 // length of each step Δt = T / n
        double u = Math.Exp(_p.Vol * Math.Sqrt(dt)), d = 1.0 / u;    // up factor u = e^{σ√Δt}, down factor d = 1/u
        double pu = (Math.Exp((_p.Rate - _p.DivYield) * dt) - d) / (u - d);   // risk-neutral up probability p = (e^{(r-q)Δt} - d)/(u - d)
        double disc = Math.Exp(-_p.Rate * dt);                       // per-step discount factor e^{-rΔt}
        bool american = opt.Exercise.Type == ExerciseType.American;  // whether early exercise is allowed

        // [new double[n+1]] creates an array of length n+1. At expiry there are n+1 nodes
        // Node index j = number of down moves: j=0 all up (highest price), j=n all down (lowest price)
        var v = new double[_n + 1];                                  // [var] let the compiler infer the type (here double[])

        // Step 1: compute the payoff at every node at expiry. Node price = S0 · u^{(n-j)} · d^{j} = S0 · u^{n-2j} (since d = 1/u)
        for (int j = 0; j <= _n; j++) v[j] = opt.Payoff.Value(_p.Spot * Math.Pow(u, _n - 2 * j));

        // Step 2: work backwards from expiry (backward induction) all the way to today (i = 0)
        for (int i = _n - 1; i >= 0; i--)                            // i = time step, from n-1 down to 0
            for (int j = 0; j <= i; j++)                             // step i has i+1 nodes
            {
                // Continuation value = discount × [p × value after up + (1-p) × value after down]
                // After an up move the down count is unchanged → v[j]; after a down move it is +1 → v[j+1]. Overwrite v[j] directly to save memory
                v[j] = disc * (pu * v[j] + (1.0 - pu) * v[j + 1]);

                // American: at each node compare "continue holding" with "exercise now" and take the larger
                if (american) v[j] = Math.Max(v[j], opt.Payoff.Value(_p.Spot * Math.Pow(u, i - 2 * j)));
            }
        return v[0];                                                 // back at the root node = today's price
    }
}

// ---------- Engine 3: Monte Carlo (European, any payoff) ----------
public sealed class MCEuropeanEngine : IPricingEngine<VanillaOption>
{
    private readonly BlackScholesProcess _p;
    private readonly int _paths, _seed;                              // two fields declared on one line: number of paths, random seed

    // [int seed = 42] optional parameter, defaults to 42 if not passed. Fixed seed → same result every run, easy to test and reproduce
    public MCEuropeanEngine(BlackScholesProcess p, int paths, int seed = 42) { _p = p; _paths = paths; _seed = seed; }

    public double Calculate(VanillaOption opt)
    {
        if (opt.Exercise.Type != ExerciseType.European)              // plain MC can't handle early exercise (needs Longstaff-Schwartz)
            throw new ArgumentException("MCEuropeanEngine: European exercise only");

        double t = opt.Exercise.Expiry;
        // Exact GBM solution: S_T = S0 · exp[(r - q - σ²/2)T + σ√T · Z], Z ~ N(0,1)
        // A European only looks at the expiry price, so jump straight to T; no need to simulate the path in between
        double drift = (_p.Rate - _p.DivYield - 0.5 * _p.Vol * _p.Vol) * t;   // (r - q - σ²/2)T
        double volT = _p.Vol * Math.Sqrt(t);                                  // σ√T
        var rng = new Random(_seed);                                          // random number generator

        double sum = 0.0;
        for (int i = 0; i < _paths; i++)                             // simulate _paths paths
            sum += opt.Payoff.Value(_p.Spot * Math.Exp(drift + volT * Normal.Sample(rng)));   // generate S_T, compute payoff, accumulate
        return Math.Exp(-_p.Rate * t) * sum / _paths;                // price = e^{-rT} × average payoff
    }
}

// ---------- Engine 4: Monte Carlo Asian option (arithmetic average, equally spaced observations) ----------
// Note it implements IPricingEngine<AsianOption>, so it can only be attached to an AsianOption
public sealed class MCAsianEngine : IPricingEngine<AsianOption>
{
    private readonly BlackScholesProcess _p;
    private readonly int _paths, _seed;

    public MCAsianEngine(BlackScholesProcess p, int paths, int seed = 42) { _p = p; _paths = paths; _seed = seed; }

    public double Calculate(AsianOption opt)
    {
        if (opt.Exercise.Type != ExerciseType.European)
            throw new ArgumentException("MCAsianEngine: European exercise only");

        int n = opt.Fixings;                                         // number of observations
        double t = opt.Exercise.Expiry, dt = t / n;                  // time between two observations
        double drift = (_p.Rate - _p.DivYield - 0.5 * _p.Vol * _p.Vol) * dt;  // drift of each small step
        double volDt = _p.Vol * Math.Sqrt(dt);                               // volatility of each small step σ√Δt
        var rng = new Random(_seed);

        double sum = 0.0;
        for (int i = 0; i < _paths; i++)                             // outer loop: each path
        {
            double s = _p.Spot, avg = 0.0;                           // each path starts from S0; avg accumulates first
            for (int k = 0; k < n; k++)                              // inner loop: step to each observation date
            {
                s *= Math.Exp(drift + volDt * Normal.Sample(rng));   // [*=] s = s * ..., take one step
                avg += s;                                            // [+=] record the price on this observation date
            }
            sum += opt.Payoff.Value(avg / n);                        // key point: the same call payoff, applied to the "average price" instead of S_T
        }
        return Math.Exp(-_p.Rate * t) * sum / _paths;                // discount and average
    }
}
```

### Usage example

```csharp
public static class Program
{
    // Program entry point: execution starts at Main
    public static void Main()
    {
        // ---- 1. Prepare market data and contract terms ----
        // [named arguments Spot: 100] say what each number is, more readable (could also just write new BlackScholesProcess(100, 0.05, 0.0, 0.20))
        var process = new BlackScholesProcess(Spot: 100, Rate: 0.05, DivYield: 0.0, Vol: 0.20);
        var call    = new PlainVanillaPayoff(OptionType.Call, 100);       // call payoff with K = 100
        var put     = new PlainVanillaPayoff(OptionType.Put, 100);        // put payoff with K = 100
        var digital = new CashOrNothingPayoff(OptionType.Call, 100, 1.0); // pays 1 if S_T > 100
        var euro    = new EuropeanExercise(1.0);                          // expires in 1 year, exercise at expiry only
        var amer    = new AmericanExercise(1.0);                          // exercisable any time within 1 year

        // ---- 2. Prepare pricing engines ----
        var analytic = new AnalyticEuropeanEngine(process);
        var tree     = new BinomialVanillaEngine(process, 500);           // 500-step binomial tree
        var mc       = new MCEuropeanEngine(process, 200_000);            // [200_000] the _ is just a digit separator for readability, equals 200000

        // ---- 3. Same product, different engines → results should be close (also a good unit test) ----
        var euCall = new VanillaOption(call, euro);                       // composition: call payoff + European exercise = European call
        // [$"...{expression:F4}"] string interpolation: the expression in {} is evaluated and inserted; :F4 means 4 decimal places
        euCall.SetPricingEngine(analytic); Console.WriteLine($"EU call  analytic : {euCall.NPV():F4}");
        euCall.SetPricingEngine(tree);     Console.WriteLine($"EU call  binomial : {euCall.NPV():F4}");
        euCall.SetPricingEngine(mc);       Console.WriteLine($"EU call  MC       : {euCall.NPV():F4}");

        // ---- 4. Same put payoff, different exercise → European put and American put ----
        var euPut = new VanillaOption(put, euro);
        var amPut = new VanillaOption(put, amer);
        euPut.SetPricingEngine(analytic);  Console.WriteLine($"EU put   analytic : {euPut.NPV():F4}");
        amPut.SetPricingEngine(tree);      Console.WriteLine($"AM put   binomial : {amPut.NPV():F4}");   // should be ≥ European put (early-exercise premium)

        // ---- 5. A new payoff type: the MC engine prices it without changing a line ----
        var dig = new VanillaOption(digital, euro);
        dig.SetPricingEngine(mc);          Console.WriteLine($"Digital  MC       : {dig.NPV():F4}");

        // The analytic engine doesn't support digitals → throws ArgumentException. [try/catch] catch the exception and print it instead of crashing
        try { dig.SetPricingEngine(analytic); dig.NPV(); }
        catch (ArgumentException e)        { Console.WriteLine($"Digital  analytic : rejected ({e.Message})"); }

        // ---- 6. Asian option: the same call payoff, just applied to the average price ----
        var asian = new AsianOption(call, euro, fixings: 12);             // observe once a month
        asian.SetPricingEngine(new MCAsianEngine(process, 200_000));
        Console.WriteLine($"Asian    MC       : {asian.NPV():F4}");       // should be < European call (the average price is less volatile)

        // Uncommenting the line below gives a "compile error": tree is IPricingEngine<VanillaOption> and can't be attached to an AsianOption
        // That's the type safety the OneAssetOption<TSelf> generic design provides
        // asian.SetPricingEngine(tree);

        // ---- 7. Scenario analysis: records are immutable; copy with "with" and change Spot ----
        var bumped = process with { Spot = 101 };                         // the original process is unchanged; bumped is a new object with S0 = 101
        // e.g. use it to compute delta ≈ [V(S0+1) - V(S0)] / 1:
        //   var callUp = new VanillaOption(call, euro);
        //   callUp.SetPricingEngine(new AnalyticEuropeanEngine(bumped));
        //   euCall.SetPricingEngine(analytic);   // note: euCall last had MC attached; both sides must use the same engine, otherwise the difference includes MC error
        //   double delta = callUp.NPV() - euCall.NPV();
    }
}
```

### Connections
- **Builds on:** [[csharp-abstract-classes]], [[csharp-arrow-syntax]], [[csharp-constructors-base]], [[csharp-ternary-operator]], [[csharp-syntax-cheatsheet]].
- **Same design idea:** [[pricing-app-architecture]], [[design-patterns-pricing]] (Strategy = swappable engine).
- **Engines:** [[black-scholes-formula]], [[binomial-replication]], [[american-early-exercise]], [[monte-carlo-pricing]]. **Products:** [[digital-options]], [[asian-options]].

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
