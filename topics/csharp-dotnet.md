---
id: csharp-dotnet
title: "C# & .NET"
type: topic
domain: quant-dev
sources: [src-rbc-quantdev-prep]
---
# C# & .NET

**Sections:** [[csharp-essentials]] · [[dotnet-concurrency-wpf]]

<a id="csharp-essentials"></a>

## C# / .NET Essentials for Quant Dev
<!-- section: csharp-essentials | prerequisites: [oop-pillars] | related: [dotnet-concurrency-wpf, pricing-app-architecture, monte-carlo-pricing] | sources: [src-rbc-quantdev-prep] | tags: [csharp, dotnet, gc, interop] -->

- **Interface vs abstract class:** interface = contract, multiple implementation, no state (default methods since C# 8) → pluggable things (models, data sources). Abstract class = shared state + partial implementation, single inheritance → shared instrument behaviour.
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
