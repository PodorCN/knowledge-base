---
id: implied-volatility-skew
title: "Implied Volatility & Skew"
type: topic
domain: quant-models
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew]
---
# Implied Volatility & Skew

**Sections:** [[implied-volatility]] · [[realized-volatility]] · [[vol-term-structure]] · [[volatility-skew]] · [[fx-vol-conventions]]

<a id="implied-volatility"></a>

## Implied Volatility (inversion & quoting convention)
<!-- section: implied-volatility | prerequisites: [black-scholes-formula, root-finding] | related: [volatility-surface, realized-volatility, put-call-parity, bond-duration, otm-stitching] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep, src-quant-study-notes-pcp-skew] | tags: [implied-vol, newton, quoting] -->

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
- Deep OTM / short-dated: vega → 0, Newton explodes → bisection / Brent. Production: Jäckel's *"Let's be rational"*. Good seed $\sigma_0\approx\sqrt{2\pi/T}\,C/S$.
- **Call IV = put IV** at same $(K,T)$ by [[put-call-parity]].
- **Three meanings of "calibrating vol":** (1) invert each option (what desks do), (2) fit one σ to the chain (fails: −86% on 4300 put, +541% on 5700 call), (3) estimate realised vol (P-measure, risk only).
- **Circular?** Price → IV → price adds nothing for one option; value is as a common unit, an interpolator, and because European payoffs are model-free given the whole surface.

| Bond world | Option world |
|---|---|
| YTM (flat curve — false) | IV (constant σ — false) |
| Yield curve | Vol surface |
| Callable bonds need a term-structure model | Barriers/cliquets need LV/SV |

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
