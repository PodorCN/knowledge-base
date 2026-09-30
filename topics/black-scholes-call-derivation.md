---
id: black-scholes-call-derivation
title: "Deriving Black–Scholes"
type: topic
domain: black-scholes
sources: [src-bs-derivation-study-notes, src-rbc-quantdev-prep, src-squarepoint-dqa-workbook]
---
# Deriving Black–Scholes

Big picture: price = discounted expectation of the payoff under the risk-neutral measure $\mathbb Q$. Every step of this chapter either constructs $\mathbb Q$ or computes that one expectation, and the two terms of the result are then read as probabilities under two different measures — which is exactly the distinction between $N(d_1)$ and $N(d_2)$.

**Prerequisites:** [[risk-neutral-pricing]], [[ito-lemma]], [[normal-distribution]], [[expectation-linearity-indicators]], [[black-scholes-formula]].

**Leads to:** [[greeks]], [[digital-options]] (priced off $N(d_2)$).

**Sections:** [[bs-call-setup-risk-neutral]] · [[girsanov-risk-neutral-dynamics]] · [[lognormal-under-q]] · [[payoff-indicator-split]] · [[term-b-risk-neutral-probability]] · [[term-a-direct-integration]] · [[term-a-stock-numeraire]] · [[combine-call-price]] · [[delta-vs-itm-probability]]

Setting of this chapter: no dividends ($q=0$), constant $r$ and $\sigma$, valuation at $t=0$, maturity $T$. $\mathbb P$ is the real-world measure, $\mathbb Q$ the risk-neutral measure, $\mathbb Q^S$ the stock-numeraire measure; $\phi$ and $N$ are the standard normal pdf and CDF.

<a id="bs-call-setup-risk-neutral"></a>

## Setup and Risk-Neutral Pricing
<!-- section: bs-call-setup-risk-neutral | prerequisites: [no-arbitrage, option-payoffs-moneyness, risk-neutral-pricing] | related: [black-scholes-formula] | sources: [src-bs-derivation-study-notes] | tags: [black-scholes, risk-neutral, ftap] -->

The call's price today is its discounted expected payoff under $\mathbb Q$. This is the only place $\mathbb Q$ enters as an assumption.

### Setup
$$C_T=(S_T-K)^+=\max(S_T-K,0)$$

**Variables:**

- $C_T$ call value at maturity
- $S_T$ stock price at maturity
- $K$ strike
- $C_0$ today's call price (to be found)

### Step 1 — Risk-neutral pricing formula
The fundamental theorem of asset pricing (FTAP) says that no arbitrage implies the existence of a measure $\mathbb Q$, equivalent to the real-world measure $\mathbb P$, under which the discounted price of every traded asset is a martingale:

$$e^{-rt}S_t=E^{\mathbb Q}\!\left[e^{-rT}S_T\mid\mathcal F_t\right],\qquad V_0=e^{-rT}E^{\mathbb Q}[X_T]\ \ \text{for any payoff }X_T$$

**Variables:**

- $r$ constant risk-free rate
- $S_t$ stock price at $t\le T$
- $\mathcal F_t$ information at time $t$
- $X_T$ payoff at maturity
- $V_0$ today's price of that payoff

**Martingale:** $E[X_T\mid\mathcal F_t]=X_t$ — the best forecast of the future is today's value ([[martingales-ito-isometry]]).

Applying this to $X_T=(S_T-K)^+$:

$$C_0=e^{-rT}E^{\mathbb Q}\big[(S_T-K)^+\big]$$

Every step after this computes the same expectation.

### Why $\mathbb Q$ and not $\mathbb P$?
Under $\mathbb P$ the stock's expected return is $\mu$, which is unobservable and subjective. The option price must be unique and objective, so it cannot depend on $\mu$. $\mathbb Q$ is constructed in Step 2 so that $\mu$ cancels and only $r$ and $\sigma$ remain.

### Connections
- **Builds on:** [[risk-neutral-pricing]], [[option-payoffs-moneyness]].

<a id="girsanov-risk-neutral-dynamics"></a>

## Stock Dynamics under ℚ (Girsanov)
<!-- section: girsanov-risk-neutral-dynamics | prerequisites: [bs-call-setup-risk-neutral, brownian-motion, ito-lemma] | related: [lognormal-under-q, geometric-brownian-motion] | sources: [src-bs-derivation-study-notes] | tags: [girsanov, risk-neutral, dynamics] -->

Girsanov's theorem shifts the drift of the Brownian motion by the market price of risk. Under the new measure the stock drifts at $r$ instead of $\mu$.

### Step 2 — Real-world GBM
$$dS_t=\mu S_t\,dt+\sigma S_t\,dW_t^{\mathbb P}$$

**Variables:**

- $\mu$ real-world expected return
- $\sigma$ constant volatility
- $W_t^{\mathbb P}$ Brownian motion under $\mathbb P$

### Girsanov change of measure
$$W_t^{\mathbb Q}=W_t^{\mathbb P}+\theta t,\qquad \theta=\frac{\mu-r}{\sigma}$$

**Variables:**

- $\theta$ market price of risk
- $W_t^{\mathbb Q}$ the shifted process, a standard Brownian motion under $\mathbb Q$

A Brownian-motion identity is a property of a (process, measure) pair, not of the process alone:

$$W_t^{\mathbb Q}\sim N(0,t)\ \text{under }\mathbb Q,\qquad W_t^{\mathbb Q}\sim N(\theta t,t)\ \text{under }\mathbb P$$

Substituting $dW_t^{\mathbb P}=dW_t^{\mathbb Q}-\theta\,dt$:

$$
\begin{aligned}
dS_t
&=\mu S_t\,dt+\sigma S_t\left(dW_t^{\mathbb Q}-\frac{\mu-r}{\sigma}\,dt\right)\\
&=rS_t\,dt+\sigma S_t\,dW_t^{\mathbb Q}
\end{aligned}
$$

$\mu$ cancels and the drift becomes $r$. This is why the option price does not depend on $\mu$ (with dividends the drift is $r-q$, [[risk-neutral-pricing]]).

### Connections
- **Builds on:** [[bs-call-setup-risk-neutral]], [[geometric-brownian-motion]].

<a id="lognormal-under-q"></a>

## Solving for the Terminal Stock Price with Itô's Lemma
<!-- section: lognormal-under-q | prerequisites: [girsanov-risk-neutral-dynamics, ito-lemma, normal-distribution] | related: [geometric-brownian-motion, lognormal-distribution] | sources: [src-bs-derivation-study-notes] | tags: [ito, lognormal, risk-neutral] -->

Applying Itô's lemma to $\ln S$ under $\mathbb Q$ gives $S_T$ explicitly as a lognormal variable driven by one standard normal $Z$.

### Step 3 — Itô's lemma
If $dS=a\,dt+b\,dW$ and $f(t,S)$ is smooth, then ([[ito-lemma]])

$$df=f_t\,dt+f_S\,dS+\frac12 f_{SS}(dS)^2,\qquad (dW)^2=dt$$

Apply this to $f=\ln S$, with $f_t=0$, $f_S=1/S$ and $f_{SS}=-1/S^2$:

$$d\ln S_t=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t^{\mathbb Q}$$

The $-\frac12\sigma^2$ term is the Itô correction from the convexity of $\ln S$ together with $(dW)^2=dt$.

Integrating from $0$ to $T$ and writing $W_T^{\mathbb Q}=\sqrt{T}\,Z$:

$$S_T=S_0\exp\left[\left(r-\frac12\sigma^2\right)T+\sigma\sqrt{T}\,Z\right],\qquad Z\sim N(0,1)\ \text{under }\mathbb Q$$

**Variables:**

- $S_0$ spot today
- $Z$ standard normal random variable
- $T$ maturity

Thus $S_T$ is lognormal under $\mathbb Q$ ([[lognormal-distribution]]).

### Connections
- **Same result as:** [[geometric-brownian-motion]] with $\mu\to r$.

<a id="payoff-indicator-split"></a>

## Splitting the Payoff with an Indicator
<!-- section: payoff-indicator-split | prerequisites: [option-payoffs-moneyness, expectation-linearity-indicators] | related: [term-b-risk-neutral-probability, digital-options] | sources: [src-bs-derivation-study-notes] | tags: [payoff, indicator, expectation] -->

The call payoff is split into "receive the stock if exercised" minus "pay the strike if exercised", and linearity of expectation prices the two parts separately.

### Step 4 — Indicator decomposition
Define $\mathbf 1_A=1$ if $A$ happens and $0$ otherwise. Then

$$(S_T-K)^+=(S_T-K)\mathbf 1_{\{S_T>K\}}=S_T\mathbf 1_{\{S_T>K\}}-K\mathbf 1_{\{S_T>K\}}$$

By linearity of expectation ([[expectation-linearity-indicators]]):

$$C_0=e^{-rT}\left(E^{\mathbb Q}\big[S_T\mathbf 1_{\{S_T>K\}}\big]-K\,E^{\mathbb Q}\big[\mathbf 1_{\{S_T>K\}}\big]\right)$$

- **Term A:** $E^{\mathbb Q}[S_T\mathbf 1_{\{S_T>K\}}]$ — the stock leg (an asset-or-nothing payoff).
- **Term B:** $K\,E^{\mathbb Q}[\mathbf 1_{\{S_T>K\}}]$ — the strike leg (a cash-or-nothing payoff, [[digital-options]]).

<a id="term-b-risk-neutral-probability"></a>

## Term B and the Risk-Neutral Exercise Probability
<!-- section: term-b-risk-neutral-probability | prerequisites: [payoff-indicator-split, lognormal-under-q, normal-distribution] | related: [delta-vs-itm-probability] | sources: [src-bs-derivation-study-notes] | tags: [d2, risk-neutral, probability] -->

The expectation of an indicator is a probability, so Term B is $K$ times the $\mathbb Q$-probability of exercise, which the lognormal formula turns into $N(d_2)$.

### Step 5 — Term B = $K\,N(d_2)$
Use the identity $E[\mathbf 1_A]=\mathbb Q(A)$. From the lognormal expression for $S_T$,

$$S_T>K\iff Z>\frac{-\ln(S_0/K)-(r-\frac12\sigma^2)T}{\sigma\sqrt T}=-d_2,\qquad d_2=\frac{\ln(S_0/K)+(r-\frac12\sigma^2)T}{\sigma\sqrt T}$$

✏️ Correction: the original notes wrote $+(r-\frac12\sigma^2)T$ in the numerator; solving $S_T>K$ for $Z$ gives the minus sign shown (the same fix applies to $-d_1$ in Route B).

By symmetry of the normal distribution, $\mathbb Q(Z>-x)=N(x)$:

$$\text{Term B}=K\,\mathbb Q(S_T>K)=K\,N(d_2)$$

$N(d_2)$ is the risk-neutral probability that the call finishes in the money.

<a id="term-a-direct-integration"></a>

## Term A by Direct Integration
<!-- section: term-a-direct-integration | prerequisites: [term-b-risk-neutral-probability, normal-distribution] | related: [term-a-stock-numeraire] | sources: [src-bs-derivation-study-notes] | tags: [integration, d1, black-scholes] -->

Term A can be computed by writing the expectation as an integral against the normal density and completing the square.

### Step 6, Route A — Complete the square
With $\phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$ the standard normal density,

$$\text{Term A}=\int_{-d_2}^{\infty}S_0\,e^{(r-\frac12\sigma^2)T+\sigma\sqrt T\,z}\,\phi(z)\,dz$$

Complete the square in the exponent:

$$-\frac12z^2+\sigma\sqrt T\,z-\frac12\sigma^2T=-\frac12\big(z-\sigma\sqrt T\big)^2$$

Therefore

$$\text{Term A}=S_0e^{rT}\int_{-d_2}^{\infty}\phi\big(z-\sigma\sqrt T\big)\,dz$$

With $y=z-\sigma\sqrt T$ the lower limit becomes $-d_2-\sigma\sqrt T=-d_1$:

$$\text{Term A}=S_0e^{rT}\int_{-d_1}^{\infty}\phi(y)\,dy=S_0e^{rT}N(d_1),\qquad d_1=d_2+\sigma\sqrt T$$

**Variables:**

- $z$ integration variable (value of $Z$)
- $y$ shifted integration variable
- $d_1,d_2$ as in [[black-scholes-formula]] with $q=0$, $\tau=T$

<a id="term-a-stock-numeraire"></a>

## Term A under the Stock Numeraire
<!-- section: term-a-stock-numeraire | prerequisites: [term-b-risk-neutral-probability, girsanov-risk-neutral-dynamics] | related: [term-a-direct-integration, delta-vs-itm-probability] | sources: [src-bs-derivation-study-notes] | tags: [numeraire, stock-numeraire, girsanov] -->

Route B avoids the integral: measuring value in units of the stock turns Term A into a probability, just like Term B, but under a different measure.

### Step 6, Route B — Change of numeraire
A numeraire is any traded asset $N_t>0$ used as the unit of account. The Geman–El Karoui–Rochet theorem says that for a numeraire $N$ a measure $\mathbb Q^N$ exists under which $V_t/N_t$ is a martingale for every traded price $V_t$:

$$\frac{d\mathbb Q^N}{d\mathbb Q}=\frac{N_T/B_T}{N_0/B_0}$$

**Variables:**

- $N_t$ numeraire asset price
- $\mathbb Q^N$ measure associated with numeraire $N$
- $B_t=e^{rt}$ money-market account ($B_0=1$), the numeraire of $\mathbb Q$

✏️ Correction: the original notes wrote the density as a product $\frac{N_T}{B_T}\frac{N_0}{B_0}$; it is the ratio shown (it must equal 1 at $T=0$).

Apply this with $N=S$:

$$\frac{d\mathbb Q^S}{d\mathbb Q}=\frac{S_Te^{-rT}}{S_0}$$

This reweights outcomes by $S_T$: paths with higher $S_T$ receive more weight under $\mathbb Q^S$. The stock-leg term becomes

$$
\begin{aligned}
\text{Term A}
&=S_0e^{rT}\,E^{\mathbb Q}\left[\frac{S_Te^{-rT}}{S_0}\mathbf 1_{\{S_T>K\}}\right]\\
&=S_0e^{rT}\,E^{\mathbb Q^S}\big[\mathbf 1_{\{S_T>K\}}\big]=S_0e^{rT}\,\mathbb Q^S(S_T>K)
\end{aligned}
$$

The $S_Te^{-rT}/S_0$ factor is absorbed by the measure change, so no integral remains.

✏️ Correction: the original notes wrote Term A $=S_0\,\mathbb Q^S(S_T>K)$, dropping the factor $e^{rT}$; with Term A defined undiscounted (Step 4) it is $S_0e^{rT}\,\mathbb Q^S(S_T>K)$, matching Route A and Step 7.

### Dynamics of $S$ under $\mathbb Q^S$
Using $W^{\mathbb Q}$ in the density,

$$\frac{d\mathbb Q^S}{d\mathbb Q}=\exp\left(\sigma W_T^{\mathbb Q}-\frac12\sigma^2T\right)$$

Girsanov with $\theta=-\sigma$ gives $W_t^S=W_t^{\mathbb Q}-\sigma t$ as a standard Brownian motion under $\mathbb Q^S$. Substituting into $dS=rS\,dt+\sigma S\,dW^{\mathbb Q}$:

$$dS_t=(r+\sigma^2)S_t\,dt+\sigma S_t\,dW_t^S$$

Itô's lemma on $\ln S$ gives

$$\ln S_T=\ln S_0+\left(r+\frac12\sigma^2\right)T+\sigma\sqrt T\,Z,\qquad Z\sim N(0,1)\ \text{under }\mathbb Q^S$$

The only difference from Step 3 is the drift $r+\frac12\sigma^2$ instead of $r-\frac12\sigma^2$. Using the same probability template as Step 5:

$$S_T>K\iff Z>\frac{-\ln(S_0/K)-(r+\frac12\sigma^2)T}{\sigma\sqrt T}=-d_1\qquad\Rightarrow\qquad \mathbb Q^S(S_T>K)=N(d_1)$$

**Intuition:** to value receiving an asset $X$ when an event happens, use $X$ as numeraire: value = (price of $X$ today) × (probability of the event under $X$'s measure).

<a id="combine-call-price"></a>

## Combining the Terms: Black–Scholes Call Price
<!-- section: combine-call-price | prerequisites: [term-a-direct-integration, term-a-stock-numeraire] | related: [black-scholes-formula, delta-vs-itm-probability, greeks] | sources: [src-bs-derivation-study-notes] | tags: [black-scholes, call-price, d1, d2] -->

Putting Term A and Term B back into Step 4 recovers the Black–Scholes formula.

### Step 7 — Combine
$$C_0=e^{-rT}\Big(S_0e^{rT}N(d_1)-K\,N(d_2)\Big)=S_0N(d_1)-Ke^{-rT}N(d_2)$$

- $S_0N(d_1)$ is the present value of receiving the stock when exercise occurs.
- $Ke^{-rT}N(d_2)$ is the present value of paying $K$ when exercise occurs.
- $N(d_1)$ is also the call's delta, $\partial C/\partial S$ ([[greeks]]).

### Summary: $\mathbb Q$ versus $\mathbb Q^S$

| Measure | $\mathbb Q$ (money-market numeraire) | $\mathbb Q^S$ (stock numeraire) |
|---|---|---|
| Brownian motion | $W^{\mathbb Q}$, standard under $\mathbb Q$ | $W^S=W^{\mathbb Q}-\sigma t$, standard under $\mathbb Q^S$ |
| Drift of $\ln S$ | $r-\frac12\sigma^2$ | $r+\frac12\sigma^2$ |
| Event $S_T>K$ | $Z>-d_2$ | $Z>-d_1$ |
| Probability | $N(d_2)$ | $N(d_1)$ |
| Pays for | Strike leg, $Ke^{-rT}N(d_2)$ | Stock leg, $S_0N(d_1)$ |

What changes between $\mathbb Q$ and $\mathbb Q^S$ is not the sample space, $\sigma$, or the shape of the randomness; it is the probability weight assigned to each outcome (equivalently, the drift). $\mathbb Q^S$ up-weights high-$S_T$ paths through $d\mathbb Q^S/d\mathbb Q\propto S_T$.

### Worked example
$S_0=100$, $K=100$, $r=5\%$, $\sigma=20\%$, $T=1$:

$$d_1=\frac{0+(0.05+0.02)\cdot1}{0.2}=0.35,\quad N(d_1)=0.6368;\qquad d_2=0.35-0.20=0.15,\quad N(d_2)=0.5596$$

$$C_0=100\times0.6368-100e^{-0.05}\times0.5596\approx10.45$$

### Follow-up points
- Girsanov replaces $\mu$ with $r$ under $\mathbb Q$; economically, the option is replicable and hedgeable, so its price cannot depend on the stock's subjective expected return.
- $N(d_2)$ is the risk-neutral probability of exercise; $N(d_1)$ is the exercise probability under the stock measure and the call's delta.
- The $-\frac12\sigma^2$ term is the Itô correction: convexity of $\ln S$ plus $(dW)^2=dt$.
- Change of numeraire values an asset received on an event by using that asset as the unit of account.

### References
- Hull, *Options, Futures, and Other Derivatives*, Ch. 15 appendix.
- Shreve, *Stochastic Calculus for Finance II*, Ch. 5 (risk-neutral pricing, Girsanov) and Ch. 9 (change of numeraire).
- Geman, El Karoui & Rochet (1995), *Journal of Applied Probability*.

The step breakdown, table and intuition phrasing are the author's own synthesis (self-derived / not directly from a single source) built on these standard, verifiable results.

### Connections
- **Result:** [[black-scholes-formula]]. **Interpretation:** [[delta-vs-itm-probability]].

<a id="delta-vs-itm-probability"></a>

## Delta vs Probability of Finishing ITM (N(d1) vs N(d2))
<!-- section: delta-vs-itm-probability | prerequisites: [combine-call-price, risk-neutral-pricing] | related: [greeks, digital-options, lognormal-distribution] | sources: [src-rbc-quantdev-prep, src-squarepoint-dqa-workbook] | tags: [delta, probability, measure] -->

The derivation shows that $N(d_1)$ and $N(d_2)$ are both probabilities of the same event, $S_T>K$, under two different measures — and that neither is the real-world probability.

### Key points
- $N(d_2)$ = **risk-neutral** probability that $S_T>K$ (= the undiscounted cash-or-nothing digital).
- $N(d_1)$ = the same probability under the **share measure** $\mathbb Q^S$ (stock as numeraire); with dividends the call delta is $e^{-q\tau}N(d_1)$ ([[greeks]]).
- Neither is the physical ($\mathbb P$) probability. They are close for short-dated ATM options and diverge for long-dated or high-vol options.
- **ATM-forward call delta > 0.5:** at $K=F$, $d_1=\tfrac12\sigma\sqrt T>0$. The lognormal is right-skewed: its median is below the forward ([[lognormal-distribution]]).

### Connections
- **Builds on:** [[combine-call-price]], [[term-a-stock-numeraire]].
- **Why it matters:** [[digital-options]] are priced off $N(d_2)$, and skew adjusts it.
