---
id: implied-volatility-skew
title: "Implied Volatility & Skew"
type: topic
domain: quant-models
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew, src-quant-finance-study-notes]
---
# Implied Volatility & Skew

**Sections:** [[implied-volatility]] · [[realized-volatility]] · [[vol-term-structure]] · [[volatility-skew]] · [[fx-vol-conventions]]

<a id="implied-volatility"></a>

## Implied Volatility (inversion & quoting convention)
<!-- section: implied-volatility | prerequisites: [black-scholes-formula, root-finding] | related: [volatility-surface, realized-volatility, put-call-parity, bond-duration, otm-stitching, implied-forward-regression, black-76, american-early-exercise] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew, src-quant-finance-study-notes] | tags: [implied-vol, newton, quoting, initial-guess, manaster-koehler] -->

$$C_{BS}(F,K,T,D,\sigma)=C_{mkt},\qquad \sigma_{n+1}=\sigma_n-\frac{C_{BS}(\sigma_n)-C_{mkt}}{\mathcal V(\sigma_n)}$$

**Variables:**

- $F$ forward
- $K$ strike
- $T$ expiry
- $D$ discount factor
- σ implied vol solved for
- $\mathcal V=\partial C/\partial\sigma$ vega

### Key points
- Vega > 0 ⇒ price strictly increasing in σ ⇒ **unique** solution (if price within [[option-price-bounds]]).
- Newton converges in ~1 step near ATM (vega large, ~constant): 5000 put, mid 151.20 → 16.81%.
- Deep OTM / short-dated: vega → 0, Newton explodes → bisection / Brent. Production: Jäckel's *"Let's be rational"*. Seeds: see *Initial guess for Newton* below.
- **Call IV = put IV** at same $(K,T)$ by [[put-call-parity]].
- **Three meanings of "calibrating vol":** (1) invert each option (what desks do), (2) fit one σ to the chain (fails: −86% on 4300 put, +541% on 5700 call), (3) estimate realised vol (P-measure, risk only).
- **Circular?** Price → IV → price adds nothing for one option; value is as a common unit, an interpolator, and because European payoffs are model-free given the whole surface.

| Bond world | Option world |
|---|---|
| YTM (flat curve — false) | IV (constant σ — false) |
| Yield curve | Vol surface |
| Callable bonds need a term-structure model | Barriers/cliquets need LV/SV |

### Newton with Black-76 after a parity regression
Once [[implied-forward-regression]] gives $D$ and $F$, invert [[black-76]] (no need for $r$, $q$, dividends separately):

$$\sigma_{n+1}=\sigma_n-\frac{C(\sigma_n)-C_{mkt}}{\text{Vega}(\sigma_n)},\qquad \text{Vega}=D\,F\,\phi(d_1)\sqrt T$$

**Variables:**

- $\sigma_n$ guess at iteration $n$
- $C_{mkt}$ observed price
- $\phi(\cdot)$ standard normal pdf

**Example** (computed in Python): $D=0.96,F=102,K=100,T=1,C_{mkt}=9.00$.

| Iter | σ | Model C | Vega |
|---|---|---|---|
| 0 | 0.2000 | 8.7211 | 38.30 |
| 1 | 0.2073 | 9.0000 | 38.30 |

**IV ≈ 20.73%.** Parity put $P=9-0.96\times2=7.08$ gives the **same IV** (same $D$ and $F$).

**Practical points (自己推理):**

- Use the **OTM** option at each strike (puts for $K<F$, calls for $K>F$) → [[otm-stitching]].
- Fitting $D,F$ from data captures market-implied borrow / dividends / funding; a wrong $F$ makes call IV ≠ put IV.
- **American options:** early exercise breaks parity → de-Americanise or use a tree first ([[american-early-exercise]]); cleanest on SPX.
- Use mids; drop quotes violating $C<D\max(F-K,0)$ (no IV exists).
- Repeat per strike and expiry → **vol surface**.

### Initial guess for Newton
**Why it matters:** start too high → vega small → overshoot to negative σ; deep ITM/OTM at low σ → vega ≈ 0 → huge step.

**Option 1: Manaster–Koehler (1982)**

$$\sigma_0=\sqrt{\frac{2\,|\ln(F/K)|}{T}}\quad\Big(\text{spot form: }\sqrt{\tfrac2T\,|\ln(S/K)+rT|}\Big),\qquad \frac{\partial\,\text{Vega}}{\partial\sigma}=\text{Vega}\cdot\frac{d_1d_2}{\sigma}=0\iff d_1d_2=0\iff\sigma^2T=2|\ln(F/K)|$$

**Variables:**

- $F$ forward
- $K$ strike
- $T$ expiry
- $S$ spot
- $r$ risk-free rate

→ $\sigma_0$ is where **vega is maximal** = the **inflection point** of $C(\sigma)$ (convex below, concave above) → Newton moves monotonically and never overshoots. Fails at ATM ($\sigma_0=0$).

**Option 2: Brenner–Subrahmanyam (ATM)**

$$\sigma_0\approx\sqrt{\frac{2\pi}{T}}\cdot\frac{C}{D\,F}$$

**Variables:**

- $C$ market price
- $D$ discount factor

First-order Taylor expansion of BS at ATM; poor away from the money (Corrado–Miller 1996 adds a moneyness correction).

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

1. Check price ∈ $[D\max(F-K,0),\ DF]$; otherwise no IV exists.
2. Start from MK; if $F\approx K$, use Brenner–Subrahmanyam.
3. Safeguarded Newton: keep a bracket, bisect if a step leaves it or vega is too small (Newton/Brent hybrid, [[root-finding]]).
4. Production: **Jäckel "Let's Be Rational" (2015)**: machine precision in ~2 iterations.

**One-liner:** "Start at the vega-maximising σ, √(2|ln(F/K)|/T), the inflection point of price in σ, so Newton converges monotonically. Near ATM use Brenner–Subrahmanyam, and always keep a bisection fallback."

### Connections
- **Collect across (K,T):** [[volatility-surface]]. **Contrast:** [[realized-volatility]]. **Analogy:** [[bond-duration]] (YTM).

<a id="realized-volatility"></a>

## Realised / Historical Volatility (EWMA) & Variance Risk Premium
<!-- section: realized-volatility | prerequisites: [returns-simple-log] | related: [implied-volatility, gamma-theta-pnl, variance-swaps, risk-neutral-pricing] | sources: [src-vol-surface-exotics-notes] | tags: [ewma, garch, vrp] -->

$$\hat\sigma_{ann}=\mathrm{std}(r_t)\sqrt{252},\qquad \sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)r_{t-1}^2$$

**Variables:**

- $r_t$ daily log return
- 252 trading days/yr
- λ EWMA decay (0.94 daily, RiskMetrics)

- 1% daily std → ≈ 15.9% annual.
- P-measure (risk, forecasting) vs implied = Q-measure (pricing). Implied usually > subsequently realised → **variance risk premium**.

### Connections
- **Traded against implied via:** [[gamma-theta-pnl]], [[variance-swaps]].

<a id="vol-term-structure"></a>

## Vol Term Structure, Forward Vol & Event Variance
<!-- section: vol-term-structure | prerequisites: [implied-volatility] | related: [volatility-surface, surface-no-arbitrage, forward-smile, cliquets-forward-start] | sources: [src-vol-surface-exotics-notes] | tags: [forward-vol, total-variance, earnings] -->

$$\bar\sigma^2=\frac1T\int_0^T\sigma(t)^2dt,\qquad \sigma_{fwd}(T_1,T_2)=\sqrt{\frac{\sigma_2^2T_2-\sigma_1^2T_1}{T_2-T_1}},\qquad \sigma_T^2T=\sigma_{base}^2T+\sigma_{event}^2$$

**Variables:**

- σ(t) instantaneous deterministic vol
- $\bar\sigma$ RMS vol to plug into BS
- $\sigma_1,\sigma_2$ implied vols for $T_1<T_2$
- $\sigma_{base}$ diffusive vol
- $\sigma_{event}$ std of the one-day event move

### Examples
- 3M 20%, 6M 22% → forward vol $\sqrt{(0.0242-0.01)/0.25}=23.8\%$.
- Base 25%, 1M expiry spanning earnings at 40% → $\sigma_{event}^2=(0.16-0.0625)/12=0.0081$ → ±9% implied move.

### Key idea
**Total variance $w=\sigma^2T$ is additive in time** → interpolate in $w$ (at constant log-moneyness), require $w$ non-decreasing in $T$.

### Connections
- **Constraint:** calendar arbitrage in [[surface-no-arbitrage]]. **Future smiles:** [[forward-smile]].

<a id="volatility-skew"></a>

## Volatility Skew & Smile (why equity skew is negative)
<!-- section: volatility-skew | prerequisites: [volatility-surface] | related: [digital-options, variance-swaps, autocallables, heston-model, jump-diffusion, fx-vol-conventions] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes, src-quant-study-notes-pcp-skew] | tags: [skew, smile, leverage-effect] -->

- **Skew** (left wing up) = equity; **smile** (both wings up) = FX typical.
- 3M chain, S = 100: 90 put 26% (price 1.45 vs 0.71 at flat 20%) — the market charges ~2× for downside protection.

### Why equity skew is negative
1. **Leverage effect** — price ↓ → leverage ↑ → vol ↑.
2. **Crash fear** — hedgers' demand for downside puts (post-1987).
3. **Supply of upside calls** from overwriters.
→ OTM puts richer than OTM calls; $\partial\sigma/\partial K<0$.

### Where skew shows up in prices
- [[digital-options]]: skew term $-\mathcal V\,\partial\sigma/\partial K>0$ makes digital calls dearer.
- [[variance-swaps]]: $1/K^2$ weights on expensive puts → var strike > ATM vol.
- [[autocallables]]: investor sells a deep OTM put priced in the steep part of the skew.
- [[sticky-strike-vs-sticky-moneyness]]: skew makes delta depend on dynamics.

### Models producing skew
Heston ρ < 0 ([[heston-model]]); jumps for short-dated skew ([[jump-diffusion]]); SVI ρ parameter.

<a id="fx-vol-conventions"></a>

## FX Vol Quoting (ATM, Risk Reversal, Butterfly)
<!-- section: fx-vol-conventions | prerequisites: [volatility-surface] | related: [second-order-greeks, sabr, volatility-skew] | sources: [src-vol-surface-exotics-notes] | tags: [fx, risk-reversal, butterfly, delta-quoting] -->

$$\sigma_{25C}=\sigma_{ATM}+\tfrac12RR+BF,\qquad \sigma_{25P}=\sigma_{ATM}-\tfrac12RR+BF$$

**Variables:**

- $\sigma_{ATM}$ delta-neutral straddle vol
- $RR$ 25-delta risk reversal (call vol − put vol
- skew)
- $BF$ 25-delta butterfly (avg wing − ATM
- curvature)

ATM 7.0%, RR −0.5%, BF 0.2% → 25Δ call 6.95%, put 7.45%.

- OTC market quotes **vol**, not price; per tenor, often also 10Δ.
- Interpolate across delta: vanna–volga (standard, not arb-free), SABR, polynomial.
- Traps: delta conventions (spot vs forward, premium-adjusted), market vs smile strangle.
