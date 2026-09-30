---
id: greeks-sensitivities
title: "Greeks"
type: topic
domain: black-scholes
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes]
---
# Greeks

The Greeks are the partial derivatives of an option's value with respect to its inputs. This chapter gives the Black–Scholes first-order Greeks and the local P&L expansion built from them, the second-order cross-Greeks that matter when spot and vol move together, and the units and bump-and-reprice conventions used in practice.

**Prerequisites:** [[black-scholes-formula]], [[taylor-expansions]].

**Leads to:** [[delta-hedging]], [[gamma-theta-pnl]], [[sticky-strike-vs-sticky-moneyness]], [[scenario-risk-grids]].

**Sections:** [[greeks]] · [[second-order-greeks]] · [[greeks-conventions-bumping]]

<a id="greeks"></a>

## The Greeks (Δ, Γ, 𝒱, Θ, Rho)
<!-- section: greeks | prerequisites: [black-scholes-formula] | related: [delta-hedging, gamma-theta-pnl, second-order-greeks, greeks-conventions-bumping, delta-vs-itm-probability, sticky-strike-vs-sticky-moneyness, taylor-expansions] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [delta, gamma, vega, theta, rho] -->

Delta and gamma measure sensitivity to the spot, vega to volatility, theta to the passage of time and rho to the interest rate. Together they give a Taylor expansion of the option's P&L.

### Formulas
$$\Delta_C=e^{-q\tau}N(d_1),\qquad \Delta_P=e^{-q\tau}\big(N(d_1)-1\big),\qquad \Gamma=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt\tau},\qquad \mathcal V=Se^{-q\tau}\phi(d_1)\sqrt\tau$$
$$\Theta_C=-\frac{Se^{-q\tau}\phi(d_1)\,\sigma}{2\sqrt\tau}+qSe^{-q\tau}N(d_1)-rKe^{-r\tau}N(d_2),\qquad \mathrm{Rho}_C=\tau Ke^{-r\tau}N(d_2)$$

**Variables:**

- $\Delta_C,\Delta_P$ call and put delta, $\partial V/\partial S$
- $\Gamma$ gamma, $\partial^2V/\partial S^2$ (the same for call and put)
- $\mathcal V$ vega, $\partial V/\partial\sigma$ (the same for call and put)
- $\Theta_C$ call theta, $\partial V/\partial t$ (per year)
- $\mathrm{Rho}_C$ call rho, $\partial V/\partial r$
- $\phi$ standard normal pdf; $N$ standard normal CDF
- $S,K,\tau,r,q,\sigma,d_1,d_2$ as in [[black-scholes-formula]]

Equivalently, since $Se^{-q\tau}=DF$, $\mathcal V=DF\phi(d_1)\sqrt\tau$ in forward notation ([[black-76]]).

### Worked example ($S=K=100,\ T=1,\ r=q=0,\ \sigma=20\%$)
$\Delta=N(0.1)=0.54$; $\Gamma=\phi(0.1)/(100\times0.2)=0.397/20=0.0199$; vega = 39.7 per 100% vol = 0.397 per vol point.

### Profiles
- $\Gamma$ peaks near ATM and grows as expiry approaches (ATM $\Gamma\sim1/\sqrt T$) → short-dated books are gamma-heavy.
- Vega peaks near ATM and grows with $\sqrt T$ → long-dated books are vega-heavy.
- Long vanilla: $\Gamma,\mathcal V>0$; $\Theta$ usually < 0 (not always for puts or with dividends).

### Local P&L
$$\Delta V\approx\Delta\,\delta S+\tfrac12\Gamma\,(\delta S)^2+\mathcal V\,\delta\sigma+\Theta\,\delta t+\mathrm{Rho}\,\delta r$$

**Variables:**

- $\Delta V$ change in option value
- $\delta S,\delta\sigma,\delta t,\delta r$ changes in spot, volatility, time and rate

Example: $\Delta$ = 0.5, $\Gamma$ = 0.02, stock +2 → $0.5\times2+\tfrac12\times0.02\times4\approx1.04$. A long call can lose while the stock rises (theta, vol crush).

### Connections
- **Builds on:** [[black-scholes-formula]]; the P&L expansion is a Taylor expansion ([[taylor-expansions]]).
- **Used by:** [[delta-hedging]], [[gamma-theta-pnl]], [[second-order-greeks]]; units and bumps in [[greeks-conventions-bumping]].
- **Surface-aware delta:** [[sticky-strike-vs-sticky-moneyness]]. **Probability reading of $N(d_1)$:** [[delta-vs-itm-probability]].

<a id="second-order-greeks"></a>

## Vanna, Volga & Vanna–Volga
<!-- section: second-order-greeks | prerequisites: [greeks] | related: [fx-vol-conventions, barrier-options, sticky-strike-vs-sticky-moneyness] | sources: [src-rbc-quantdev-prep] | tags: [vanna, volga, cross-greeks] -->

Vanna and volga are the second-order sensitivities involving volatility. They matter whenever spot and vol move together, and they underlie the vanna–volga smile-pricing method.

### Formulas
$$\text{Vanna}=\frac{\partial\Delta}{\partial\sigma}=\frac{\partial\mathcal V}{\partial S},\qquad \text{Volga}=\frac{\partial\mathcal V}{\partial\sigma}$$

**Variables:**

- $\Delta$ delta
- $\mathcal V$ vega
- $\sigma$ volatility
- $S$ spot

### Key points
- They matter when spot and vol move together (equities: spot ↓, vol ↑) and for exotic / barrier books ([[barrier-options]]).
- **Vanna–volga:** a quick smile-adjustment pricing method; the FX market standard for interpolating across delta (not arbitrage-free) ([[fx-vol-conventions]]).

### Connections
- **Builds on:** [[greeks]].

<a id="greeks-conventions-bumping"></a>

## Greek Units, Conventions & Bump-and-Reprice
<!-- section: greeks-conventions-bumping | prerequisites: [greeks] | related: [price-reconciliation, sticky-strike-vs-sticky-moneyness, monte-carlo-pricing] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [finite-difference, cash-greeks, conventions] -->

Analytic Greeks are per unit of the input; desks report them in cash units per market move, and exotic books compute them by finite differences. Both choices must be stated explicitly.

### Units (be explicit in an app)
- Delta in shares and **dollar delta** $=\Delta\cdot S\cdot\text{qty}$; gamma as dollar gamma per 1% move ($\tfrac12\Gamma S^2(1\%)^2$, or $\Gamma S\cdot\text{qty}$ per 1% as the change in delta).
- Vega per 1 vol point (analytic vega × 0.01); theta per calendar or business day; rho per 1 bp.
- Mismatched conventions between the app and the risk system are a classic "numbers don't match" ticket ([[price-reconciliation]]).

Here qty is the position size.

### Bump-and-reprice
$$\Delta\approx\frac{V(S+\delta S)-V(S-\delta S)}{2\,\delta S},\qquad \Gamma\approx\frac{V(S+\delta S)-2V(S)+V(S-\delta S)}{(\delta S)^2}$$

**Variables:**

- $V(\cdot)$ pricer evaluated at a bumped spot
- $\delta S$ bump size (~1% of spot)

### Key points
- Too small a bump → round-off / Monte Carlo noise; too large → truncation error.
- Desk "cash" Greeks bump the whole surface → the surface dynamics must be defined (sticky strike vs sticky delta, [[sticky-strike-vs-sticky-moneyness]]).

### Connections
- **Builds on:** [[greeks]].
- **Related:** [[price-reconciliation]], [[monte-carlo-pricing]] (AAD as the alternative to bumping).
