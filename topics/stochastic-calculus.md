---
id: stochastic-calculus
title: "Stochastic Calculus"
type: topic
domain: black-scholes
sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep]
---
# Stochastic Calculus

This chapter moves from one-period replication to continuous time. It introduces Brownian motion, Itô's lemma (the chain rule with a second-order correction), geometric Brownian motion as the stock model, martingales, and finally the risk-neutral pricing formula that the Black–Scholes chapters evaluate.

**Prerequisites:** [[normal-distribution]], [[lognormal-distribution]], [[taylor-expansions]], [[binomial-replication]].

**Leads to:** [[black-scholes-pde]], [[black-scholes-formula]], [[girsanov-risk-neutral-dynamics]], [[monte-carlo-pricing]].

**Sections:** [[brownian-motion]] · [[ito-lemma]] · [[geometric-brownian-motion]] · [[martingales-ito-isometry]] · [[risk-neutral-pricing]]

<a id="brownian-motion"></a>

## Brownian Motion
<!-- section: brownian-motion | prerequisites: [normal-distribution] | related: [ito-lemma, martingales-ito-isometry] | sources: [src-squarepoint-dqa-workbook] | tags: [wiener-process] -->

Brownian motion is the continuous-time random walk: it starts at zero, has continuous paths and independent normal increments whose variance equals elapsed time.

### Definition
$W_0=0$; paths are continuous; increments over disjoint intervals are independent; $W_t-W_s\sim N(0,t-s)$ for $s<t$. Hence

$$E[W_t]=0,\qquad \mathrm{Var}(W_t)=t,\qquad \mathrm{Cov}(W_s,W_t)=\min(s,t)$$

**Variables:**

- $W_t$ Brownian motion at time $t$
- $s,t$ times with $s<t$

### Worked example
$\mathrm{Cov}(W_2,W_5)=2$, $\mathrm{Corr}(W_2,W_5)=2/\sqrt{2\cdot5}=\sqrt{2/5}\approx0.632$.

### Key points
- Paths are continuous but nowhere differentiable; increments over $dt$ are of size $O(\sqrt{dt})$, so the quadratic variation over $[0,t]$ is $t$.

### Connections
- **Builds on:** [[normal-distribution]].
- **Next:** [[ito-lemma]] ($(dW)^2=dt$), [[martingales-ito-isometry]], [[geometric-brownian-motion]].

<a id="ito-lemma"></a>

## Itô's Lemma
<!-- section: ito-lemma | prerequisites: [brownian-motion, taylor-expansions] | related: [geometric-brownian-motion, black-scholes-pde, martingales-ito-isometry, jensens-inequality] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [ito, quadratic-variation] -->

Itô's lemma is the chain rule for functions of a diffusion. It is a second-order Taylor expansion in which $(dW)^2=dt$ is kept, because it is of the same order as $dt$.

### Formula
$$dX=a\,dt+b\,dW\ \Rightarrow\ df(t,X)=\Big(f_t+a\,f_x+\tfrac12b^2f_{xx}\Big)dt+b\,f_x\,dW$$
$$(dW)^2=dt,\qquad dt\,dW=0,\qquad (dt)^2=0$$

**Variables:**

- $X_t$ Itô process
- $a$ drift of $X$
- $b$ diffusion coefficient of $X$
- $W$ Brownian motion
- $f(t,x)$ smooth function; subscripts denote partial derivatives ($f_t=\partial f/\partial t$, $f_x$, $f_{xx}$)

### Worked examples
- $f=\ln S$ under GBM ($a=\mu S$, $b=\sigma S$) → $d\ln S=(\mu-\tfrac12\sigma^2)dt+\sigma dW$.
- $d(S^2)=(2\mu+\sigma^2)S^2dt+2\sigma S^2dW$.
- $d(W^2)=dt+2W\,dW$ ⇒ $\int_0^TW\,dW=(W_T^2-T)/2$ (mean 0, variance $T^2/2$).

### Key points
- The extra $\tfrac12 b^2f_{xx}$ term exists because $(dW)^2$ is of order $dt$ — convexity again ([[jensens-inequality]]).

### Connections
- **Builds on:** [[brownian-motion]], [[taylor-expansions]].
- **Used by:** [[geometric-brownian-motion]], [[black-scholes-pde]] (Itô on $V(S,t)$), [[gamma-theta-pnl]] (the $\tfrac12\Gamma S^2\sigma^2$ term), [[lognormal-under-q]].

<a id="geometric-brownian-motion"></a>

## Geometric Brownian Motion (GBM)
<!-- section: geometric-brownian-motion | prerequisites: [ito-lemma, lognormal-distribution] | related: [black-scholes-formula, jensens-inequality, risk-neutral-pricing, monte-carlo-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [gbm, lognormal] -->

GBM is the Black–Scholes model of a stock: returns over short intervals are normal with constant drift and volatility, so the price itself is lognormal.

### Formulas
$$dS_t=\mu S_t\,dt+\sigma S_t\,dW_t\ \Rightarrow\ S_t=S_0\exp\big[(\mu-\tfrac12\sigma^2)t+\sigma W_t\big]$$
$$E[S_t]=S_0e^{\mu t},\qquad \mathrm{Var}(S_t)=S_0^2e^{2\mu t}(e^{\sigma^2t}-1),\qquad E[\ln(S_t/S_0)]=(\mu-\tfrac12\sigma^2)t$$

**Variables:**

- $S_t$ stock price at $t$ ($S_0$ today)
- $\mu$ real-world drift (expected return)
- $\sigma$ volatility
- $W_t$ Brownian motion

The solution follows from Itô on $\ln S$ ([[ito-lemma]]); the moments from [[lognormal-distribution]] with $m=\ln S_0+(\mu-\tfrac12\sigma^2)t$, $s^2=\sigma^2t$.

### Worked example
$\mu$ = 8%, $\sigma$ = 20% → expected log return $8\%-2\%=6\%$ per year; expected simple return $e^{0.08}-1\approx8.33\%$.

### Key points
- GBM is the Black–Scholes assumption. Real markets break it (jumps, skew) → [[volatility-skew]].

### Connections
- **Builds on:** [[ito-lemma]], [[lognormal-distribution]].
- **Under $\mathbb Q$:** $\mu\to r-q$ ([[risk-neutral-pricing]]) ⇒ [[black-scholes-formula]]. **Simulated in:** [[monte-carlo-pricing]].

<a id="martingales-ito-isometry"></a>

## Martingales & Itô Isometry
<!-- section: martingales-ito-isometry | prerequisites: [brownian-motion, ito-lemma] | related: [risk-neutral-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [martingale, isometry] -->

A martingale is a process whose best forecast of the future is its current value. Itô integrals against Brownian motion are martingales, and the Itô isometry gives their variance.

### Formulas
$$E[M_t\mid\mathcal F_s]=M_s\ \ (s<t);\qquad E\Big[\int_0^TH_t\,dW_t\Big]=0,\qquad E\Big[\Big(\int_0^TH_t\,dW_t\Big)^2\Big]=E\Big[\int_0^TH_t^2\,dt\Big]$$

**Variables:**

- $M_t$ martingale
- $\mathcal F_s$ information available at time $s$
- $H_t$ adapted, square-integrable integrand
- $W_t$ Brownian motion
- $T$ horizon

### Key points
- $W_t^2$ is **not** a martingale ($E[W_t^2\mid\mathcal F_s]=W_s^2+(t-s)$); $W_t^2-t$ is.
- Martingale = zero *expected* change, not zero realised change.

### Connections
- **Builds on:** [[brownian-motion]], [[ito-lemma]].
- **Foundation of:** [[risk-neutral-pricing]] (discounted prices are $\mathbb Q$-martingales).

<a id="risk-neutral-pricing"></a>

## Risk-Neutral Pricing (ℚ vs ℙ)
<!-- section: risk-neutral-pricing | prerequisites: [martingales-ito-isometry, binomial-replication, geometric-brownian-motion] | related: [black-scholes-formula, delta-vs-itm-probability, realized-volatility, breeden-litzenberger, bs-call-setup-risk-neutral] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [risk-neutral, measure, numeraire] -->

The continuous-time version of binomial replication: the price of a replicable payoff equals its discounted expectation under the risk-neutral measure $\mathbb Q$, under which the stock drifts at $r-q$ instead of $\mu$.

### Formula
$$dS_t=(r-q)S_t\,dt+\sigma S_t\,dW_t^{\mathbb Q},\qquad V_t=e^{-r(T-t)}\,E^{\mathbb Q}\big[h(S_T)\mid\mathcal F_t\big]$$

**Variables:**

- $\mathbb Q$ risk-neutral measure ($\mathbb P$: real-world measure)
- $W_t^{\mathbb Q}$ Brownian motion under $\mathbb Q$
- $r$ risk-free rate
- $q$ continuous dividend yield
- $\sigma$ volatility
- $h(S_T)$ payoff at maturity $T$
- $V_t$ derivative value at time $t$
- $\mathcal F_t$ information at $t$

### Key points
- The price of a replicable payoff is the cost of replication; the $\mathbb Q$-expectation is a **representation** of that cost, not a claim that investors are risk-neutral.
- The physical drift $\mu$ drops out → the Black–Scholes price is independent of $\mu$.
- Incomplete markets: no unique $\mathbb Q$, hence no unique price.
- **ℙ vs ℚ:** historical/realised vol is a $\mathbb P$-number (risk, forecasting); implied vol is a $\mathbb Q$-number (pricing). The gap is the variance risk premium ([[realized-volatility]]).

### Connections
- **Discrete version:** [[binomial-replication]] ($p^*$).
- **Constructed step by step in:** [[bs-call-setup-risk-neutral]], [[girsanov-risk-neutral-dynamics]].
- **Leads to:** [[black-scholes-formula]]; $N(d_2)$ = $\mathbb Q$-probability of finishing ITM ([[delta-vs-itm-probability]]).
- **Density from prices:** [[breeden-litzenberger]].
