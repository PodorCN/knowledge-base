---
id: fixed-income-bonds
title: "Bonds"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes]
---
# Bonds

A bond is a stream of discounted cash flows. This chapter defines the yield measures used to quote it, the duration–convexity approximation of its interest-rate risk, the spreads used to compare it with government bonds, and the accrued-interest mechanics needed to compute its daily return.

**Prerequisites:** [[discounting-compounding]], [[geometric-series-annuities]], [[taylor-expansions]], [[returns-simple-log]].

**Leads to:** [[implied-volatility]] (the yield-to-maturity analogy), [[root-finding]] (solving for yields), [[swaptions]] (rates products).

**Sections:** [[bond-yield-measures]] · [[bond-duration]] · [[bond-spreads-g-z-oas]] · [[accrued-interest-bond-returns]]

Notation for this chapter: $P$ bond price, $M$ face (par) value, $c$ annual coupon amount, $y$ yield.

<a id="bond-yield-measures"></a>

## Bond Yield Measures (nominal, current, YTM, YTC)
<!-- section: bond-yield-measures | prerequisites: [geometric-series-annuities, discounting-compounding] | related: [bond-duration, bond-spreads-g-z-oas, root-finding] | sources: [src-quant-finance-study-notes] | tags: [bonds, ytm, ytc, current-yield] -->

A bond's yield summarises its price as a single rate. Different yield measures answer different questions: the coupon rate on face, the income on the price paid, or the single discount rate that reproduces the price.

### Nominal & current yield
$$\text{Nominal yield}=\frac{c}{M},\qquad \text{Current yield}=\frac{c}{P}$$

**Variables:**

- $c$ annual coupon amount
- $M$ face (par) value
- $P$ market price

Examples: $50/1000=5\%$; $60/950=6.32\%$.

### Yield to maturity (YTM)
$$P=\sum_{t=1}^n\frac{c}{(1+y)^t}+\frac{M}{(1+y)^n},\qquad y\approx\frac{c+(M-P)/n}{(M+P)/2}$$

**Variables:**

- $y$ yield to maturity: the single annual rate that discounts all cash flows back to the price
- $n$ years to maturity
- $c,M,P$ as above

The coupon stream is an annuity plus the face value ([[geometric-series-annuities]]); $y$ has no closed form and is solved numerically ([[root-finding]]).

| Case | Inputs | Approximate YTM | Exact YTM |
|---|---|---|---|
| Discount | $M$ = 1000, 6% coupon, $n$ = 5, $P$ = 950 | $70/975=7.18\%$ | **7.23%** ✏️ (original chat: 7.19%) |
| Premium | $M$ = 1000, 8% coupon, $n$ = 10, $P$ = 1100 | $70/1050=6.67\%$ | — |

Excel: `=RATE(5, 60, -950, 1000)` → 7.23%.

### Yield to call (YTC)
Same as YTM, with the call date and call price replacing maturity and face. Example: $P$ = 1050, 7% coupon, callable in 3 years at 1020: $\frac{70+(1020-1050)/3}{(1020+1050)/2}=60/1035\approx5.80\%$.

### Ordering of the yields

| Bond | Price vs face | Ordering |
|---|---|---|
| Par | $P=M$ | Coupon = Current = YTM |
| Discount | $P<M$ | Coupon < Current < YTM |
| Premium | $P>M$ | Coupon > Current > YTM |

### Connections
- **Builds on:** [[geometric-series-annuities]], [[discounting-compounding]].
- **Solved by:** [[root-finding]]. **Risk:** [[bond-duration]]. **Spreads over the curve:** [[bond-spreads-g-z-oas]].

<a id="bond-duration"></a>

## Bond Price, Duration & Convexity
<!-- section: bond-duration | prerequisites: [bond-yield-measures, taylor-expansions] | related: [implied-volatility, greeks] | sources: [src-squarepoint-dqa-workbook, src-quant-finance-study-notes] | tags: [bonds, duration, convexity, ytm] -->

Duration is the first-order sensitivity of a bond's price to its yield and convexity the second-order term: together they are a second-order Taylor expansion of the price–yield curve.

### Formulas
$$P(y)=\sum_t\frac{CF_t}{(1+y)^t},\qquad D_{Mac}=\frac{\sum_t t\,CF_t/(1+y)^t}{P},\qquad D_{mod}=\frac{D_{Mac}}{1+y}$$
$$\frac{\Delta P}{P}\approx-D_{mod}\,\Delta y+\frac12\,\mathcal C\,(\Delta y)^2$$

**Variables:**

- $P(y)$ bond price as a function of yield
- $CF_t$ cash flow paid at year $t$ (coupons, plus face at maturity)
- $y$ yield to maturity
- $D_{Mac}$ Macaulay duration (PV-weighted average time of the cash flows)
- $D_{mod}$ modified duration
- $\mathcal C$ convexity
- $\Delta y$ yield change (decimal)

### Worked examples
- $D_{mod}=5$, yield +100 bp → price ≈ −5%. This is a local approximation (convexity and curve shape matter).
- $D_{mod}=7$, $\mathcal C=60$, +100 bp: $-7\times0.01+0.5\times60\times0.0001=-7\%+0.3\%=\mathbf{-6.7\%}$.

### Key points
- The convexity term is always positive → it helps a long position whichever way yields move (second-order Taylor; cf. option gamma in [[greeks]]).
- **Analogy:** YTM is to bonds what [[implied-volatility]] is to options: a quoting unit from a "wrong" flat model.

### Connections
- **Builds on:** [[bond-yield-measures]], [[taylor-expansions]].
- **Used by:** [[accrued-interest-bond-returns]] (curve term of the return decomposition).

<a id="bond-spreads-g-z-oas"></a>

## G-spread, Z-spread & OAS
<!-- section: bond-spreads-g-z-oas | prerequisites: [bond-yield-measures] | related: [bond-duration, binomial-replication, monte-carlo-pricing] | sources: [src-quant-finance-study-notes] | tags: [credit-spread, z-spread, oas, yield-curve, relative-value] -->

A bond's spread measures its extra yield over government bonds. The three spreads differ in whether they use the whole curve and whether they strip out embedded options.

### Formulas
$$G=y_{\text{bond}}-y_{\text{gov}},\qquad P=\sum_t\frac{CF_t}{(1+z_t+Z)^t},\qquad OAS=Z-\text{option cost}$$

**Variables:**

- $G$ G-spread
- $y_{\text{bond}}$ bond YTM
- $y_{\text{gov}}$ YTM of a maturity-matched government bond
- $P$ bond price
- $CF_t$ cash flow at $t$
- $z_t$ government (Treasury) spot rate for maturity $t$
- $Z$ Z-spread: the constant add-on to every spot rate that reproduces the price
- $OAS$ option-adjusted spread
- $\text{option cost}$ value of the embedded option in spread terms (from a binomial tree or Monte Carlo)

### Worked example (3y, 5% coupon, $P$ = 980, spots 3% / 3.5% / 4%)
Z ≈ **178 bps** ✏️ (original chat: ≈150 bps; recomputed 177.8 bps).

### Worked example: 5y, 6% annual coupon, $P$ = 980, callable at 1000 in year 3
Spot curve: 3.00%, 3.30%, 3.60%, 3.85%, 4.00% → 5y Treasury par yield **3.97%**.

| Step | Value |
|---|---|
| YTM | **6.48%** (verified) |
| G-spread = 6.48% − 3.97% | **≈ 251 bps** ✏️ (original used 3.95% → 253) |
| Z-spread (solve) | **≈ 253 bps** ✏️ (original 258) |
| Option cost (assumed) | 45 bps |
| OAS = Z − 45 | **≈ 208 bps** ✏️ (original 213) |

### Comparison

| Spread | Uses full curve? | Adjusts for options? | Best for |
|---|---|---|---|
| G | No | No | Quick comparisons, bullets |
| Z | Yes | No | Precise valuation of bullets |
| OAS | Yes | Yes | Callables, MBS, structured |

- **Non-callable:** G ≈ Z = OAS.
- **Callable** (the investor is short a call): OAS < Z.
- **Putable** (the investor is long a put): OAS > Z.
- **Relative value:** Bond A (non-callable) Z = 230 = OAS; Bond B (callable) Z = 258 but OAS = 213 → A is better value despite the lower Z. Compare structures on **OAS**.

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
- **Practical uses:** relative value across maturities; steepening can move Z vs G without any credit change; G depends on the benchmark choice; in 2022–23 (2s10s ≈ −100 bps) short corporates showed Z < G. For bullets the two are usually within 5–15 bps.

**Interview answer:** "G is a single-point approximation; Z is curve-aware and cash-flow weighted. Their difference measures how the curve's shape interacts with the bond's cash-flow timing."

### Connections
- **Builds on:** [[bond-yield-measures]].
- **Option cost via:** [[binomial-replication]] trees or [[monte-carlo-pricing]].

<a id="accrued-interest-bond-returns"></a>

## Accrued Interest & Daily Bond Return
<!-- section: accrued-interest-bond-returns | prerequisites: [bond-yield-measures, returns-simple-log] | related: [bond-duration, bond-spreads-g-z-oas] | sources: [src-quant-finance-study-notes] | tags: [accrued-interest, day-count, clean-dirty, total-return] -->

Bonds are quoted "clean", but a buyer pays the "dirty" price, which includes the coupon earned since the last payment. A bond's return must therefore be computed on dirty prices.

### Accrued interest
$$AI=\frac{c}{m}\times\frac{\text{days accrued}}{\text{days in coupon period}},\qquad \text{Dirty}=\text{Clean}+AI$$

**Variables:**

- $AI$ accrued interest
- $c$ annual coupon amount
- $m$ coupon payments per year

Days are counted by the day-count convention in the table below.

| Convention | Rule | Used for |
|---|---|---|
| 30/360 | 30-day months, 360-day year | US corporates, munis |
| ACT/ACT | Actual / actual | US Treasuries |
| ACT/360 | Actual / 360 | Money market, some floaters |
| ACT/365 | Actual / 365 | UK gilts |

### Worked examples
- Corporate, 30/360: 6% semi-annual (30 per period), last coupon Mar 15, today Jul 20 → 125/180 → $AI=20.83$; clean 985 → dirty **1005.83**.
- Treasury, ACT/ACT: 4% semi-annual (20 per period), Feb 28 → Apr 16 = 47 days of 181 → $AI=5.19$.
- Day after a coupon: 30 × 1/180 = 0.17; day before the next coupon: 30 × 179/180 = 29.83.
- Excel: `ACCRINT()`.

### Daily bond return
$$r=\frac{(P_1+AI_1+c_{\text{paid}})-(P_0+AI_0)}{P_0+AI_0}$$

**Variables:**

- $r$ one-day total return
- $P_0,P_1$ clean price at start and end of the day
- $AI_0,AI_1$ accrued interest at start and end
- $c_{\text{paid}}$ coupon paid that day (usually 0)

| Case | Dirty₀ | Dirty₁ | Coupon | Return |
|---|---|---|---|---|
| Normal day | 98.50 + 0.80 = 99.30 | 98.65 + 0.82 = 99.47 | 0 | **+0.171%** |
| Coupon day | 99.10 + 2.50 = 101.60 | 99.05 + 0 = 99.05 | 2.50 | **−0.049%** (not −2.51%) |

### Key points
- **Decomposition:** price return $=(P_1-P_0)/\text{Dirty}_0$; carry $=(AI_1-AI_0+c_{\text{paid}})/\text{Dirty}_0$. The price return further splits into curve (−duration × Δy), spread (−spread duration × Δs), roll-down, convexity and a residual.
- **Practical:** settlement conventions (T+1 UST, T+2 most corporates); correct day count; FX for cross-currency; coupon reinvestment assumption for indices.

### Connections
- **Builds on:** [[bond-yield-measures]], [[returns-simple-log]] (stock version).
- **Curve term:** [[bond-duration]].
