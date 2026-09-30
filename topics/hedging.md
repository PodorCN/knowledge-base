---
id: hedging
title: "Hedging"
type: topic
domain: risk-management
sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew, src-chat-long-gamma]
---
# Hedging

This chapter looks at options from the hedger's side. Delta hedging removes first-order spot risk; what remains is a gamma–theta trade whose P&L depends on realised versus implied volatility. Hedging gamma as well changes the position rather than making it cheaper. Finally, hedge ratios depend on how the smile moves, and discontinuous payoffs such as digitals require an overhedge.

**Prerequisites:** [[greeks]], [[black-scholes-pde]], [[volatility-surface]], [[digital-options]].

**Leads to:** [[scenario-risk-grids]], [[model-risk-governance]] (reserves for overhedges).

**Sections:** [[delta-hedging]] · [[gamma-theta-pnl]] · [[delta-gamma-hedging]] · [[sticky-strike-vs-sticky-moneyness]] · [[call-spread-overhedge]]

<a id="delta-hedging"></a>

## Delta Hedging & Its Residual Risks
<!-- section: delta-hedging | prerequisites: [greeks] | related: [gamma-theta-pnl, call-spread-overhedge, barrier-options, binomial-replication] | sources: [src-squarepoint-dqa-workbook] | tags: [hedging, delta-neutral] -->

A delta hedge holds $-\Delta$ units of the underlying per option so that small spot moves have no first-order effect on the position. It leaves every other risk in place.

### Key points
- Short a call with position delta −50 → **buy 50 shares**. Check contract multipliers.
- Delta-neutral ≠ risk-free: gamma, vega, jumps, discrete rebalancing and costs remain.
- It breaks down when Δ is discontinuous: digitals and barriers near expiry / the barrier → **pin risk** → [[call-spread-overhedge]], barrier shifts ([[barrier-options]]).

### Connections
- **Builds on:** [[greeks]]. **Discrete analogue:** the $\Delta$ of [[binomial-replication]].
- **P&L of a hedged option:** [[gamma-theta-pnl]]. **Hedging gamma too:** [[delta-gamma-hedging]].

<a id="gamma-theta-pnl"></a>

## Gamma–Theta Trade-off & Realised vs Implied Vol P&L
<!-- section: gamma-theta-pnl | prerequisites: [black-scholes-pde, greeks, delta-hedging] | related: [realized-volatility, implied-volatility, variance-swaps, jensens-inequality, delta-gamma-hedging, ito-lemma] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook, src-chat-long-gamma] | tags: [gamma, theta, realised-vol, variance-risk-premium] -->

A delta-hedged long option earns from convexity when the stock moves and pays theta every day. Under Black–Scholes the two are tied together by the implied vol, so the hedged P&L is positive exactly when realised variance exceeds implied variance.

### Formulas
$$\Theta=-\tfrac12\,\Gamma\,\sigma_{\text{imp}}^2\,S^2\quad(r=0),\qquad \text{P\&L}_{\text{hedged}}\approx\tfrac12\,\Gamma\,S^2\big(\sigma_{\text{real}}^2-\sigma_{\text{imp}}^2\big)\,\Delta t$$

**Variables:**

- $\Theta$ time decay per unit time
- $\Gamma$ gamma
- $S$ underlying price
- $\sigma_{\text{imp}}$ implied vol paid for the option
- $\sigma_{\text{real}}$ realised vol over the step
- $\Delta t$ time step

The first relation is the Black–Scholes PDE of [[black-scholes-pde]] for a delta-neutral book with $r=0$ (Hull ch. 19 gives the Θ–Γ relation).

### Key points
- Long gamma pays theta; it wins iff realised > implied. It's about movement **relative to what you paid**, not "a lot of movement".
- A heuristic: it ignores vol repricing, jumps and costs.
- The P&L is path-dependent (weighted by Γ, i.e. by where spot went) → [[variance-swaps]] remove that dependence.

### Why long gamma loses money on average
Long gamma is paying an insurance premium for convexity, and that premium is usually priced rich. Running example: $S=100$, $\sigma_{\text{imp}}=20\%$, $\Gamma=0.0398$, $\Theta\approx-0.032$/day.

#### 1. Theta is charged every day, so the price must move enough to break even
The daily break-even move is

$$|\Delta S^*|=\sigma_{\text{imp}}\,S\,\sqrt{\Delta t}$$

**Variables:**

- $\Delta S^*$ the price move whose gamma gain exactly offsets theta
- $\Delta t$ time step, 1 day = 1/252

**Notes:**

- With the numbers: $20\%\times100\times\sqrt{1/252}\approx1.26$ per day.
- If the price moves less than 1.26 a day on average, you lose.
- Equivalently, you only make money if realised vol > the implied vol you paid.

#### 2. Implied vol usually exceeds realised vol (variance risk premium)
- Empirically, index-option implied variance is on average above the variance subsequently realised.
- So systematic long gamma / long vol has negative long-run returns ([[realized-volatility]]).
- This is also why short-gamma (option-selling) strategies usually collect steadily and lose big in one go in a crash.

#### 3. Path dependence: when and where the move happens matters
- Gamma P&L ≈ ½Γ(ΔS)², but Γ itself changes with $S$ and time: largest ATM, near 0 deep ITM or OTM.
- A big move after the option is already deep OTM earns almost nothing.
- So the P&L can be negative even if realised vol > implied over the whole period.
- The actual P&L is driven by **gamma-weighted realised variance** (自己推理; a common result in the vol-trading literature, e.g. Sinclair, *Volatility Trading*).

#### 4. Usually also long vega: IV crush risk
- Buying options is usually long vega too.
- Typical case: buying a straddle before earnings.
- After the announcement implied vol drops sharply; even if the stock moves, the vega loss can wipe out the gamma gain.

#### 5. Transaction costs + discrete hedging
- The option bid–ask is often wide (entry cost).
- Gamma scalping re-hedges delta frequently, paying costs each time.
- Hedging too infrequently makes the P&L very noisy (discrete-hedging error).

#### 6. Near expiry, gamma and theta both blow up
- ATM options near expiry have sharply rising Γ and equally rising Θ.
- The daily theta cost is high.
- With $S$ near the strike, delta flips between 0 and 1 (pin risk), making hedging hard ([[call-spread-overhedge]]).

#### 7. Negative carry: psychological and career pressure (自己推理)
- Most of the time you lose a little; you make money only in a few big moves.
- Drawdowns can be long, testing PM evaluations and LP patience.

**References:**

- Hull, *Options, Futures, and Other Derivatives*, ch. 19
- Carr & Wu (2009), "Variance Risk Premiums", *RFS*
- Bakshi & Kapadia (2003), "Delta-Hedged Gains and the Negative Market Volatility Risk Premium", *RFS*

### Connections
- **Builds on:** [[black-scholes-pde]] (rearranged), [[greeks]]; convexity as in [[jensens-inequality]] and [[ito-lemma]].
- **Compares:** [[realized-volatility]] vs [[implied-volatility]]. **Neutralising gamma instead:** [[delta-gamma-hedging]].

<a id="delta-gamma-hedging"></a>

## Delta-Gamma Hedging (is it cheaper?)
<!-- section: delta-gamma-hedging | prerequisites: [delta-hedging, gamma-theta-pnl] | related: [greeks, vol-term-structure, volatility-skew] | sources: [src-chat-long-gamma] | tags: [gamma-neutral, speed, hedging-cost] -->

Short answer: **not cheaper — it is a different position.** Hedging gamma with another option also removes theta, so you stop paying for convexity and also stop receiving it. The real savings are in hedge execution, not in the price of convexity. (Numbers below computed with Black–Scholes, flat vol 20%, $r=0$.)

### Why theta disappears with gamma
For a delta-neutral book, the relation of [[gamma-theta-pnl]], $\Theta+\tfrac12\sigma^2S^2\Gamma=0$ ($r=0$), holds for the whole book:

**Variables:**

- $\Theta$ book time decay
- $\sigma$ implied vol
- $S$ underlying price
- $\Gamma$ book gamma

**Consequences:**

- So $\Gamma=0\Rightarrow\Theta\approx0$ (Hull ch. 19, "Relationship between delta, theta, and gamma").
- The hedge option has to be **sold** (you were long gamma); the theta it earns offsets the theta you paid.
- The price of convexity doesn't change; you have just sold the insurance back.

### Worked example: long 1 ATM call ($K=100$, 3 months)
Original position: Γ = 0.0398, Θ = −0.0316/day, vega = 0.199.

| Hedge option | Sell $w=\Gamma/\Gamma_H$ units | Θ after hedge | Vega after hedge |
|---|---|---|---|
| 110 call, same 3 months | 1.50 | 0 | 0 |
| 100 call, 6 months | 1.42 | 0 | −0.199 |

Here $\Gamma_H$ is the gamma of one hedge option.

P&L after an instantaneous jump:

| ΔS | Delta hedge only | Δ-Γ hedge (110 call) | Δ-Γ hedge (6M ATM) |
|---|---|---|---|
| −10 | +1.92 | +0.48 | −0.08 |
| −5 | +0.50 | +0.07 | −0.01 |
| +5 | +0.48 | −0.08 | −0.01 |
| +10 | +1.77 | −0.64 | −0.06 |

- The gamma gain essentially disappears; that is the price.
- **Same expiry, different strike:** under BS, vega ∝ Γ within one expiry, so vega is hedged too, but an asymmetric third-order term remains (**speed**, $\partial\Gamma/\partial S$): a gain on down moves, a loss on up moves.
- **Different expiry:** gamma- and theta-neutral, but now short vega, i.e. a bet on the term structure (自己推理 from the flat-vol model).

### Where it actually saves / costs
**Saves:**

- Much smaller delta drift in big moves → rebalance less often → lower stock trading costs and discrete-hedging error.
- Less gap risk (you can't re-hedge in the middle of a gap).
- For a short-gamma dealer it is insurance: tail risk falls sharply.

**Costs:**

- The option bid–ask is far wider than the stock's → each round trip costs more.
- The hedge option has a different IV (skew / term structure) → Θ is not exactly 0; you effectively hold a vol-spread position.
- Residual risks: vega, speed, skew moves, model risk.
- Both options' Greeks change over time, so gamma-neutrality drifts and must be rebalanced.

### It depends on who you are (自己推理)

| You are | What Δ-Γ hedging means |
|---|---|
| Deliberately long gamma, betting realised > implied | Hedges away your alpha; pointless |
| Dealer who sold options to clients, passively short gamma | Very valuable: locks in bid–ask profit, removes tail risk |
| Just want a steadier delta hedge | Less frequent rebalancing and less gap risk, but you pay option bid–ask |

**References:**

- Hull, *Options, Futures, and Other Derivatives*, ch. 19 "The Greek Letters" (gamma neutrality; delta–theta–gamma relation)

### Connections
- **Builds on:** [[delta-hedging]], [[gamma-theta-pnl]].
- **Residual exposures:** vega and term structure ([[vol-term-structure]]), skew ([[volatility-skew]]).

<a id="sticky-strike-vs-sticky-moneyness"></a>

## Sticky Strike vs Sticky Moneyness (smile dynamics)
<!-- section: sticky-strike-vs-sticky-moneyness | prerequisites: [volatility-surface, greeks] | related: [greeks-conventions-bumping, second-order-greeks, local-volatility-dupire, digital-options] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [smile-dynamics, shadow-delta] -->

When spot moves, the implied vol used for a given option depends on an assumption about how the smile moves. The assumption changes the delta, so a surface without stated dynamics gives unusable Greeks.

### Definitions
- **Sticky strike:** each strike keeps its implied vol when spot moves.
- **Sticky moneyness / delta:** the smile moves with spot. Delta gains a term $\mathcal V\cdot\partial\sigma/\partial S$ (the "shadow delta").

### Worked example — index 5000 → 4900, 3M 5000 put

| Rule | Vol | Put | Change | Delta |
|---|---|---|---|---|
| Before | 16.92% | 152.26 | — | — |
| Sticky strike | 16.92% | 202.20 | +49.9 | −0.452 |
| Sticky moneyness | 15.52% | 188.76 | +36.5 | −0.315 |

- The hedge ratios differ by ~30%.
- With negative skew, the sticky-moneyness call delta < the sticky-strike delta.

### Regimes (Derman)
Calm trending markets ≈ sticky strike; fearful markets ≈ **sticky implied tree** (ATM vol moves ~2× the sticky-strike speed).

### Connections
- **Builds on:** [[volatility-surface]], [[greeks]].
- **Implemented in:** [[greeks-conventions-bumping]] (surface bumps). **Model-implied dynamics:** [[local-volatility-dupire]] (≈ sticky tree). **Smile-adjusted delta:** [[digital-options]].

<a id="call-spread-overhedge"></a>

## Call-Spread Overhedge & Pin Risk
<!-- section: call-spread-overhedge | prerequisites: [digital-options, delta-hedging] | related: [barrier-options, model-risk-governance, static-replication] | sources: [src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep] | tags: [pin-risk, overhedge, digital, reserves] -->

A digital's payoff jumps at the strike, so near expiry its delta becomes unmanageable. Desks instead hedge with a call spread placed so that it always pays at least as much as the digital.

### Why digitals can't be delta-hedged near expiry
The payoff jumps 0 → 1 at $K$; as $t\to T$ near $K$, Δ → a δ-function and Γ flips between ±∞ → infinite rebalancing = **pin risk**.

### The desk solution: a left-shifted call spread
Short a digital call at $K$ → buy $1/\varepsilon$ call spreads on $[K-\varepsilon,K]$:

- $S_T\le K-\varepsilon$: both pay 0. $S_T\ge K$: both pay 1. In between: the hedge pays > 0 while the digital pays 0 → a **cushion** (super-replication).
- A symmetric spread $[K-\varepsilon,K+\varepsilon]$ would be **under-hedged** on $(K,K+\varepsilon)$.
- Example: $\varepsilon=1$ → $(C(99)-C(100))/1=0.4701$ vs a flat-vol digital of 0.4602; the desk books the conservative side.

Here $\varepsilon$ is the spread width and $C(\cdot)$ the call price at a strike.

### Width ε = quoting margin
A wider $\varepsilon$ tames Γ and pin risk but costs more ($K-\varepsilon$ is deeper ITM, at a higher IV). It is chosen by liquidity, pin risk and time to expiry.

### App design (RBC prep)
Huge digital gamma the day before expiry is a **feature**; show theoretical and overhedged Greeks and flag the regime rather than silently capping.

### Connections
- **Builds on:** [[digital-options]], [[delta-hedging]].
- **Same idea for barriers:** barrier shift in [[barrier-options]]. **Booked as reserves:** [[model-risk-governance]].
