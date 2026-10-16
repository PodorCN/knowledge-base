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

Adding Poisson-arriving jumps to GBM (Merton 1976), or to a Heston stochastic-vol process (Bates 1996), generates the steep short-dated smile/skew that pure continuous diffusions cannot produce as $T\to 0$.

### Formula
$$\frac{dS_t}{S_{t^-}} = (r - q - \lambda k)\,dt + \sigma\,dW_t + (J - 1)\,dN_t,\qquad \ln J \sim N(m_J, s_J^2),\qquad k = E[J - 1] = e^{m_J + \frac12 s_J^2} - 1$$
$$C_{\text{Merton}}(S_0, K, T) = \sum_{n=0}^{\infty} \frac{e^{-\lambda' T}(\lambda' T)^n}{n!}\,C_{\text{BS}}\!\left(S_0, K, T, r_n, \sigma_n^2\right)$$
$$\lambda' = \lambda(1+k),\qquad r_n = r - \lambda k + \frac{n\ln(1+k)}{T},\qquad \sigma_n^2 = \sigma^2 + \frac{n s_J^2}{T}$$

**Variables:**

- $S_t, S_{t^-}$ spot price at time $t$ and just before a jump at $t^-$ ($S_0$: initial spot)
- $r, q, \sigma, K, T$ risk-free rate, dividend yield, diffusive volatility, strike, and maturity
- $W_t$ standard Brownian motion under $\mathbb Q$
- $N_t$ Poisson counting process with intensity $\lambda > 0$ (independent of $W_t$)
- $J$ random gross jump multiplier ($S_t = J\,S_{t^-}$ at a jump), with log-jump mean $m_J$ and variance $s_J^2$
- $k = E[J-1]$ expected proportional jump size; $-\lambda k\,dt$ is the drift compensator keeping $e^{-(r-q)t}S_t$ a $\mathbb Q$-martingale
- $C_{\text{Merton}}, C_{\text{BS}}$ Merton jump-diffusion call price and standard Black–Scholes call price
- $n$ number of jumps occurring in $[0,T]$
- $\lambda', r_n, \sigma_n^2$ jump-adjusted Poisson intensity, $n$-jump effective short rate, and $n$-jump effective variance

### Key points
- **Why $-\lambda k\,dt$ appears:** Since $E[dN_t] = \lambda\,dt$ and each jump changes $S$ by $(J-1)S_{t^-}$, the expected jump contribution per $dt$ is $\lambda k\,S_{t^-}\,dt$. Subtracting $\lambda k$ from the drift ensures $E^{\mathbb Q}[S_T] = S_0 e^{(r-q)T}$ (no-arbitrage forward constraint).
- **Pro:** Generates realistic **short-dated skew and kurtosis** ($m_J < 0$ gives downside crash skew; $s_J > 0$ gives wings, [[volatility-skew]]).
- **Con:** Markets with random jump sizes are **incomplete** — jumps cannot be delta-hedged using the underlying alone, and discrete jumps create replication error ($O((\Delta S/S)^3)$) in [[variance-swaps]].

### Connections
- **Builds on:** [[geometric-brownian-motion]], [[exponential-poisson-process]] (jump arrivals).

<a id="local-stochastic-volatility"></a>

## Local-Stochastic Volatility (LSV)
<!-- section: local-stochastic-volatility | prerequisites: [local-volatility-dupire, heston-model] | related: [autocallables, forward-smile, monte-carlo-pricing, barrier-options] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [lsv, leverage-function, particle-method] -->

LSV multiplies a stochastic variance by a local "leverage function" calibrated so that every vanilla is still matched. It combines local vol's exact fit with stochastic vol's realistic dynamics.

### Formula
$$\frac{dS_t}{S_t}=(r-q)\,dt+L(S_t,t)\sqrt{v_t}\,dW_t,\qquad \sigma_{\text{loc}}^2(K,T)=L^2(K,T)\,E^{\mathbb Q}[v_T\mid S_T=K]$$

**Variables:**

- $S_t, S_T$ spot at times $t$ and $T$; $r$ rate; $q$ dividend yield
- $L(S,t)$ leverage function, calibrated via Gyöngy's theorem so that $L^2(K,T) = \sigma_{\text{loc}}^2(K,T) / E^{\mathbb Q}[v_T\mid S_T=K]$ (particle methods or Fokker–Planck PDE are standard)
- $\sigma_{\text{loc}}(K,T)$ Dupire local volatility at strike $K$ and maturity $T$
- $v_t, v_T$ stochastic variance at times $t$ and $T$ (sets how the smile evolves)
- $W_t$ Brownian motion under $\mathbb Q$

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

SABR (Hagan et al. 2002, *Stochastic Alpha, Beta, Rho*) models a single forward rate or FX forward under the $T$-forward measure with CEV backbone and lognormal stochastic volatility. Its asymptotic implied-vol formula is fitted per expiry and is the market standard for rates and FX smiles.

### Formula
$$dF_t = \alpha_t F_t^\beta\,dW_t^1,\qquad d\alpha_t = \nu\alpha_t\,dW_t^2,\qquad d\langle W^1, W^2\rangle_t = \rho\,dt$$
$$\sigma_N(K,F_0) \approx \alpha_0\,\frac{F_0 - K}{\int_K^{F_0} u^{-\beta}\,du}\left(\frac{z}{x(z)}\right)\big(1 + O(T)\big),\qquad z = \frac{\nu}{\alpha_0}(F_0 K)^{(1-\beta)/2}\ln\frac{F_0}{K}$$
$$\text{Shifted SABR (negative rates):}\quad d(F_t + s) = \alpha_t (F_t + s)^\beta\,dW_t^1$$

**Variables:**

- $F_t, F_0$ forward rate or forward price at time $t$ and today (already a martingale under the $T$-forward measure, so zero drift)
- $\alpha_t, \alpha_0$ stochastic volatility state and its initial value $\alpha_0 > 0$ (controls overall **ATM vol level**)
- $\beta\in[0,1]$ CEV backbone exponent ($\beta=0$ normal/Bachelier, $\beta=1$ lognormal/Black, $\beta=1/2$ CIR-like; usually fixed by convention before fitting $\alpha_0,\rho,\nu$)
- $\rho\in(-1,1)$ correlation between forward and volatility Brownian motions $W_t^1, W_t^2$ (controls **smile skew/slope**)
- $\nu \ge 0$ vol-of-vol (controls **smile curvature/wings**)
- $K, T$ strike and option expiry
- $\sigma_N(K,F_0)$ Hagan implied normal (Bachelier) volatility
- $z, x(z)$ dimensionless log-moneyness scaling and Hagan function $x(z)=\ln\!\big((\sqrt{1-2\rho z+z^2}+z-\rho)/(1-\rho)\big)$
- $O(T)$ maturity expansion correction term
- $u$ dummy integration variable
- $s > 0$ rate shift allowing $F_t > -s$ in negative-rate regimes

### Key points
- **Four parameters, four clear roles:** $\beta$ sets the ATM backbone dynamics ($\sigma_{\text{ATM}}\propto F_0^{\beta-1}$ for Black vol), $\alpha_0$ pins ATM level, $\rho$ tilts the skew, and $\nu$ lifts the wings (butterflies).
- **Fitted per expiry** (or per expiry $\times$ swap tenor cell in the [[swaptions]] cube) — SABR is an interpolation/hedging smile model for a single maturity $T$, not a joint term-structure model across expiries.
- **Normal (Bachelier) vol & Shifted SABR:** Because interest rates can approach or cross zero, rates desks quote **normal (Bachelier) implied vol** $\sigma_N$ in bp/year ($\sigma_N \approx F_0\,\sigma_{\text{Black}}$ near ATM, [[black-76]]) and use $\beta=0$ or Shifted SABR ($F_t + s$) to prevent $F_t^\beta$ from breaking down when $F_t \le 0$.

### Connections
- **Builds on:** [[volatility-surface]].
- **Equity counterpart:** [[svi]]. **Used for:** the [[swaptions]] cube, [[fx-vol-conventions]].
