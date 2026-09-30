---
id: puzzles-markov
title: "Puzzles & Markov Chains"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Puzzles & Markov Chains

Interview probability puzzles mostly reduce to three techniques: condition on the first step and solve a recursion, find the stationary distribution of a Markov chain, or use the distribution of an ordered sample. The same backward-induction logic later prices American options.

**Prerequisites:** [[expectation-linearity-indicators]], [[distributions-reference]].

**Leads to:** [[american-early-exercise]] (backward induction), [[stationarity-ar1]] (continuous-state stationarity).

**Sections:** [[first-step-analysis]] · [[markov-chains]] · [[order-statistics]]

<a id="first-step-analysis"></a>

## First-Step Analysis (waiting times, stopping)
<!-- section: first-step-analysis | prerequisites: [expectation-linearity-indicators] | related: [markov-chains, exponential-poisson-process, american-early-exercise, total-expectation-variance] | sources: [src-squarepoint-dqa-workbook] | tags: [recursion, waiting-time, coupon-collector, optimal-stopping] -->

Condition on what happens at the first step, express the expected remaining time (or value) from each state, and solve the resulting linear equations.

### Formulas
$$E=1+(1-p)E\ \Rightarrow\ E=\frac1p\qquad\text{(trials to first success)}$$

Two consecutive heads with a fair coin:

$$E_0=1+\tfrac12E_0+\tfrac12E_1,\qquad E_1=1+\tfrac12E_0\ \Rightarrow\ E_0=6;\qquad\text{general: }E_0=\frac{1+p}{p^2}$$

Coupon collector:

$$E[T_{\text{coupon}}]=n\sum_{j=1}^n\frac1j=nH_n$$

**Variables:**

- $p$ success (heads) probability per trial
- $E$ expected number of trials to the first success
- $E_k$ expected remaining trials from state $k$ ($k$ = current run of heads)
- $n$ number of coupon types
- $T_{\text{coupon}}$ number of draws until all $n$ types are collected
- $H_n=\sum_{j=1}^n1/j$ harmonic number

### Worked examples
- Roll a die until the first six; the expected **sum** including the six is $m=3.5+\tfrac56m\Rightarrow m=21$.
- One optional re-roll of a die: keep 4–6, re-roll 1–3 → value $4.25$ (backward induction with continuation value 3.5).

### Key points
- **Trap:** HH has probability 1/4 per block of two tosses, but overlapping windows aren't independent, so the waiting time is not geometric.

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Generalises to:** [[markov-chains]] (absorbing chains).
- **Same logic as:** [[american-early-exercise]] — exercise if the payoff ≥ the continuation value (backward induction).

<a id="markov-chains"></a>

## Markov Chains & Stationary Distributions
<!-- section: markov-chains | prerequisites: [first-step-analysis] | related: [stationarity-ar1] | sources: [src-squarepoint-dqa-workbook] | tags: [markov, stationary, regime] -->

A Markov chain's next state depends only on the current state. Its long-run behaviour is described by a stationary distribution that the transition matrix leaves unchanged.

### Formulas
$$P(X_{t+1}=j\mid X_t=i,\dots)=P_{ij},\qquad \pi=\pi P,\qquad \sum_i\pi_i=1$$

Two states (A→B with probability $a$, B→A with probability $b$):

$$\pi_A=\frac{b}{a+b},\qquad \pi_B=\frac{a}{a+b}$$

**Variables:**

- $X_t$ state at time $t$
- $P$ transition matrix, $P_{ij}$ probability of moving from $i$ to $j$ (rows sum to 1)
- $\pi$ stationary distribution (row vector)
- $a,b$ switching probabilities in the two-state chain

### Key points
- Finite + irreducible ⇒ unique $\pi$; + aperiodic ⇒ convergence to $\pi$ from any start.
- Regime-switching intuition in finance (calm / stressed regimes).

### Connections
- **Builds on:** [[first-step-analysis]].
- **Contrast:** [[stationarity-ar1]] (continuous-state stationarity).

<a id="order-statistics"></a>

## Order Statistics of Uniforms
<!-- section: order-statistics | prerequisites: [distributions-reference] | related: [expectation-linearity-indicators, first-step-analysis] | sources: [src-squarepoint-dqa-workbook] | tags: [max, min, uniform] -->

The distribution of the maximum (or $k$-th smallest) of independent draws follows from the fact that the maximum is below $x$ only if every draw is.

### Formulas
$$M=\max_i U_i:\quad P(M\le x)=x^n,\quad f_M(x)=nx^{n-1},\quad E[M]=\frac{n}{n+1};\qquad E[U_{(k)}]=\frac{k}{n+1}$$

**Variables:**

- $U_i\sim U(0,1)$ iid, $i=1,\dots,n$
- $M$ maximum of the $U_i$
- $f_M$ density of $M$
- $x\in[0,1]$
- $U_{(k)}$ the $k$-th smallest of the $U_i$

### Key points
- **Trick:** the CDF of the maximum is the product of the individual CDFs (independence).
- $E[\max(X,Y)]=2/3$ for two independent uniforms; $P(X+Y<1)=1/2$ (area of a triangle).

### Connections
- **Builds on:** [[distributions-reference]]. **Related interview family:** [[first-step-analysis]].
