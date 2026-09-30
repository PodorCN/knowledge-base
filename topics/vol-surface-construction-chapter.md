---
id: vol-surface-construction-chapter
title: "Building the Volatility Surface"
type: topic
domain: quant-models
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew]
---
# Building the Volatility Surface

This chapter turns raw option quotes into a clean, arbitrage-free surface. It starts with the desk recipe as a roadmap, then covers each step in turn: extracting the forward and discount factor from put–call parity, using only OTM quotes, fitting a smooth smile (SVI), the link between option prices and the risk-neutral density, and the no-arbitrage checks the finished surface must pass.

**Prerequisites:** [[volatility-surface]], [[vol-term-structure]], [[put-call-parity]], [[ols-regression]], [[risk-neutral-pricing]].

**Leads to:** [[local-volatility-dupire]] (needs a smooth, arbitrage-free surface), [[digital-options]], [[variance-swaps]].

**Sections:** [[vol-surface-construction]] · [[implied-forward-regression]] · [[otm-stitching]] · [[svi]] · [[breeden-litzenberger]] · [[surface-no-arbitrage]]

<a id="vol-surface-construction"></a>

## Building a Vol Surface (the desk recipe)
<!-- section: vol-surface-construction | prerequisites: [volatility-surface, put-call-parity] | related: [implied-forward-regression, otm-stitching, svi, surface-no-arbitrage, american-early-exercise, sticky-strike-vs-sticky-moneyness, model-risk-governance, fx-vol-conventions, sabr] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [pipeline, calibration, real-time] -->

The surface is built in six steps; the following sections of this chapter treat each step in detail.

### The 6-step recipe
1. **Clean quotes** — use mids; drop zero bids, crossed, stale and abnormally wide quotes (VIX drops puts after two consecutive zero-bid strikes).
2. **Extract $F$ and $D$** per expiry from parity → [[implied-forward-regression]].
3. **Invert OTM options only** (puts below $F$, calls above) → [[otm-stitching]].
4. **Fit a smooth smile** per expiry: [[svi]] (equity), [[sabr]] (rates/FX), spline/kernel. Weighted least squares (1/spread², vega); fit **inside bid/ask**.
5. **Interpolate across expiries in total variance** $\omega=\sigma^2T$ at constant log-moneyness ([[vol-term-structure]]).
6. **Check no-arbitrage**: calendar, butterfly, wings → [[surface-no-arbitrage]].

Then **state the dynamics** (sticky strike / moneyness): Greeks are meaningless without it ([[sticky-strike-vs-sticky-moneyness]]).

### Real-time design (RBC prep)
Ingest bid/ask → filter → forward & IV per expiry → SVI/SSVI fit with **warm start** → arbitrage checks → publish an **immutable versioned snapshot** → reprice only affected trades, throttled. Speed: incremental fits, vectorised IV, expiries in parallel.

### Robustness to one bad quote
Vega / inverse-spread weights, a bid–ask band, a robust loss, rejection of no-arbitrage violators, trader overrides with an audit trail.

### Asset-class differences
- **Index:** dense listed strikes; the recipe applies directly.
- **Single stock:** de-Americanise ([[american-early-exercise]]), imply discrete dividends/borrow per expiry, strip earnings event variance ([[vol-term-structure]]); thinner liquidity.
- **FX:** the market quotes vols (ATM/RR/BF) → [[fx-vol-conventions]].
- **Rates:** swaption cube, normal vol, (shifted) SABR → [[sabr]].

### Daily practice
Synchronise spot and option snapshots; trading time, not calendar time; event variance; independent price verification vs consensus (Totem) and P&L explain → [[model-risk-governance]].

### Who builds them
Sell-side market makers (intraday; SVI/SSVI, Orc wing, SABR + trader overrides); the buy side consumes vendors (Bloomberg BVOL, OptionMetrics, ORATS); Cboe's VIX uses the same inputs (OTM options + parity forward).

### Connections
- **Builds on:** [[volatility-surface]], [[put-call-parity]].

<a id="implied-forward-regression"></a>

## Implied Forward & Discount via Parity Regression
<!-- section: implied-forward-regression | prerequisites: [put-call-parity, ols-regression] | related: [forward-pricing, black-76, delta-one-products, discounting-compounding, vol-surface-construction] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [parity, ols, implied-dividend, box-spread] -->

Put–call parity says $C-P$ is a straight line in the strike with intercept $DF$ and slope $-D$. Regressing observed $C-P$ on $K$ across strikes therefore recovers the market's discount factor and forward, including all unobservable dividends, borrow and funding.

### Formulas
$$Y_i=C_{mkt}(K_i)-P_{mkt}(K_i)=\underbrace{DF}_{\alpha}+\underbrace{(-D)}_{\beta}\,K_i\ \Rightarrow\ D=-\beta,\qquad F=\frac{\alpha}{D}=-\frac\alpha\beta$$
$$r_{\text{imp}}=-\frac{\ln D}{T},\qquad q_{\text{imp}}=r_{\text{imp}}-\frac1T\ln\frac FS$$

**Variables:**

- $C_{mkt}(K_i),P_{mkt}(K_i)$ call and put mids at strike $K_i$
- $Y_i$ regression response
- $D$ discount factor; $F$ forward
- $\alpha$ intercept, $\beta$ slope of the OLS fit ([[ols-regression]])
- $S$ spot; $T$ expiry
- $r_{\text{imp}}$ implied rate
- $q_{\text{imp}}$ implied dividend yield + borrow

### Why it's needed
Discrete dividends, hard-to-borrow repo and dealer funding are unobservable; plugging in Treasury rates and dividend guesses makes call and put IVs **diverge near ATM**.

### Why regress, not solve from two strikes
The slope is fragile when the strikes are close:

| Strikes used | D | implied r | F |
|---|---|---|---|
| 4900 & 5100 | 0.98250 | 7.08% ✗ | 5031.30 |
| 4300 & 5700 | 0.98966 | 4.17% | 5031.16 |
| All 15 (OLS) | 0.99004 | 4.02% | 5031.29 |
| Truth | 0.99008 | 4.00% | 5031.26 |

- **F** is robust (the level of the line); **D** (the slope) is not.
- Alternative for illiquid names: take $D$ from the curve and solve $F_i=K_i+(C_i-P_i)/D$ near ATM.
- VIX does a version of this at the strike with the smallest $|C-P|$.

### Interpretation
- The slope is the **box-spread** discount factor: $[C-P](K_1)-[C-P](K_2)=D\,(K_2-K_1)$.
- Option-implied rates ≠ Treasuries — Treasuries yield ~40 bp less (convenience yield; van Binsbergen–Diamond–Grotteria).

### Connections
- **Builds on:** [[put-call-parity]] + [[ols-regression]] — a cross-domain link (statistics ↔ derivatives).
- **Feeds:** [[black-76]] inversion ([[implied-volatility]]), [[delta-one-products]] (implied dividends/borrow), step 2 of [[vol-surface-construction]].

<a id="otm-stitching"></a>

## OTM Liquidity Stitching (why discard ITM quotes)
<!-- section: otm-stitching | prerequisites: [put-call-parity, implied-volatility] | related: [vol-surface-construction, variance-swaps] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes] | tags: [otm, vega, data-cleaning] -->

At each strike only the out-of-the-money option is used: puts below the forward, calls above. Nothing is lost, because parity makes the call and put IVs equal.

### Rule
Left wing ($K<F$) from OTM **puts**, right wing ($K>F$) from OTM **calls**, blended around $K\approx F$.

### Why discard deep ITM quotes
1. **Vanishing vega:** an ITM option is worth ≈ intrinsic value; $\Delta\sigma\approx\Delta\text{Price}/\mathcal V$ — a 1-tick price bounce divided by a tiny vega is huge fake vol noise.
2. **Wide, stale bid–ask:** ITM options are capital-heavy and costly to delta-hedge.

Nothing is lost: by [[put-call-parity]], ITM call IV = OTM put IV at the same strike, so the surface joins seamlessly at $K=F$.

Also filter quotes violating conversion/reversal or box bounds before fitting SVI/SABR.

### Connections
- **Builds on:** [[put-call-parity]], [[implied-volatility]].
- **Same OTM strip used in:** [[variance-swaps]] / VIX. **Step 3 of:** [[vol-surface-construction]].

<a id="svi"></a>

## SVI Smile Parametrisation
<!-- section: svi | prerequisites: [volatility-surface, vol-term-structure] | related: [surface-no-arbitrage, vol-surface-construction, sabr, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [svi, ssvi, parametrisation] -->

SVI describes one expiry's smile with five parameters, in total variance as a function of log-moneyness. It has linear wings and known conditions for absence of arbitrage.

### Formula
$$\omega(k)=a+b\Big[\rho\,(k-m)+\sqrt{(k-m)^2+\varsigma^2}\Big]$$

**Variables:**

- $\omega=\sigma_{BS}^2T$ total implied variance
- $k=\ln(K/F)$ log-moneyness
- $a$ overall level
- $b$ wing slope
- $\rho$ skew / rotation ($-1<\rho<1$, negative for equity)
- $m$ horizontal shift
- $\varsigma$ ATM curvature (written $\sigma$ in raw SVI; renamed here to avoid confusion with volatility)

### Worked example
Weighted least squares (1/spread², vega). A 3M fit: $a=0.0012,\ b=0.0443,\ \rho=-0.595,\ m=0.0616,\ \varsigma=0.0645$; 15/15 fitted vols inside bid/ask.

### Key points
- Linear wings in $|k|$ satisfy **Lee's bound** iff $b(1\pm\rho)\le2$ ([[surface-no-arbitrage]]).
- SSVI (surface SVI) has known no-arbitrage conditions (Gatheral & Jacquier).
- Smooth fits matter because [[local-volatility-dupire]] divides by the density.

### Connections
- **Builds on:** [[volatility-surface]], [[vol-term-structure]] (total variance).
- **Checked by:** [[surface-no-arbitrage]]. **Alternative:** [[sabr]].

<a id="breeden-litzenberger"></a>

## Breeden–Litzenberger (density from option prices)
<!-- section: breeden-litzenberger | prerequisites: [risk-neutral-pricing, option-payoffs-moneyness] | related: [digital-options, surface-no-arbitrage, static-replication, volatility-surface] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [risk-neutral-density, butterfly, static-replication] -->

Differentiating call prices with respect to the strike reads off the risk-neutral distribution: the first derivative is (minus) a digital, the second derivative is the density.

### Formulas
$$f_T(K)=\frac1D\,\frac{\partial^2C(K,T)}{\partial K^2}=e^{rT}\,\frac{\partial^2C}{\partial K^2},\qquad \text{Digital}(K)=-\frac{\partial C}{\partial K}$$

**Variables:**

- $f_T(K)$ risk-neutral density of $S_T$ evaluated at $K$
- $C(K,T)$ call price read off the surface
- $D=e^{-rT}$ discount factor
- $\text{Digital}(K)$ price of a cash-or-nothing call paying 1 if $S_T>K$

### Key points
- First derivative in strike → digital (tight call spread); second derivative → density (tight butterfly).
- Butterfly price ≥ 0 ⇔ density ≥ 0 → the butterfly-arbitrage check ([[surface-no-arbitrage]]).
- Surface ⇔ densities ⇔ all European payoffs priced model-free.

### Connections
- **Builds on:** [[risk-neutral-pricing]].
- **Gives:** [[digital-options]] (1st derivative), [[surface-no-arbitrage]] (2nd derivative). **General principle:** [[static-replication]].

<a id="surface-no-arbitrage"></a>

## No-Arbitrage Conditions on a Vol Surface
<!-- section: surface-no-arbitrage | prerequisites: [breeden-litzenberger, vol-term-structure, option-price-bounds] | related: [svi, no-arbitrage] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [calendar, butterfly, lee] -->

A fitted surface can still admit arbitrage. Four conditions — calendar, butterfly, call-spread and wing (Lee) — must be checked before the surface is published.

### Conditions

| Condition | Statement |
|---|---|
| **Calendar** | total variance $\omega(k,T)$ non-decreasing in $T$ at fixed $k$ |
| **Butterfly** | $C$ convex in $K$ ⇔ density $f_T(K)=\frac1D\partial^2C/\partial K^2\ge0$ |
| **Call spread** | $-D\le\partial C/\partial K\le0$ |
| **Wings (Lee)** | $\limsup_{\lvert k\rvert\to\infty}\omega(k)/\lvert k\rvert\le2$ |

**Variables:**

- $\omega=\sigma^2T$ total implied variance
- $k=\ln(K/F)$ log-moneyness
- $C(K)$ call price
- $D$ discount factor
- $f_T$ risk-neutral density

### Key points
- A fit inside bid/ask is not the end: also check stability against yesterday's parameters and choose the dynamics.

### Connections
- **From:** [[breeden-litzenberger]] (butterfly), [[vol-term-structure]] (calendar), [[option-price-bounds]] (call spread), [[no-arbitrage]].
- **Parametrisation satisfying Lee:** [[svi]].
