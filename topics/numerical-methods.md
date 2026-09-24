---
id: numerical-methods
title: "Numerical Methods"
type: topic
domain: quant-models
sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Numerical Methods

**Sections:** [[root-finding]] · [[pde-finite-difference]] · [[monte-carlo-pricing]]

<a id="root-finding"></a>

## Root Finding (Newton, Bisection, Brent)
<!-- section: root-finding | prerequisites: [] | related: [implied-volatility] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [numerics, newton, brent] -->

$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}\quad\text{(Newton)}$$

**Variables:**

- $f$ function whose root is sought
- $f'$ its derivative

- Newton: quadratic convergence near root; explodes when $f'\to0$.
- Bisection: guaranteed (needs a bracket), linear. Brent: bracketed + fast — robust default.
- For IV: check price within arbitrage bounds first, bracket, good initial guess.

<a id="pde-finite-difference"></a>

## PDE / Finite-Difference Pricing
<!-- section: pde-finite-difference | prerequisites: [black-scholes-pde] | related: [monte-carlo-pricing, barrier-options, american-early-exercise, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [pde, grid, crank-nicolson] -->

Solve the pricing PDE backward on a (S, t) grid.

- Accurate, stable Greeks in 1–2 factors; natural for **American exercise** and **single-asset barriers** (barrier = boundary; align grid nodes with H).
- Discrete dividends: jump conditions at ex-dates.
- Curse of dimensionality → multi-asset goes to [[monte-carlo-pricing]].

<a id="monte-carlo-pricing"></a>

## Monte Carlo Pricing
<!-- section: monte-carlo-pricing | prerequisites: [risk-neutral-pricing, lln-clt] | related: [pde-finite-difference, autocallables, barrier-options, asian-options, greeks-conventions-bumping, local-stochastic-volatility] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [monte-carlo, aad, longstaff-schwartz, variance-reduction] -->

Simulate risk-neutral paths, average discounted payoff; error ∝ $1/\sqrt N$ ([[lln-clt]]).

- **Workhorse** for high-dimensional / path-dependent: worst-of autocallables, baskets, cliquets.
- **Variance reduction:** antithetic paths; control variates (closed-form geometric Asian, flat-vol barrier).
- **Greeks:** AAD (adjoint algorithmic differentiation — "Smoking Adjoints") or bumping with common random numbers.
- **Early exercise:** Longstaff–Schwartz regression.
- **Barriers:** discrete monitoring needs BGK shift; Brownian-bridge crossing probabilities for continuous ones.
- Performance (.NET): avoid allocations in hot loops (Span, ArrayPool), parallelise paths.

### Numerical method map
| Method | Idea | Typical products |
|---|---|---|
| Closed form | analytic under flat vol | Reiner–Rubinstein barrier, geometric Asian, Margrabe, digital |
| [[static-replication]] | build from vanillas | digitals, var swaps, any European |
| [[pde-finite-difference]] | solve pricing PDE on a grid | single-asset barriers, American, local vol |
| **Monte Carlo** | simulate paths | autocallables, baskets, cliquets |
