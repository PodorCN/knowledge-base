---
id: greeks-sensitivities
title: "Greeks & Sensitivities"
type: topic
domain: risk-management
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook]
---
# Greeks & Sensitivities

**Sections:** [[greeks]] · [[second-order-greeks]] · [[greeks-conventions-bumping]]

<a id="greeks"></a>

## The Greeks (Δ, Γ, vega, Θ, ρ)
<!-- section: greeks | prerequisites: [black-scholes-formula] | related: [delta-hedging, gamma-theta-pnl, second-order-greeks, greeks-conventions-bumping, delta-vs-itm-probability, sticky-strike-vs-sticky-moneyness] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [delta, gamma, vega, theta, rho] -->

$$\Delta_C=e^{-q\tau}N(d_1),\quad \Delta_P=e^{-q\tau}(N(d_1)-1),\quad \Gamma=\frac{e^{-q\tau}n(d_1)}{S\sigma\sqrt\tau},\quad \mathcal V=Se^{-q\tau}n(d_1)\sqrt\tau$$
$$\Theta_C=-\frac{Se^{-q\tau}n(d_1)\sigma}{2\sqrt\tau}+qSe^{-q\tau}N(d_1)-rKe^{-r\tau}N(d_2),\qquad \rho_C=\tau Ke^{-r\tau}N(d_2)$$

**Variables:**

- $n$ standard normal pdf
- others as in [[black-scholes-formula]]. Γ and vega identical for call and put

### Reference ($S=K=100,T=1,r=q=0,\sigma=20\%$)
Δ = 0.54, Γ = 0.397/20 = 0.0199, vega = 39.7 per 100% vol = 0.397 per vol point.

### Profiles
- Γ peaks near ATM, grows as expiry approaches (ATM Γ ~ $1/\sqrt T$) → short-dated = gamma-heavy.
- Vega peaks near ATM, grows with $\sqrt T$ → long-dated = vega-heavy.
- Long vanilla: Γ, vega > 0; Θ usually < 0 (not always for puts/with dividends).

### Local P&L
$$\Delta V\approx\Delta\,\delta S+\tfrac12\Gamma(\delta S)^2+\mathcal V\,\delta\sigma+\Theta\,\delta t+\rho\,\delta r$$
Δ = 0.5, Γ = 0.02, stock +2 → ≈ 1.04. A long call can lose while the stock rises (Θ, vol crush).

### Connections
- [[delta-hedging]], [[gamma-theta-pnl]], [[second-order-greeks]], units & bumps in [[greeks-conventions-bumping]].
- **Surface-aware delta:** [[sticky-strike-vs-sticky-moneyness]].

<a id="second-order-greeks"></a>

## Vanna, Volga & Vanna–Volga
<!-- section: second-order-greeks | prerequisites: [greeks] | related: [fx-vol-conventions, barrier-options, sticky-strike-vs-sticky-moneyness] | sources: [src-rbc-quantdev-prep] | tags: [vanna, volga, cross-greeks] -->

$$\text{Vanna}=\frac{\partial\Delta}{\partial\sigma}=\frac{\partial\mathcal V}{\partial S},\qquad \text{Volga}=\frac{\partial\mathcal V}{\partial\sigma}$$

**Variables:**

- Δ delta
- $\mathcal V$ vega
- σ vol
- $S$ spot

- Matter when spot and vol move together (equities: spot ↓ vol ↑) and for exotic / barrier books.
- **Vanna–volga**: quick smile-adjustment pricing method; FX market standard for interpolating across delta (not arbitrage-free).

<a id="greeks-conventions-bumping"></a>

## Greek Units, Conventions & Bump-and-Reprice
<!-- section: greeks-conventions-bumping | prerequisites: [greeks] | related: [price-reconciliation, sticky-strike-vs-sticky-moneyness, monte-carlo-pricing] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [finite-difference, cash-greeks, conventions] -->

### Units (be explicit in an app)
- Delta in shares and **$ delta** $=\Delta S\cdot qty$; gamma as $ gamma per 1% move ($\tfrac12\Gamma S^2(1\%)^2$ or $\Gamma S\cdot qty$ per 1%).
- Vega per 1 vol point (analytic vega × 0.01); theta per calendar or business day; rho per 1 bp.
- Mismatched conventions between app and risk system = classic "numbers don't match" ticket.

### Bump-and-reprice
$$\Delta\approx\frac{V(S+h)-V(S-h)}{2h},\qquad \Gamma\approx\frac{V(S+h)-2V(S)+V(S-h)}{h^2}$$

**Variables:** $h$ bump size (~1% of spot).
- Too small → round-off / MC noise; too large → truncation error.
- Desk "cash" Greeks bump the whole surface → must define sticky strike vs sticky delta.

### Connections
- [[price-reconciliation]], [[sticky-strike-vs-sticky-moneyness]], [[monte-carlo-pricing]] (AAD alternative).
