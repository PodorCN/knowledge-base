---
id: no-arbitrage-parity
title: "Options: Payoffs, Parity & Replication"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Options: Payoffs, Parity & Replication

This chapter applies no-arbitrage to options before any model is introduced. It defines call and put payoffs, derives model-free price bounds and put–call parity, prices an option by replication in a one-period binomial model — the discrete origin of risk-neutral pricing — and shows how other payoffs are built statically from vanillas.

**Prerequisites:** [[no-arbitrage]], [[forward-pricing]], [[discounting-compounding]].

**Leads to:** [[risk-neutral-pricing]], [[black-scholes-pde]], [[implied-volatility]], [[implied-forward-regression]], [[digital-options]].

**Sections:** [[option-payoffs-moneyness]] · [[option-price-bounds]] · [[put-call-parity]] · [[binomial-replication]] · [[static-replication]]

<a id="option-payoffs-moneyness"></a>

## Option Payoffs, Exercise Style & Moneyness
<!-- section: option-payoffs-moneyness | prerequisites: [] | related: [put-call-parity, option-price-bounds, american-early-exercise] | sources: [src-squarepoint-dqa-workbook] | tags: [call, put, itm, otm] -->

A call gives the right to buy the underlying at the strike, a put the right to sell. What they pay at expiry depends only on the terminal price.

### Definitions
$$\text{Call payoff}=(S_T-K)^+,\qquad \text{Put payoff}=(K-S_T)^+,\qquad x^+=\max(x,0)$$

**Variables:**

- $S_T$ underlying price at expiry $T$
- $K$ strike
- $x^+$ positive part of $x$

### Key points
- **European:** exercise only at expiry. **American:** exercise any time up to expiry ([[american-early-exercise]]).
- **Payoff ≠ profit**: profit also subtracts the premium and its financing.
- A call is in the money (ITM) if $S>K$; a put is ITM if $S<K$. "ATM" may mean spot-moneyness ($K=S$) or **forward**-moneyness ($K=F$) — state which. Vol surfaces use log-moneyness $k=\ln(K/F)$.

### Connections
- **Used by:** [[option-price-bounds]], [[put-call-parity]], [[bs-call-setup-risk-neutral]].

<a id="option-price-bounds"></a>

## European Option Price Bounds
<!-- section: option-price-bounds | prerequisites: [no-arbitrage, option-payoffs-moneyness] | related: [put-call-parity, surface-no-arbitrage, implied-volatility] | sources: [src-squarepoint-dqa-workbook] | tags: [bounds, arbitrage] -->

Without any model, comparing payoffs state by state bounds the price of a European option.

### Formulas
$$\max(0,\ S_0-Ke^{-rT})\le C\le S_0,\qquad \max(0,\ Ke^{-rT}-S_0)\le P\le Ke^{-rT}$$

**Variables:**

- $C,P$ European call and put prices
- $S_0$ spot price (no dividends)
- $K$ strike
- $r$ continuously compounded risk-free rate
- $T$ time to expiry

### Key points
- Derived by state-by-state payoff comparison (e.g. a call is worth at least a forward struck at $K$, and never more than the stock).
- Check quotes against the bounds **before** inverting implied vol; outside them no implied vol exists ([[implied-volatility]]).
- Revisit the bounds with dividends, American exercise or negative rates.

### Connections
- **Builds on:** [[no-arbitrage]], [[option-payoffs-moneyness]].
- **Extended to strike-derivative bounds in:** [[surface-no-arbitrage]] ($-D\le\partial C/\partial K\le0$).

<a id="put-call-parity"></a>

## Put–Call Parity
<!-- section: put-call-parity | prerequisites: [no-arbitrage, forward-pricing, option-payoffs-moneyness] | related: [implied-forward-regression, otm-stitching, implied-volatility, black-scholes-formula, binomial-replication] | sources: [src-quant-study-notes-pcp-skew, src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [parity, replication, model-free] -->

A call minus a put with the same strike and expiry pays $S_T-K$ in every state — a forward. Parity is therefore model-free and holds under any dynamics.

### Formula
$$C(K,T)-P(K,T)=S_0e^{-qT}-Ke^{-rT}=D(T)\,[F(T)-K]$$

**Variables:**

- $C,P$ European call and put prices with the same $K$ and $T$
- $S_0$ spot price
- $r$ risk-free rate
- $q$ continuous dividend yield (plus borrow)
- $D(T)=e^{-rT}$ discount factor
- $F(T)=S_0e^{(r-q)T}$ forward price

### Static replication proof

| Portfolio at $t=0$ | Cost | $S_T\ge K$ | $S_T<K$ |
|---|---|---|---|
| A: fiduciary call = call + zero-coupon bond paying $K$ | $C+Ke^{-rT}$ | $S_T$ | $K$ |
| B: protective put = put + $e^{-qT}$ shares | $P+S_0e^{-qT}$ | $S_T$ | $K$ |

- Both portfolios pay $\max(S_T,K)$ in every state ⇒ same price today ([[no-arbitrage]]).
- The argument uses no model: it holds under GBM, stochastic vol, jumps — any dynamics.

### Worked example (arbitrage)
$r=q=0$, $S_0=K=100$: $C=12$, $P=9$, but parity requires $C-P=0$. Sell the call, buy the put, buy one share, borrow 100 → +3 today, and 0 at expiry in every state.

### Four roles in vol-surface construction
1. **Same implied vol for call and put** at $(K,T)$: $C_{BS}-P_{BS}$ doesn't depend on σ, so one σ fits both → [[implied-volatility]].
2. **Extract $D$ and $F$** by regressing $C-P$ on $K$ → [[implied-forward-regression]].
3. **OTM stitching**: ITM call IV = OTM put IV → [[otm-stitching]].
4. **Data cleaning**: drop quotes violating conversion/reversal or box-spread bounds.

### Engineering use
Regression test for a pricing library: any update that breaks parity on European vanillas is a bug (RBC prep) → [[model-release-regression-testing]].

### Connections
- **Builds on:** [[no-arbitrage]], [[forward-pricing]].
- **Used by:** [[implied-forward-regression]], [[otm-stitching]], [[model-release-regression-testing]], [[black-scholes-formula]] (consistency check).
- **American options:** parity becomes an inequality ([[american-early-exercise]]).

<a id="binomial-replication"></a>

## One-Period Binomial Replication
<!-- section: binomial-replication | prerequisites: [no-arbitrage, option-payoffs-moneyness] | related: [risk-neutral-pricing, black-scholes-pde, delta-hedging] | sources: [src-squarepoint-dqa-workbook] | tags: [replication, risk-neutral, binomial] -->

If the stock can only move to two prices, a position in shares and cash reproduces any option payoff exactly. The option price is the cost of that portfolio, and it can be rewritten as a discounted expectation under an artificial "risk-neutral" probability.

### Formulas
$$\Delta=\frac{V_u-V_d}{S_u-S_d},\qquad B=(V_d-\Delta S_d)\,e^{-r\Delta t},\qquad V_0=\Delta S_0+B=e^{-r\Delta t}\big[p^*V_u+(1-p^*)V_d\big],\qquad p^*=\frac{e^{r\Delta t}-d}{u-d}$$

**Variables:**

- $S_0$ stock price today
- $S_u=uS_0$, $S_d=dS_0$ stock price after an up / down move ($u>d$)
- $V_u,V_d$ option payoff in the up / down state
- $V_0$ option price today
- $\Delta$ number of shares held
- $B$ cash in the bank (negative = borrowing)
- $r$ risk-free rate; $\Delta t$ length of the period, so $e^{r\Delta t}$ is the gross risk-free growth
- $p^*$ risk-neutral up-probability; it lies in $(0,1)$ iff $d<e^{r\Delta t}<u$ (no arbitrage)

### Worked example
$S_0=100$, up to 120 or down to 80, $r=0$, call with $K=100$ ($V_u=20$, $V_d=0$):

- $\Delta=\frac{20-0}{120-80}=0.5$, $B=0-0.5\times80=-40$, $C=0.5\times100-40=10$; $p^*=\frac{1-0.8}{1.2-0.8}=0.5$.
- A "real" up-probability of 80% is irrelevant (using it would give $0.8\times20=16$ — wrong).
- The put with $K=100$ is worth 10 by parity ($C-P=S_0-K=0$).

### Connections
- **Builds on:** [[no-arbitrage]].
- **Continuous-time limit:** [[black-scholes-pde]]. **Abstraction:** [[risk-neutral-pricing]].
- $\Delta$ here is the [[delta-hedging]] ratio; multi-period trees are used for American options ([[american-early-exercise]], [[csharp-pricing-library-example]]).

<a id="static-replication"></a>

## Static Replication
<!-- section: static-replication | prerequisites: [no-arbitrage, put-call-parity] | related: [breeden-litzenberger, digital-options, variance-swaps, call-spread-overhedge, principal-protected-note] | sources: [src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew] | tags: [replication, model-free] -->

When a payoff can be written as a fixed combination of vanilla options, bonds and the underlying, its price follows from their market prices with no model. This is the cleanest answer whenever it applies; path-dependent payoffs need dynamics (models).

### Examples
- Forward = call − put ([[put-call-parity]]).
- Digital = tight call spread ([[digital-options]], [[call-spread-overhedge]]).
- Log contract → variance-swap strip with $2/K^2$ weights ([[variance-swaps]]).
- Principal-protected note = zero-coupon bond + call ([[principal-protected-note]]).
- More generally, the whole call-price curve gives the risk-neutral density ([[breeden-litzenberger]]).

### Connections
- **Builds on:** [[no-arbitrage]], [[put-call-parity]].
- **Numerical-method map:** [[monte-carlo-pricing]].
