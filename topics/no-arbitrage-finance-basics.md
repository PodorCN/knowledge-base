---
id: no-arbitrage-finance-basics
title: "No-Arbitrage & Finance Basics"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-quant-study-notes-pcp-skew, src-rbc-quantdev-prep, src-quant-finance-study-notes]
---
# No-Arbitrage & Finance Basics

**Sections:** [[returns-simple-log]] · [[no-arbitrage]] · [[discounting-compounding]] · [[geometric-series-annuities]] · [[forward-pricing]] · [[bond-duration]] · [[bond-yield-measures]] · [[bond-spreads-g-z-oas]] · [[accrued-interest-bond-returns]]

<a id="returns-simple-log"></a>

## Simple vs Log Returns (stock returns)
<!-- section: returns-simple-log | prerequisites: [] | related: [jensens-inequality, geometric-brownian-motion, sharpe-ratio, accrued-interest-bond-returns, taylor-expansions] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [returns, compounding, total-return, annualisation] -->

$$R_t=\frac{P_t-P_{t-1}+D_t}{P_{t-1}},\quad r_t=\log(1+R_t),\quad 1+R_{0:T}=\prod(1+R_t),\quad r_{0:T}=\sum r_t,\quad \log(1+R)\approx R-\tfrac12R^2$$

**Variables:**

- $P_t$ price (prior / current close)
- $D_t$ cash distribution in the period (dividend on the ex-date)
- $R_t$ simple return (price return if $D_t=0$, total return otherwise)
- $r_t$ log return

- Simple returns aggregate **across assets** (portfolio = weighted sum with start-of-period weights); log returns aggregate **across time** (time-additive, symmetric, closer to normal).
- +10% then −10% = −1% (volatility drag, [[jensens-inequality]]). Average log return ≈ $\mu-\sigma^2/2$: μ = 8%, σ = 20% → ≈ 6%.
- **Annualising:** simple $(1+r_d)^{252}-1$; log $r_d\times252$.
- **Corporate actions:** use adjusted prices (splits, dividends, spin-offs, mergers, rights issues).

| Example | Result |
|---|---|
| 150 → 152.25 | price +1.50%; log 1.489% |
| Ex-div: 150 → 149.50, D = 1.20 | price −0.33%, **total +0.47%** |
| +2%, −1%, +1.5% | chained **+2.51%** (not additive 2.5%) |
| Daily avg 0.05% | annualised $(1.0005)^{252}-1=13.4\%$ |

| | Bond | Stock |
|---|---|---|
| Income accrues continuously | Yes | No |
| Needs AI | Yes | No |
| Quote | Clean | Actual |
| Return | (Dirty₁ + C − Dirty₀)/Dirty₀ | (P₁ + D − P₀)/P₀ |

Bond version: [[accrued-interest-bond-returns]].

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
<!-- section: discounting-compounding | prerequisites: [] | related: [forward-pricing, bond-duration, implied-forward-regression, geometric-series-annuities, limit-definition-e] | sources: [src-squarepoint-dqa-workbook] | tags: [present-value, discount-factor] -->

$$PV=Ke^{-rT}\ (\text{continuous}),\qquad PV=\frac{K}{(1+y)^T}\ (\text{annual}),\qquad D(T)=e^{-rT}$$

**Variables:**

- $K$ future payment
- $r$ continuously compounded rate
- $y$ annual yield
- $T$ years
- $D(T)$ discount factor

- State the convention; never mix. 1 bp = 0.01% = 0.0001.
- The option market has its **own** discount factor (box-spread rate) ≠ Treasury — see [[implied-forward-regression]].

<a id="geometric-series-annuities"></a>

## Geometric Series, Perpetuities & Annuities
<!-- section: geometric-series-annuities | prerequisites: [discounting-compounding] | related: [bond-yield-measures, bond-duration, limit-definition-e] | sources: [src-quant-finance-study-notes] | tags: [geometric-series, perpetuity, annuity, gordon] -->

### Formula
$$a+ar+ar^2+\cdots+ar^{n-1},\qquad S_n=a\,\frac{1-r^n}{1-r}\ (r\ne1),\qquad S_\infty=\frac{a}{1-r}\ (|r|<1)$$

**Variables:**

- $a$ first term
- $r$ common ratio
- $n$ number of terms
- $S_n$ sum of the first $n$ terms; if $r=1$, $S_n=na$
- $S_\infty$ infinite sum (diverges if $|r|\ge1$)

**Derivation:** $S-rS=a-ar^n\Rightarrow S=a\frac{1-r^n}{1-r}$.

**Example:** $1+\tfrac12+\tfrac14+\cdots=\frac{1}{1-0.5}=2$.

### Finance applications
$$\text{Perpetuity: }PV=\frac{C}{y},\qquad \text{Gordon: }PV=\frac{C_1}{y-g}\ (g<y),\qquad \text{Annuity: }PV=\frac{C}{y}\Big[1-\frac{1}{(1+y)^n}\Big]$$

**Variables:**

- $C$ cash flow per period; $C_1$ first-period cash flow
- $y$ discount rate per period
- $g$ growth rate per period
- $n$ number of periods

Perpetuity: $a=\frac{C}{1+y}$, $r=\frac{1}{1+y}$. Gordon: $r=\frac{1+g}{1+y}$, so $g<y$ **is** the $|r|<1$ convergence condition.

### Connections
- **Builds on:** [[discounting-compounding]]. **Used by:** [[bond-yield-measures]] (coupon stream = annuity + face).

<a id="forward-pricing"></a>

## Forward Pricing (carry, dividends, borrow)
<!-- section: forward-pricing | prerequisites: [no-arbitrage, discounting-compounding] | related: [put-call-parity, delta-one-products, implied-forward-regression, black-76] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep, src-quant-finance-study-notes] | tags: [forward, carry, dividends, repo, cash-and-carry] -->

**Core idea:** a long forward = borrow cash, buy stock today, hold to $T$. The forward price equals the cost of that replication.

$$F_0=S_0e^{rT}\ (\text{no div}),\qquad F_{0,T}=S_0e^{(r-q)T}\quad(\text{continuous yield}),\qquad F_0=\big(S_0-PV(D)\big)e^{rT},\ \ PV(D)=\sum_iD_ie^{-rt_i}$$
$$F(0,T)=\Big(S_0-\sum_{t_i\le T}D_ie^{-rt_i}\Big)e^{(r-b)T}\quad(\text{discrete divs + borrow})$$
$$V_t=S_te^{-q\tau}-Ke^{-r\tau}=(F_t-K)e^{-r\tau}\quad\text{(value of existing long forward struck at }K)$$

**Variables:**

- $F_0$ forward price agreed today
- $S_0$ spot
- $r$ continuously compounded funding / risk-free rate
- $q$ dividend yield (+borrow); cost of carry $=r-q$
- $D_i$ cash dividend with ex-date $t_i<T$
- $b$ borrow (stock-loan) cost
- $K$ delivery price fixed at inception (at inception $K=F_0\Rightarrow V=0$)
- $\tau=T-t$

### Examples
- $S=100$, $r=5\%$, 1y → $100e^{0.05}\approx105.13$.
- Continuous: $S_0=100,r=5\%,q=2\%,T=1$ → $F_0=100e^{0.03}=103.05$.
- Discrete: $D=2$ at $t=0.5$ → $PV(D)=2e^{-0.025}=1.9506$ → $F_0=98.049\times e^{0.05}=103.08$.

### Arbitrage enforcement

| If market forward... | Strategy | Name |
|---|---|---|
| $F_{mkt}>F_0$ | Borrow, buy stock, **short** forward | Cash-and-carry |
| $F_{mkt}<F_0$ | Short stock, invest, **long** forward | Reverse cash-and-carry |

### Key points
- **Forward ≠ expected future spot**: set by replication; risk preferences irrelevant.
- **"The forward is the single most important input"**: most "wrong price" tickets are dividend/borrow issues.
- Futures ≈ forwards with deterministic rates; stochastic rates correlated with the underlying → convexity difference (daily margining).
- **Frictions** (borrow cost, lending ≠ borrowing rate, t-costs) widen a no-arbitrage *band*; in practice the implied repo/borrow is backed out of the forward (自己推理).

### Connections
- **Builds on:** [[no-arbitrage]], [[discounting-compounding]].
- **Implied from options:** [[implied-forward-regression]] (parity regression gives $F$ and implied $q$).
- **Used by:** [[put-call-parity]] ($C-P=D(F-K)$), [[black-76]], [[delta-one-products]].

<a id="bond-duration"></a>

## Bond Price, Duration & Convexity
<!-- section: bond-duration | prerequisites: [discounting-compounding] | related: [implied-volatility, bond-yield-measures, taylor-expansions, greeks] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [bonds, duration, convexity, ytm] -->

$$P(y)=\sum_t\frac{CF_t}{(1+y)^t},\quad D_{Mac}=\frac{\sum_t t\,CF_t/(1+y)^t}{P},\quad D_{mod}=\frac{D_{Mac}}{1+y},\quad \frac{\Delta P}{P}\approx-D_{mod}\Delta y+\frac12C(\Delta y)^2$$

**Variables:**

- $CF_t$ cash flow at year $t$
- $y$ yield to maturity
- $C$ convexity
- $\Delta y$ yield change (decimal)

- $D_{mod}=5$, +100 bp → ≈ −5%. Local approximation (convexity, curve shape matter).
- $D_{mod}=7$, $C=60$, +100 bp: $-7\times0.01+0.5\times60\times0.0001=-7\%+0.3\%=\mathbf{-6.7\%}$. The convexity term is always positive → helps a long either way (second-order Taylor, cf. option gamma in [[greeks]]).
- **Analogy:** YTM is to bonds what [[implied-volatility]] is to options: a quoting unit from a "wrong" flat model.

<a id="bond-yield-measures"></a>

## Bond Yield Measures (nominal, current, YTM, YTC)
<!-- section: bond-yield-measures | prerequisites: [bond-duration, geometric-series-annuities] | related: [bond-spreads-g-z-oas, root-finding] | sources: [src-quant-finance-study-notes] | tags: [bonds, ytm, ytc, current-yield] -->

### Nominal & current yield
$$\text{Nominal}=\frac{C}{F},\qquad \text{Current}=\frac{C}{P}$$

**Variables:**

- $C$ annual coupon
- $F$ face value
- $P$ market price

e.g. $50/1000=5\%$; $60/950=6.32\%$.

### Yield to maturity (YTM)
$$P=\sum_{t=1}^n\frac{C}{(1+y)^t}+\frac{F}{(1+y)^n},\qquad y\approx\frac{C+(F-P)/n}{(F+P)/2}$$

**Variables:**

- $y$ YTM
- $n$ years to maturity

| Case | Inputs | Approx. YTM | Exact YTM |
|---|---|---|---|
| Discount | F=1000, 6% coupon, n=5, P=950 | $70/975=7.18\%$ | **7.23%** ✏️ (original chat: 7.19%) |
| Premium | F=1000, 8% coupon, n=10, P=1100 | $70/1050=6.67\%$ | — |

Excel: `=RATE(5, 60, -950, 1000)` → 7.23%.

### Yield to call (YTC)
Same as YTM, with call date and call price replacing maturity and face. e.g. P=1050, 7% coupon, callable in 3y at 1020: $\frac{70+(1020-1050)/3}{(1020+1050)/2}=60/1035\approx5.80\%$.

| Bond | Price vs face | Ordering |
|---|---|---|
| Par | P = F | Coupon = Current = YTM |
| Discount | P < F | Coupon < Current < YTM |
| Premium | P > F | Coupon > Current > YTM |

### Connections
- **Solved by:** [[root-finding]]. **Spreads over the curve:** [[bond-spreads-g-z-oas]].

<a id="bond-spreads-g-z-oas"></a>

## G-spread, Z-spread & OAS
<!-- section: bond-spreads-g-z-oas | prerequisites: [bond-yield-measures] | related: [bond-duration, binomial-replication, monte-carlo-pricing] | sources: [src-quant-finance-study-notes] | tags: [credit-spread, z-spread, oas, yield-curve, relative-value] -->

### Formula
$$G=y_{\text{bond}}-y_{\text{gov}},\qquad P=\sum_t\frac{CF_t}{(1+z_t+Z)^t},\qquad OAS=Z-\text{Option cost}$$

**Variables:**

- $y_{\text{bond}}$ bond YTM
- $y_{\text{gov}}$ YTM of a maturity-matched government bond
- $CF_t$ cash flow at $t$
- $z_t$ Treasury spot rate at $t$
- $Z$ Z-spread (constant add-on)
- Option cost: value of the embedded option (binomial tree / Monte Carlo)

**Mini example (3y, 5% coupon, P = 980, spots 3% / 3.5% / 4%):** Z ≈ **178 bps** ✏️ (original chat: ≈150 bps; recomputed 177.8 bps).

### Unified example: 5y, 6% annual coupon, P = 980, callable at 1000 in year 3
Spot curve: 3.00%, 3.30%, 3.60%, 3.85%, 4.00% → 5y Treasury par yield **3.97%**.

| Step | Value |
|---|---|
| YTM | **6.48%** (verified) |
| G-spread = 6.48% − 3.97% | **≈ 251 bps** ✏️ (original used 3.95% → 253) |
| Z-spread (solve) | **≈ 253 bps** ✏️ (original 258) |
| Option cost (assumed) | 45 bps |
| OAS = Z − 45 | **≈ 208 bps** ✏️ (original 213) |

| Spread | Uses full curve? | Adjusts for options? | Best for |
|---|---|---|---|
| G | No | No | Quick comparisons, bullets |
| Z | Yes | No | Precise valuation of bullets |
| OAS | Yes | Yes | Callables, MBS, structured |

- **Non-callable:** G ≈ Z = OAS.
- **Callable** (investor is short a call): OAS < Z.
- **Putable** (investor is long a put): OAS > Z.
- **Relative value:** Bond A (non-call) Z = 230 = OAS; Bond B (callable) Z = 258 but OAS = 213 → A is better value despite the lower Z. Compare structures on **OAS**.

### Interpreting Z − G
Z discounts each cash flow at its own spot rate; G uses one yield point. The gap reflects **curve shape × cash-flow timing**.

| Curve | Mechanism | Result |
|---|---|---|
| Upward | Early coupons discounted at lower short rates | **Z > G** |
| Flat | All rates equal | **Z = G** |
| Inverted | Early coupons discounted at higher short rates | **Z < G** |

Same bond, three curves (recomputed):

| Scenario | Spots (1–5y) | Treasury par yield | G | Z | Z − G |
|---|---|---|---|---|---|
| Upward | 3.00 / 3.30 / 3.60 / 3.85 / 4.00 | 3.97% | 251 | 253 | **+2** |
| Flat | 4.00 ×5 | 4.00% | 248 | 248 | **0** |
| Inverted | 5.00 / 4.70 / 4.40 / 4.15 / 4.00 | 4.03% | 245 | 243 | **−2** |

✏️ Original chat said ±5 bps; recomputed ±2 bps; the sign pattern is unchanged.

- **Magnitude drivers:** curve steepness; cash-flow profile (front-loaded / high coupon / amortising → bigger gap; zero-coupon → Z ≈ G).
- **Practical uses:** relative value across maturities; steepening can move Z vs G without any credit change; G depends on benchmark choice; in 2022–23 (2s10s ≈ −100 bps) short corporates showed Z < G. For bullets the two are usually within 5–15 bps.

**One-liner:** "G is a single-point approximation; Z is curve-aware and cash-flow weighted. Their difference measures how the curve's shape interacts with the bond's cash-flow timing."

### Connections
- **Builds on:** [[bond-yield-measures]]. **Option cost via:** [[binomial-replication]] trees or [[monte-carlo-pricing]].

<a id="accrued-interest-bond-returns"></a>

## Accrued Interest & Daily Bond Return
<!-- section: accrued-interest-bond-returns | prerequisites: [bond-yield-measures] | related: [returns-simple-log, bond-duration, bond-spreads-g-z-oas] | sources: [src-quant-finance-study-notes] | tags: [accrued-interest, day-count, clean-dirty, total-return] -->

### Accrued interest
$$AI=\frac{C_{\text{annual}}}{m}\times\frac{\text{days accrued}}{\text{days in period}},\qquad \text{Dirty}=\text{Clean}+AI$$

**Variables:**

- $C_{\text{annual}}$ annual coupon
- $m$ payments per year

| Convention | Rule | Used for |
|---|---|---|
| 30/360 | 30-day months, 360-day year | US corporates, munis |
| ACT/ACT | Actual / actual | US Treasuries |
| ACT/360 | Actual / 360 | Money market, some floaters |
| ACT/365 | Actual / 365 | UK gilts |

- Corporate, 30/360: 6% semi (\$30), last coupon Mar 15, today Jul 20 → 125/180 → $AI=20.83$; clean 985 → dirty **1005.83**.
- Treasury, ACT/ACT: 4% semi (\$20), Feb 28 → Apr 16 = 47 days of 181 → $AI=5.19$.
- Day after coupon: \$30 × 1/180 = 0.17; day before next coupon: \$30 × 179/180 = 29.83.
- Excel: `ACCRINT()`.

### Daily bond return
$$r=\frac{(P_1+AI_1+C)-(P_0+AI_0)}{P_0+AI_0}$$

**Variables:**

- $P_0,P_1$ clean price at start / end
- $AI_0,AI_1$ accrued interest at start / end
- $C$ coupon paid that day (usually 0)

| Case | Dirty₀ | Dirty₁ | Coupon | Return |
|---|---|---|---|---|
| Normal day | 98.50 + 0.80 = 99.30 | 98.65 + 0.82 = 99.47 | 0 | **+0.171%** |
| Coupon day | 99.10 + 2.50 = 101.60 | 99.05 + 0 = 99.05 | 2.50 | **−0.049%** (not −2.51%) |

- **Decomposition:** price return $=(P_1-P_0)/\text{Dirty}_0$; carry $=(AI_1-AI_0+C)/\text{Dirty}_0$; price return further splits into curve (−duration × Δy), spread (−spread duration × Δs), roll-down, convexity, residual.
- **Practical:** settlement conventions (T+1 UST, T+2 most corporates); correct day count; FX for cross-currency; coupon reinvestment assumption for indices.

### Connections
- **Stock version:** [[returns-simple-log]]. **Curve term:** [[bond-duration]].
