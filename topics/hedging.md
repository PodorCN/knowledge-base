---
id: hedging
title: "Hedging"
type: topic
domain: risk-management
sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew]
---
# Hedging

**Sections:** [[delta-hedging]] · [[gamma-theta-pnl]] · [[sticky-strike-vs-sticky-moneyness]] · [[call-spread-overhedge]]

<a id="delta-hedging"></a>

## Delta Hedging & Its Residual Risks
<!-- section: delta-hedging | prerequisites: [greeks] | related: [gamma-theta-pnl, call-spread-overhedge, barrier-options] | sources: [src-squarepoint-dqa-workbook] | tags: [hedging, delta-neutral] -->

- Short call with position delta −50 → **buy 50 shares**. Check contract multipliers.
- Delta-neutral ≠ risk-free: gamma, vega, jumps, discrete rebalancing, costs remain.
- Breaks down when Δ is discontinuous: digitals and barriers near expiry/barrier → **pin risk** → [[call-spread-overhedge]], barrier shifts.

### Connections
- **P&L of a hedged option:** [[gamma-theta-pnl]]. **Discrete analogue:** [[binomial-replication]].

<a id="gamma-theta-pnl"></a>

## Gamma–Theta Trade-off & Realised vs Implied Vol P&L
<!-- section: gamma-theta-pnl | prerequisites: [black-scholes-pde, greeks] | related: [realized-volatility, implied-volatility, variance-swaps, jensens-inequality] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [gamma, theta, realised-vol] -->

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

### Connections
- **From:** [[black-scholes-pde]] rearranged. **Compares:** [[realized-volatility]] vs [[implied-volatility]].

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
