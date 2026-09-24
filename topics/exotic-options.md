---
id: exotic-options
title: "Exotic Options"
type: topic
domain: pricing
sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep]
---
# Exotic Options

**Sections:** [[digital-options]] · [[barrier-options]] · [[asian-options]] · [[variance-swaps]] · [[cliquets-forward-start]] · [[quanto-options]]

<a id="digital-options"></a>

## Digital (Binary) Options & the Skew Adjustment
<!-- section: digital-options | prerequisites: [black-scholes-formula, breeden-litzenberger, volatility-skew] | related: [call-spread-overhedge, delta-vs-itm-probability, autocallables, static-replication] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [digital, binary, skew-adjustment, chain-rule] -->

### Flat-vol prices
$$\text{CoN}=e^{-rT}N(d_2),\qquad \text{AoN}=Se^{-qT}N(d_1),\qquad C_{vanilla}=\text{AoN}-K\cdot\text{CoN}$$

**Variables:**

- CoN pays 1 if $S_T>K$
- AoN pays $S_T$ if $S_T>K$
- others as in BS. Example $S=K=100,T=1,r=q=0,\sigma=20\%$: CoN $=N(-0.1)=0.4602$

### With a smile — chain rule
Digital = limit of a tight call spread: $\frac{C(K-\varepsilon)-C(K+\varepsilon)}{2\varepsilon}\to-\frac{dC(K,\sigma(K))}{dK}$. Because σ depends on K:
$$D(K)=-\frac{\partial C_{BS}}{\partial K}-\frac{\partial C_{BS}}{\partial\sigma}\frac{\partial\sigma}{\partial K}=\underbrace{e^{-rT}N(d_2)}_{\text{flat-vol}}\ \underbrace{-\ \mathcal V_{BS}(K)\,\frac{\partial\sigma}{\partial K}}_{\text{skew term}}$$

**Variables:**

- $\mathcal V_{BS}=S_0e^{-qT}\sqrt T\,n(d_1)>0$ vega at $K$
- $\partial\sigma/\partial K$ smile slope

### Sign analysis (equity, $\partial\sigma/\partial K<0$)
- Skew term > 0 ⇒ **digital call dearer** than $e^{-rT}N(d_2)$; digital put $e^{-rT}N(-d_2)+\mathcal V\,\partial\sigma/\partial K$ **cheaper**.
- ATM example: flat 0.508 → surface 0.644 (+27%). Digitals trade off the **slope** of the smile, not its level.
- **Call-spread intuition:** buy $K-\varepsilon$ at higher IV, sell $K+\varepsilon$ at lower IV → net cost inflated.

### Structured payout ratio Q
Option budget $C(K)$ funds $Q$ digitals: $Q=\frac{C(K)}{D(K)}=\frac{C_{BS}(K,\sigma(K))}{e^{-rT}N(d_2)-\mathcal V\,\partial\sigma/\partial K}<Q_{BS\text{-flat}}$. Ignoring skew ⇒ over-promise $Q$ and lose at inception.

**Three pricing tiers:** ① analytic skew-adjusted, ② discrete call spread with market vols at each strike, ③ dynamic smile model (Dupire, SABR/Heston) via PDE/MC.

### Connections
- **Derived from:** [[breeden-litzenberger]] + [[volatility-skew]]. **Hedged by:** [[call-spread-overhedge]].
- **Inside:** [[autocallables]] (coupon & autocall digitals). **Probability link:** [[delta-vs-itm-probability]].

<a id="barrier-options"></a>

## Barrier Options (knock-in/out)
<!-- section: barrier-options | prerequisites: [black-scholes-formula, volatility-surface] | related: [local-volatility-dupire, local-stochastic-volatility, monte-carlo-pricing, pde-finite-difference, autocallables, call-spread-overhedge, second-order-greeks] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [barrier, knock-out, bgk, reverse-barrier] -->

### In–out parity & closed form ($H\le K$, continuous monitoring)
$$C_{DO}=C_{vanilla}-C_{DI},\qquad C_{DI}=Se^{-qT}\Big(\frac HS\Big)^{2\lambda}N(y)-Ke^{-rT}\Big(\frac HS\Big)^{2\lambda-2}N(y-\sigma\sqrt T)$$
$$\lambda=\frac{r-q+\sigma^2/2}{\sigma^2},\qquad y=\frac{\ln(H^2/(SK))}{\sigma\sqrt T}+\lambda\sigma\sqrt T$$

**Variables:**

- $H$ barrier
- $C_{DI}$ down-and-in call
- others as BS. Example $S=K=100,H=90,T=1,r=q=0,\sigma=20\%$: vanilla 7.966, DI 1.498, DO 6.467

### Discrete monitoring — BGK correction
Shift barrier $H\to He^{\pm0.5826\sigma\sqrt{\Delta t}}$ (away from spot). Daily monitoring MC: 6.730 ± 0.029; BGK 6.669; continuous formula understates by ~4%. Price the frequency on the term sheet.

### No single "right" vol
3M DO call, K 5000, H 4500: knock-out discount 0.89 at ATM vol vs 9.03 at barrier-level vol — **10×**. Value depends on vol near the barrier and how the smile moves → local vol / LSV.

### Greeks near the barrier
- DO call near H: large Δ, Γ flips sign, vega can turn negative.
- **Reverse knock-out (up-and-out call):** barrier ITM; payoff largest right before it dies → Δ flips large +/−, huge Γ/vega, gap risk. Desks apply **barrier shifts / reserves**.

### Numerics
PDE with barrier as boundary (align nodes); MC with Brownian-bridge crossing probability.

### Connections
- **Inside:** [[autocallables]] (down-and-in put). **Models:** [[local-volatility-dupire]], [[local-stochastic-volatility]]. **Overhedge cousin:** [[call-spread-overhedge]].

<a id="asian-options"></a>

## Asian Options
<!-- section: asian-options | prerequisites: [black-scholes-formula] | related: [monte-carlo-pricing] | sources: [src-vol-surface-exotics-notes] | tags: [asian, averaging] -->

Payoff on the average price → **averaging kills vol** → cheaper.
- 3M ATM call, daily averaging, 16.49% vol, 200k paths: Asian 102.99 vs vanilla 178.98 (ratio 0.58).
- Continuous averaging from inception: effective vol ≈ $\sigma/\sqrt3$ ($1/\sqrt3=0.577$) — geometric-average approximation (inferred in source).
- Geometric Asian has closed form → MC **control variate** for arithmetic.

<a id="variance-swaps"></a>

## Variance Swaps & the VIX Strip
<!-- section: variance-swaps | prerequisites: [static-replication, otm-stitching] | related: [gamma-theta-pnl, volatility-skew, realized-volatility, jump-diffusion] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [variance-swap, vix, replication] -->

Payoff: notional × (realised variance − $K_{var}$).
$$K_{var}^2=\frac{2}{TD}\Big[\int_0^F\frac{P(K)}{K^2}dK+\int_F^\infty\frac{C(K)}{K^2}dK\Big]$$

**Variables:**

- $K_{var}$ fair variance strike (quoted as vol)
- $P,C$ OTM put/call prices from the surface
- $1/K^2$ weights
- $F$ forward
- $D$ discount factor
- $T$ tenor

- Replicated statically by the OTM strip + delta-hedged forward — **same construction as VIX**.
- Low strikes weigh most and are expensive under skew → **var strike > ATM vol** (19.72% vs 16.49% in example).
- Replication error: jumps, strike truncation. Vol swaps / VIX options need vol-of-vol.

### Connections
- **Removes path-dependence of:** [[gamma-theta-pnl]]. **Priced by:** [[volatility-skew]].

<a id="cliquets-forward-start"></a>

## Cliquets & Forward-Start Options
<!-- section: cliquets-forward-start | prerequisites: [forward-smile] | related: [heston-model, local-stochastic-volatility, vol-term-structure] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [cliquet, forward-start] -->

Cliquet = sum of capped/floored periodic returns; forward-start = option whose strike is set at a future date.
- Value depends on the **forward smile** → local vol underprices; use SV / LSV.
- "Model choice changes price materially".

<a id="quanto-options"></a>

## Quanto Options
<!-- section: quanto-options | prerequisites: [risk-neutral-pricing] | related: [worst-of-correlation, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [quanto, fx, correlation] -->

Payoff on a foreign underlying paid in domestic currency at a **fixed** FX rate.
$$\text{drift adjustment}=-\rho\,\sigma_S\,\sigma_{FX}$$

**Variables:**

- ρ stock/FX correlation
- $\sigma_S$ stock vol
- $\sigma_{FX}$ FX vol

Extra market data: FX vol and stock–FX correlation.
