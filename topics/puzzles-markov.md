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
<!-- section: first-step-analysis | prerequisites: [expectation-linearity-indicators] | related: [markov-chains, exponential-poisson-process, american-early-exercise, total-expectation-variance, martingales-ito-isometry] | sources: [src-squarepoint-dqa-workbook] | tags: [recursion, waiting-time, coupon-collector, optimal-stopping] -->

Condition on what happens at the first step, express the expected remaining time (or hitting probability) from each state, and solve the resulting linear equations — or apply Optional Stopping to a natural martingale.

### Formulas
$$E=1+(1-p)E\ \Rightarrow\ E=\frac1p\qquad\text{(trials to first success)}$$

Two consecutive heads with a coin:

$$E_0=1+(1-p)E_0+pE_1,\qquad E_1=1+(1-p)E_0\ \Rightarrow\ E_0=\frac{1+p}{p^2}\quad(E_0=6\text{ for }p=\tfrac12)$$

Coupon collector:

$$E[T_{\text{coupon}}]=n\sum_{j=1}^n\frac1j=nH_n$$

Gambler's ruin / symmetric & biased random walk on $\{-A, \dots, B\}$ starting at $S_0=0$ (hit $+B$ before $-A$, stopping time $\tau=\inf\{t: S_t\in\{-A,B\}\}$):

$$\text{Fair }(p=\tfrac12):\quad P(S_\tau=B)=\frac{A}{A+B},\qquad E[\tau]=AB$$
$$\text{Biased }(p\ne\tfrac12,\, q=1-p):\quad P(S_\tau=B)=\frac{1-(q/p)^A}{1-(q/p)^{A+B}},\qquad E[\tau]=\frac{B\,P(S_\tau=B)-A\big(1-P(S_\tau=B)\big)}{p-q}$$

**Variables:**

- $p, q=1-p$ up-step (heads/success) and down-step (tails/failure) probabilities per trial
- $E$ expected number of trials to the first success
- $E_k$ expected remaining trials from state $k$ ($k\in\{0,1\}$ = current consecutive run of heads)
- $n, j$ total number of coupon types and count of distinct coupons already collected
- $T_{\text{coupon}}$ number of draws until all $n$ types are collected
- $H_n=\sum_{j=1}^n1/j\approx \ln n + \gamma$ harmonic number
- $S_t$ random walk position at step $t$ starting from $S_0=0$
- $A, B > 0$ lower barrier distance ($-A$) and upper barrier distance ($+B$)
- $\tau$ first hitting time of $\{-A, B\}$; $S_\tau\in\{-A,B\}$ stopped position

### Worked examples
- **Optional Stopping shortcut (fair walk):** For $p=1/2$, both $S_t$ and $S_t^2 - t$ are martingales ([[martingales-ito-isometry]]). Since $|S_{t\wedge\tau}|\le\max(A,B)$ is bounded, Doob's Optional Stopping Theorem gives $E[S_\tau]=S_0=0 \Rightarrow B\,p_B - A(1-p_B)=0 \Rightarrow p_B = A/(A+B)$, and $E[S_\tau^2 - \tau]=0 \Rightarrow E[\tau] = E[S_\tau^2] = B^2\frac{A}{A+B} + A^2\frac{B}{A+B} = AB$. For $p\ne 1/2$, use the exponential martingale $(q/p)^{S_t}$ for hitting probability and $S_t - (p-q)t$ for $E[\tau]$.
- **Expected sum of rolls until first six:** $m=3.5+\tfrac56m\Rightarrow m=21$ (or by Wald's identity: $E[N]\cdot E[X] = 6\times 3.5 = 21$).
- **One optional re-roll of a die:** keep $4,5,6$, re-roll $1,2,3$ → value $\frac12(5) + \frac12(3.5) = 4.25$ (backward induction with continuation value $3.5$; with two optional re-rolls, keep $5,6$ in round 1 since continuation value is $4.25$, giving $\frac13(5.5)+\frac23(4.25)=4.67$).

### Key points
- **Pattern trap (HH vs HT):** For a fair coin, $E[\tau_{HH}] = 6$ whereas $E[\tau_{HT}] = 4$. After the first $H$, a $T$ immediately completes $HT$ (state never resets to $0$), whereas a $T$ resets $HH$ all the way back to state $0$. By Conway's leading-number / martingale betting argument, $E[\tau_{HH}] = 2^2 + 2^1 = 6$ because $HH$ overlaps with itself at length $1$ and $2$, while $HT$ has no self-overlap ($E[\tau_{HT}] = 2^2 = 4$).

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Generalises to:** [[markov-chains]] (absorbing chains), [[martingales-ito-isometry]] (Optional Stopping).
- **Same logic as:** [[american-early-exercise]] — exercise if the payoff ≥ the continuation value (backward induction).

<a id="markov-chains"></a>

## Markov Chains & Stationary Distributions
<!-- section: markov-chains | prerequisites: [first-step-analysis] | related: [stationarity-ar1] | sources: [src-squarepoint-dqa-workbook] | tags: [markov, stationary, regime] -->

A Markov chain's next state depends only on the current state. Ergodic chains converge to a unique stationary distribution $\pi=\pi P$, while absorbing chains are solved in closed form via the fundamental matrix $N=(I-Q)^{-1}$.

### Formulas
$$P(X_{t+1}=j\mid X_t=i,\dots)=P_{ij},\qquad \pi=\pi P,\qquad \sum_i\pi_i=1$$

Two states ($A\to B$ with probability $a$, $B\to A$ with probability $b$):

$$\pi_A=\frac{b}{a+b},\qquad \pi_B=\frac{a}{a+b}$$

Absorbing Markov chain in canonical block form (transient states $T$, absorbing states $A$):

$$P=\begin{pmatrix}Q & R\\ 0 & I\end{pmatrix},\qquad N=(I-Q)^{-1}=\sum_{k=0}^\infty Q^k,\qquad \tau_{\text{abs}}=N\mathbf 1,\qquad B_{\text{abs}}=NR$$

**Variables:**

- $X_t, X_{t+1}$ chain state at times $t$ and $t+1$
- $i, j$ state indices
- $P$ transition matrix with entries $P_{ij}$ (rows sum to $1$)
- $\pi, \pi_i$ stationary distribution row vector and its $i$-th component ($\pi_A, \pi_B$ in the two-state chain)
- $a, b$ switching probabilities $P_{AB}=a$ and $P_{BA}=b$ in the two-state chain
- $Q$ transient-to-transient sub-matrix of transition probabilities
- $R$ transient-to-absorbing sub-matrix of transition probabilities
- $I$ identity matrix
- $N=(I-Q)^{-1}$ fundamental matrix ($N_{ij}$ = expected number of visits to transient state $j$ before absorption, starting from transient state $i$; $k$: step index)
- $\tau_{\text{abs}} = N\mathbf 1$ vector of expected steps until absorption from each transient state ($\mathbf 1$: column vector of ones)
- $B_{\text{abs}} = NR$ matrix of absorption probabilities ($B_{\text{abs},ij}$ = probability of being absorbed in state $j$ starting from transient state $i$)

### Key points
- **Stationary vs limiting distribution:** Finite + irreducible $\Rightarrow$ unique stationary distribution $\pi$ with $\pi_i = 1/E[T_{ii}]$ (reciprocal of mean return time); adding **aperiodicity** guarantees $P^t \to \mathbf 1\pi$ from any initial state.
- **Reversibility (detailed balance):** If $\pi_i P_{ij} = \pi_j P_{ji}$ for all $i,j$ (always holds on trees and birth–death chains), $\pi$ can be found immediately by local ratios without inverting $P - I$.
- **Absorbing chains in interviews:** Any pattern-waiting or ruin puzzle can be written as a small transient transition matrix $Q$; expected waiting time from state $i$ is row $i$ of $(I-Q)^{-1}\mathbf 1$, which is identical to solving the first-step equations.

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
