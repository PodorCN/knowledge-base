---
id: hedging
title: "Hedging"
type: topic
domain: risk-management
sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew]
---
# Hedging

**Sections:** [[delta-hedging]] · [[gamma-theta-pnl]] · [[delta-gamma-hedging]] · [[sticky-strike-vs-sticky-moneyness]] · [[call-spread-overhedge]]

<a id="delta-hedging"></a>

## Delta Hedging & Its Residual Risks
<!-- section: delta-hedging | prerequisites: [greeks] | related: [gamma-theta-pnl, call-spread-overhedge, barrier-options] | sources: [src-squarepoint-dqa-workbook] | tags: [hedging, delta-neutral] -->

- Short call with position delta −50 → **buy 50 shares**. Check contract multipliers.
- Delta-neutral ≠ risk-free: gamma, vega, jumps, discrete rebalancing, costs remain.
- Breaks down when Δ is discontinuous: digitals and barriers near expiry/barrier → **pin risk** → [[call-spread-overhedge]], barrier shifts.

### Connections
- **P&L of a hedged option:** [[gamma-theta-pnl]]. **Discrete analogue:** [[binomial-replication]]. **Hedging gamma too:** [[delta-gamma-hedging]].

<a id="gamma-theta-pnl"></a>

## Gamma–Theta Trade-off & Realised vs Implied Vol P&L
<!-- section: gamma-theta-pnl | prerequisites: [black-scholes-pde, greeks] | related: [realized-volatility, implied-volatility, variance-swaps, jensens-inequality, delta-gamma-hedging] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-chat-long-gamma] | tags: [gamma, theta, realised-vol, variance-risk-premium] -->

$$\text{P\&L}_{\text{hedged}}\approx\tfrac12\Gamma S^2\big(\sigma_{\text{realised}}^2-\sigma_{\text{implied}}^2\big)\Delta t$$

**Variables:**

- Γ gamma
- $S$ spot
- $\sigma_{\text{realised}}$ vol over the step
- $\sigma_{\text{implied}}$ vol paid
- $\Delta t$ time step

- Long gamma pays theta; wins iff realised > implied. It's about movement **relative to what you paid**, not "a lot of movement".
- Heuristic: ignores vol repricing, jumps, costs.
- Path-dependent P&L (weighted by Γ, i.e. where spot went) → [[variance-swaps]] remove that dependence.

### Why long gamma loses money on average
Long gamma is paying an insurance premium for convexity, and that premium is usually priced rich. Running example: $S=100$, $\sigma_{imp}=20\%$, $\Gamma=0.0398$, $\Theta\approx-0.032$/day.

**1. Theta is charged every day, so the price must move enough to break even.** Under BS ($r=0$) theta and gamma are tied together:

$$\Theta=-\tfrac12\,\Gamma\,\sigma_{imp}^2\,S^2$$

**Variables:**

- $\Theta$ time decay per unit time
- $\Gamma$ gamma
- $\sigma_{imp}$ implied vol paid for the option
- $S$ underlying price

The daily break-even move is

$$|\Delta S^*|=\sigma_{imp}\,S\,\sqrt{\Delta t}$$

**Variables:**

- $\Delta S^*$ the price move whose gamma gain exactly offsets theta
- $\Delta t$ time step, 1 day = 1/252

With the numbers: $20\%\times100\times\sqrt{1/252}\approx1.26$ per day. If the price moves less than 1.26 a day on average, you lose. Equivalently, you only make money if realised vol > the implied vol you paid (BS result; Hull ch. 19 gives the Θ–Γ relation).

**2. Implied vol usually exceeds realised vol (variance risk premium).** Empirically, index-option implied variance is on average above the variance subsequently realised, so systematic long gamma / long vol has negative long-run returns ([[realized-volatility]]). This is also why short-gamma (option-selling) strategies usually collect steadily and lose big in one go in a crash.

**3. Path dependence: when and where the move happens matters.** Gamma P&L ≈ ½Γ(ΔS)², but Γ itself changes with $S$ and time: largest ATM, near 0 deep ITM or OTM. A big move after the option is already deep OTM earns almost nothing, so P&L can be negative even if realised vol > implied over the whole period. Actual P&L is driven by **gamma-weighted realised variance** (自己推理; a common result in the vol-trading literature, e.g. Sinclair, *Volatility Trading*).

**4. Usually also long vega: IV crush risk.** Buying options is usually long vega too. Typical case: buying a straddle before earnings; after the announcement implied vol drops sharply, and even if the stock moves, the vega loss can wipe out the gamma gain.

**5. Transaction costs + discrete hedging.** The option bid–ask is often wide (entry cost). Gamma scalping re-hedges delta frequently, paying costs each time. Hedging too infrequently makes P&L very noisy (discrete-hedging error).

**6. Near expiry, gamma and theta both blow up.** ATM options near expiry have sharply rising Γ and equally rising Θ. Daily theta cost is high, and with $S$ near the strike delta flips between 0 and 1 (pin risk), making hedging hard ([[call-spread-overhedge]]).

**7. Negative carry: psychological and career pressure (自己推理).** Most of the time you lose a little; you make money only in a few big moves. Drawdowns can be long, testing PM evaluations and LP patience.

References: Hull, *Options, Futures, and Other Derivatives*, ch. 19; Carr & Wu (2009), "Variance Risk Premiums", *RFS*; Bakshi & Kapadia (2003), "Delta-Hedged Gains and the Negative Market Volatility Risk Premium", *RFS*.

### Connections
- **From:** [[black-scholes-pde]] rearranged. **Compares:** [[realized-volatility]] vs [[implied-volatility]].
- **Vega side:** [[greeks]]. **Neutralising gamma instead:** [[delta-gamma-hedging]].

<a id="delta-gamma-hedging"></a>

## Delta-Gamma Hedging (is it cheaper?)
<!-- section: delta-gamma-hedging | prerequisites: [delta-hedging, gamma-theta-pnl] | related: [greeks, vol-term-structure, volatility-skew] | sources: [src-chat-long-gamma] | tags: [gamma-neutral, speed, hedging-cost] -->

Short answer: **not cheaper, it is a different position.** Hedging gamma also removes theta, so you stop paying for convexity and also stop receiving it. The real savings are in hedge execution, not in the price of convexity. (Numbers below computed with BS, flat vol 20%, $r=0$.)

### Why theta disappears with gamma
For a delta-neutral book the BS PDE ($r=0$) reads

$$\Theta+\tfrac12\,\sigma^2S^2\,\Gamma=0$$

**Variables:**

- $\Theta$ book time decay
- $\sigma$ implied vol
- $S$ underlying price
- $\Gamma$ book gamma

So $\Gamma=0\Rightarrow\Theta\approx0$ (Hull ch. 19, "Relationship between delta, theta, and gamma"). The hedge option has to be **sold** (you were long gamma); the theta it earns offsets the theta you paid. The price of convexity doesn't change; you have just sold the insurance back.

### Worked example: long 1 ATM call ($K=100$, 3 months)
Original position: Γ = 0.0398, Θ = −0.0316/day, vega = 0.199.

| Hedge option | Sell $w=-\Gamma/\Gamma_T$ | Θ after hedge | Vega after hedge |
|---|---|---|---|
| 110 call, same 3 months | 1.50 | 0 | 0 |
| 100 call, 6 months | 1.42 | 0 | −0.199 |

P&L after an instantaneous jump:

| ΔS | Delta hedge only | Δ-Γ hedge (110 call) | Δ-Γ hedge (6M ATM) |
|---|---|---|---|
| −10 | +1.92 | +0.48 | −0.08 |
| −5 | +0.50 | +0.07 | −0.01 |
| +5 | +0.48 | −0.08 | −0.01 |
| +10 | +1.77 | −0.64 | −0.06 |

- The gamma gain essentially disappears; that is the price.
- **Same expiry, different strike:** under BS vega ∝ Γ within one expiry, so vega is hedged too, but an asymmetric third-order term remains (**speed**, $\partial\Gamma/\partial S$): gain on down moves, loss on up moves.
- **Different expiry:** gamma- and theta-neutral, but now short vega, i.e. a bet on the term structure (自己推理 from the flat-vol model).

### Where it actually saves / costs
**Saves:**
- Much smaller delta drift in big moves → rebalance less often → lower stock trading costs and discrete-hedging error.
- Less gap risk (you can't re-hedge in the middle of a gap).
- For a short-gamma dealer it is insurance: tail risk falls sharply.

**Costs:**
- Option bid–ask is far wider than stock → each round trip costs more.
- The hedge option has a different IV (skew / term structure) → Θ is not exactly 0; you effectively hold a vol-spread position.
- Residual risks: vega, speed, skew moves, model risk.
- Both options' Greeks change over time, so gamma-neutrality drifts and must be rebalanced.

### It depends on who you are (自己推理)
| You are | What Δ-Γ hedging means |
|---|---|
| Deliberately long gamma, betting realised > implied | Hedges away your alpha; pointless |
| Dealer who sold options to clients, passively short gamma | Very valuable: locks in bid–ask profit, removes tail risk |
| Just want a steadier delta hedge | Less frequent rebalancing and less gap risk, but you pay option bid–ask |

References: Hull, *Options, Futures, and Other Derivatives*, ch. 19 "The Greek Letters" (gamma neutrality; delta–theta–gamma relation).

### Connections
- **Builds on:** [[delta-hedging]], [[gamma-theta-pnl]].
- **Residual exposures:** vega and term structure ([[vol-term-structure]]), skew ([[volatility-skew]]).

<a id="sticky-strike-vs-sticky-moneyness"></a>

## Sticky Strike vs Sticky Moneyness (smile dynamics)
<!-- section: sticky-strike-vs-sticky-moneyness | prerequisites: [volatility-surface, greeks] | related: [greeks-conventions-bumping, second-order-greeks, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [smile-dynamics, shadow-delta] -->

- **Sticky strike:** each strike keeps its IV when spot moves.
- **Sticky moneyness / delta:** smile moves with spot. Delta gains $\mathcal V\cdot\partial\sigma/\partial S$ ("shadow delta").

### Example — index 5000 → 4900, 3M 5000 put
| Rule | Vol | Put | Change | Delta |
|---|---|---|---|---|
| Before | 16.92% | 152.26 | — | — |
| Sticky strike | 16.92% | 202.20 | +49.9 | −0.452 |
| Sticky moneyness | 15.52% | 188.76 | +36.5 | −0.315 |
Hedge ratios differ by ~30%. With negative skew, sticky-moneyness call delta < sticky-strike delta.

### Regimes (Derman)
Calm trending ≈ sticky strike; fearful ≈ **sticky implied tree** (ATM vol moves ~2× sticky-strike speed). A surface without stated dynamics gives unusable Greeks.

### Connections
- **Implemented in:** [[greeks-conventions-bumping]] (surface bumps). **Model-implied dynamics:** [[local-volatility-dupire]] (≈ sticky tree).

<a id="call-spread-overhedge"></a>

## Call-Spread Overhedge & Pin Risk
<!-- section: call-spread-overhedge | prerequisites: [digital-options, delta-hedging] | related: [barrier-options, model-risk-governance, static-replication] | sources: [src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep] | tags: [pin-risk, overhedge, digital, reserves] -->

### Why digitals can't be delta-hedged near expiry
Payoff jumps 0 → 1 at $K$; as $t\to T$ near $K$, Δ → δ-function, Γ flips ±∞ → infinite rebalancing = **pin risk**.

### The desk solution: left-shifted call spread
Short a digital call at $K$ → buy $1/\varepsilon$ call spreads on $[K-\varepsilon,K]$:
- $S_T\le K-\varepsilon$: both 0. $S_T\ge K$: both 1. In between: hedge pays > 0, digital pays 0 → **cushion** (super-replication).
- Symmetric $[K-\varepsilon,K+\varepsilon]$ would be **under-hedged** on $(K,K+\varepsilon)$.
- Example: $\varepsilon=1$ → $(C(99)-C(100))/1=0.4701$ vs flat digital 0.4602; desk books the conservative side.

### Width ε = quoting margin
Wider ε tames Γ and pin risk but costs more (K−ε deeper ITM, higher IV). Chosen by liquidity, pin risk, time to expiry.

### App design (RBC Q5b.3)
Huge digital gamma the day before expiry is a **feature**; show theoretical and overhedged Greeks and flag the regime rather than silently capping.

### Connections
- **Same idea for barriers:** barrier shift in [[barrier-options]]. **Booked as reserves:** [[model-risk-governance]].
