---
id: vol-surface-construction-chapter
title: "Building the Vol Surface"
type: topic
domain: quant-models
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew]
---
# Building the Vol Surface

**Sections:** [[volatility-surface]] · [[vol-surface-construction]] · [[implied-forward-regression]] · [[otm-stitching]] · [[svi]] · [[surface-no-arbitrage]] · [[breeden-litzenberger]]

<a id="volatility-surface"></a>

## The Volatility Surface σ(K,T)
<!-- section: volatility-surface | prerequisites: [implied-volatility] | related: [volatility-skew, vol-term-structure, vol-surface-construction, breeden-litzenberger, sticky-strike-vs-sticky-moneyness, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [smile, skew, surface] -->

$$\sigma_{imp}=f(K,T)$$

**Variables:**

- $K$ strike (or moneyness $k=\ln(K/F)$, or delta)
- $T$ expiry

- One point = single option IV; fix $T$ → **smile/skew**; fix $K$ → **term structure**; both → **surface**.
- If BS were right: a flat plane. Departure from flat = how wrong BS is (equity skew in modern form since 1987).
- Surface ⇔ full set of call prices ⇔ risk-neutral density per maturity ([[breeden-litzenberger]]) ⇒ **European payoffs are model-free**; BS is just a coordinate system.
- **Interpolate vol (or total variance), not price**: prices are convex in K and grow ~√T → linear price interpolation is biased (2M 4800 put: price-interp 67.90, vol-interp 70.80, truth 71.98).
- Where BS still bites: **Greeks** (surface dynamics) and **path-dependent / forward-start** payoffs.

### Worked example (index at 5000, synthetic)
| Expiry | ATM-fwd vol | 90% | 110% | 90–110 skew |
|---|---|---|---|---|
| 1M | 14.98% | 25.84% | 11.34% | 14.5 pts |
| 3M | 16.49% | 23.30% | 11.91% | 11.4 pts |
| 6M | 17.48% | 22.43% | 13.45% | 9.0 pts |
Typical: upward ATM term structure, skew flattening with maturity.

### Connections
- **Shape:** [[volatility-skew]], [[vol-term-structure]]. **Build:** [[vol-surface-construction]]. **Dynamics:** [[sticky-strike-vs-sticky-moneyness]].
- **Models on top:** [[local-volatility-dupire]], [[heston-model]], [[local-stochastic-volatility]].

<a id="vol-surface-construction"></a>

## Building a Vol Surface (the desk recipe)
<!-- section: vol-surface-construction | prerequisites: [volatility-surface, put-call-parity] | related: [implied-forward-regression, otm-stitching, svi, surface-no-arbitrage, american-early-exercise, sticky-strike-vs-sticky-moneyness, model-risk-governance] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [pipeline, calibration, real-time] -->

### The 6-step recipe
1. **Clean quotes** — mids; drop zero bids, crossed, stale, abnormally wide (VIX drops puts after two consecutive zero-bid strikes).
2. **Extract $F$ and $D$** per expiry from parity → [[implied-forward-regression]].
3. **Invert OTM options only** (puts below F, calls above) → [[otm-stitching]].
4. **Fit a smooth smile** per expiry: [[svi]] (equity), [[sabr]] (rates/FX), spline/kernel. Weighted LS (1/spread², vega); fit **inside bid/ask**.
5. **Interpolate across expiries in total variance** $w=\sigma^2T$ at constant log-moneyness ([[vol-term-structure]]).
6. **Check no-arbitrage**: calendar, butterfly, wings → [[surface-no-arbitrage]].

Then: **state the dynamics** (sticky strike / moneyness) — Greeks are meaningless without it.

### Real-time design (RBC Q5b.10)
Ingest bid/ask → filter → forward & IV per expiry → SVI/SSVI fit with **warm start** → arbitrage checks → publish **immutable versioned snapshot** → reprice only affected trades, throttled. Speed: incremental fits, vectorised IV, expiries in parallel.

### Robustness to one bad quote
Vega / inverse-spread weights, bid–ask band, robust loss, reject no-arb violators, trader overrides with audit trail.

### Asset-class differences
- **Index:** dense listed strikes; recipe applies directly.
- **Single stock:** de-Americanise ([[american-early-exercise]]), imply discrete dividends/borrow per expiry, strip earnings event variance; thinner liquidity.
- **FX:** market quotes vols (ATM/RR/BF) → [[fx-vol-conventions]].
- **Rates:** swaption cube, normal vol, (shifted) SABR → [[sabr]].

### Daily practice
Synchronise spot/option snapshots; trading-time not calendar-time; event variance; independent price verification vs consensus (Totem), P&L explain → [[model-risk-governance]].

### Who builds them
Sell-side market makers (intraday; SVI/SSVI, Orc wing, SABR + trader overrides); buy-side consumes vendors (Bloomberg BVOL, OptionMetrics, ORATS); Cboe's VIX uses the same inputs (OTM + parity forward).

<a id="implied-forward-regression"></a>

## Implied Forward & Discount via Parity Regression
<!-- section: implied-forward-regression | prerequisites: [put-call-parity, ols-regression] | related: [forward-pricing, black-76, delta-one-products, discounting-compounding, vol-surface-construction] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [parity, ols, implied-dividend, box-spread] -->

$$Y_i=C_{mkt}(K_i)-P_{mkt}(K_i)=\underbrace{DF}_{\alpha}+\underbrace{(-D)}_{\beta}K_i\ \Rightarrow\ D=-\beta,\ \ F=\frac{\alpha}{D}=-\frac\alpha\beta$$
$$r_{imp}=-\frac{\ln D}{T},\qquad q_{imp}=r_{imp}-\frac1T\ln\frac FS$$

**Variables:**

- $C,P$ call/put mids at strike $K_i$
- $D$ discount factor
- $F$ forward
- α intercept, β slope
- $S$ spot
- $q_{imp}$ implied dividend + borrow

### Why it's needed
Discrete dividends, hard-to-borrow repo and dealer funding are unobservable; plugging in Treasury rates / dividend guesses makes call and put IVs **diverge near ATM**.

### Why regress, not solve from two strikes
Slope is fragile when strikes are close:

| Strikes used | D | implied r | F |
|---|---|---|---|
| 4900 & 5100 | 0.98250 | 7.08% ✗ | 5031.30 |
| 4300 & 5700 | 0.98966 | 4.17% | 5031.16 |
| All 15 (OLS) | 0.99004 | 4.02% | 5031.29 |
| Truth | 0.99008 | 4.00% | 5031.26 |

**F** is robust (level of the line); **D** (slope) is not. Alternative for illiquid names: take $D$ from the curve, solve $F_i=K_i+(C_i-P_i)/D$ near ATM (VIX does a version at the strike with smallest $|C-P|$).

### Interpretation
Slope = **box-spread** discount factor: $[C-P](K_1)-[C-P](K_2)=D(K_2-K_1)$. Option-implied rates ≠ Treasuries — Treasuries yield ~40 bp less (convenience yield; van Binsbergen–Diamond–Grotteria).

### Connections
- **Uses:** [[put-call-parity]] + [[ols-regression]] — a nice cross-domain link (stats ↔ derivatives).
- **Feeds:** [[black-76]] inversion, [[delta-one-products]] (implied dividends/borrow), [[vol-surface-construction]] step 2.

<a id="otm-stitching"></a>

## OTM Liquidity Stitching (why discard ITM quotes)
<!-- section: otm-stitching | prerequisites: [put-call-parity, implied-volatility] | related: [vol-surface-construction, variance-swaps] | sources: [src-quant-study-notes-pcp-skew, src-vol-surface-exotics-notes] | tags: [otm, vega, data-cleaning] -->

**Rule:** left wing ($K<F$) from OTM **puts**, right wing ($K>F$) from OTM **calls**, blend around $K\approx F$.

### Why discard deep ITM
1. **Vanishing vega:** ITM ≈ intrinsic value; $\Delta\sigma\approx\Delta\text{Price}/\mathcal V$ — a 1-tick bounce ÷ tiny vega = huge fake vol noise.
2. **Wide, stale bid–ask:** capital-heavy, costly to delta-hedge.

Nothing is lost: by [[put-call-parity]], ITM call IV = OTM put IV at the same strike, so the surface joins seamlessly at $K=F$.

Also: filter quotes violating conversion/reversal or box bounds before SVI/SABR.

### Connections
- **Same OTM strip used in:** [[variance-swaps]] / VIX. **Step 3 of:** [[vol-surface-construction]].

<a id="svi"></a>

## SVI Smile Parametrisation
<!-- section: svi | prerequisites: [volatility-surface, vol-term-structure] | related: [surface-no-arbitrage, vol-surface-construction, sabr, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [svi, ssvi, parametrisation] -->

$$w(k)=a+b\Big[\rho(k-m)+\sqrt{(k-m)^2+\sigma^2}\Big]$$

**Variables:**

- $w=\sigma_{BS}^2T$ total implied variance
- $k=\ln(K/F)$ log-moneyness
- $a$ level
- $b$ wing slope
- ρ skew/rotation ($-1<\rho<1$, negative for equity)
- $m$ horizontal shift
- σ ATM curvature

- Weighted least squares (1/spread², vega). Example 3M fit: $a=0.0012,b=0.0443,\rho=-0.595,m=0.0616,\sigma=0.0645$, 15/15 inside bid/ask.
- Linear wings in $|k|$ satisfy **Lee's bound** iff $b(1\pm\rho)\le2$.
- SSVI (surface SVI) has known no-arbitrage conditions (Gatheral & Jacquier).
- Smooth fits matter because [[local-volatility-dupire]] divides by the density.

### Connections
- **Checked by:** [[surface-no-arbitrage]]. **Alternative:** [[sabr]].

<a id="surface-no-arbitrage"></a>

## No-Arbitrage Conditions on a Vol Surface
<!-- section: surface-no-arbitrage | prerequisites: [volatility-surface, breeden-litzenberger, vol-term-structure] | related: [svi, option-price-bounds, no-arbitrage] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [calendar, butterfly, lee] -->

| Condition | Statement |
|---|---|
| **Calendar** | total variance $w(k,T)$ non-decreasing in $T$ at fixed $k$ |
| **Butterfly** | $C$ convex in $K$ ⇔ density $q_T(K)=\frac1D\partial^2C/\partial K^2\ge0$ |
| **Call spread** | $-D\le\partial C/\partial K\le0$ |
| **Wings (Lee)** | $\limsup_{|k|\to\infty}w(k)/|k|\le2$ |

**Variables:**

- $w=\sigma^2T$
- $k=\ln(K/F)$
- $C(K)$ call price
- $D$ discount factor
- $q_T$ risk-neutral density

Fit inside bid/ask ≠ done: also check stability vs yesterday's parameters and choose dynamics.

### Connections
- **From:** [[breeden-litzenberger]] (butterfly), [[vol-term-structure]] (calendar), [[option-price-bounds]] (call spread). **Parametrisation satisfying Lee:** [[svi]].

<a id="breeden-litzenberger"></a>

## Breeden–Litzenberger (density from option prices)
<!-- section: breeden-litzenberger | prerequisites: [risk-neutral-pricing, option-payoffs-moneyness] | related: [digital-options, surface-no-arbitrage, static-replication, volatility-surface] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [risk-neutral-density, butterfly, static-replication] -->

$$q_T(K)=\frac1D\frac{\partial^2C(K,T)}{\partial K^2}=e^{rT}\frac{\partial^2C}{\partial K^2},\qquad \text{Digital}(K)=-\frac{\partial C}{\partial K}$$

**Variables:**

- $q_T(K)$ risk-neutral density of $S_T$ at $K$
- $C(K,T)$ call price read off the surface
- $D=e^{-rT}$

- 1st derivative in strike → digital (tight call spread); 2nd → density (tight butterfly).
- Butterfly price ≥ 0 ⇔ density ≥ 0 → butterfly-arbitrage check.
- Surface ⇔ densities ⇔ all European payoffs priced model-free.

### Connections
- **Gives:** [[digital-options]] (1st derivative), [[surface-no-arbitrage]] (2nd). **General principle:** [[static-replication]].
