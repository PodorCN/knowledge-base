---
id: black-scholes
title: "Black–Scholes"
type: topic
domain: pricing
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes]
---
# Black–Scholes

**Sections:** [[black-scholes-pde]] · [[black-scholes-formula]] · [[greeks]] · [[second-order-greeks]] · [[greeks-conventions-bumping]] · [[delta-vs-itm-probability]] · [[black-76]] · [[american-early-exercise]]

<a id="black-scholes-pde"></a>

## Black–Scholes PDE (derivation)
<!-- section: black-scholes-pde | prerequisites: [ito-lemma, binomial-replication] | related: [black-scholes-formula, gamma-theta-pnl, pde-finite-difference, delta-hedging] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [pde, delta-hedging, replication] -->

$$\frac{\partial V}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}+(r-q)S\frac{\partial V}{\partial S}-rV=0,\qquad V(T,S)=h(S)$$

**Variables:**

- $V(S,t)$ option value
- $\sigma$ vol
- $r$ rate
- $q$ dividend yield
- $h$ payoff

### Derivation (4 steps)
1. Itô on $V(S,t)$: $dV=(V_t+\mu SV_S+\tfrac12\sigma^2S^2V_{SS})dt+\sigma SV_SdW$.
2. Hold $\Delta=V_S$ shares → the $dW$ term cancels.
3. Hedged portfolio is riskless ⇒ must earn $r$ (else arbitrage).
4. μ cancels → PDE contains only $r,\sigma$, contract terms.

**Why no μ:** dynamic replication prices the risk away; your stock forecast is irrelevant.

### Connections
- **Rearranged as:** $\Theta+\tfrac12\Gamma\sigma^2S^2+rSV_S-rV=0$ → [[gamma-theta-pnl]].
- **Solved numerically by:** [[pde-finite-difference]].

<a id="black-scholes-formula"></a>

## Black–Scholes Formula
<!-- section: black-scholes-formula | prerequisites: [geometric-brownian-motion, risk-neutral-pricing] | related: [black-scholes-pde, greeks, implied-volatility, black-76, put-call-parity, delta-vs-itm-probability] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [black-scholes, bsm] -->

$$C=Se^{-q\tau}N(d_1)-Ke^{-r\tau}N(d_2),\qquad P=Ke^{-r\tau}N(-d_2)-Se^{-q\tau}N(-d_1)$$
$$d_1=\frac{\ln(S/K)+(r-q+\tfrac12\sigma^2)\tau}{\sigma\sqrt\tau},\qquad d_2=d_1-\sigma\sqrt\tau$$

**Variables:**

- $S$ spot
- $K$ strike
- $\tau=T-t$ years to expiry
- $r$ rate
- $q$ dividend yield (or borrow-adjusted carry)
- $\sigma$ volatility
- $N$ standard normal CDF

### Reference numbers
$S=K=100,T=1,r=q=0,\sigma=20\%$: $d_1=0.1,d_2=-0.1$, $C=100(0.5398-0.4602)=7.97$.

**ATM shortcut:** $C_{ATM}\approx0.4\,S\sigma\sqrt T$ ($0.4\approx1/\sqrt{2\pi}$) → 8.0.

### Assumptions and where they break (equities)
GBM with constant σ, frictionless continuous hedging, constant r, no jumps, known dividends → broken by skew, jumps/gaps, discrete dividends, borrow, costs. BS survives as a **quoting language** ([[implied-volatility]]).

### Connections
- **Derived from:** [[black-scholes-pde]] or [[risk-neutral-pricing]]. **Sensitivities:** [[greeks]]. **Forward form:** [[black-76]].
- **Decomposition:** $C=\text{AoN}-K\cdot\text{CoN}$ → [[digital-options]].

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

<a id="delta-vs-itm-probability"></a>

## Delta vs Probability of Finishing ITM (N(d1) vs N(d2))
<!-- section: delta-vs-itm-probability | prerequisites: [greeks, risk-neutral-pricing] | related: [digital-options, lognormal-distribution] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [delta, probability, measure] -->

- $N(d_2)$ = **risk-neutral** probability $S_T>K$ (= undiscounted cash-or-nothing digital).
- $N(d_1)$ = that probability under the **share measure** (stock as numeraire); call delta $=e^{-q\tau}N(d_1)$.
- Neither is the physical probability. Close for short-dated ATM, diverge for long-dated / high vol.
- **ATM-forward call delta > 0.5:** at $K=F$, $d_1=\tfrac12\sigma\sqrt T>0$. Lognormal is right-skewed: median < forward.

### Connections
- **Why it matters:** [[digital-options]] are priced off $N(d_2)$; skew adjusts it. Built on [[lognormal-distribution]].

<a id="black-76"></a>

## Black-76 (forward-based Black formula)
<!-- section: black-76 | prerequisites: [black-scholes-formula, forward-pricing] | related: [implied-forward-regression, swaptions, sabr] | sources: [src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep] | tags: [black-76, forward, swaption] -->

$$C=D\,[F\,N(d_1)-K\,N(d_2)],\qquad d_{1,2}=\frac{\ln(F/K)\pm\tfrac12\sigma^2T}{\sigma\sqrt T}$$

**Variables:**

- $D$ discount factor
- $F$ forward
- $K$ strike
- σ Black vol
- $T$ expiry

- Surface practice: get $D,F$ from [[implied-forward-regression]], then invert Black-76 → no dividend/rate guesses needed.
- Swaptions: replace $D$ by annuity $A$ and $F$ by forward swap rate → [[swaptions]]. Rates often quoted in **normal (Bachelier)** vol.

<a id="american-early-exercise"></a>

## American Options, Early Exercise & De-Americanisation
<!-- section: american-early-exercise | prerequisites: [option-payoffs-moneyness, forward-pricing] | related: [first-step-analysis, pde-finite-difference, vol-surface-construction, put-call-parity] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-vol-surface-exotics-notes] | tags: [american, early-exercise, dividends] -->

- **American call, no dividends, r ≥ 0:** never exercise early (lose optionality, pay K early).
- **With dividends:** exercise only just before an ex-date, if dividend > time value lost (≈ $D>K(1-e^{-r\Delta t})$ + remaining optionality).
- **American put:** early exercise when deep ITM (receive K earlier, earn interest). Borrow costs matter.
- Parity becomes an inequality.

### De-Americanisation (for vol surfaces)
Single-stock listed options are American → convert prices to European-equivalents (tree / PDE) **before** inverting to IV, or invert the American pricer directly. Surface always built on European-equivalent vols; mixing is a common consistency bug.

### Connections
- **Backward induction:** [[first-step-analysis]], [[pde-finite-difference]], Longstaff–Schwartz in [[monte-carlo-pricing]].
- **Feeds:** [[vol-surface-construction]] (single-stock case).
