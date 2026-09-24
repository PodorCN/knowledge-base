---
id: volatility-models
title: "Volatility Models"
type: topic
domain: quant-models
sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Volatility Models

**Sections:** [[local-volatility-dupire]] · [[heston-model]] · [[jump-diffusion]] · [[local-stochastic-volatility]] · [[sabr]] · [[forward-smile]]

<a id="local-volatility-dupire"></a>

## Local Volatility (Dupire)
<!-- section: local-volatility-dupire | prerequisites: [volatility-surface, breeden-litzenberger] | related: [heston-model, local-stochastic-volatility, forward-smile, barrier-options, svi, pde-finite-difference] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [local-vol, dupire] -->

$$\sigma_{loc}^2(K,T)=\frac{\partial C/\partial T+(r-q)K\,\partial C/\partial K+qC}{\tfrac12K^2\,\partial^2C/\partial K^2}$$

**Variables:**

- $C(K,T)$ call-price surface
- $\sigma_{loc}(S,t)$ local vol at spot level $K$ and time $T$
- $r,q$ rate and dividend yield

| Pros | Cons |
|---|---|
| Fits today's surface **exactly**; fast PDE | **Forward smile too flat** → misprices forward-start, cliquets; wrong dynamics |

- Denominator ∝ density → numerically unstable unless the surface is smooth & arbitrage-free → fit [[svi]] first.
- Standard for short-dated barriers / first pass.

### Connections
- **Needs:** [[breeden-litzenberger]] density. **Fails at:** [[forward-smile]]. **Fixed by:** [[local-stochastic-volatility]].

<a id="heston-model"></a>

## Heston Stochastic Volatility
<!-- section: heston-model | prerequisites: [geometric-brownian-motion, ito-lemma] | related: [local-volatility-dupire, local-stochastic-volatility, volatility-skew, forward-smile, jump-diffusion] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [stochastic-vol, heston, feller] -->

$$dS_t=(r-q)S_tdt+\sqrt{v_t}S_tdW^S_t,\qquad dv_t=\kappa(\theta-v_t)dt+\xi\sqrt{v_t}dW^v_t,\qquad d\langle W^S,W^v\rangle=\rho\,dt$$

**Variables:**

- $v_t$ instantaneous variance
- κ mean-reversion speed
- θ long-run variance
- ξ vol-of-vol (smile curvature)
- ρ spot–vol correlation (skew
- negative for equity)

- **Feller:** $2\kappa\theta>\xi^2$ keeps $v_t>0$.
- Pros: realistic dynamics, semi-closed-form vanillas. Cons: can't fit short-dated skew well; calibration unstable. (Bergomi family also used.)

### Connections
- **Skew source:** ρ < 0 → [[volatility-skew]]. **Short-dated fix:** [[jump-diffusion]]. **Combined with LV:** [[local-stochastic-volatility]].

<a id="jump-diffusion"></a>

## Jump-Diffusion (Merton, Bates)
<!-- section: jump-diffusion | prerequisites: [geometric-brownian-motion, exponential-poisson-process] | related: [heston-model, volatility-skew, variance-swaps] | sources: [src-rbc-quantdev-prep] | tags: [jumps, short-dated-skew] -->

GBM + Poisson-arriving jumps (Merton); + stochastic vol (Bates).
- **Pro:** generates steep **short-dated skew** that pure diffusions can't.
- **Con:** jumps can't be delta-hedged; more parameters.
- Jumps also cause replication error in [[variance-swaps]].

<a id="local-stochastic-volatility"></a>

## Local-Stochastic Volatility (LSV)
<!-- section: local-stochastic-volatility | prerequisites: [local-volatility-dupire, heston-model] | related: [autocallables, forward-smile, monte-carlo-pricing, barrier-options] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [lsv, leverage-function, particle-method] -->

$$\frac{dS_t}{S_t}=(r-q)dt+L(S_t,t)\sqrt{v_t}\,dW_t$$

**Variables:**

- $L(S,t)$ leverage function calibrated so every vanilla is matched (particle methods standard)
- $v_t$ stochastic variance (sets how the smile evolves)

- Fits surface **exactly** + realistic dynamics → **industry standard for equity exotics**. Cons: complex, slow, needs a mixing parameter.
- Around it: discrete cash dividends near-dated/yield further out; stochastic rates for long notes; correlation matrix for multi-asset.

| Model | Fits vanillas | Dynamics | Used for |
|---|---|---|---|
| Flat BS | no | none | quoting, sanity |
| Local vol | exactly | forward smile too flat | short barriers |
| SV (Heston, Bergomi) | approx. | realistic | forward-start, vol-of-vol |
| **LSV** | exactly | realistic | equity exotics |

### Connections
- **Used to price:** [[autocallables]], [[barrier-options]], [[cliquets-forward-start]] via [[monte-carlo-pricing]].

<a id="sabr"></a>

## SABR & Normal (Bachelier) Vol
<!-- section: sabr | prerequisites: [volatility-surface] | related: [svi, swaptions, fx-vol-conventions, black-76] | sources: [src-vol-surface-exotics-notes] | tags: [sabr, rates, normal-vol] -->

Stochastic-vol smile model fitted **per expiry** (per expiry–tenor pair in rates); standard for rates and FX smiles. Since negative rates, rates vol quoted as **normal (Bachelier) vol in bp**, often with **shifted SABR**. (Hagan et al.)

### Connections
- **Equity counterpart:** [[svi]]. **Used for:** [[swaptions]] cube, [[fx-vol-conventions]].

<a id="forward-smile"></a>

## Forward Smile
<!-- section: forward-smile | prerequisites: [vol-term-structure, local-volatility-dupire] | related: [cliquets-forward-start, heston-model, local-stochastic-volatility] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [forward-skew, model-risk] -->

The smile the model implies **at a future date**. Today's surface doesn't pin it down.
- Local vol reproduces today's surface but flattens future smiles → **underprices forward skew**.
- SV / LSV keep a realistic forward smile → needed for forward-starts, cliquets.
- Classic example of "model choice changes price materially".

### Connections
- **Priced products:** [[cliquets-forward-start]]. **Right models:** [[heston-model]], [[local-stochastic-volatility]].
