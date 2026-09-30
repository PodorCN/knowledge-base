---
id: no-arbitrage-finance-basics
title: "Returns, No-Arbitrage & Forwards"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep, src-quant-finance-study-notes]
---
# Returns, No-Arbitrage & Forwards

This chapter introduces the basic financial quantities: how returns are measured and aggregated, the no-arbitrage principle, discounting conventions, geometric series for valuing cash-flow streams, and the first derivative priced purely by replication — the forward.

**Prerequisites:** [[limit-definition-e]] (continuous compounding), [[jensens-inequality]] (volatility drag).

**Leads to:** [[bond-yield-measures]] (bonds), [[put-call-parity]] (options), [[risk-neutral-pricing]], [[sharpe-ratio]], [[delta-one-products]].

**Sections:** [[returns-simple-log]] · [[no-arbitrage]] · [[discounting-compounding]] · [[geometric-series-annuities]] · [[forward-pricing]]

<a id="returns-simple-log"></a>

## Simple vs Log Returns (stock returns)
<!-- section: returns-simple-log | prerequisites: [taylor-expansions, jensens-inequality] | related: [geometric-brownian-motion, sharpe-ratio, accrued-interest-bond-returns] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [returns, compounding, total-return, annualisation] -->

A return can be measured as a simple (percentage) change or as a log change. Simple returns add up across assets; log returns add up across time.

### Formulas
$$R_t=\frac{P_t-P_{t-1}+\mathrm{Div}_t}{P_{t-1}},\qquad r_t=\ln(1+R_t),\qquad \ln(1+R)\approx R-\tfrac12R^2$$
$$1+R_{0:T}=\prod_{t=1}^T(1+R_t),\qquad r_{0:T}=\sum_{t=1}^Tr_t$$

**Variables:**

- $P_{t-1},P_t$ prior and current closing price
- $\mathrm{Div}_t$ cash distribution in the period (dividend, counted on the ex-date)
- $R_t$ simple return (price return if $\mathrm{Div}_t=0$, total return otherwise)
- $r_t$ log return
- $R_{0:T},r_{0:T}$ simple and log return over periods $1,\dots,T$

### Key points
- Simple returns aggregate **across assets** (portfolio return = weighted sum with start-of-period weights); log returns aggregate **across time** (time-additive, symmetric, closer to normal).
- +10% then −10% = −1% (volatility drag, [[jensens-inequality]]). The average log return ≈ $\mu-\sigma^2/2$: $\mu$ = 8%, $\sigma$ = 20% → ≈ 6%.
- **Annualising a daily return** $r_d$: simple $(1+r_d)^{252}-1$; log $r_d\times252$.
- **Corporate actions:** use adjusted prices (splits, dividends, spin-offs, mergers, rights issues).

### Worked examples

| Example | Result |
|---|---|
| 150 → 152.25 | price return +1.50%; log return 1.489% |
| Ex-dividend: 150 → 149.50, $\mathrm{Div}$ = 1.20 | price return −0.33%, **total return +0.47%** |
| +2%, −1%, +1.5% | chained **+2.51%** (not the additive 2.5%) |
| Daily average 0.05% | annualised $(1.0005)^{252}-1=13.4\%$ |

### Stock vs bond returns

| | Bond | Stock |
|---|---|---|
| Income accrues continuously | Yes | No |
| Needs accrued interest (AI) | Yes | No |
| Quote | Clean | Actual |
| Return | (Dirty₁ + coupon − Dirty₀)/Dirty₀ | (P₁ + Div − P₀)/P₀ |

The bond version is developed in [[accrued-interest-bond-returns]].

### Connections
- **Builds on:** [[taylor-expansions]], [[jensens-inequality]].
- **Used by:** [[sharpe-ratio]], [[realized-volatility]], [[time-series-momentum]]. **Continuous-time model:** [[geometric-brownian-motion]].

<a id="no-arbitrage"></a>

## No-Arbitrage & the Law of One Price
<!-- section: no-arbitrage | prerequisites: [] | related: [put-call-parity, forward-pricing, binomial-replication, static-replication, surface-no-arbitrage] | sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew] | tags: [arbitrage, replication] -->

All of derivatives pricing rests on one assumption: there is no free lunch. Two portfolios with the same future cash flows must cost the same today.

### Definitions
- **Arbitrage:** a strategy that costs ≤ 0 today, pays ≥ 0 in every future state, and pays > 0 in some state (or yields positive cash today with no future obligation).
- **Law of one price:** identical future cash flows in every state ⇒ the same price today (otherwise buy the cheap one, sell the rich one).

### Connections
- **The root of the whole pricing tree:**
  - [[forward-pricing]] — replicate a forward by buying the stock with borrowed money.
  - [[put-call-parity]] — fiduciary call ≡ protective put.
  - [[binomial-replication]] → [[black-scholes-pde]] — dynamic replication.
  - [[static-replication]] — build exotic payoffs from vanillas.
  - [[surface-no-arbitrage]] — calendar and butterfly constraints on the vol surface.

<a id="discounting-compounding"></a>

## Discounting & Compounding Conventions
<!-- section: discounting-compounding | prerequisites: [limit-definition-e] | related: [forward-pricing, bond-duration, implied-forward-regression, geometric-series-annuities] | sources: [src-squarepoint-dqa-workbook] | tags: [present-value, discount-factor] -->

A payment in the future is worth less today. The discount factor converts it to a present value; the formula depends on the compounding convention.

### Formulas
$$PV=Ke^{-rT}\ \ (\text{continuous}),\qquad PV=\frac{K}{(1+y)^T}\ \ (\text{annual}),\qquad D(T)=e^{-rT}$$

**Variables:**

- $PV$ present value
- $K$ amount paid at time $T$
- $r$ continuously compounded rate
- $y$ annually compounded yield
- $T$ time to payment in years
- $D(T)$ discount factor to $T$ (written $D$ when $T$ is clear)

### Key points
- State the convention and never mix conventions. 1 bp = 0.01% = 0.0001.
- The option market has its **own** discount factor (the box-spread rate), which differs from Treasuries — see [[implied-forward-regression]].

### Connections
- **Builds on:** [[limit-definition-e]].
- **Used by:** [[geometric-series-annuities]], [[forward-pricing]], [[bond-yield-measures]], [[put-call-parity]].

<a id="geometric-series-annuities"></a>

## Geometric Series, Perpetuities & Annuities
<!-- section: geometric-series-annuities | prerequisites: [discounting-compounding] | related: [bond-yield-measures, bond-duration, limit-definition-e] | sources: [src-quant-finance-study-notes] | tags: [geometric-series, perpetuity, annuity, gordon] -->

A stream of equal (or constantly growing) discounted cash flows is a geometric series, so its value has a closed form.

### Formula
$$S_n=a+ax+ax^2+\cdots+ax^{n-1}=a\,\frac{1-x^n}{1-x}\ \ (x\ne1),\qquad S_\infty=\frac{a}{1-x}\ \ (|x|<1)$$

**Variables:**

- $a$ first term
- $x$ common ratio
- $n$ number of terms
- $S_n$ sum of the first $n$ terms; if $x=1$, $S_n=na$
- $S_\infty$ infinite sum (diverges if $|x|\ge1$)

**Derivation:** $S_n-xS_n=a-ax^n\Rightarrow S_n=a\frac{1-x^n}{1-x}$.

**Example:** $1+\tfrac12+\tfrac14+\cdots=\frac{1}{1-0.5}=2$.

### Finance applications
$$\text{Perpetuity: }PV=\frac{C}{y},\qquad \text{Gordon: }PV=\frac{C_1}{y-g}\ \ (g<y),\qquad \text{Annuity: }PV=\frac{C}{y}\Big[1-\frac{1}{(1+y)^n}\Big]$$

**Variables:**

- $C$ cash flow per period (first paid one period from now)
- $C_1$ first-period cash flow of a growing stream
- $y$ discount rate per period
- $g$ growth rate per period
- $n$ number of periods

Perpetuity: $a=\frac{C}{1+y}$, $x=\frac{1}{1+y}$. Gordon: $x=\frac{1+g}{1+y}$, so $g<y$ **is** the $|x|<1$ convergence condition.

### Connections
- **Builds on:** [[discounting-compounding]].
- **Used by:** [[bond-yield-measures]] (coupon stream = annuity + face value).

<a id="forward-pricing"></a>

## Forward Pricing (carry, dividends, borrow)
<!-- section: forward-pricing | prerequisites: [no-arbitrage, discounting-compounding] | related: [put-call-parity, delta-one-products, implied-forward-regression, black-76] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-quant-finance-study-notes] | tags: [forward, carry, dividends, repo, cash-and-carry] -->

**Core idea:** a long forward can be replicated by borrowing cash, buying the stock today and holding it to $T$. By no-arbitrage the forward price equals the cost of that replication.

### Formulas
$$F_0=S_0e^{rT}\ \ (\text{no dividends}),\qquad F_0=S_0e^{(r-q)T}\ \ (\text{continuous yield}),\qquad F_0=\big(S_0-PV(\mathrm{Div})\big)e^{rT},\ \ PV(\mathrm{Div})=\sum_i\mathrm{Div}_ie^{-rt_i}$$
$$F_0=\Big(S_0-\sum_{t_i\le T}\mathrm{Div}_ie^{-rt_i}\Big)e^{(r-b)T}\quad(\text{discrete dividends + borrow})$$
$$V_t=S_te^{-q\tau}-Ke^{-r\tau}=(F_t-K)e^{-r\tau}\quad\text{(value at }t\text{ of an existing long forward struck at }K)$$

**Variables:**

- $F_0$ forward price agreed today for delivery at $T$ ($F_t$: the same at time $t$)
- $S_0,S_t$ spot price today and at $t$
- $r$ continuously compounded funding / risk-free rate
- $q$ continuous dividend yield (plus borrow cost where stated); cost of carry $=r-q$
- $\mathrm{Div}_i$ cash dividend with ex-date $t_i<T$
- $PV(\mathrm{Div})$ present value of the dividends
- $b$ borrow (stock-loan) cost
- $K$ delivery price fixed at inception (at inception $K=F_0$, so $V=0$)
- $V_t$ value of the forward contract at $t$
- $\tau=T-t$ time to maturity

### Worked examples
- $S_0=100$, $r=5\%$, $T=1$ → $F_0=100e^{0.05}\approx105.13$.
- Continuous yield: $S_0=100,r=5\%,q=2\%,T=1$ → $F_0=100e^{0.03}=103.05$.
- Discrete dividend: $\mathrm{Div}=2$ at $t=0.5$ → $PV(\mathrm{Div})=2e^{-0.025}=1.9506$ → $F_0=98.049\times e^{0.05}=103.08$.

### Arbitrage enforcement

| If the market forward... | Strategy | Name |
|---|---|---|
| $F_{mkt}>F_0$ | Borrow, buy stock, **short** forward | Cash-and-carry |
| $F_{mkt}<F_0$ | Short stock, invest, **long** forward | Reverse cash-and-carry |

### Key points
- **Forward ≠ expected future spot**: it is set by replication; risk preferences are irrelevant.
- **"The forward is the single most important input"**: most "wrong price" tickets are dividend/borrow issues.
- Futures ≈ forwards when rates are deterministic; stochastic rates correlated with the underlying create a convexity difference (daily margining).
- **Frictions** (borrow cost, lending ≠ borrowing rate, transaction costs) widen a no-arbitrage *band*; in practice the implied repo/borrow is backed out of the forward (自己推理).

### Connections
- **Builds on:** [[no-arbitrage]], [[discounting-compounding]].
- **Implied from options:** [[implied-forward-regression]] (the parity regression gives $F$ and implied $q$).
- **Used by:** [[put-call-parity]] ($C-P=D(F-K)$), [[black-76]], [[delta-one-products]], [[fx-carry-spot-slide]].
