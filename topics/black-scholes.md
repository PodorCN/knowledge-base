---
id: black-scholes
title: "Black–Scholes"
type: topic
domain: pricing
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes]
---
# Black–Scholes

**Sections:** [[black-scholes-pde]] · [[black-scholes-formula]] · [[black-76]] · [[delta-vs-itm-probability]] · [[american-early-exercise]]

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

<a id="delta-vs-itm-probability"></a>

## Delta vs Probability of Finishing ITM (N(d1) vs N(d2))
<!-- section: delta-vs-itm-probability | prerequisites: [greeks, risk-neutral-pricing] | related: [digital-options, lognormal-distribution] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [delta, probability, measure] -->

- $N(d_2)$ = **risk-neutral** probability $S_T>K$ (= undiscounted cash-or-nothing digital).
- $N(d_1)$ = that probability under the **share measure** (stock as numeraire); call delta $=e^{-q\tau}N(d_1)$.
- Neither is the physical probability. Close for short-dated ATM, diverge for long-dated / high vol.
- **ATM-forward call delta > 0.5:** at $K=F$, $d_1=\tfrac12\sigma\sqrt T>0$. Lognormal is right-skewed: median < forward.

### Connections
- **Why it matters:** [[digital-options]] are priced off $N(d_2)$; skew adjusts it. Built on [[lognormal-distribution]].

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
