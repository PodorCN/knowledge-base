---
id: no-arbitrage-finance-basics
title: "No-Arbitrage & Finance Basics"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep]
---
# No-Arbitrage & Finance Basics

**Sections:** [[returns-simple-log]] · [[no-arbitrage]] · [[discounting-compounding]] · [[forward-pricing]] · [[bond-duration]]

<a id="returns-simple-log"></a>

## Simple vs Log Returns
<!-- section: returns-simple-log | prerequisites: [] | related: [jensens-inequality, geometric-brownian-motion, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [returns, compounding] -->

$$R_t=\frac{P_t-P_{t-1}+D_t}{P_{t-1}},\quad r_t=\log(1+R_t),\quad 1+R_{0:T}=\prod(1+R_t),\quad r_{0:T}=\sum r_t,\quad \log(1+R)\approx R-\tfrac12R^2$$

**Variables:**

- $P_t$ price
- $D_t$ cash distribution in the period
- $R_t$ simple return
- $r_t$ log return

- Simple returns aggregate **across assets** (portfolio = weighted sum with start-of-period weights); log returns aggregate **across time**.
- +10% then −10% = −1% (volatility drag, [[jensens-inequality]]).

<a id="no-arbitrage"></a>

## No-Arbitrage & the Law of One Price
<!-- section: no-arbitrage | prerequisites: [] | related: [put-call-parity, forward-pricing, binomial-replication, static-replication, surface-no-arbitrage] | sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew] | tags: [arbitrage, replication] -->

**Arbitrage:** cost ≤ 0 today, payoff ≥ 0 in every state, > 0 in some state (or positive cash today).

**Law of one price:** identical future cash flows in every state ⇒ same price today (else buy cheap, sell rich).

### Connections
- **The root of the whole pricing tree:**
  - [[forward-pricing]] — replicate by buying the stock with borrowed money.
  - [[put-call-parity]] — fiduciary call ≡ protective put.
  - [[binomial-replication]] → [[black-scholes-pde]] — dynamic replication.
  - [[static-replication]] — build exotic payoffs from vanillas.
  - [[surface-no-arbitrage]] — calendar / butterfly constraints on the vol surface.

<a id="discounting-compounding"></a>

## Discounting & Compounding Conventions
<!-- section: discounting-compounding | prerequisites: [] | related: [forward-pricing, bond-duration, implied-forward-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [present-value, discount-factor] -->

$$PV=Ke^{-rT}\ (\text{continuous}),\qquad PV=\frac{K}{(1+y)^T}\ (\text{annual}),\qquad D(T)=e^{-rT}$$

**Variables:**

- $K$ future payment
- $r$ continuously compounded rate
- $y$ annual yield
- $T$ years
- $D(T)$ discount factor

- State the convention; never mix. 1 bp = 0.01% = 0.0001.
- The option market has its **own** discount factor (box-spread rate) ≠ Treasury — see [[implied-forward-regression]].

<a id="forward-pricing"></a>

## Forward Pricing (carry, dividends, borrow)
<!-- section: forward-pricing | prerequisites: [no-arbitrage, discounting-compounding] | related: [put-call-parity, delta-one-products, implied-forward-regression, black-76] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [forward, carry, dividends, repo] -->

$$F_{0,T}=S_0e^{(r-q)T}\quad(\text{continuous yield}),\qquad F(0,T)=\Big(S_0-\sum_{t_i\le T}D_ie^{-rt_i}\Big)e^{(r-b)T}\quad(\text{discrete divs + borrow})$$
$$V_t=S_te^{-q\tau}-Ke^{-r\tau}=(F_t-K)e^{-r\tau}\quad\text{(value of existing long forward struck at }K)$$

**Variables:**

- $S_0$ spot
- $r$ funding rate
- $q$ dividend yield (+borrow)
- $D_i$ cash dividend with ex-date $t_i$
- $b$ borrow (stock-loan) cost
- $K$ delivery price
- $\tau=T-t$

### Key points
- Replication: buy stock, finance at $r$ → fair delivery price. A new forward is worth 0 at inception.
- Example: $S=100$, $r=5\%$, 1y → $100e^{0.05}\approx105.13$.
- **"The forward is the single most important input"** — most "wrong price" tickets are dividend/borrow issues.
- Futures ≈ forwards with deterministic rates; differ with stochastic rates (daily margining).

### Connections
- **Builds on:** [[no-arbitrage]], [[discounting-compounding]].
- **Implied from options:** [[implied-forward-regression]] (parity regression gives $F$ and implied $q$).
- **Used by:** [[put-call-parity]] ($C-P=D(F-K)$), [[black-76]], [[delta-one-products]].

<a id="bond-duration"></a>

## Bond Price & Duration
<!-- section: bond-duration | prerequisites: [discounting-compounding] | related: [implied-volatility] | sources: [src-squarepoint-dqa-workbook] | tags: [bonds, duration, ytm] -->

$$P(y)=\sum_t\frac{CF_t}{(1+y)^t},\quad D_{Mac}=\frac{\sum_t t\,CF_t/(1+y)^t}{P},\quad D_{mod}=\frac{D_{Mac}}{1+y},\quad \frac{\Delta P}{P}\approx-D_{mod}\Delta y$$

**Variables:**

- $CF_t$ cash flow at year $t$
- $y$ yield to maturity

- $D_{mod}=5$, +100 bp → ≈ −5%. Local approximation (convexity, curve shape matter).
- **Analogy:** YTM is to bonds what [[implied-volatility]] is to options — a quoting unit from a "wrong" flat model.
