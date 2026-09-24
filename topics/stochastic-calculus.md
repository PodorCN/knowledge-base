---
id: stochastic-calculus
title: "Stochastic Calculus"
type: topic
domain: stochastic-finance
sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep]
---
# Stochastic Calculus

**Sections:** [[brownian-motion]] · [[ito-lemma]] · [[geometric-brownian-motion]] · [[martingales-ito-isometry]] · [[risk-neutral-pricing]]

<a id="brownian-motion"></a>

## Brownian Motion
<!-- section: brownian-motion | prerequisites: [normal-distribution] | related: [ito-lemma, martingales-ito-isometry] | sources: [src-squarepoint-dqa-workbook] | tags: [wiener-process] -->

$W_0=0$, continuous paths, independent increments, $W_t-W_s\sim N(0,t-s)$.

$$E[W_t]=0,\quad \mathrm{Var}(W_t)=t,\quad \mathrm{Cov}(W_s,W_t)=\min(s,t)$$

**Variables:**

- $W_t$ Brownian motion at time $t$
- $s<t$

- $\mathrm{Cov}(W_2,W_5)=2$, $\mathrm{Corr}=\sqrt{2/5}\approx0.632$.
- Paths continuous, nowhere differentiable; increments over $dt$ are $O(\sqrt{dt})$ → quadratic variation $t$.

### Connections
- **Next:** [[ito-lemma]] ($(dW)^2=dt$), [[martingales-ito-isometry]], [[geometric-brownian-motion]].

<a id="ito-lemma"></a>

## Itô's Lemma
<!-- section: ito-lemma | prerequisites: [brownian-motion] | related: [geometric-brownian-motion, black-scholes-pde, martingales-ito-isometry] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [ito, quadratic-variation] -->

$$dX=a\,dt+b\,dW\ \Rightarrow\ df(t,X)=\Big(f_t+af_x+\tfrac12b^2f_{xx}\Big)dt+bf_x\,dW;\qquad (dW)^2=dt,\ dt\,dW=0,\ (dt)^2=0$$

**Variables:**

- $a$ drift
- $b$ diffusion coefficient
- $f$ smooth function
- subscripts = partial derivatives

### Quick examples
- $f=\log S$ under GBM → $d\log S=(\mu-\tfrac12\sigma^2)dt+\sigma dW$.
- $d(S^2)=(2\mu+\sigma^2)S^2dt+2\sigma S^2dW$.
- $d(W^2)=dt+2W\,dW$ ⇒ $\int_0^TW\,dW=(W_T^2-T)/2$ (mean 0, var $T^2/2$).

The extra $\tfrac12 f_{xx}$ term exists because $(dW)^2$ is order $dt$ — convexity again ([[jensens-inequality]]).

### Connections
- **Used by:** [[geometric-brownian-motion]], [[black-scholes-pde]] (Itô on $V(S,t)$), [[gamma-theta-pnl]] (the ½ΓS²σ² term).

<a id="geometric-brownian-motion"></a>

## Geometric Brownian Motion (GBM)
<!-- section: geometric-brownian-motion | prerequisites: [ito-lemma, lognormal-distribution] | related: [black-scholes-formula, jensens-inequality, risk-neutral-pricing, monte-carlo-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [gbm, lognormal] -->

$$dS=\mu S\,dt+\sigma S\,dW\ \Rightarrow\ S_t=S_0\exp\big[(\mu-\tfrac12\sigma^2)t+\sigma W_t\big]$$
$$E[S_t]=S_0e^{\mu t},\quad \mathrm{Var}(S_t)=S_0^2e^{2\mu t}(e^{\sigma^2t}-1),\quad E[\log(S_t/S_0)]=(\mu-\tfrac12\sigma^2)t$$

**Variables:**

- $\mu$ drift
- $\sigma$ volatility
- $W_t$ Brownian motion

- μ = 8%, σ = 20% → expected log return 6%; expected simple return $e^{0.08}-1\approx8.33\%$.
- The Black–Scholes assumption. Real markets break it (jumps, skew) → [[volatility-skew]].

### Connections
- **Under Q:** $\mu\to r-q$ ([[risk-neutral-pricing]]) ⇒ [[black-scholes-formula]]. **Simulated in:** [[monte-carlo-pricing]].

<a id="martingales-ito-isometry"></a>

## Martingales & Itô Isometry
<!-- section: martingales-ito-isometry | prerequisites: [brownian-motion, ito-lemma] | related: [risk-neutral-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [martingale, isometry] -->

$$E[M_t\mid\mathcal F_s]=M_s;\qquad E\Big[\int_0^TH_tdW_t\Big]=0,\quad E\Big[\Big(\int_0^TH_tdW_t\Big)^2\Big]=E\Big[\int_0^TH_t^2dt\Big]$$

**Variables:**

- $M$ martingale
- $\mathcal F_s$ information at $s$
- $H$ adapted square-integrable integrand

- $W_t^2$ is **not** a martingale ($E[W_t^2|\mathcal F_s]=W_s^2+(t-s)$); $W_t^2-t$ is.
- Martingale = zero *expected* change, not zero realised change.

### Connections
- **Foundation of:** [[risk-neutral-pricing]] (discounted prices are Q-martingales).

<a id="risk-neutral-pricing"></a>

## Risk-Neutral Pricing (Q vs P)
<!-- section: risk-neutral-pricing | prerequisites: [martingales-ito-isometry, binomial-replication] | related: [black-scholes-formula, delta-vs-itm-probability, realized-volatility, breeden-litzenberger] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [risk-neutral, measure, numeraire] -->

$$dS=(r-q)S\,dt+\sigma S\,dW^Q,\qquad V_t=e^{-r(T-t)}E^Q[h(S_T)\mid\mathcal F_t]$$

**Variables:**

- $Q$ risk-neutral measure
- $r$ rate
- $q$ dividend yield
- $h$ payoff
- $W^Q$ Q-Brownian motion

### Key points
- Price of a replicable payoff = cost of replication; Q-expectation is a **representation** of that, not a claim investors are risk-neutral.
- Physical drift μ drops out → BS price independent of μ.
- Incomplete markets: no unique Q / price.
- **P vs Q:** historical/realised vol is a P-number (risk, forecasting); implied vol is a Q-number (pricing). Gap = variance risk premium.

### Connections
- **Discrete version:** [[binomial-replication]] ($q^*$). **Leads to:** [[black-scholes-formula]]; $N(d_2)$ = Q-prob of finishing ITM ([[delta-vs-itm-probability]]).
- **Density from prices:** [[breeden-litzenberger]].
