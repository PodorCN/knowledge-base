---
id: numerical-methods
title: "Numerical Methods"
type: topic
domain: pricing
sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes]
---
# Numerical Methods

When no closed form exists, prices and implied quantities are computed numerically. This chapter covers the three workhorses: root finding (implied vols, yields), finite-difference solution of the pricing PDE, and Monte Carlo simulation — and when to use which.

**Prerequisites:** [[black-scholes-pde]], [[risk-neutral-pricing]], [[lln-clt]].

**Leads to:** [[implied-volatility]] (Newton inversion), [[barrier-options]], [[autocallables]], [[local-stochastic-volatility]].

**Sections:** [[root-finding]] · [[pde-finite-difference]] · [[monte-carlo-pricing]]

<a id="root-finding"></a>

## Root Finding (Newton, Bisection, Brent)
<!-- section: root-finding | prerequisites: [taylor-expansions] | related: [implied-volatility, bond-yield-measures] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [numerics, newton, brent] -->

Solving $f(x)=0$ numerically: Newton's method uses the derivative for fast quadratic convergence; bracketing methods trade speed for guaranteed convergence when derivatives vanish or oscillate.

### Formula
$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}\quad\text{(Newton–Raphson)},\qquad x_{n+1}=x_n-f(x_n)\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}\quad\text{(Secant)}$$
$$|e_{n+1}|\approx\frac{|f''(x^*)|}{2|f'(x^*)|}\,e_n^2\quad\text{(Newton quadratic error)},\qquad |b_n-a_n|=2^{-n}(b_0-a_0)\quad\text{(Bisection bracket)}$$

**Variables:**

- $f(x)$ target function whose root $x^*$ satisfies $f(x^*)=0$
- $f'(x), f''(x)$ first and second derivatives of $f$
- $x_n, x_{n-1}, x_{n+1}$ iterates at steps $n-1, n, n+1$
- $x^*$ true root of $f(x)=0$
- $e_n = x_n - x^*$ error at step $n$
- $[a_n, b_n]$ bracketing interval at step $n$ with $f(a_n)f(b_n)\le 0$ ($[a_0, b_0]$ initial bracket)
- $n$ iteration index

Newton's step is the root of the first-order Taylor expansion of $f$ at $x_n$ ([[taylor-expansions]]).

### Key points
- **Newton–Raphson:** quadratic convergence ($O(e_n^2)$ — correct digits double each step) near a simple root; explodes or cycles when $f'(x_n)\to 0$ (e.g. deep OTM/ITM options where Vega $\mathcal V\to 0$).
- **Bisection:** guaranteed linear convergence ($1$ bit of accuracy per function evaluation) whenever $f$ is continuous on $[a_0,b_0]$ with $f(a_0)f(b_0)<0$.
- **Brent's method:** combines root bracketing, bisection, secant, and inverse quadratic interpolation — superlinear speed near the root with guaranteed stays-in-bracket fallback. The production default when analytic derivatives are unavailable or unreliable.
- **Implied volatility inversion:** check no-arbitrage price bounds first, maintain a tight bracket $[a_n,b_n]$, start from a rational/Brenner–Subrahmanyam guess, and use safeguarded Newton (fall back to bisection if the Newton step leaves the bracket) or Jäckel's *Let's Be Rational* algorithm ([[implied-volatility]]).

### Connections
- **Used by:** [[implied-volatility]], [[bond-yield-measures]] (YTM).

<a id="pde-finite-difference"></a>

## PDE / Finite-Difference Pricing
<!-- section: pde-finite-difference | prerequisites: [black-scholes-pde] | related: [monte-carlo-pricing, barrier-options, american-early-exercise, local-volatility-dupire] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [pde, grid, crank-nicolson] -->

Finite-difference methods discretise the pricing PDE on a grid $(S_i, t_m)$ and march backward from the terminal payoff $V(S,T)=h(S)$ to $t=0$.

### Formula
Write the spatial differential operator of the Black–Scholes / local-vol PDE as $\mathcal L V = rS\,V_S + \tfrac12\sigma^2 S^2 V_{SS} - rV$, so $V_t + \mathcal L V = 0$. Replacing derivatives by central differences in $S$ (step $\Delta S$) and backward steps in time (step $\Delta t$) yields the $\theta$-scheme:

$$\frac{V_i^{m+1}-V_i^m}{\Delta t} + (1-\theta)\,(\mathcal L_h V)_i^{m+1} + \theta\,(\mathcal L_h V)_i^m = 0$$
$$(I - \theta\,\Delta t\,\mathcal L_h)\,V^m = \big(I + (1-\theta)\,\Delta t\,\mathcal L_h\big)\,V^{m+1}$$

**Variables:**

- $V_i^m$ grid approximation to option value $V(S_i, t_m)$ at spatial node $i$ and time level $m$
- $V^m, V^{m+1}$ column vectors of nodal values across spatial nodes at times $t_m$ and $t_{m+1}$
- $S, S_i$ spot price and $i$-th spatial grid node ($S_i = S_0 + i\,\Delta S$ or uniform in $\ln S$)
- $t, t_m, T$ time, $m$-th time grid node, and maturity
- $\Delta S, \Delta t$ spatial grid spacing and time-step size
- $r, \sigma$ risk-free rate and volatility (constant or local $\sigma(S_i,t_m)$)
- $V_t, V_S, V_{SS}$ partial derivatives $\partial V/\partial t$, $\partial V/\partial S$, $\partial^2 V/\partial S^2$
- $\mathcal L, \mathcal L_h$ continuous differential operator and its tridiagonal central-difference matrix approximation
- $\theta\in[0,1]$ scheme weight ($\theta=0$ Explicit, $\theta=1$ Fully Implicit, $\theta=1/2$ Crank–Nicolson)
- $I$ identity matrix
- $h(S)$ terminal payoff at maturity $T$

### Scheme comparison

| Scheme | Weight $\theta$ | Accuracy | Stability | Linear solver per step |
|---|---|---|---|---|
| **Explicit Euler** | $\theta = 0$ | $O(\Delta t, \Delta S^2)$ | Conditionally stable: requires $\Delta t = O(\Delta S^2)$ | Direct update $O(N_S)$ |
| **Fully Implicit** | $\theta = 1$ | $O(\Delta t, \Delta S^2)$ | Unconditionally stable ($L$-stable, damps oscillations) | Tridiagonal Thomas algorithm $O(N_S)$ |
| **Crank–Nicolson** | $\theta = 1/2$ | $O(\Delta t^2, \Delta S^2)$ | Unconditionally $A$-stable (can oscillate at kinks/barriers) | Tridiagonal Thomas algorithm $O(N_S)$ |

**Notes:**

- $N_S$ number of spatial grid nodes.

### Key points
- **Tridiagonal solve:** Because central differences couple node $i$ only to $i-1, i, i+1$, the matrix $I - \theta\,\Delta t\,\mathcal L_h$ is tridiagonal and solves in $O(N_S)$ time via the **Thomas algorithm** (LU without pivoting), not $O(N_S^3)$.
- **Rannacher smoothing:** Crank–Nicolson is second-order accurate in time ($O(\Delta t^2)$), but non-smooth payoffs (strike kinks, digital steps, barriers) trigger spurious oscillations in $\Delta$ and $\Gamma$ near expiry. Taking 2–4 half-steps of **Fully Implicit** ($\theta=1$) right at maturity and then switching to Crank–Nicolson ($\theta=1/2$) restores smooth second-order convergence.
- **Grid alignment & American exercise:** Place a grid node directly on the strike $K$ or barrier $H$ ([[barrier-options]]). For American options, apply the early-exercise projection $V_i^m \leftarrow \max(V_i^m, h(S_i))$ at each step (or solve the linear complementarity problem via PSOR, [[american-early-exercise]]).
- **Curse of dimensionality:** Grid size scales as $O(N_S^d)$ in $d$ spatial dimensions — fast and exact in $d=1,2$ factors (yielding $\Delta,\Gamma,\Theta$ directly off the same grid), but $d\ge 3$ multi-asset products require [[monte-carlo-pricing]].

### Connections
- **Builds on:** [[black-scholes-pde]].
- **Used for:** [[barrier-options]], [[american-early-exercise]], [[local-volatility-dupire]].

<a id="monte-carlo-pricing"></a>

## Monte Carlo Pricing
<!-- section: monte-carlo-pricing | prerequisites: [risk-neutral-pricing, lln-clt] | related: [pde-finite-difference, autocallables, barrier-options, asian-options, greeks-conventions-bumping, local-stochastic-volatility, static-replication] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [monte-carlo, aad, longstaff-schwartz, variance-reduction] -->

Monte Carlo simulates $M$ risk-neutral paths and averages the discounted payoff. By the CLT its statistical standard error falls as $\sigma_Y/\sqrt{M}$ regardless of state-space dimension $d$ ([[lln-clt]]).

### Formula
$$V_0\approx \hat V_M = e^{-rT}\,\frac1M\sum_{j=1}^M Y^{(j)},\qquad SE(\hat V_M)=\frac{s_Y}{\sqrt M}$$
$$\text{Exact GBM step:}\quad S_{t+\Delta t}=S_t\exp\!\Big(\big(r-q-\tfrac12\sigma^2\big)\Delta t+\sigma\sqrt{\Delta t}\,Z\Big)$$
$$\text{Euler–Maruyama step:}\quad S_{t+\Delta t}=S_t+\big(r-q\big)S_t\,\Delta t+\sigma(S_t,t)S_t\sqrt{\Delta t}\,Z$$
$$\text{Antithetic estimator:}\quad \hat Y_{\text{anti}}=\frac{Y(Z)+Y(-Z)}{2},\qquad \mathrm{Var}(\hat Y_{\text{anti}})=\frac{\mathrm{Var}(Y)}{2}\big(1+\mathrm{Corr}(Y(Z),Y(-Z))\big)$$
$$\text{Control variate:}\quad \hat Y_{\text{CV}}=Y-\beta\big(X-E^{\mathbb Q}[X]\big),\qquad \beta^*=\frac{\mathrm{Cov}(Y,X)}{\mathrm{Var}(X)},\qquad \mathrm{Var}(\hat Y_{\text{CV}})=\mathrm{Var}(Y)\big(1-\rho_{XY}^2\big)$$

**Variables:**

- $V_0, \hat V_M$ true option value and $M$-path Monte Carlo estimator
- $M$ number of simulated paths
- $Y^{(j)} = h(S^{(j)})$ pathwise payoff on the $j$-th path under $\mathbb Q$ ($Y$: generic discounted payoff random variable; $s_Y$: sample standard deviation of discounted payoffs)
- $SE(\hat V_M)$ standard error of the Monte Carlo estimator
- $S_t, S_{t+\Delta t}$ simulated asset price at times $t$ and $t+\Delta t$
- $r, q, \sigma, T, \Delta t$ risk-free rate, dividend yield, volatility, maturity, and time step
- $Z\sim N(0,1)$ standard normal draw
- $Y(Z), Y(-Z)$ payoffs evaluated on a standard normal vector $Z$ and its reflection $-Z$
- $\hat Y_{\text{anti}}, \hat Y_{\text{CV}}$ antithetic-variates and control-variates payoff estimators
- $X$ control variate with known closed-form expectation $E^{\mathbb Q}[X]$ (e.g. underlying $S_T$, geometric Asian, or flat-vol vanilla)
- $\beta, \beta^*$ control weight and variance-minimising weight
- $\rho_{XY}$ correlation between target payoff $Y$ and control payoff $X$

### Key points
- **Exact vs Euler discretisation:** Under flat-vol GBM, the exact log-normal transition has **zero discretisation bias** for any step size $\Delta t$ (a European payoff needs only a single jump $0\to T$). Under local/stochastic vol ($\sigma(S_t,t)$ or Heston), Euler–Maruyama has weak convergence $O(\Delta t)$ and strong convergence $O(\sqrt{\Delta t})$ (Milstein adds $\frac12\sigma\sigma_S S^2((Z^2-1)\Delta t)$ to raise strong order to $O(\Delta t)$).
- **Variance reduction:** Halving the standard error by brute force requires $4\times$ more paths. Antithetic variates reduce variance whenever $Y(Z)$ is monotone in $Z$ ($\mathrm{Corr}(Y(Z),Y(-Z))<0$) at half the RNG cost; a strongly correlated control variate ($\rho_{XY}=0.95$) cuts variance by $1-\rho_{XY}^2 \approx 10\times$.
- **Greeks:** Pathwise differentiation (differentiate the path wrt $S_0$ when the payoff is Lipschitz; fails for digitals/barriers where the derivative is a Dirac delta — use the Likelihood Ratio Method or payoff smoothing), bumping with **common random numbers** ([[greeks-conventions-bumping]]), or **AAD** (Adjoint Algorithmic Differentiation, computing all sensitivities in $O(1)$ multiple of the forward pass).
- **Early exercise & barriers:** Longstaff–Schwartz least-squares Monte Carlo (regress continuation value on basis functions of ITM paths); discrete barriers use the Broadie–Glasserman–Kou (BGK) shift, while continuous barriers sample the Brownian-bridge minimum/maximum between grid dates ([[barrier-options]]).
- **Performance (.NET):** Pre-allocate path buffers (`Span<double>`, `ArrayPool<double>`), vectorise RNG + exp across paths, and parallelise across independent chunks with thread-local RNG streams ([[csharp-essentials]]).

### Numerical-method map

| Method | Idea | Typical products |
|---|---|---|
| Closed form | analytic under flat vol | Reiner–Rubinstein barrier, geometric Asian, Margrabe, digital |
| [[static-replication]] | build from vanillas | digitals, variance swaps, any European |
| [[pde-finite-difference]] | solve the pricing PDE on a grid | single-asset barriers, American, local vol |
| **Monte Carlo** | simulate paths | autocallables, baskets, cliquets |

### Connections
- **Builds on:** [[risk-neutral-pricing]], [[lln-clt]].
- **Used for:** [[autocallables]], [[barrier-options]], [[asian-options]], [[local-stochastic-volatility]]; implemented in [[csharp-pricing-library-example]].
