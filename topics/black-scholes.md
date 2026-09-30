---
id: black-scholes
title: "Black–Scholes Model"
type: topic
domain: black-scholes
sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-quant-finance-study-notes]
---
# Black–Scholes Model

This chapter prices European options under geometric Brownian motion. It derives the Black–Scholes PDE by dynamic hedging, states the closed-form call and put prices, rewrites them in forward form (Black-76, the form used on vol surfaces), and explains when American options are exercised early.

**Prerequisites:** [[ito-lemma]], [[geometric-brownian-motion]], [[risk-neutral-pricing]], [[binomial-replication]], [[put-call-parity]].

**Leads to:** [[black-scholes-call-derivation]] (the risk-neutral derivation), [[greeks]], [[implied-volatility]].

**Sections:** [[black-scholes-pde]] · [[black-scholes-formula]] · [[black-76]] · [[american-early-exercise]]

Notation for the Black–Scholes track: $S$ spot, $K$ strike, $t$ current time, $T$ expiry, $\tau=T-t$ (formulas written at $t=0$ use $T$), $r$ risk-free rate, $q$ dividend yield, $\sigma$ volatility, $D=e^{-r\tau}$ discount factor, $F=Se^{(r-q)\tau}$ forward, $N(\cdot)$ and $\phi(\cdot)$ the standard normal CDF and pdf.

<a id="black-scholes-pde"></a>

## Black–Scholes PDE (derivation)
<!-- section: black-scholes-pde | prerequisites: [ito-lemma, binomial-replication] | related: [black-scholes-formula, gamma-theta-pnl, pde-finite-difference, delta-hedging] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [pde, delta-hedging, replication] -->

Hedging an option continuously with $\Delta$ shares removes all randomness; a riskless portfolio must earn the risk-free rate, which gives a PDE for the option value that does not involve the stock's expected return.

### Formula
$$\frac{\partial V}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}+(r-q)S\frac{\partial V}{\partial S}-rV=0,\qquad V(S,T)=h(S)$$

**Variables:**

- $V(S,t)$ option value as a function of spot and time
- $S$ spot price
- $\sigma$ volatility
- $r$ risk-free rate
- $q$ dividend yield
- $h$ payoff at expiry $T$

### Derivation (4 steps)
1. Itô on $V(S,t)$ under $dS=\mu S\,dt+\sigma S\,dW$: $dV=(V_t+\mu SV_S+\tfrac12\sigma^2S^2V_{SS})dt+\sigma SV_S\,dW$ ([[ito-lemma]]).
2. Hold $\Delta=V_S$ shares against the option → the $dW$ term cancels.
3. The hedged portfolio is riskless ⇒ it must earn $r$ (otherwise there is an arbitrage).
4. $\mu$ cancels → the PDE contains only $r$, $\sigma$ and the contract terms.

Here $\mu$ is the real-world drift and subscripts denote partial derivatives.

### Key points
- **Why no $\mu$:** dynamic replication prices the risk away; your stock forecast is irrelevant ([[risk-neutral-pricing]]).
- It is the continuous-time limit of [[binomial-replication]].

### Connections
- **Builds on:** [[ito-lemma]], [[binomial-replication]].
- **Rearranged as** $\Theta+\tfrac12\Gamma\sigma^2S^2+(r-q)S\Delta-rV=0$ → [[gamma-theta-pnl]].
- **Solved in closed form:** [[black-scholes-formula]]. **Solved numerically:** [[pde-finite-difference]].

<a id="black-scholes-formula"></a>

## Black–Scholes Formula
<!-- section: black-scholes-formula | prerequisites: [geometric-brownian-motion, risk-neutral-pricing, black-scholes-pde] | related: [greeks, implied-volatility, black-76, put-call-parity, delta-vs-itm-probability, digital-options] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [black-scholes, bsm] -->

Solving the PDE (or evaluating the risk-neutral expectation, [[black-scholes-call-derivation]]) gives closed-form prices for European calls and puts.

### Formulas
$$C=Se^{-q\tau}N(d_1)-Ke^{-r\tau}N(d_2),\qquad P=Ke^{-r\tau}N(-d_2)-Se^{-q\tau}N(-d_1)$$
$$d_1=\frac{\ln(S/K)+(r-q+\tfrac12\sigma^2)\tau}{\sigma\sqrt\tau},\qquad d_2=d_1-\sigma\sqrt\tau$$

**Variables:**

- $C,P$ European call and put prices
- $S$ spot price
- $K$ strike
- $\tau=T-t$ years to expiry
- $r$ risk-free rate
- $q$ dividend yield (or borrow-adjusted carry)
- $\sigma$ volatility
- $N(\cdot)$ standard normal CDF

### Worked example
$S=K=100,\ T=1,\ r=q=0,\ \sigma=20\%$: $d_1=0.1$, $d_2=-0.1$, $C=100\,(0.5398-0.4602)=7.97$.

**ATM shortcut:** $C_{ATM}\approx0.4\,S\sigma\sqrt T$ (with $0.4\approx1/\sqrt{2\pi}$, from $N(d)\approx\tfrac12+d/\sqrt{2\pi}$, [[taylor-expansions]]) → 8.0.

### Assumptions and where they break (equities)
GBM with constant $\sigma$, frictionless continuous hedging, constant $r$, no jumps, known dividends → broken by skew, jumps/gaps, discrete dividends, borrow, costs. BS survives as a **quoting language** ([[implied-volatility]]).

### Key points
- **Decomposition:** $C=\text{AoN}-K\cdot\text{CoN}$ (asset-or-nothing minus $K$ cash-or-nothing digitals) → [[digital-options]].
- Call and put satisfy [[put-call-parity]].

### Connections
- **Derived from:** [[black-scholes-pde]] or [[risk-neutral-pricing]] (step by step in [[black-scholes-call-derivation]]).
- **Sensitivities:** [[greeks]]. **Forward form:** [[black-76]]. **Inverted for:** [[implied-volatility]].

<a id="black-76"></a>

## Black-76 (forward-based Black formula)
<!-- section: black-76 | prerequisites: [black-scholes-formula, forward-pricing] | related: [implied-forward-regression, swaptions, sabr] | sources: [src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep, src-quant-finance-study-notes] | tags: [black-76, forward, swaption] -->

Writing Black–Scholes in terms of the forward and the discount factor removes the need to know $r$ and $q$ separately. This is the form used to build vol surfaces and, with an annuity in place of the discount factor, to price swaptions.

### Formulas
$$C=D\,[F\,N(d_1)-K\,N(d_2)],\qquad P=D\,[K\,N(-d_2)-F\,N(-d_1)],\qquad d_{1,2}=\frac{\ln(F/K)\pm\tfrac12\sigma^2T}{\sigma\sqrt T}$$

**Variables:**

- $D$ discount factor to expiry
- $F$ forward price for expiry $T$
- $K$ strike
- $\sigma$ Black volatility
- $T$ time to expiry

With $D=e^{-rT}$ and $F=Se^{(r-q)T}$ this is identical to [[black-scholes-formula]].

### Key points
- Surface practice: get $D$ and $F$ from [[implied-forward-regression]], then invert Black-76 → no dividend or rate guesses needed.
- Swaptions: replace $D$ by the annuity $A$ and $F$ by the forward swap rate → [[swaptions]]. Rates are often quoted in **normal (Bachelier)** vol ([[sabr]]).

### Connections
- **Builds on:** [[black-scholes-formula]], [[forward-pricing]].
- **Used by:** [[implied-volatility]], [[implied-forward-regression]], [[swaptions]].

<a id="american-early-exercise"></a>

## American Options, Early Exercise & De-Americanisation
<!-- section: american-early-exercise | prerequisites: [option-payoffs-moneyness, forward-pricing, first-step-analysis] | related: [pde-finite-difference, vol-surface-construction, put-call-parity, monte-carlo-pricing] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-vol-surface-exotics-notes] | tags: [american, early-exercise, dividends] -->

An American option may be exercised at any time. Exercising early is optimal only when the payoff now exceeds the value of continuing — the same backward-induction rule as in [[first-step-analysis]].

### Key points
- **American call, no dividends, $r\ge0$:** never exercise early (you lose optionality and pay $K$ early).
- **With dividends:** exercise only just before an ex-date, if the dividend exceeds the time value lost (≈ $\mathrm{Div}>K(1-e^{-r\Delta t})$ + remaining optionality, with $\mathrm{Div}$ the cash dividend and $\Delta t$ the time from this ex-date to the next ex-date or to expiry).
- **American put:** early exercise when deep ITM (receive $K$ earlier and earn interest on it). Borrow costs matter.
- Put–call parity becomes an inequality ([[put-call-parity]]).

### De-Americanisation (for vol surfaces)
Single-stock listed options are American → convert prices to European equivalents (tree / PDE) **before** inverting to implied vol, or invert the American pricer directly. The surface is always built on European-equivalent vols; mixing the two is a common consistency bug.

### Connections
- **Backward induction:** [[first-step-analysis]], [[pde-finite-difference]], Longstaff–Schwartz in [[monte-carlo-pricing]], binomial tree in [[csharp-pricing-library-example]].
- **Feeds:** [[vol-surface-construction]] (single-stock case).
