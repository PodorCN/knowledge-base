---
id: implied-volatility-skew
title: "Implied Volatility & the Volatility Surface"
type: topic
domain: quant-models
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew, src-quant-finance-study-notes]
---
# Implied Volatility & the Volatility Surface

Markets quote options in volatility, not price. This chapter explains how an implied volatility is computed and why it is used as a quoting unit, contrasts it with realised volatility, and then assembles implied vols across strikes and expiries into the volatility surface — its term structure, its skew, and the FX market's delta-based quoting conventions.

**Prerequisites:** [[black-scholes-formula]], [[black-76]], [[put-call-parity]], [[root-finding]], [[greeks]].

**Leads to:** [[vol-surface-construction]], [[local-volatility-dupire]], [[digital-options]], [[variance-swaps]].

**Sections:** [[implied-volatility]] · [[realized-volatility]] · [[volatility-surface]] · [[vol-term-structure]] · [[volatility-skew]] · [[fx-vol-conventions]]

Notation for the quant-models track: $k=\ln(K/F)$ log-moneyness, $\omega=\sigma^2T$ total implied variance, $\sigma_{\text{imp}}$ implied and $\sigma_{\text{real}}$ realised volatility, $\mathcal V$ vega, $D$ discount factor, $F$ forward.

<a id="implied-volatility"></a>

## Implied Volatility (inversion & quoting convention)
<!-- section: implied-volatility | prerequisites: [black-scholes-formula, black-76, root-finding] | related: [volatility-surface, realized-volatility, put-call-parity, bond-duration, otm-stitching, implied-forward-regression, american-early-exercise, option-price-bounds] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew, src-quant-finance-study-notes] | tags: [implied-vol, newton, quoting, initial-guess, manaster-koehler] -->

The implied volatility of an option is the single $\sigma$ that makes the Black–Scholes (Black-76) price equal to the market price. Because the price is strictly increasing in $\sigma$, the inversion has a unique solution and is solved with Newton's method.

### Formula
$$C_{BS}(F,K,T,D,\sigma)=C_{mkt},\qquad \sigma_{n+1}=\sigma_n-\frac{C_{BS}(\sigma_n)-C_{mkt}}{\mathcal V(\sigma_n)},\qquad \mathcal V=D\,F\,\phi(d_1)\sqrt T$$

**Variables:**

- $C_{BS}$ Black-76 call price ([[black-76]])
- $C_{mkt}$ observed market price (mid)
- $F$ forward
- $K$ strike
- $T$ expiry
- $D$ discount factor
- $\sigma$ implied vol solved for; $\sigma_n$ guess at iteration $n$
- $\mathcal V=\partial C/\partial\sigma$ vega ([[greeks]])
- $\phi$ standard normal pdf

### Key points
- Vega > 0 ⇒ price strictly increasing in $\sigma$ ⇒ a **unique** solution, if the price is within the [[option-price-bounds]].
- Newton converges in ~1 step near ATM (vega large and ~constant): e.g. a 5000 put with mid 151.20 → 16.81%.
- Deep OTM / short-dated: vega → 0 and Newton explodes → bisection / Brent ([[root-finding]]). Production: Jäckel's *"Let's be rational"*.
- **Call IV = put IV** at the same $(K,T)$ by [[put-call-parity]].
- **Three meanings of "calibrating vol":** (1) invert each option (what desks do); (2) fit one σ to the whole chain (fails: −86% error on the 4300 put, +541% on the 5700 call); (3) estimate realised vol ($\mathbb P$-measure, for risk only, [[realized-volatility]]).
- **Circular?** Price → IV → price adds nothing for one option; the value is as a common unit, an interpolator, and because European payoffs are model-free given the whole surface ([[volatility-surface]]).

| Bond world | Option world |
|---|---|
| YTM (flat curve — false) | IV (constant σ — false) |
| Yield curve | Vol surface |
| Callable bonds need a term-structure model | Barriers/cliquets need LV/SV |

### Worked example: Newton with Black-76 after a parity regression
Once [[implied-forward-regression]] gives $D$ and $F$, invert Black-76 directly (no need for $r$, $q$ or dividends separately). Computed in Python: $D=0.96,\ F=102,\ K=100,\ T=1,\ C_{mkt}=9.00$.

| Iter | σ | Model C | Vega |
|---|---|---|---|
| 0 | 0.2000 | 8.7211 | 38.30 |
| 1 | 0.2073 | 9.0000 | 38.30 |

**IV ≈ 20.73%.** The parity put $P=9-0.96\times(102-100)=7.08$ gives the **same IV** (same $D$ and $F$).

### Practical points (自己推理)
- Use the **OTM** option at each strike (puts for $K<F$, calls for $K>F$) → [[otm-stitching]].
- Fitting $D,F$ from data captures market-implied borrow / dividends / funding; a wrong $F$ makes call IV ≠ put IV.
- **American options:** early exercise breaks parity → de-Americanise or use a tree first ([[american-early-exercise]]); cleanest on SPX.
- Use mids; drop quotes violating $C<D\max(F-K,0)$ (no IV exists).
- Repeat per strike and expiry → the **vol surface** ([[volatility-surface]]).

### Initial guess for Newton
**Why it matters:** starting too high → vega small → overshoot to a negative σ; deep ITM/OTM at low σ → vega ≈ 0 → a huge step.

**Option 1: Manaster–Koehler (1982)**

$$\sigma_0=\sqrt{\frac{2\,|\ln(F/K)|}{T}}\quad\Big(\text{spot form: }\sqrt{\tfrac2T\,|\ln(S/K)+rT|}\Big),\qquad \frac{\partial\mathcal V}{\partial\sigma}=\mathcal V\cdot\frac{d_1d_2}{\sigma}=0\iff d_1d_2=0\iff\sigma^2T=2|\ln(F/K)|$$

**Variables:**

- $\sigma_0$ initial guess
- $F,K,T$ forward, strike, expiry
- $S$ spot; $r$ risk-free rate
- $d_1,d_2$ Black-76 terms

→ $\sigma_0$ is where **vega is maximal** = the **inflection point** of $C(\sigma)$ (convex below, concave above) → Newton moves monotonically and never overshoots. It fails at ATM ($\sigma_0=0$).

**Option 2: Brenner–Subrahmanyam (ATM)**

$$\sigma_0\approx\sqrt{\frac{2\pi}{T}}\cdot\frac{C}{D\,F}$$

**Variables:**

- $C$ market call price
- $D$ discount factor; $F$ forward; $T$ expiry

A first-order Taylor expansion of Black–Scholes at ATM (the $C\approx0.4\,S\sigma\sqrt T$ shortcut of [[black-scholes-formula]]); poor away from the money (Corrado–Miller 1996 adds a moneyness correction).

**Test** (computed; $D=0.96,F=102,T=1$):

| Case | Start | Path | Result |
|---|---|---|---|
| K=100, true 20.73% | MK 0.199 | 0.199 → 0.2073 | ✅ 1 step |
| | BS 0.230 | 0.230 → 0.2073 | ✅ 1 step |
| | 3.0 | 3.0 → −3.05 → 4.61 → −27.4 | ❌ diverges |
| K=150, true 25% | MK 0.878 | 0.878 → 0.345 → 0.269 → 0.251 → 0.250 | ✅ monotone |
| | BS 0.020 | blows up | ❌ vega ≈ 0 |
| | 3.0 | swings ± | ⚠️ unstable |

**Practical recipe (自己推理):**

1. Check the price ∈ $[D\max(F-K,0),\ DF]$; otherwise no IV exists.
2. Start from MK; if $F\approx K$, use Brenner–Subrahmanyam.
3. Safeguarded Newton: keep a bracket, bisect if a step leaves it or vega is too small (Newton/Brent hybrid, [[root-finding]]).
4. Production: **Jäckel "Let's Be Rational" (2015)**: machine precision in ~2 iterations.

**Interview answer:** "Start at the vega-maximising σ, √(2|ln(F/K)|/T), the inflection point of price in σ, so Newton converges monotonically. Near ATM use Brenner–Subrahmanyam, and always keep a bisection fallback."

### Connections
- **Builds on:** [[black-76]], [[root-finding]].
- **Collected across $(K,T)$:** [[volatility-surface]]. **Contrast:** [[realized-volatility]]. **Analogy:** [[bond-duration]] (YTM).

<a id="realized-volatility"></a>

## Realised / Historical Volatility (EWMA) & Variance Risk Premium
<!-- section: realized-volatility | prerequisites: [returns-simple-log] | related: [implied-volatility, gamma-theta-pnl, variance-swaps, risk-neutral-pricing, structural-risk-premia] | sources: [src-vol-surface-exotics-notes] | tags: [ewma, garch, vrp] -->

Realised volatility is measured from past returns under the real-world measure; implied volatility is a price under $\mathbb Q$. Implied usually exceeds subsequently realised vol, and the gap is the variance risk premium.

### Formulas
$$\hat\sigma_{\text{ann}}=\mathrm{std}(r_t)\,\sqrt{252},\qquad \sigma_t^2=\lambda\,\sigma_{t-1}^2+(1-\lambda)\,r_{t-1}^2$$

**Variables:**

- $\hat\sigma_{\text{ann}}$ annualised historical volatility
- $r_t$ daily log return
- 252 trading days per year
- $\sigma_t^2$ EWMA variance estimate for day $t$
- $\lambda$ EWMA decay (0.94 for daily data, RiskMetrics)

### Key points
- A 1% daily standard deviation → ≈ 15.9% annual.
- Realised vol is a $\mathbb P$-measure quantity (risk, forecasting); implied vol is a $\mathbb Q$-measure quantity (pricing). Implied is usually above subsequently realised → the **variance risk premium** ([[structural-risk-premia]]).

### Connections
- **Builds on:** [[returns-simple-log]].
- **Traded against implied via:** [[gamma-theta-pnl]], [[variance-swaps]].

<a id="volatility-surface"></a>

## The Volatility Surface σ(K,T)
<!-- section: volatility-surface | prerequisites: [implied-volatility] | related: [volatility-skew, vol-term-structure, vol-surface-construction, breeden-litzenberger, sticky-strike-vs-sticky-moneyness, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [smile, skew, surface] -->

Collecting the implied vols of all listed options gives a function of strike and expiry. Its departures from a flat plane measure how wrong Black–Scholes is; at the same time, the surface prices every European payoff without a model.

### Definition
$$\sigma_{\text{imp}}=f(K,T)$$

**Variables:**

- $\sigma_{\text{imp}}$ implied volatility
- $K$ strike (or log-moneyness $k=\ln(K/F)$, or delta)
- $T$ expiry

### Key points
- One point = a single option's IV; fix $T$ → the **smile/skew**; fix $K$ → the **term structure**; both → the **surface**.
- If BS were right the surface would be a flat plane. The departure from flat measures how wrong BS is (equity skew in its modern form since 1987).
- Surface ⇔ full set of call prices ⇔ risk-neutral density per maturity ([[breeden-litzenberger]]) ⇒ **European payoffs are model-free**; BS is just a coordinate system.
- **Interpolate vol (or total variance), not price**: prices are convex in $K$ and grow ~$\sqrt T$, so linear price interpolation is biased (2M 4800 put: price-interpolation 67.90, vol-interpolation 70.80, truth 71.98).
- Where BS still bites: **Greeks** (surface dynamics, [[sticky-strike-vs-sticky-moneyness]]) and **path-dependent / forward-start** payoffs ([[forward-smile]]).

### Worked example (index at 5000, synthetic)

| Expiry | ATM-forward vol | 90% strike | 110% strike | 90–110 skew |
|---|---|---|---|---|
| 1M | 14.98% | 25.84% | 11.34% | 14.5 pts |
| 3M | 16.49% | 23.30% | 11.91% | 11.4 pts |
| 6M | 17.48% | 22.43% | 13.45% | 9.0 pts |

Typical: an upward ATM term structure, with the skew flattening as maturity grows.

### Connections
- **Builds on:** [[implied-volatility]].
- **Shape:** [[vol-term-structure]], [[volatility-skew]]. **Build:** [[vol-surface-construction]]. **Dynamics:** [[sticky-strike-vs-sticky-moneyness]].
- **Models on top:** [[local-volatility-dupire]], [[heston-model]], [[local-stochastic-volatility]].

<a id="vol-term-structure"></a>

## Vol Term Structure, Forward Vol & Event Variance
<!-- section: vol-term-structure | prerequisites: [volatility-surface] | related: [surface-no-arbitrage, forward-smile, cliquets-forward-start] | sources: [src-vol-surface-exotics-notes] | tags: [forward-vol, total-variance, earnings] -->

Variance, not volatility, adds up over time. Working in total variance gives forward vols between two expiries and lets a one-day event (such as earnings) be separated from the diffusive vol.

### Formulas
$$\bar\sigma^2=\frac1T\int_0^T\sigma(t)^2\,dt,\qquad \sigma_{\text{fwd}}(T_1,T_2)=\sqrt{\frac{\sigma_2^2T_2-\sigma_1^2T_1}{T_2-T_1}},\qquad \sigma_T^2\,T=\sigma_{\text{base}}^2\,T+\sigma_{\text{event}}^2$$

**Variables:**

- $\sigma(t)$ instantaneous deterministic vol
- $\bar\sigma$ RMS vol to plug into Black–Scholes for expiry $T$
- $\sigma_1,\sigma_2$ implied vols for expiries $T_1<T_2$
- $\sigma_{\text{fwd}}(T_1,T_2)$ forward vol between $T_1$ and $T_2$
- $\sigma_T$ implied vol of an expiry spanning the event
- $\sigma_{\text{base}}$ diffusive (non-event) vol
- $\sigma_{\text{event}}$ standard deviation of the one-day event move

### Worked examples
- 3M 20%, 6M 22% → forward vol $\sqrt{(0.22^2\times0.5-0.20^2\times0.25)/0.25}=\sqrt{(0.0242-0.01)/0.25}=23.8\%$.
- Base 25%; a 1M expiry spanning earnings is at 40% → $\sigma_{\text{event}}^2=(0.40^2-0.25^2)/12=(0.16-0.0625)/12=0.0081$ → ±9% implied move.

### Key idea
**Total variance $\omega=\sigma^2T$ is additive in time** → interpolate in $\omega$ (at constant log-moneyness), and require $\omega$ to be non-decreasing in $T$ (no calendar arbitrage).

### Connections
- **Builds on:** [[volatility-surface]].
- **Constraint:** calendar arbitrage in [[surface-no-arbitrage]]. **Future smiles:** [[forward-smile]]. **Products:** [[cliquets-forward-start]].

<a id="volatility-skew"></a>

## Volatility Skew & Smile (why equity skew is negative)
<!-- section: volatility-skew | prerequisites: [volatility-surface] | related: [digital-options, variance-swaps, autocallables, heston-model, jump-diffusion, fx-vol-conventions, lognormal-distribution] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew] | tags: [skew, smile, leverage-effect] -->

In equity markets implied vol falls as the strike rises: downside puts are dear relative to Black–Scholes at a flat vol. This skew drives the prices of many exotic products.

### Definitions
- **Skew:** the left wing is up (equity). **Smile:** both wings are up (typical of FX).
- Example, 3M chain with $S$ = 100: the 90 put trades at 26% vol (price 1.45, vs 0.71 at a flat 20%) — the market charges ~2× for downside protection.

### Why equity skew is negative
1. **Leverage effect** — price ↓ → leverage ↑ → vol ↑.
2. **Crash fear** — hedgers' demand for downside puts (post-1987).
3. **Supply of upside calls** from overwriters.

→ OTM puts are richer than OTM calls; $\partial\sigma/\partial K<0$.

### Where skew shows up in prices
- [[digital-options]]: the skew term $-\mathcal V\,\partial\sigma/\partial K>0$ makes digital calls dearer.
- [[variance-swaps]]: $1/K^2$ weights on expensive puts → variance strike > ATM vol.
- [[autocallables]]: the investor sells a deep OTM put priced in the steep part of the skew.
- [[sticky-strike-vs-sticky-moneyness]]: skew makes delta depend on the surface dynamics.

### Models producing skew
Heston with $\rho<0$ ([[heston-model]]); jumps for short-dated skew ([[jump-diffusion]]); the SVI $\rho$ parameter ([[svi]]).

### Connections
- **Builds on:** [[volatility-surface]]; it is the failure of the lognormal assumption ([[lognormal-distribution]]).

<a id="fx-vol-conventions"></a>

## FX Vol Quoting (ATM, Risk Reversal, Butterfly)
<!-- section: fx-vol-conventions | prerequisites: [volatility-surface, greeks] | related: [second-order-greeks, sabr, volatility-skew] | sources: [src-vol-surface-exotics-notes] | tags: [fx, risk-reversal, butterfly, delta-quoting] -->

The OTC FX market quotes the smile directly in vol terms, per tenor, by three numbers: the ATM vol, the 25-delta risk reversal (skew) and the 25-delta butterfly (curvature).

### Formulas
$$\sigma_{25C}=\sigma_{ATM}+\tfrac12RR+BF,\qquad \sigma_{25P}=\sigma_{ATM}-\tfrac12RR+BF$$

**Variables:**

- $\sigma_{25C},\sigma_{25P}$ vols of the 25-delta call and put
- $\sigma_{ATM}$ delta-neutral straddle vol
- $RR$ 25-delta risk reversal: call vol − put vol (measures skew)
- $BF$ 25-delta butterfly: average wing vol − ATM vol (measures curvature)

### Worked example
ATM 7.0%, RR −0.5%, BF 0.2% → 25Δ call $7.0-0.25+0.2=6.95\%$, 25Δ put $7.0+0.25+0.2=7.45\%$.

### Key points
- The OTC market quotes **vol**, not price; per tenor, often also at 10Δ.
- Interpolating across delta: vanna–volga (standard, not arbitrage-free, [[second-order-greeks]]), SABR ([[sabr]]), polynomial.
- Traps: delta conventions (spot vs forward delta, premium-adjusted), market vs smile strangle.

### Connections
- **Builds on:** [[volatility-surface]], [[greeks]] (delta as the strike coordinate).
