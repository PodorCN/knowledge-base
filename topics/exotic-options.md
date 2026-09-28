---
id: exotic-options
title: "Exotic Options"
type: topic
domain: pricing
sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-finance-study-notes]
---
# Exotic Options

**Sections:** [[digital-options]] · [[barrier-options]] · [[asian-options]] · [[variance-swaps]] · [[cliquets-forward-start]] · [[quanto-options]]

<a id="digital-options"></a>

## Digital (Binary) Options & the Skew Adjustment
<!-- section: digital-options | prerequisites: [black-scholes-formula, breeden-litzenberger, volatility-skew] | related: [call-spread-overhedge, delta-vs-itm-probability, autocallables, static-replication, sticky-strike-vs-sticky-moneyness] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-finance-study-notes] | tags: [digital, binary, skew-adjustment, chain-rule] -->

### Flat-vol prices
$$\text{CoN}=e^{-rT}N(d_2),\qquad \text{AoN}=Se^{-qT}N(d_1),\qquad C_{vanilla}=\text{AoN}-K\cdot\text{CoN}$$

**Variables:**

- CoN pays 1 if $S_T>K$
- AoN pays $S_T$ if $S_T>K$
- others as in BS. Example $S=K=100,T=1,r=q=0,\sigma=20\%$: CoN $=N(-0.1)=0.4602$

### Call-spread replication
Buy $\tfrac1\varepsilon$ calls at $K$, sell $\tfrac1\varepsilon$ calls at $K+\varepsilon$:

| $S_T$ | Payoff |
|---|---|
| $\le K$ | 0 |
| $K$ to $K+\varepsilon$ | $(S_T-K)/\varepsilon$ |
| $\ge K+\varepsilon$ | 1 |

$$C_{dig}(K)=\lim_{\varepsilon\to0}\frac{C(K)-C(K+\varepsilon)}{\varepsilon}=-\frac{dC_{mkt}}{dK}$$

**Variables:**

- $\varepsilon$ spread width
- $C_{mkt}(K)$ market vanilla call price at $K$

### With a smile — chain rule
Digital = limit of a tight call spread: $\frac{C(K-\varepsilon)-C(K+\varepsilon)}{2\varepsilon}\to-\frac{dC(K,\sigma(K))}{dK}$. Because σ depends on K:

$$D(K)=-\frac{\partial C_{BS}}{\partial K}-\frac{\partial C_{BS}}{\partial\sigma}\frac{\partial\sigma}{\partial K}=\underbrace{e^{-rT}N(d_2)}_{\text{flat-vol}}\ \underbrace{-\ \mathcal V_{BS}(K)\,\frac{\partial\sigma}{\partial K}}_{\text{skew term}}$$

**Variables:**

- $\mathcal V_{BS}=S_0e^{-qT}\sqrt T\,n(d_1)>0$ vega at $K$
- $\partial\sigma/\partial K$ smile slope

### Forward-form derivation ($\partial C_{BS}/\partial K$ at fixed σ)
$$\frac{\partial C_{BS}}{\partial K}=D\Big[F\phi(d_1)\tfrac{\partial d_1}{\partial K}-N(d_2)-K\phi(d_2)\tfrac{\partial d_2}{\partial K}\Big],\qquad \tfrac{\partial d_1}{\partial K}=\tfrac{\partial d_2}{\partial K}=-\tfrac{1}{K\sigma\sqrt T}$$

**Key identity** $F\phi(d_1)=K\phi(d_2)$:

$$\frac{\phi(d_2)}{\phi(d_1)}=e^{(d_1^2-d_2^2)/2}=e^{d_1\sigma\sqrt T-\sigma^2T/2}=e^{\ln(F/K)}=\frac FK$$

→ the first and third terms cancel: $\dfrac{\partial C_{BS}}{\partial K}=-D\,N(d_2)$, so

$$C_{dig}(K)=D\,N(d_2)-\text{Vega}(K)\cdot\frac{d\sigma}{dK},\qquad \text{Vega}=DF\phi(d_1)\sqrt T$$

**Variables:**

- $D$ discount factor, $F$ forward
- $D\,N(d_2)$ flat-vol BS digital
- $d\sigma/dK$ smile slope at $K$
- $\phi$ standard normal pdf

### Sign analysis (equity, $\partial\sigma/\partial K<0$)
- Skew term > 0 ⇒ **digital call dearer** than $e^{-rT}N(d_2)$; digital put $e^{-rT}N(-d_2)+\mathcal V\,\partial\sigma/\partial K$ **cheaper**.
- ATM example: flat 0.508 → surface 0.644 (+27%). Digitals trade off the **slope** of the smile, not its level.
- **Call-spread intuition:** buy $K-\varepsilon$ at higher IV, sell $K+\varepsilon$ at lower IV → net cost inflated.

| Skew | $d\sigma/dK$ | Digital call | Digital put |
|---|---|---|---|
| Equity put skew | < 0 | **More expensive** than BS | Cheaper |
| Upside skew (some commodities) | > 0 | Cheaper | More expensive |

(Digital call + digital put $=D$ → adjustments are equal and opposite.)

### Numbers (computed)
$D=0.96,F=102,T=1,K=100,\sigma=20.73\%,d\sigma/dK=-0.001$; $d_1=0.1992,\ d_2=-0.0081$; check $F\phi(d_1)=39.893=K\phi(d_2)$ ✅

| Term | Value |
|---|---|
| $D\,N(d_2)=0.96\times0.4968$ | 0.4769 |
| $-\text{Vega}\cdot d\sigma/dK=-38.30\times(-0.001)$ | +0.0383 |
| **Digital price** | **0.5152** |

Check with a 99/101 call spread ÷ 2:

| Strike | σ (skew) | Call (skew) | Call (flat 20.73%) |
|---|---|---|---|
| 99 | 20.83% | 9.5247 | 9.4868 |
| 101 | 20.63% | 8.4944 | 8.5330 |
| **(C₉₉−C₁₀₁)/2** | | **0.5152** | **0.4769** |

A skew of 1 vol point per 10 strikes adds ~8% to the digital: the **slope is a first-order input**.

### Why vanillas have no such adjustment
1. **IV is defined to price that vanilla correctly**: nothing left to correct.
2. **What each product needs from the smile:**

| Product | Relation to vanilla prices | Needs from smile |
|---|---|---|
| Vanilla $C(K)$ | price itself | **level** $\sigma(K)$ |
| Digital $-\partial C/\partial K$ | 1st derivative | level + **slope** $\sigma'(K)$ |
| Butterfly / density $\partial^2C/\partial K^2$ | 2nd derivative | level + slope + **curvature** $\sigma''(K)$ |

3. $D\,N(d_2)$ silently assumes a flat smile (自己推理 framing).
4. For a vanilla the smile effect shows up in **delta**: $\Delta_{total}=\Delta_{BS}+\text{Vega}\cdot\partial\sigma/\partial S$ (smile-adjusted delta; sticky-strike vs sticky-delta, [[sticky-strike-vs-sticky-moneyness]]) (自己推理 link).

### Link to distribution skewness
$C_{dig}(K)=D\cdot\mathbb Q(S_T>K)$ ($\mathbb Q$: risk-neutral measure): a point on the risk-neutral **CDF**; one more derivative gives the density ([[breeden-litzenberger]]). Equity put skew ↔ negative risk-neutral skewness (fat left tail) → near ATM, $\mathbb Q(S_T>K)$ is higher than $N(d_2)$.

### Trading points
- Hedge with a call spread, **overhedged** (always pays ≥ 1); the width is a risk choice ([[call-spread-overhedge]]).
- **Pin risk:** delta/gamma blow up near $K$ at expiry.
- The price depends on **smile interpolation**: two surfaces fitting vanillas equally well can give different digital prices (Wystup & Van Mulken, *Slope Matters*).

**One-liner:** "A digital is −dC/dK, and C = C_BS(K, σ(K)) depends on K through σ too, so the chain rule adds −Vega·σ′(K). A vanilla uses its own strike's IV, defined to fit its price, so it needs only the level, not the slope."

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

- **Cliquet:** sum of capped/floored periodic returns.
- **Forward-start:** option whose strike is set at a future date.
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
