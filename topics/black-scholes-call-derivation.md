---
id: black-scholes-call-derivation
title: "Black–Scholes Call Price: Derivation Study Notes"
type: topic
domain: black-scholes
sources: [src-bs-derivation-study-notes]
---
# Black–Scholes Call Price: Derivation Study Notes

*September 21, 2026*

Big picture: price = discounted expectation of the payoff under the risk-neutral measure $Q$. Everything below either constructs $Q$ or computes that one expectation.

**Sections:** [[bs-call-setup-risk-neutral]] · [[girsanov-risk-neutral-dynamics]] · [[lognormal-under-q]] · [[payoff-indicator-split]] · [[term-b-risk-neutral-probability]] · [[term-a-direct-integration]] · [[term-a-stock-numeraire]] · [[combine-call-price]]

<a id="bs-call-setup-risk-neutral"></a>

## Setup and Risk-Neutral Pricing
<!-- section: bs-call-setup-risk-neutral | prerequisites: [no-arbitrage, option-payoffs-moneyness] | related: [risk-neutral-pricing, black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [black-scholes, risk-neutral, ftap] -->

### Setup

$$C_T=(S_T-K)^+=\max(S_T-K,0)$$

**Variables:**

- $C_T$ call value at maturity
- $S_T$ stock price at maturity
- $K$ strike
- $C_0$ today's call price

Goal: find $C_0$, today's price.

### Step 1 — Risk-neutral pricing formula

The fundamental theorem of asset pricing (FTAP) says that no arbitrage implies the existence of a measure $Q$, equivalent to the real-world measure $P$, under which the discounted price of every traded asset is a martingale:

$$e^{-rt}S_t=E^Q\!\left[e^{-rT}S_T\mid\mathcal F_t\right]$$

For any payoff $X_T$:

$$V_0=e^{-rT}E^Q[X_T]$$

**Variables:**

- $r$ constant risk-free rate
- $\mathcal F_t$ information at time $t$
- $V_0$ today's price
- $Q$ risk-neutral measure
- $P$ real-world measure
- $X_T$ payoff at maturity

**Martingale:** $E[X_T\mid\mathcal F_t]=X_t$ — the best forecast of the future is today's value.

Applying this to $X_T=(S_T-K)^+$:

$$C_0=e^{-rT}E^Q[(S_T-K)^+]$$

This is the only place $Q$ enters as a new assumption. Every step after this computes the same expectation.

### Why $Q$ and not $P$?

Under $P$, the stock's expected return is $\mu$, which is unobservable and subjective. The option price must be unique and objective, so it cannot depend on $\mu$. $Q$ is constructed in Step 2 so that $\mu$ cancels and only $r$ and $\sigma$ remain.

<a id="girsanov-risk-neutral-dynamics"></a>

## Stock Dynamics under Q (Girsanov)
<!-- section: girsanov-risk-neutral-dynamics | prerequisites: [risk-neutral-pricing, brownian-motion, ito-lemma] | related: [lognormal-under-q, geometric-brownian-motion] | sources: [src-bs-derivation-study-notes] | tags: [girsanov, risk-neutral, dynamics] -->

### Step 2 — Real-world GBM

$$dS_t=\mu S_t\,dt+\sigma S_t\,dW_t^P$$

**Variables:**

- $\mu$ real-world expected return
- $\sigma$ constant volatility
- $W_t^P$ Brownian motion under $P$
- $\theta=(\mu-r)/\sigma$ market price of risk
- $r$ risk-free rate

### Girsanov change of measure

Define

$$W_t^Q=W_t^P+\theta t,\qquad \theta=\frac{\mu-r}{\sigma}$$

where $\theta$ is the market price of risk. Then $W_t^Q$ is a standard Brownian motion under $Q$.

A Brownian-motion identity is a property of a (process, measure) pair, not of the process alone:

$$W_t^Q\sim N(0,t)\ \text{under }Q,\qquad W_t^Q\sim N(\theta t,t)\ \text{under }P$$

Substituting $dW_t^P=dW_t^Q-\theta\,dt$:

$$
\begin{aligned}
dS_t
&=\mu S_t\,dt+\sigma S_t\left(dW_t^Q-\frac{\mu-r}{\sigma}\,dt\right)\\
&=rS_t\,dt+\sigma S_t\,dW_t^Q
\end{aligned}
$$

$\mu$ cancels; the drift becomes $r$. This is why the option price does not depend on $\mu$.

<a id="lognormal-under-q"></a>

## Solving for the Terminal Stock Price with Itô's Lemma
<!-- section: lognormal-under-q | prerequisites: [girsanov-risk-neutral-dynamics, ito-lemma, normal-distribution] | related: [geometric-brownian-motion, lognormal-distribution, black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [ito, lognormal, risk-neutral] -->

### Step 3 — Itô's lemma

If $dS=a\,dt+b\,dW$ and $f(t,S)$ is smooth, then

$$df=f_t\,dt+f_S\,dS+\frac12 f_{SS}(dS)^2,\qquad (dW)^2=dt$$

Apply this to $f=\ln S$, with $f_t=0$, $f_S=1/S$, and $f_{SS}=-1/S^2$:

$$d\ln S_t=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t^Q$$

The $-\frac12\sigma^2$ term is the Itô correction from the convexity of $\ln S$ together with $(dW)^2=dt$.

Integrating from $0$ to $T$ and using $W_T^Q=\sqrt{T}\,Z$, where $Z\sim N(0,1)$:

$$
S_T=S_0\exp\left[\left(r-\frac12\sigma^2\right)T+\sigma\sqrt{T}\,Z\right]
$$

Thus $S_T$ is lognormal under $Q$.

<a id="payoff-indicator-split"></a>

## Splitting the Payoff with an Indicator
<!-- section: payoff-indicator-split | prerequisites: [option-payoffs-moneyness, normal-distribution] | related: [term-b-risk-neutral-probability, black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [payoff, indicator, expectation] -->

### Step 4 — Indicator decomposition

Define $\mathbf 1_A=1$ if $A$ happens and $0$ otherwise. Then

$$
(S_T-K)^+=(S_T-K)\mathbf 1_{\{S_T>K\}}
=S_T\mathbf 1_{\{S_T>K\}}-K\mathbf 1_{\{S_T>K\}}
$$

By linearity of expectation:

$$C_0=e^{-rT}\left(E^Q[S_T\mathbf 1_{\{S_T>K\}}]-K E^Q[\mathbf 1_{\{S_T>K\}}]\right)$$

- **Term A:** $E^Q[S_T\mathbf 1_{\{S_T>K\}}]$
- **Term B:** $K E^Q[\mathbf 1_{\{S_T>K\}}]$

<a id="term-b-risk-neutral-probability"></a>

## Term B and the Risk-Neutral Exercise Probability
<!-- section: term-b-risk-neutral-probability | prerequisites: [payoff-indicator-split, lognormal-under-q, normal-distribution] | related: [delta-vs-itm-probability, black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [d2, risk-neutral, probability] -->

### Step 5 — Term B = $N(d_2)$

Use the identity $E[\mathbf 1_A]=Q(A)$. From the lognormal expression for $S_T$,

$$
S_T>K
\iff
Z>\frac{-\ln(S_0/K)+(r-\frac12\sigma^2)T}{\sigma\sqrt T}
=-d_2
$$

By normal-CDF symmetry, $Q(Z>-x)=N(x)$:

$$
\text{Term B}=KQ(S_T>K)=KN(d_2)
$$

$N(d_2)$ is the risk-neutral probability that the call finishes in the money.

<a id="term-a-direct-integration"></a>

## Term A by Direct Integration
<!-- section: term-a-direct-integration | prerequisites: [term-b-risk-neutral-probability, normal-distribution] | related: [term-a-stock-numeraire, black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [integration, d1, black-scholes] -->

### Route A — Complete the square

Let $\phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$. Then

$$
\text{Term A}
=\int_{-d_2}^{\infty}S_0e^{(r-\frac12\sigma^2)T+\sigma\sqrt Tz}\,\phi(z)\,dz
$$

Complete the square in the exponent:

$$
-\frac12z^2+\sigma\sqrt Tz-\frac12\sigma^2T
=-\frac12(z-\sigma\sqrt T)^2
$$

Therefore,

$$
\text{Term A}
=S_0e^{rT}\int_{-d_2}^{\infty}\phi(z-\sigma\sqrt T)\,dz
$$

With $y=z-\sigma\sqrt T$, the lower limit becomes $-d_2-\sigma\sqrt T=-d_1$:

$$
\text{Term A}
=S_0e^{rT}\int_{-d_1}^{\infty}\phi(y)\,dy
=S_0e^{rT}N(d_1),
\qquad d_1=d_2+\sigma\sqrt T
$$

<a id="term-a-stock-numeraire"></a>

## Term A under the Stock Numeraire
<!-- section: term-a-stock-numeraire | prerequisites: [risk-neutral-pricing, normal-distribution] | related: [term-a-direct-integration, delta-vs-itm-probability] | sources: [src-bs-derivation-study-notes] | tags: [numeraire, stock-numeraire, girsanov] -->

### Route B — Change of numeraire

A numeraire is any traded asset $N_t>0$ used as the unit of account. The Geman–El Karoui–Rochet theorem says that for a numeraire $N$, a measure $Q^N$ exists under which $V_t/N_t$ is a martingale:

$$\frac{dQ^N}{dQ}=\frac{N_T}{B_T}\frac{N_0}{B_0}$$

Apply this with $N=S$, $B_0=1$, and $B_T=e^{rT}$:

$$\frac{dQ^S}{dQ}=\frac{S_Te^{-rT}}{S_0}$$

This reweights outcomes by $S_T$: paths with higher $S_T$ receive more weight under $Q^S$.

The stock-leg term becomes

$$
\begin{aligned}
\text{Term A}
&=S_0E^Q\left[\frac{S_Te^{-rT}}{S_0}\mathbf 1_{\{S_T>K\}}\right]\\
&=S_0E^{Q^S}[\mathbf 1_{\{S_T>K\}}]
=S_0Q^S(S_T>K)
\end{aligned}
$$

The $S_Te^{-rT}/S_0$ factor is absorbed by the measure change, so no integral remains.

### Dynamics of $S$ under $Q^S$

Using $W^Q$ in the density,

$$\frac{dQ^S}{dQ}=\exp\left(\sigma W_T^Q-\frac12\sigma^2T\right)$$

Girsanov with $\theta=-\sigma$ gives

$$W_t^S=W_t^Q-\sigma t$$

as standard Brownian motion under $Q^S$. Substituting into $dS=rS\,dt+\sigma S\,dW^Q$:

$$dS_t=(r+\sigma^2)S_t\,dt+\sigma S_t\,dW_t^S$$

Itô's lemma on $\ln S$ gives

$$
\ln S_T=\ln S_0+\left(r+\frac12\sigma^2\right)T+\sigma\sqrt T\,Z,
\qquad Z\sim N(0,1)\ \text{under }Q^S
$$

The only difference from Step 3 is the drift $r+\frac12\sigma^2$ instead of $r-\frac12\sigma^2$.

Using the same probability template as Step 5:

$$
S_T>K
\iff
Z>\frac{-\ln(S_0/K)+(r+\frac12\sigma^2)T}{\sigma\sqrt T}
=-d_1
$$

Thus

$$Q^S(S_T>K)=N(d_1)$$

**Intuition:** to value receiving an asset $X$ when an event happens, use $X$ as numeraire: value = (price of $X$ today) × (probability of the event under $X$'s measure).

<a id="combine-call-price"></a>

## Combining the Terms: Black–Scholes Call Price
<!-- section: combine-call-price | prerequisites: [term-a-direct-integration, term-a-stock-numeraire] | related: [black-scholes-formula, delta-vs-itm-probability, greeks] | sources: [src-bs-derivation-study-notes] | tags: [black-scholes, call-price, d1, d2] -->

### Step 7 — Combine

$$
\begin{aligned}
C_0
&=e^{-rT}\left(S_0e^{rT}N(d_1)-KN(d_2)\right)\\
&=S_0N(d_1)-Ke^{-rT}N(d_2)
\end{aligned}
$$

- $S_0N(d_1)$ is the present value of receiving the stock when exercise occurs.
- $Ke^{-rT}N(d_2)$ is the present value of paying $K$ when exercise occurs.
- $N(d_1)$ is also the call's delta, $\partial C/\partial S$.

### Summary: $Q$ versus $Q^S$

| Measure | $Q$ (money-market numeraire) | $Q^S$ (stock numeraire) |
|---|---|---|
| Brownian motion | $W^Q$, standard under $Q$ | $W^S=W^Q-\sigma t$, standard under $Q^S$ |
| Drift of $\ln S_T$ | $r-\frac12\sigma^2$ | $r+\frac12\sigma^2$ |
| Event $S_T>K$ | $Z>-d_2$ | $Z>-d_1$ |
| Probability | $N(d_2)$ | $N(d_1)$ |
| Pays for | Strike leg, $Ke^{-rT}N(d_2)$ | Stock leg, $S_0N(d_1)$ |

What changes between $Q$ and $Q^S$ is not the sample space, $\sigma$, or the shape of randomness; it is the probability weight assigned to each outcome (equivalently, the drift). $Q^S$ up-weights high-$S_T$ paths through $dQ^S/dQ\propto S_T$.

### Numerical check

For $S_0=100$, $K=100$, $r=5\%$, $\sigma=20\%$, and $T=1$:

$$
d_1=\frac{0+(0.05+0.02)\cdot1}{0.2}=0.35,
\qquad N(d_1)=0.6368
$$

$$
d_2=0.35-0.20=0.15,
\qquad N(d_2)=0.5596
$$

$$
C_0=100(0.6368)-100e^{-0.05}(0.5596)\approx10.45
$$

### Follow-up points

- Girsanov replaces $\mu$ with $r$ under $Q$; economically, the option is replicable and hedgeable, so its price cannot depend on the stock's subjective expected return.
- $N(d_2)$ is the risk-neutral probability of exercise; $N(d_1)$ is the exercise probability under the stock measure and the call's delta.
- The $-\frac12\sigma^2$ term is the Itô correction: convexity of $\ln S$ plus $(dW)^2=dt$.
- Change of numeraire values an asset received on an event by using that asset as the unit of account.

### References

- Hull, *Options, Futures, and Other Derivatives*, Ch. 15 appendix.
- Shreve, *Stochastic Calculus for Finance II*, Ch. 5 (risk-neutral pricing, Girsanov) and Ch. 9 (change of numeraire).
- Geman, El Karoui & Rochet (1995), *Journal of Applied Probability*.

The step breakdown, table, and intuition phrasing are the author's own synthesis (self-derived / not directly from a single source) built on these standard, verifiable results.
