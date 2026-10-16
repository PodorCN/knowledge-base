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

**Sections:** [[brownian-motion]] · [[ito-lemma]] · [[geometric-brownian-motion]] · [[ornstein-uhlenbeck-mean-reversion]] · [[martingales-ito-isometry]] · [[risk-neutral-pricing]]

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
<!-- section: ito-lemma | prerequisites: [brownian-motion, taylor-expansions] | related: [geometric-brownian-motion, ornstein-uhlenbeck-mean-reversion, black-scholes-pde, martingales-ito-isometry, jensens-inequality] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [ito, quadratic-variation] -->

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
- **Used by:** [[geometric-brownian-motion]], [[ornstein-uhlenbeck-mean-reversion]], [[black-scholes-pde]] (Itô on $V(S,t)$), [[gamma-theta-pnl]] (the $\tfrac12\Gamma S^2\sigma^2$ term), [[lognormal-under-q]].

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

<a id="ornstein-uhlenbeck-mean-reversion"></a>

## Ornstein–Uhlenbeck (Vasicek) & Mean Reversion
<!-- section: ornstein-uhlenbeck-mean-reversion | prerequisites: [ito-lemma, stationarity-ar1] | related: [martingales-ito-isometry, heston-model] | sources: [src-squarepoint-dqa-workbook, src-rbc-quantdev-prep] | tags: [ou-process, vasicek, mean-reversion, half-life] -->

The Ornstein–Uhlenbeck (OU) process is the continuous-time counterpart of a stationary AR(1): a linear restoring force pulls $X_t$ back toward its long-run mean $\theta$ at speed $\kappa$, while additive Gaussian noise drives fluctuations.

### Formulas
$$dX_t = \kappa(\theta - X_t)\,dt + \sigma\,dW_t\ \Rightarrow\ X_t = \theta + (X_0 - \theta)e^{-\kappa t} + \sigma\int_0^t e^{-\kappa(t-s)}\,dW_s$$
$$E[X_t\mid X_0] = \theta + (X_0 - \theta)e^{-\kappa t},\qquad \mathrm{Var}(X_t\mid X_0) = \frac{\sigma^2}{2\kappa}\big(1 - e^{-2\kappa t}\big),\qquad X_\infty \sim N\!\left(\theta,\,\frac{\sigma^2}{2\kappa}\right)$$
$$\text{Half-life:}\quad t_{1/2} = \frac{\ln 2}{\kappa},\qquad \text{Exact } \Delta t \text{ AR(1):}\quad X_{t+\Delta t} = \theta(1 - e^{-\kappa\Delta t}) + e^{-\kappa\Delta t} X_t + \varepsilon_{t,\Delta t}$$

**Variables:**

- $X_t, X_0, X_\infty$ state at time $t$, initial state, and stationary long-run distribution as $t\to\infty$
- $\kappa > 0$ mean-reversion speed
- $\theta$ long-run equilibrium mean
- $\sigma > 0$ volatility of innovations
- $W_t$ standard Brownian motion ($s$: integration time variable)
- $t_{1/2}$ half-life (time for the expected deviation $|E[X_t]-\theta|$ to halve)
- $\Delta t$ discrete sampling interval; $\varepsilon_{t,\Delta t}\sim N\!\big(0,\frac{\sigma^2}{2\kappa}(1-e^{-2\kappa\Delta t})\big)$ exact discrete innovation

### Worked example
- **Integrating factor derivation (interview whiteboard staple):** Apply [[ito-lemma]] to $f(t,X_t) = e^{\kappa t}(X_t - \theta)$:
  $$d\big(e^{\kappa t}(X_t - \theta)\big) = \kappa e^{\kappa t}(X_t - \theta)\,dt + e^{\kappa t}\,dX_t = \sigma e^{\kappa t}\,dW_t$$
  Integrating from $0$ to $t$ and multiplying by $e^{-\kappa t}$ gives the closed-form solution; [[martingales-ito-isometry]] (Itô isometry) gives $\mathrm{Var}(X_t\mid X_0) = \sigma^2 \int_0^t e^{-2\kappa(t-s)}\,ds = \frac{\sigma^2}{2\kappa}(1-e^{-2\kappa t})$.
- **Numerical check:** If a pairs-trading spread has daily AR(1) autoregressive coefficient $\phi = e^{-\kappa\Delta t} = 0.95$ ($\Delta t = 1$ day), then $\kappa = -\ln(0.95) \approx 0.0513\text{ day}^{-1}$ and the half-life is $t_{1/2} = \ln 2 / \kappa \approx 13.5\text{ trading days}$.

### Key points
- **Exact link to AR(1):** Sampling an OU process at grid step $\Delta t$ yields a discrete [[stationarity-ar1]] process with slope $\phi = e^{-\kappa\Delta t}\in(0,1)$ and intercept $c = \theta(1-\phi)$.
- **OU (Vasicek) vs CIR (Feller square-root):** OU is Gaussian and can go **negative** (used for spreads, log-vol, and post-2014 negative short rates). Multiplying the diffusion by $\sqrt{X_t}$ gives the Cox–Ingersoll–Ross (CIR) process $dX_t = \kappa(\theta - X_t)\,dt + \xi\sqrt{X_t}\,dW_t$, which stays strictly positive when $2\kappa\theta > \xi^2$ and drives variance in [[heston-model]].

### Connections
- **Builds on:** [[ito-lemma]], [[stationarity-ar1]], [[martingales-ito-isometry]].
- **Used in:** [[heston-model]] (square-root CIR variant for variance $v_t$), statistical-arbitrage spread modelling, Vasicek short-rate models.

<a id="martingales-ito-isometry"></a>

## Martingales & Itô Isometry
<!-- section: martingales-ito-isometry | prerequisites: [brownian-motion, ito-lemma] | related: [risk-neutral-pricing] | sources: [src-squarepoint-dqa-workbook] | tags: [martingale, isometry] -->

A martingale is a stochastic process whose best forecast of future values is its current value. Itô integrals with respect to Brownian motion are continuous martingales, and the Itô isometry determines their variance.

### Definition
A real-valued stochastic process $M_t$ adapted to filtration $(\mathcal F_t)_{t\ge 0}$ with $E[|M_t|] < \infty$ for all $t\ge 0$ is a **martingale** if for all $s\le t$:

$$E[M_t\mid\mathcal F_s]=M_s$$

Equivalently, the expected future increment given all current information is zero: $E[M_t-M_s\mid\mathcal F_s]=0$.

**Variables:**

- $M_t$ stochastic process at time $t$
- $\mathcal F_s$ filtration (history and information up to time $s$)
- $s,t$ time indices with $s\le t$

### Formula
For any adapted process $H_t$ satisfying $\int_0^T E[H_t^2]\,dt < \infty$, the Itô integral $I_t = \int_0^t H_u\,dW_u$ is a continuous martingale with $E[I_t]=0$, and satisfies the **Itô isometry**:

$$E\left[\left(\int_0^T H_t\,dW_t\right)^2\right] = E\left[\int_0^T H_t^2\,dt\right]$$

Hence $\mathrm{Var}\left(\int_0^T H_t\,dW_t\right)=\int_0^T E[H_t^2]\,dt$.

**Variables:**

- $H_t$ adapted, square-integrable integrand
- $W_t$ standard Brownian motion
- $T$ time horizon

### Key points
- **Zero conditional drift:** A martingale has zero conditional drift ($E[dM_t\mid\mathcal F_t]=0$). In continuous diffusion form $dM_t = \mu_t\,dt + \sigma_t\,dW_t$, the process is a martingale if and only if $\mu_t = 0$.
- **Examples & non-examples:**
  - Brownian motion $W_t$ is a martingale ($E[W_t\mid\mathcal F_s]=W_s$).
  - $W_t^2$ is **not** a martingale ($E[W_t^2\mid\mathcal F_s]=W_s^2+(t-s)$); but $W_t^2-t$ is a martingale.
  - The exponential martingale $\mathcal E_t = \exp(\sigma W_t - \frac12\sigma^2 t)$ is a martingale ($E[\mathcal E_t]=1$).
- **Submartingale vs supermartingale:** $E[M_t\mid\mathcal F_s]\ge M_s$ (submartingale, upward drift, e.g. stock price under $\mathbb P$); $E[M_t\mid\mathcal F_s]\le M_s$ (supermartingale, downward drift).
- **Foundation of pricing:** Under the risk-neutral measure $\mathbb Q$, discounted asset prices $e^{-rt}S_t$ are martingales ([[risk-neutral-pricing]], [[bs-call-setup-risk-neutral]]).

### Connections
- **Builds on:** [[brownian-motion]], [[ito-lemma]].
- **Foundation of:** [[risk-neutral-pricing]] (discounted prices are $\mathbb Q$-martingales), [[bs-call-setup-risk-neutral]] (FTAP and pricing formula).

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
