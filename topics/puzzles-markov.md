---
id: puzzles-markov
title: "Puzzles & Markov Chains"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Puzzles & Markov Chains

**Sections:** [[first-step-analysis]] · [[markov-chains]] · [[order-statistics]]

<a id="first-step-analysis"></a>

## First-Step Analysis (waiting times, stopping)
<!-- section: first-step-analysis | prerequisites: [expectation-linearity-indicators] | related: [markov-chains, exponential-poisson-process, american-early-exercise] | sources: [src-squarepoint-dqa-workbook] | tags: [recursion, waiting-time, coupon-collector, optimal-stopping] -->

### Formulas
$$E=1+(1-p)E\Rightarrow E=\tfrac1p\qquad\text{(first success)}$$
Two consecutive heads (fair coin): $E_0=1+\tfrac12E_0+\tfrac12E_1,\ E_1=1+\tfrac12E_0\Rightarrow E_0=6$; general $E_0=\frac{1+p}{p^2}$.
$$E[T_{\text{coupon}}]=n\sum_{j=1}^n\frac1j=nH_n$$

**Variables:**

- $p$ success/heads probability
- $E_k$ expected remaining trials from state $k$
- $n$ coupon types
- $H_n$ harmonic number

### More drills
- Roll until first six, expected **sum** incl. the six: $m=3.5+\tfrac56m\Rightarrow m=21$.
- One optional re-roll: keep 4–6, re-roll 1–3 → value $4.25$ (backward induction with continuation value 3.5).

### Key points
- Trap: HH has prob 1/4 per block but overlapping windows aren't independent — not geometric.

### Connections
- **Generalises to:** [[markov-chains]] (absorbing chains).
- **Same logic as:** [[american-early-exercise]] — exercise if payoff ≥ continuation value (backward induction).

<a id="markov-chains"></a>

## Markov Chains & Stationary Distributions
<!-- section: markov-chains | prerequisites: [first-step-analysis] | related: [stationarity-ar1] | sources: [src-squarepoint-dqa-workbook] | tags: [markov, stationary, regime] -->

### Formulas
$$P(X_{t+1}=j\mid X_t=i,\dots)=P_{ij},\qquad \pi=\pi P,\ \ \sum_i\pi_i=1$$
Two states (A→B w.p. $a$, B→A w.p. $b$): $\pi_A=\frac{b}{a+b},\ \pi_B=\frac{a}{a+b}$.

**Variables:**

- $P$ transition matrix (rows sum to 1)
- $\pi$ stationary row vector

### Key points
- Finite + irreducible ⇒ unique $\pi$; + aperiodic ⇒ convergence from any start.
- Regime-switching intuition in finance (calm/stressed).

### Connections
- **Builds on:** [[first-step-analysis]]. **Contrast:** [[stationarity-ar1]] (continuous-state stationarity).

<a id="order-statistics"></a>

## Order Statistics of Uniforms
<!-- section: order-statistics | prerequisites: [distributions-reference] | related: [expectation-linearity-indicators] | sources: [src-squarepoint-dqa-workbook] | tags: [max, min, uniform] -->

### Formulas
$$M=\max_i U_i:\ P(M\le x)=x^n,\ f_M(x)=nx^{n-1},\ E[M]=\frac{n}{n+1};\qquad E[U_{(k)}]=\frac{k}{n+1}$$

**Variables:**

- $U_i\sim U(0,1)$ iid, $i=1..n$
- $U_{(k)}$ the $k$-th smallest

### Key points
- $E[\max(X,Y)]=2/3$ for two uniforms; $P(X+Y<1)=1/2$ (triangle area).
- Trick: CDF of the max = product of CDFs (independence).

### Connections
- **Builds on:** [[distributions-reference]]. Related interview family: [[first-step-analysis]].
