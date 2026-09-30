---
id: exotic-options
title: "Exotic Options"
type: topic
domain: pricing
sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-finance-study-notes]
---
# Exotic Options

Exotic options are priced with everything built so far: Black–Scholes, the volatility surface and the models on top of it. This chapter goes from the products that depend only on the surface (digitals, variance swaps) to those that also depend on its dynamics (barriers, Asians, cliquets) and on cross-asset correlation (quantos). For each product the question is the same: which feature of the surface or model drives the price?

**Prerequisites:** [[black-scholes-formula]], [[greeks]], [[volatility-surface]], [[volatility-skew]], [[breeden-litzenberger]], [[forward-smile]], [[monte-carlo-pricing]].

**Leads to:** [[autocallables]] and the other structured products, [[call-spread-overhedge]] (hedging digitals).

**Sections:** [[digital-options]] · [[barrier-options]] · [[asian-options]] · [[variance-swaps]] · [[cliquets-forward-start]] · [[quanto-options]]

<a id="digital-options"></a>

## Digital (Binary) Options & the Skew Adjustment
<!-- section: digital-options | prerequisites: [black-scholes-formula, breeden-litzenberger, volatility-skew] | related: [call-spread-overhedge, delta-vs-itm-probability, autocallables, static-replication, sticky-strike-vs-sticky-moneyness, payoff-indicator-split] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-finance-study-notes] | tags: [digital, binary, skew-adjustment, chain-rule] -->

A digital pays a fixed amount if the option finishes in the money. It equals minus the strike-derivative of the call price, so with a smile its price depends not only on the level of implied vol at the strike but also on the **slope** of the smile.

### Flat-vol prices
$$\text{CoN}=e^{-rT}N(d_2),\qquad \text{AoN}=Se^{-qT}N(d_1),\qquad C_{\text{vanilla}}=\text{AoN}-K\cdot\text{CoN}$$

**Variables:**

- CoN cash-or-nothing call: pays 1 if $S_T>K$
- AoN asset-or-nothing call: pays $S_T$ if $S_T>K$
- $S,K,T,r,q,d_1,d_2$ as in [[black-scholes-formula]]

Example: $S=K=100,\ T=1,\ r=q=0,\ \sigma=20\%$ → CoN $=N(-0.1)=0.4602$.

### Call-spread replication
Buy $\tfrac1\varepsilon$ calls at $K$ and sell $\tfrac1\varepsilon$ calls at $K+\varepsilon$:

| $S_T$ | Payoff |
|---|---|
| $\le K$ | 0 |
| $K$ to $K+\varepsilon$ | $(S_T-K)/\varepsilon$ |
| $\ge K+\varepsilon$ | 1 |

$$C_{\text{dig}}(K)=\lim_{\varepsilon\to0}\frac{C(K)-C(K+\varepsilon)}{\varepsilon}=-\frac{dC_{mkt}}{dK}$$

**Variables:**

- $\varepsilon$ call-spread width
- $C_{mkt}(K)$ market vanilla call price at strike $K$
- $C_{\text{dig}}(K)$ price of the digital (cash-or-nothing) call

### With a smile — the chain rule
The market call price is $C_{mkt}(K)=C_{BS}(K,\sigma(K))$: it depends on $K$ directly and through the implied vol $\sigma(K)$. Differentiating:

$$C_{\text{dig}}(K)=-\frac{\partial C_{BS}}{\partial K}-\frac{\partial C_{BS}}{\partial\sigma}\,\frac{\partial\sigma}{\partial K}=\underbrace{D\,N(d_2)}_{\text{flat-vol digital}}\ \underbrace{-\ \mathcal V(K)\,\frac{\partial\sigma}{\partial K}}_{\text{skew term}}$$

**Variables:**

- $C_{BS}(K,\sigma)$ Black–Scholes call price at fixed vol
- $\sigma(K)$ implied vol at strike $K$; $\partial\sigma/\partial K$ smile slope
- $D=e^{-rT}$ discount factor
- $\mathcal V(K)=DF\phi(d_1)\sqrt T=S_0e^{-qT}\sqrt T\,\phi(d_1)>0$ vega at strike $K$
- $F$ forward; $\phi$ standard normal pdf

The first term uses $\partial C_{BS}/\partial K=-D\,N(d_2)$, proved next.

### Proof that $\partial C_{BS}/\partial K=-D\,N(d_2)$ (forward form)
With $C_{BS}=D[F\,N(d_1)-K\,N(d_2)]$ ([[black-76]]):

$$\frac{\partial C_{BS}}{\partial K}=D\Big[F\phi(d_1)\frac{\partial d_1}{\partial K}-N(d_2)-K\phi(d_2)\frac{\partial d_2}{\partial K}\Big],\qquad \frac{\partial d_1}{\partial K}=\frac{\partial d_2}{\partial K}=-\frac{1}{K\sigma\sqrt T}$$

**Key identity** $F\phi(d_1)=K\phi(d_2)$:

$$\frac{\phi(d_2)}{\phi(d_1)}=e^{(d_1^2-d_2^2)/2}=e^{d_1\sigma\sqrt T-\sigma^2T/2}=e^{\ln(F/K)}=\frac FK$$

→ the first and third terms cancel, leaving $\partial C_{BS}/\partial K=-D\,N(d_2)$.

### Sign analysis (equity, $\partial\sigma/\partial K<0$)
- The skew term is > 0 ⇒ the **digital call is dearer** than $e^{-rT}N(d_2)$; the digital put, $e^{-rT}N(-d_2)+\mathcal V\,\partial\sigma/\partial K$, is **cheaper**.
- ATM example: flat 0.508 → surface 0.644 (+27%). Digitals trade off the **slope** of the smile, not its level.
- **Call-spread intuition:** you buy $K-\varepsilon$ at a higher IV and sell $K+\varepsilon$ at a lower IV → the net cost is inflated.

| Skew | $d\sigma/dK$ | Digital call | Digital put |
|---|---|---|---|
| Equity put skew | < 0 | **More expensive** than BS | Cheaper |
| Upside skew (some commodities) | > 0 | Cheaper | More expensive |

(Digital call + digital put $=D$, so the two adjustments are equal and opposite.)

### Worked example (computed)
$D=0.96,\ F=102,\ T=1,\ K=100,\ \sigma=20.73\%,\ d\sigma/dK=-0.001$; $d_1=0.1992,\ d_2=-0.0081$; check $F\phi(d_1)=39.893=K\phi(d_2)$ ✅

| Term | Value |
|---|---|
| $D\,N(d_2)=0.96\times0.4968$ | 0.4769 |
| $-\mathcal V\cdot d\sigma/dK=-38.30\times(-0.001)$ | +0.0383 |
| **Digital price** | **0.5152** |

Check with a 99/101 call spread ÷ 2:

| Strike | σ (skew) | Call (skew) | Call (flat 20.73%) |
|---|---|---|---|
| 99 | 20.83% | 9.5247 | 9.4868 |
| 101 | 20.63% | 8.4944 | 8.5330 |
| **(C₉₉−C₁₀₁)/2** | | **0.5152** | **0.4769** |

A skew of 1 vol point per 10 strikes adds ~8% to the digital: the **slope is a first-order input**.

### Why vanillas have no such adjustment
1. **IV is defined to price that vanilla correctly**: there is nothing left to correct.
2. **What each product needs from the smile:**

| Product | Relation to vanilla prices | Needs from the smile |
|---|---|---|
| Vanilla $C(K)$ | the price itself | **level** $\sigma(K)$ |
| Digital $-\partial C/\partial K$ | 1st derivative | level + **slope** $\sigma'(K)$ |
| Butterfly / density $\partial^2C/\partial K^2$ | 2nd derivative | level + slope + **curvature** $\sigma''(K)$ |

3. $D\,N(d_2)$ silently assumes a flat smile (自己推理 framing).
4. For a vanilla the smile effect shows up in **delta** instead: $\Delta_{\text{total}}=\Delta_{BS}+\mathcal V\cdot\partial\sigma/\partial S$ (smile-adjusted delta; sticky strike vs sticky delta, [[sticky-strike-vs-sticky-moneyness]]) (自己推理 link).

### Link to distribution skewness
$C_{\text{dig}}(K)=D\cdot\mathbb Q(S_T>K)$: a point on the risk-neutral **CDF**; one more derivative gives the density ([[breeden-litzenberger]]). Equity put skew ↔ negative risk-neutral skewness (a fat left tail) → near ATM, $\mathbb Q(S_T>K)$ is higher than $N(d_2)$.

### Trading points
- Hedge with a call spread, **overhedged** (it always pays ≥ 1); the width is a risk choice ([[call-spread-overhedge]]).
- **Pin risk:** delta and gamma blow up near $K$ at expiry.
- The price depends on **smile interpolation**: two surfaces that fit the vanillas equally well can give different digital prices (Wystup & Van Mulken, *Slope Matters*).

**Interview answer:** "A digital is −dC/dK, and C = C_BS(K, σ(K)) depends on K through σ too, so the chain rule adds −Vega·σ′(K). A vanilla uses its own strike's IV, defined to fit its price, so it needs only the level, not the slope."

### Structured payout ratio
An option budget $C(K)$ funds $\mathcal Q$ digitals:

$$\mathcal Q=\frac{C(K)}{C_{\text{dig}}(K)}=\frac{C_{BS}(K,\sigma(K))}{e^{-rT}N(d_2)-\mathcal V\,\partial\sigma/\partial K}<\mathcal Q_{\text{BS-flat}}$$

**Variables:**

- $\mathcal Q$ payout ratio: number of digitals the budget buys
- $\mathcal Q_{\text{BS-flat}}$ the same ratio computed with the flat-vol digital price

Ignoring skew ⇒ over-promising $\mathcal Q$ and losing money at inception.

**Three pricing tiers:** ① analytic skew-adjusted; ② discrete call spread with market vols at each strike; ③ a dynamic smile model (Dupire, SABR/Heston) via PDE/MC.

### Connections
- **Derived from:** [[breeden-litzenberger]] + [[volatility-skew]]; the CoN leg of [[payoff-indicator-split]].
- **Hedged by:** [[call-spread-overhedge]]. **Inside:** [[autocallables]] (coupon and autocall digitals). **Probability link:** [[delta-vs-itm-probability]].

<a id="barrier-options"></a>

## Barrier Options (knock-in/out)
<!-- section: barrier-options | prerequisites: [black-scholes-formula, volatility-surface] | related: [local-volatility-dupire, local-stochastic-volatility, monte-carlo-pricing, pde-finite-difference, autocallables, call-spread-overhedge, second-order-greeks] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [barrier, knock-out, bgk, reverse-barrier] -->

A barrier option is activated (knock-in) or cancelled (knock-out) when the underlying touches a barrier. Its value depends on the vol near the barrier and on how the smile moves, so no single flat vol prices it.

### In–out parity & closed form (down barrier $H\le K$, continuous monitoring)
$$C_{DO}=C_{\text{vanilla}}-C_{DI},\qquad C_{DI}=Se^{-qT}\Big(\frac HS\Big)^{2\lambda}N(y)-Ke^{-rT}\Big(\frac HS\Big)^{2\lambda-2}N\big(y-\sigma\sqrt T\big)$$
$$\lambda=\frac{r-q+\sigma^2/2}{\sigma^2},\qquad y=\frac{\ln\big(H^2/(SK)\big)}{\sigma\sqrt T}+\lambda\sigma\sqrt T$$

**Variables:**

- $C_{DO},C_{DI}$ down-and-out and down-and-in call prices
- $C_{\text{vanilla}}$ the vanilla call with the same strike and expiry
- $H$ barrier level
- $\lambda,y$ auxiliary quantities of the closed form
- $S,K,T,r,q,\sigma$ as in [[black-scholes-formula]]

Example: $S=K=100,\ H=90,\ T=1,\ r=q=0,\ \sigma=20\%$: vanilla 7.966, DI 1.498, DO 6.467.

### Discrete monitoring — BGK correction
Shift the barrier $H\to He^{\pm0.5826\,\sigma\sqrt{\Delta t}}$ (away from spot), where $\Delta t$ is the monitoring interval. Daily-monitoring MC: 6.730 ± 0.029; BGK 6.669; the continuous formula understates by ~4%. Price the frequency written on the term sheet.

### No single "right" vol
3M down-and-out call, $K$ 5000, $H$ 4500: the knock-out discount is 0.89 at ATM vol vs 9.03 at barrier-level vol — **10×**. The value depends on the vol near the barrier and how the smile moves → local vol / LSV.

### Greeks near the barrier
- DO call near $H$: large Δ, Γ flips sign, vega can turn negative ([[second-order-greeks]]).
- **Reverse knock-out (up-and-out call):** the barrier is in the money; the payoff is largest right before it dies → Δ flips large +/−, huge Γ and vega, gap risk. Desks apply **barrier shifts / reserves** ([[model-risk-governance]]).

### Numerics
PDE with the barrier as a boundary (align nodes, [[pde-finite-difference]]); MC with Brownian-bridge crossing probabilities ([[monte-carlo-pricing]]).

### Connections
- **Builds on:** [[black-scholes-formula]], [[volatility-surface]].
- **Inside:** [[autocallables]] (down-and-in put). **Models:** [[local-volatility-dupire]], [[local-stochastic-volatility]]. **Overhedge cousin:** [[call-spread-overhedge]].

<a id="asian-options"></a>

## Asian Options
<!-- section: asian-options | prerequisites: [black-scholes-formula, monte-carlo-pricing] | related: [csharp-pricing-library-example] | sources: [src-vol-surface-exotics-notes] | tags: [asian, averaging] -->

An Asian option pays on the average price rather than the final price. **Averaging kills volatility**, so it is cheaper than the vanilla.

### Key points
- 3M ATM call, daily averaging, 16.49% vol, 200k paths: Asian 102.99 vs vanilla 178.98 (ratio 0.58).
- Continuous averaging from inception: effective vol ≈ $\sigma/\sqrt3$ ($1/\sqrt3=0.577$) — the geometric-average approximation (inferred in the source).
- The geometric Asian has a closed form → it is used as the MC **control variate** for the arithmetic Asian ([[monte-carlo-pricing]]).

### Connections
- **Builds on:** [[black-scholes-formula]], [[monte-carlo-pricing]]. **Implemented in:** [[csharp-pricing-library-example]].

<a id="variance-swaps"></a>

## Variance Swaps & the VIX Strip
<!-- section: variance-swaps | prerequisites: [static-replication, otm-stitching] | related: [gamma-theta-pnl, volatility-skew, realized-volatility, jump-diffusion] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [variance-swap, vix, replication] -->

A variance swap pays realised variance minus a fixed strike. It is replicated statically by a strip of OTM options weighted by $1/K^2$ — the same construction as the VIX index.

### Formula
Payoff: notional × (realised variance − $K_{\text{var}}^2$), with

$$K_{\text{var}}^2=\frac{2}{T\,D}\Big[\int_0^F\frac{P(K)}{K^2}\,dK+\int_F^\infty\frac{C(K)}{K^2}\,dK\Big]$$

**Variables:**

- $K_{\text{var}}$ fair variance strike (quoted in vol units)
- $P(K),C(K)$ OTM put and call prices from the surface
- $1/K^2$ strike weights
- $F$ forward; $D$ discount factor; $T$ tenor

### Key points
- Replicated statically by the OTM strip + a delta-hedged forward — **the same construction as VIX**.
- Low strikes weigh the most and are expensive under skew → **variance strike > ATM vol** (19.72% vs 16.49% in the example).
- Replication error comes from jumps ([[jump-diffusion]]) and strike truncation. Vol swaps and VIX options need vol-of-vol.

### Connections
- **Builds on:** [[static-replication]], [[otm-stitching]].
- **Removes the path-dependence of:** [[gamma-theta-pnl]]. **Priced by:** [[volatility-skew]]. **Underlying:** [[realized-volatility]].

<a id="cliquets-forward-start"></a>

## Cliquets & Forward-Start Options
<!-- section: cliquets-forward-start | prerequisites: [forward-smile] | related: [heston-model, local-stochastic-volatility, vol-term-structure] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [cliquet, forward-start] -->

These products fix their strikes in the future, so their value depends on the smile that will prevail then — the forward smile — which today's surface does not determine.

### Definitions
- **Cliquet:** a sum of capped/floored periodic returns.
- **Forward-start:** an option whose strike is set at a future date.

### Key points
- The value depends on the **forward smile** → local vol underprices; use SV / LSV ([[forward-smile]]).
- "Model choice changes price materially."

### Connections
- **Builds on:** [[forward-smile]]. **Models:** [[heston-model]], [[local-stochastic-volatility]].

<a id="quanto-options"></a>

## Quanto Options
<!-- section: quanto-options | prerequisites: [risk-neutral-pricing] | related: [worst-of-correlation, pricing-app-architecture] | sources: [src-rbc-quantdev-prep] | tags: [quanto, fx, correlation] -->

A quanto pays on a foreign underlying in domestic currency at a **fixed** FX rate. Removing the FX exposure changes the underlying's risk-neutral drift by a correlation term.

### Formula
$$\text{drift adjustment}=-\rho\,\sigma_S\,\sigma_{FX}$$

**Variables:**

- $\rho$ correlation between the stock and the FX rate
- $\sigma_S$ stock volatility
- $\sigma_{FX}$ FX volatility

### Key points
- Extra market data needed: FX vol and stock–FX correlation ([[pricing-app-architecture]]).

### Connections
- **Builds on:** [[risk-neutral-pricing]]. **Correlation risk:** [[worst-of-correlation]].
