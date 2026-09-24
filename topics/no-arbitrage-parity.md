---
id: no-arbitrage-parity
title: "No-Arbitrage & Put–Call Parity"
type: topic
domain: pricing
sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# No-Arbitrage & Put–Call Parity

**Sections:** [[option-payoffs-moneyness]] · [[option-price-bounds]] · [[put-call-parity]] · [[binomial-replication]] · [[static-replication]]

<a id="option-payoffs-moneyness"></a>

## Option Payoffs, Exercise Style & Moneyness
<!-- section: option-payoffs-moneyness | prerequisites: [] | related: [put-call-parity, option-price-bounds, american-early-exercise] | sources: [src-squarepoint-dqa-workbook] | tags: [call, put, itm, otm] -->

$$\text{Call}=(S_T-K)^+,\qquad \text{Put}=(K-S_T)^+,\qquad x^+=\max(x,0)$$

**Variables:**

- $S_T$ underlying at expiry
- $K$ strike

- European: exercise at expiry; American: any time up to expiry.
- **Payoff ≠ profit** (premium, financing).
- Call ITM if $S>K$; put ITM if $S<K$. ATM may mean spot- or **forward**-moneyness — state which. Surfaces use $k=\ln(K/F)$.

<a id="option-price-bounds"></a>

## European Option Price Bounds
<!-- section: option-price-bounds | prerequisites: [no-arbitrage, option-payoffs-moneyness] | related: [put-call-parity, surface-no-arbitrage] | sources: [src-squarepoint-dqa-workbook] | tags: [bounds, arbitrage] -->

$$\max(0,S_0-Ke^{-rT})\le C\le S_0,\qquad \max(0,Ke^{-rT}-S_0)\le P\le Ke^{-rT}$$

**Variables:**

- $S_0$ spot (no dividends)
- $K$ strike
- $r$ rate
- $T$ maturity

Derived by state-by-state payoff comparison. Check quotes against bounds **before** inverting implied vol (else no solution). Revisit with dividends/American/negative rates.

### Connections
- **Extended to strike-derivative bounds in:** [[surface-no-arbitrage]] ($-D\le\partial C/\partial K\le0$).

<a id="put-call-parity"></a>

## Put–Call Parity
<!-- section: put-call-parity | prerequisites: [no-arbitrage, forward-pricing, option-payoffs-moneyness] | related: [implied-forward-regression, otm-stitching, implied-volatility, black-scholes-formula, binomial-replication] | sources: [src-quant-study-notes-pcp-skew, src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [parity, replication, model-free] -->

$$C(K,T)-P(K,T)=S_0e^{-qT}-Ke^{-rT}=D(T)\,[F(T)-K]$$

**Variables:**

- $C,P$ European call/put, same $K$ and $T$
- $S_0$ spot
- $r$ risk-free rate
- $q$ dividend yield / borrow
- $D(T)=e^{-rT}$ discount factor
- $F(T)=S_0e^{(r-q)T}$ forward

### Static replication proof
| Portfolio at t=0 | Cost | $S_T\ge K$ | $S_T<K$ |
|---|---|---|---|
| A: fiduciary call = call + ZCB paying K | $C+Ke^{-rT}$ | $S_T$ | $K$ |
| B: protective put = put + $e^{-qT}$ shares | $P+S_0e^{-qT}$ | $S_T$ | $K$ |

Both pay $\max(S_T,K)$ in every state ⇒ same price. Holds under GBM, stochastic vol, jumps — any model.

### Four roles in vol-surface construction
1. **Same IV for call & put** at $(K,T)$: $C_{BS}-P_{BS}$ doesn't depend on σ ⇒ one root σ fits both → [[implied-volatility]].
2. **Extract $D$ and $F$** by regressing $C-P$ on $K$ → [[implied-forward-regression]].
3. **OTM stitching**: ITM call IV = OTM put IV → [[otm-stitching]].
4. **Data cleaning**: drop quotes violating conversion/reversal or box-spread bounds.

### Arbitrage example
$r=q=0$, $S=K=100$: $C=12$, $P=9$ but parity needs $C-P=0$. Sell call, buy put, buy share, borrow 100 → +3 today, 0 at expiry in every state.

### Engineering use
Regression test for a pricing library: any update that breaks parity on European vanillas is a bug (RBC prep).

### Connections
- **Builds on:** [[no-arbitrage]], [[forward-pricing]].
- **Used by:** [[implied-forward-regression]], [[otm-stitching]], [[model-release-regression-testing]].
- **American options:** parity becomes an inequality ([[american-early-exercise]]).

<a id="binomial-replication"></a>

## One-Period Binomial Replication
<!-- section: binomial-replication | prerequisites: [no-arbitrage] | related: [risk-neutral-pricing, black-scholes-pde, delta-hedging] | sources: [src-squarepoint-dqa-workbook] | tags: [replication, risk-neutral, binomial] -->

$$\Delta=\frac{V_u-V_d}{S_u-S_d},\quad B=\frac{V_d-\Delta S_d}{R},\quad V_0=\Delta S_0+B=\frac{q^*V_u+(1-q^*)V_d}{R},\quad q^*=\frac{R-d}{u-d}$$

**Variables:**

- $S_u=uS_0$, $S_d=dS_0$ up/down prices
- $V_u,V_d$ derivative payoffs
- $R$ gross risk-free growth
- $\Delta$ shares held
- $B$ bank amount
- $q^*$ risk-neutral up-probability (in (0,1) iff $d<R<u$)

**Example:** $S_0=100$, 120/80, $R=1$, $K=100$ call: $\Delta=0.5$, $B=-40$, $C=10$; $q^*=0.5$. Your 80% "real" up-probability is irrelevant (using it gives 16 — wrong). Put = 10 by parity.

### Connections
- **Continuous-time limit:** [[black-scholes-pde]]; **abstraction:** [[risk-neutral-pricing]]; Δ here = [[delta-hedging]] ratio.

<a id="static-replication"></a>

## Static Replication
<!-- section: static-replication | prerequisites: [no-arbitrage, breeden-litzenberger] | related: [put-call-parity, digital-options, variance-swaps, call-spread-overhedge, principal-protected-note] | sources: [src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew] | tags: [replication, model-free] -->

### Examples
- Parity: forward = call − put ([[put-call-parity]]).
- Digital = tight call spread ([[digital-options]], [[call-spread-overhedge]]).
- Log contract → variance swap strip with $2/K^2$ weights ([[variance-swaps]]).
- PPN = ZCB + call ([[principal-protected-note]]).

Cleanest answer whenever it applies; path-dependent payoffs need dynamics (models).
