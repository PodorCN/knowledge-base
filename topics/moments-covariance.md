---
id: moments-covariance
title: "Moments & Covariance"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Moments & Covariance

This chapter develops expectation and variance: linearity of expectation, covariance and correlation, Jensen's inequality for non-linear functions, the laws of total expectation and variance, and the conditional expectation as the best predictor. These are the building blocks of portfolio variance, regression and the $-\tfrac12\sigma^2$ corrections of stochastic calculus.

**Prerequisites:** [[probability-rules-counting]], [[conditional-probability-bayes]], [[distributions-reference]].

**Leads to:** [[portfolio-variance-diversification]] ($w^\top\Sigma w$), [[ols-regression]] (slope = Cov/Var), [[geometric-brownian-motion]] (Jensen), [[first-step-analysis]].

**Sections:** [[expectation-linearity-indicators]] · [[variance-covariance-correlation]] · [[jensens-inequality]] · [[total-expectation-variance]] · [[conditional-expectation-best-predictor]]

<a id="expectation-linearity-indicators"></a>

## Linearity of Expectation & Indicators
<!-- section: expectation-linearity-indicators | prerequisites: [probability-rules-counting] | related: [variance-covariance-correlation, first-step-analysis, jensens-inequality] | sources: [src-squarepoint-dqa-workbook] | tags: [expectation, indicator, linearity] -->

Expectation is linear whether or not the variables are independent. Writing a count as a sum of indicators turns hard counting problems into sums of probabilities.

### Formulas
$$E[aX+bY+c]=aE[X]+bE[Y]+c,\qquad E[I_A]=P(A),\qquad N=\sum_i I_i\ \Rightarrow\ E[N]=\sum_i P(A_i)$$

**Variables:**

- $X,Y$ random variables
- $a,b,c$ constants
- $I_A$ indicator of event $A$ (1 if $A$ happens, else 0)
- $N$ a count, written as a sum of indicators $I_i$ of events $A_i$

### Worked example
**Hat-check problem:** $n$ people receive random hats. Each person gets their own hat with probability $1/n$, so the expected number of matches is $n\cdot\frac1n=1$, for any $n$.

### Key points
- In general $E[g(X)]\ne g(E[X])$ for a non-linear $g$ → see [[jensens-inequality]].

### Connections
- **Builds on:** [[probability-rules-counting]].
- **Used by:** [[first-step-analysis]] (coupon collector = sum of stage waits), [[order-statistics]], [[win-rate-expectancy]].
- **Next:** [[variance-covariance-correlation]] — variance is *not* linear; covariance terms appear.

<a id="variance-covariance-correlation"></a>

## Variance, Covariance & Correlation
<!-- section: variance-covariance-correlation | prerequisites: [expectation-linearity-indicators] | related: [portfolio-variance-diversification, total-expectation-variance, normal-distribution, ols-regression, eigen-svd-psd] | sources: [src-squarepoint-dqa-workbook] | tags: [variance, covariance, correlation] -->

Variance measures dispersion; covariance and correlation measure how two variables move together. The variance of a sum contains every pairwise covariance, which is the origin of diversification.

### Formulas
$$\mathrm{Var}(X)=E[X^2]-E[X]^2,\qquad \mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y],\qquad \rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}\in[-1,1]$$
$$\mathrm{Var}(aX+bY)=a^2\sigma_X^2+b^2\sigma_Y^2+2ab\,\rho_{XY}\,\sigma_X\sigma_Y$$
$$\mathrm{Var}\Big(\sum_{i=1}^n X_i\Big)=n\sigma^2+n(n-1)\rho\sigma^2\quad\text{(equicorrelated)}$$

**Variables:**

- $X,Y,X_i$ random variables
- $a,b$ constants
- $\sigma_X,\sigma_Y$ standard deviations of $X$ and $Y$
- $\rho_{XY}$ correlation of $X$ and $Y$
- $\sigma,\rho$ common standard deviation and pairwise correlation of the equicorrelated $X_i$
- $n$ number of variables

### Key points
- $|\rho|\le1$ by Cauchy–Schwarz; $\rho$ is undefined if a variance is 0.
- **Uncorrelated but dependent:** $X\sim N(0,1)$, $Y=X^2$ gives $\mathrm{Cov}(X,Y)=E[X^3]=0$, yet $Y$ is a function of $X$.
- For **jointly normal** variables, zero covariance ⇔ independence (e.g. $X+Y \perp X-Y$ for iid normals).
- Scaling: $\mathrm{Var}(10X)=100\,\mathrm{Var}(X)$; positive scaling keeps $\rho$, negative scaling flips its sign.
- In matrix form, the covariance matrix $\Sigma$ of a random vector is PSD ([[eigen-svd-psd]]).

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Used by:** [[portfolio-variance-diversification]] ($w^\top\Sigma w$), [[ols-regression]] (slope $=\mathrm{Cov}/\mathrm{Var}$), [[pca]] (eigen-decomposition of $\Sigma$).
- **Extended by:** [[total-expectation-variance]] (law of total covariance).

<a id="jensens-inequality"></a>

## Jensen's Inequality
<!-- section: jensens-inequality | prerequisites: [expectation-linearity-indicators, taylor-expansions] | related: [geometric-brownian-motion, returns-simple-log, gamma-theta-pnl] | sources: [src-squarepoint-dqa-workbook] | tags: [convexity] -->

For a convex function the average of the function exceeds the function of the average. This single inequality explains volatility drag, the $-\tfrac12\sigma^2$ in GBM and why long options are long volatility.

### Formula
$$g\ \text{convex}\ \Rightarrow\ g(E[X])\le E[g(X)];\qquad E[\ln X]\le\ln E[X]\ \ (X>0)$$

**Variables:**

- $X$ random variable
- $g$ convex function (the inequality reverses for a concave $g$, e.g. $\ln$)

### Key points
- **Arithmetic vs geometric growth:** under GBM, $E[\ln(S_t/S_0)]=(\mu-\tfrac12\sigma^2)t < \mu t$ ([[geometric-brownian-motion]]).
- Convex option payoffs gain from mean-preserving spreads — the reason long options are "long vol".
- Higher variance alone doesn't rank *every* distribution for every convex payoff.
- Second-order Taylor view: the curvature term $\tfrac12g''\,\mathrm{Var}(X)$ is the size of the gap ([[taylor-expansions]]).

### Connections
- **Builds on:** [[expectation-linearity-indicators]], [[taylor-expansions]].
- **Explains:** [[geometric-brownian-motion]] ($-\tfrac12\sigma^2$ drift), [[returns-simple-log]] (+10% then −10% = −1%), [[gamma-theta-pnl]] (convexity pays when realised vol is high), [[lognormal-distribution]] (mean above median).

<a id="total-expectation-variance"></a>

## Laws of Total Expectation, Variance & Covariance
<!-- section: total-expectation-variance | prerequisites: [variance-covariance-correlation, conditional-probability-bayes] | related: [conditional-expectation-best-predictor, exponential-poisson-process] | sources: [src-squarepoint-dqa-workbook] | tags: [conditioning, random-sum, hidden-dependence] -->

Conditioning on a hidden variable splits a mean, variance or covariance into a "within" part and a "between" part. This handles random sums and exposes dependence created by a shared hidden factor.

### Formulas
$$E[X]=E\big[E[X\mid Y]\big],\qquad \mathrm{Var}(X)=E[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(E[X\mid Y])$$
$$\mathrm{Cov}(X,Z)=E[\mathrm{Cov}(X,Z\mid Y)]+\mathrm{Cov}(E[X\mid Y],E[Z\mid Y])$$

**Variables:**

- $X,Z$ target random variables
- $Y$ conditioning (hidden) variable

### Random sums
$$S=\sum_{i=1}^N X_i:\qquad E[S]=E[N]\,m,\qquad \mathrm{Var}(S)=E[N]\,v+\mathrm{Var}(N)\,m^2$$

**Variables:**

- $X_i$ iid summands with mean $m$ and variance $v$
- $N$ random count, independent of the $X_i$
- $S$ random sum

### Worked examples
- $Y\sim U(0,1)$, $X\mid Y\sim U(0,Y)$: $E[X]=E[Y/2]=1/4$; $\mathrm{Var}(X)=E[Y^2/12]+\mathrm{Var}(Y/2)=\frac{1/3}{12}+\frac{1/12}{4}=7/144$.
- $N\sim$ Poisson(10) trades, P&L per trade with mean 2 and variance 9: $E[S]=20$, $\mathrm{Var}(S)=10\cdot9+10\cdot4=130$ (the extra 40 is uncertainty in the trade count).
- Selected-coin tosses ([[conditional-probability-bayes]]): $\mathrm{Cov}(I_1,I_2)=\mathrm{Var}(\Theta)=1/64$ → hidden dependence.

### Key points
- **Trap:** if $N$ depends on the $X_i$ (a stopping time), these formulas don't apply automatically — use a recursion ([[first-step-analysis]]).

### Connections
- **Builds on:** [[variance-covariance-correlation]], [[conditional-probability-bayes]].
- **Related:** [[conditional-expectation-best-predictor]] (same decomposition applied to prediction error), [[exponential-poisson-process]] (Poisson counts).

<a id="conditional-expectation-best-predictor"></a>

## Conditional Expectation as Best Predictor
<!-- section: conditional-expectation-best-predictor | prerequisites: [total-expectation-variance] | related: [ols-regression, normal-distribution, bias-variance-tradeoff] | sources: [src-squarepoint-dqa-workbook] | tags: [prediction, mse, jointly-normal] -->

Among all functions of $Y$, the conditional expectation $E[X\mid Y]$ minimises mean-squared prediction error. Under joint normality it is linear — exactly the population regression line.

### Formulas
$$E[(X-g(Y))^2]=E[\mathrm{Var}(X\mid Y)]+E[(E[X\mid Y]-g(Y))^2]$$

**Variables:**

- $X$ variable to predict
- $Y$ information used to predict
- $g$ any square-integrable predictor (function of $Y$)

The second term is zero only for $g(Y)=E[X\mid Y]$, so the conditional expectation is the best predictor.

### Jointly normal case
$$E[Y\mid X=x]=\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\qquad \mathrm{Var}(Y\mid X=x)=\sigma_Y^2(1-\rho^2)$$

**Variables:**

- $(X,Y)$ jointly normal pair
- $\mu_X,\mu_Y$ means
- $\sigma_X,\sigma_Y$ standard deviations
- $\rho$ correlation
- $x$ observed value of $X$

### Key points
- $E[X\mid Y=y]$ is a number; $E[X\mid Y]$ is a random variable.
- Under joint normality the best predictor **is** linear with slope $\rho\sigma_Y/\sigma_X$ — exactly the OLS population slope.

### Connections
- **Builds on:** [[total-expectation-variance]]; uses [[normal-distribution]].
- **Bridge to:** [[ols-regression]] (linear approximation of $E[Y\mid X]$), [[bias-variance-tradeoff]].
