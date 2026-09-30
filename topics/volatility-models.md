---
id: volatility-models
title: "Volatility Models"
type: topic
domain: pricing
sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Volatility Models

A surface prices European options, but exotics also depend on how the surface moves. This chapter presents the models that sit on top of the surface: local volatility (fits today exactly but gets the dynamics wrong, visible in the forward smile), stochastic volatility (Heston), jumps, the local-stochastic combination used for equity exotics, and SABR for rates and FX.

**Prerequisites:** [[volatility-surface]], [[breeden-litzenberger]], [[svi]], [[geometric-brownian-motion]], [[exponential-poisson-process]].

**Leads to:** [[barrier-options]], [[cliquets-forward-start]], [[autocallables]], [[swaptions]].

**Sections:** [[local-volatility-dupire]] · [[forward-smile]] · [[heston-model]] · [[jump-diffusion]] · [[local-stochastic-volatility]] · [[sabr]]

<a id="local-volatility-dupire"></a>

## Local Volatility (Dupire)
<!-- section: local-volatility-dupire | prerequisites: [volatility-surface, breeden-litzenberger, svi] | related: [heston-model, local-stochastic-volatility, forward-smile, barrier-options, pde-finite-difference, sticky-strike-vs-sticky-moneyness] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [local-vol, dupire] -->

Local volatility makes the instantaneous vol a deterministic function of spot and time, chosen so that the model reproduces every vanilla price. Dupire's formula reads it directly off the call-price surface.

### Formula
$$\sigma_{\text{loc}}^2(K,T)=\frac{\partial C/\partial T+(r-q)\,K\,\partial C/\partial K+q\,C}{\tfrac12K^2\,\partial^2C/\partial K^2}$$

**Variables:**

- $C(K,T)$ call-price surface
- $\sigma_{\text{loc}}(S,t)$ local vol, evaluated at spot level $S=K$ and time $t=T$
- $r$ risk-free rate; $q$ dividend yield

### Pros and cons

| Pros | Cons |
|---|---|
| Fits today's surface **exactly**; fast PDE | **Forward smile too flat** → misprices forward-starts and cliquets; wrong dynamics |

### Key points
- The denominator is proportional to the density ([[breeden-litzenberger]]) → numerically unstable unless the surface is smooth and arbitrage-free → fit [[svi]] first.
- Standard for short-dated barriers and as a first pass.

### Connections
- **Needs:** the [[breeden-litzenberger]] density. **Fails at:** [[forward-smile]]. **Fixed by:** [[local-stochastic-volatility]].
- **Implied dynamics:** ≈ sticky tree ([[sticky-strike-vs-sticky-moneyness]]).

<a id="forward-smile"></a>

## Forward Smile
<!-- section: forward-smile | prerequisites: [vol-term-structure, local-volatility-dupire] | related: [cliquets-forward-start, heston-model, local-stochastic-volatility] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [forward-skew, model-risk] -->

The forward smile is the smile a model implies **at a future date**. Today's surface does not pin it down, so models that fit today equally well can disagree about it.

### Key points
- Local vol reproduces today's surface but flattens future smiles → it **underprices forward skew**.
- SV / LSV keep a realistic forward smile → needed for forward-starts and cliquets.
- The classic example of "model choice changes price materially".

### Connections
- **Builds on:** [[vol-term-structure]], [[local-volatility-dupire]].
- **Priced products:** [[cliquets-forward-start]]. **Right models:** [[heston-model]], [[local-stochastic-volatility]].

<a id="heston-model"></a>

## Heston Stochastic Volatility
<!-- section: heston-model | prerequisites: [geometric-brownian-motion, ito-lemma] | related: [local-volatility-dupire, local-stochastic-volatility, volatility-skew, forward-smile, jump-diffusion] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [stochastic-vol, heston, feller] -->

In Heston's model the variance is itself random and mean-reverting, and correlated with the stock. Negative correlation produces the equity skew; the vol of variance produces curvature.

### Formula
$$dS_t=(r-q)S_t\,dt+\sqrt{v_t}\,S_t\,dW^S_t,\qquad dv_t=\kappa(\bar v-v_t)\,dt+\xi\sqrt{v_t}\,dW^v_t,\qquad d\langle W^S,W^v\rangle_t=\rho\,dt$$

**Variables:**

- $S_t$ spot; $r$ rate; $q$ dividend yield
- $v_t$ instantaneous variance
- $\kappa$ mean-reversion speed
- $\bar v$ long-run variance
- $\xi$ vol-of-vol (controls smile curvature)
- $\rho$ spot–vol correlation (controls skew; negative for equity)
- $W^S,W^v$ Brownian motions of spot and variance

### Key points
- **Feller condition:** $2\kappa\bar v>\xi^2$ keeps $v_t>0$.
- Pros: realistic dynamics, semi-closed-form vanilla prices. Cons: can't fit short-dated skew well; calibration unstable. (The Bergomi family is also used.)

### Connections
- **Builds on:** [[geometric-brownian-motion]], [[ito-lemma]].
- **Skew source:** $\rho<0$ → [[volatility-skew]]. **Short-dated fix:** [[jump-diffusion]]. **Combined with LV:** [[local-stochastic-volatility]].

<a id="jump-diffusion"></a>

## Jump-Diffusion (Merton, Bates)
<!-- section: jump-diffusion | prerequisites: [geometric-brownian-motion, exponential-poisson-process] | related: [heston-model, volatility-skew, variance-swaps] | sources: [src-rbc-quantdev-prep] | tags: [jumps, short-dated-skew] -->

Adding Poisson-arriving jumps to GBM (Merton), or to a stochastic-vol model (Bates), creates the steep short-dated skew that pure diffusions cannot.

### Key points
- **Pro:** generates steep **short-dated skew** ([[volatility-skew]]).
- **Con:** jumps can't be delta-hedged; more parameters.
- Jumps also cause replication error in [[variance-swaps]].

### Connections
- **Builds on:** [[geometric-brownian-motion]], [[exponential-poisson-process]] (jump arrivals).

<a id="local-stochastic-volatility"></a>

## Local-Stochastic Volatility (LSV)
<!-- section: local-stochastic-volatility | prerequisites: [local-volatility-dupire, heston-model] | related: [autocallables, forward-smile, monte-carlo-pricing, barrier-options] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [lsv, leverage-function, particle-method] -->

LSV multiplies a stochastic variance by a local "leverage function" calibrated so that every vanilla is still matched. It combines local vol's exact fit with stochastic vol's realistic dynamics.

### Formula
$$\frac{dS_t}{S_t}=(r-q)\,dt+L(S_t,t)\sqrt{v_t}\,dW_t$$

**Variables:**

- $S_t$ spot; $r$ rate; $q$ dividend yield
- $L(S,t)$ leverage function, calibrated so that every vanilla is matched (particle methods are standard)
- $v_t$ stochastic variance (sets how the smile evolves)
- $W_t$ Brownian motion

### Key points
- Fits the surface **exactly** + realistic dynamics → the **industry standard for equity exotics**. Cons: complex, slow, needs a mixing parameter.
- Around it: discrete cash dividends near-dated / yield further out; stochastic rates for long notes; a correlation matrix for multi-asset products.

| Model | Fits vanillas | Dynamics | Used for |
|---|---|---|---|
| Flat BS | no | none | quoting, sanity checks |
| Local vol | exactly | forward smile too flat | short barriers |
| SV (Heston, Bergomi) | approximately | realistic | forward-start, vol-of-vol |
| **LSV** | exactly | realistic | equity exotics |

### Connections
- **Builds on:** [[local-volatility-dupire]], [[heston-model]].
- **Used to price:** [[autocallables]], [[barrier-options]], [[cliquets-forward-start]] via [[monte-carlo-pricing]].

<a id="sabr"></a>

## SABR & Normal (Bachelier) Vol
<!-- section: sabr | prerequisites: [volatility-surface] | related: [svi, swaptions, fx-vol-conventions, black-76] | sources: [src-vol-surface-exotics-notes] | tags: [sabr, rates, normal-vol] -->

SABR (Hagan et al.) is a stochastic-vol smile model fitted separately per expiry, and the standard for rates and FX smiles.

### Key points
- Fitted **per expiry** (per expiry–tenor pair in rates).
- Standard for rates and FX smiles.
- Since negative rates, rates vol is quoted as **normal (Bachelier) vol in bp**, often with **shifted SABR** (in place of Black vol, [[black-76]]).

### Connections
- **Builds on:** [[volatility-surface]].
- **Equity counterpart:** [[svi]]. **Used for:** the [[swaptions]] cube, [[fx-vol-conventions]].
