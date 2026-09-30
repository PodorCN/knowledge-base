---
id: numerical-methods
title: "Numerical Methods"
type: topic
domain: pricing
sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Numerical Methods

When no closed form exists, prices and implied quantities are computed numerically. This chapter covers the three workhorses: root finding (implied vols, yields), finite-difference solution of the pricing PDE, and Monte Carlo simulation — and when to use which.

**Prerequisites:** [[black-scholes-pde]], [[risk-neutral-pricing]], [[lln-clt]].

**Leads to:** [[implied-volatility]] (Newton inversion), [[barrier-options]], [[autocallables]], [[local-stochastic-volatility]].

**Sections:** [[root-finding]] · [[pde-finite-difference]] · [[monte-carlo-pricing]]

<a id="root-finding"></a>

## Root Finding (Newton, Bisection, Brent)
<!-- section: root-finding | prerequisites: [taylor-expansions] | related: [implied-volatility, bond-yield-measures] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [numerics, newton, brent] -->

Solving $f(x)=0$ numerically: Newton's method uses the derivative for fast convergence; bracketing methods trade speed for guaranteed convergence.

### Formula
$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}\quad\text{(Newton)}$$

**Variables:**

- $f$ function whose root is sought
- $f'$ its derivative
- $x_n$ iterate at step $n$

Newton's step is the root of the first-order Taylor expansion of $f$ at $x_n$ ([[taylor-expansions]]).

### Key points
- **Newton:** quadratic convergence near the root; explodes when $f'\to0$.
- **Bisection:** guaranteed (needs a bracket), linear convergence.
- **Brent:** bracketed + fast — the robust default.
- For implied vol: check the price is within the arbitrage bounds first, keep a bracket, use a good initial guess ([[implied-volatility]]).

### Connections
- **Used by:** [[implied-volatility]], [[bond-yield-measures]] (YTM).

<a id="pde-finite-difference"></a>

## PDE / Finite-Difference Pricing
<!-- section: pde-finite-difference | prerequisites: [black-scholes-pde] | related: [monte-carlo-pricing, barrier-options, american-early-exercise, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [pde, grid, crank-nicolson] -->

The pricing PDE is solved backward in time on a grid in $(S,t)$, starting from the payoff at expiry.

### Key points
- Accurate, stable Greeks in 1–2 factors; natural for **American exercise** ([[american-early-exercise]]) and **single-asset barriers** (the barrier is a boundary; align grid nodes with the barrier $H$, [[barrier-options]]).
- Discrete dividends: jump conditions at ex-dates.
- Curse of dimensionality → multi-asset products go to [[monte-carlo-pricing]].

### Connections
- **Builds on:** [[black-scholes-pde]].
- **Used for:** [[barrier-options]], [[american-early-exercise]], [[local-volatility-dupire]].

<a id="monte-carlo-pricing"></a>

## Monte Carlo Pricing
<!-- section: monte-carlo-pricing | prerequisites: [risk-neutral-pricing, lln-clt] | related: [pde-finite-difference, autocallables, barrier-options, asian-options, greeks-conventions-bumping, local-stochastic-volatility, static-replication] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [monte-carlo, aad, longstaff-schwartz, variance-reduction] -->

Monte Carlo simulates many risk-neutral paths and averages the discounted payoff. By the CLT its error falls like $1/\sqrt M$ in the number of paths $M$ ([[lln-clt]]).

### Formula
$$V_0\approx e^{-rT}\,\frac1M\sum_{j=1}^Mh\big(S^{(j)}\big),\qquad \text{standard error}\propto\frac{1}{\sqrt M}$$

**Variables:**

- $V_0$ price estimate
- $M$ number of simulated paths
- $S^{(j)}$ the $j$-th simulated path under $\mathbb Q$
- $h$ payoff (may depend on the whole path)
- $r$ risk-free rate; $T$ maturity

### Key points
- **Workhorse** for high-dimensional / path-dependent products: worst-of autocallables, baskets, cliquets.
- **Variance reduction:** antithetic paths; control variates (closed-form geometric Asian, flat-vol barrier).
- **Greeks:** AAD (adjoint algorithmic differentiation — "Smoking Adjoints") or bumping with common random numbers ([[greeks-conventions-bumping]]).
- **Early exercise:** Longstaff–Schwartz regression.
- **Barriers:** discrete monitoring needs the BGK shift; Brownian-bridge crossing probabilities for continuous monitoring ([[barrier-options]]).
- Performance (.NET): avoid allocations in hot loops (`Span`, `ArrayPool`), parallelise paths ([[csharp-essentials]]).

### Numerical-method map

| Method | Idea | Typical products |
|---|---|---|
| Closed form | analytic under flat vol | Reiner–Rubinstein barrier, geometric Asian, Margrabe, digital |
| [[static-replication]] | build from vanillas | digitals, variance swaps, any European |
| [[pde-finite-difference]] | solve the pricing PDE on a grid | single-asset barriers, American, local vol |
| **Monte Carlo** | simulate paths | autocallables, baskets, cliquets |

### Connections
- **Builds on:** [[risk-neutral-pricing]], [[lln-clt]].
- **Used for:** [[autocallables]], [[barrier-options]], [[asian-options]], [[local-stochastic-volatility]]; implemented in [[csharp-pricing-library-example]].
