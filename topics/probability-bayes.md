---
id: probability-bayes
title: "Probability Basics & Bayes"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Probability Basics & Bayes

**Sections:** [[probability-rules-counting]] · [[conditional-probability-bayes]] · [[beta-bernoulli-conjugacy]]

<a id="probability-rules-counting"></a>

## Probability Rules & Counting
<!-- section: probability-rules-counting | prerequisites: [] | related: [conditional-probability-bayes, expectation-linearity-indicators] | sources: [src-squarepoint-dqa-workbook] | tags: [counting, complement, inclusion-exclusion] -->

### Formulas
$$P(A\cup B)=P(A)+P(B)-P(A\cap B),\qquad P(A^c)=1-P(A)$$
$$P(n,k)=\frac{n!}{(n-k)!},\qquad \binom{n}{k}=\frac{n!}{k!\,(n-k)!}$$
$$P(\text{at least one})=1-(1-p)^n$$

**Variables:**

- $A,B$ events
- $n$ items / trials
- $k$ items chosen
- $p$ per-trial probability (independent trials)

### Key points
- **Mutually exclusive ≠ independent.** Two exclusive events with positive probability are *dependent* (one rules out the other).
- Sampling **with** replacement → independent draws; **without** → dependent. E.g. two aces without replacement: $\frac{4}{52}\cdot\frac{3}{51}=\frac{1}{221}$.
- At least one six in four rolls: $1-(5/6)^4\approx 0.5177$.
- Before using a ratio of counts, check the elementary outcomes are **equally likely**.

### Connections
- **Used by:** [[conditional-probability-bayes]] — conditioning is "restrict the sample space, renormalise".
- **Used by:** [[expectation-linearity-indicators]] — indicator tricks often replace hard counting.

<a id="conditional-probability-bayes"></a>

## Conditional Probability & Bayes' Theorem
<!-- section: conditional-probability-bayes | prerequisites: [probability-rules-counting] | related: [beta-bernoulli-conjugacy, total-expectation-variance, maximum-likelihood, hypothesis-testing] | sources: [src-squarepoint-dqa-workbook] | tags: [bayes, base-rate, independence] -->

### Formulas
$$P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(D)=\sum_j P(D\mid H_j)P(H_j)$$
$$P(H_i\mid D)=\frac{P(D\mid H_i)P(H_i)}{\sum_j P(D\mid H_j)P(H_j)},\qquad \frac{P(H_1\mid D)}{P(H_0\mid D)}=\frac{P(H_1)}{P(H_0)}\cdot\frac{P(D\mid H_1)}{P(D\mid H_0)}$$

**Variables:**

- $H_i$ disjoint hypotheses covering all cases
- $D$ observed data
- $P(H_i)$ prior
- $P(D\mid H_i)$ likelihood
- $P(D)$ evidence (normaliser)
- $P(H_i\mid D)$ posterior

### Worked examples
- **Signal & base rate:** favourable state 10%; signal fires 80% when favourable, 20% otherwise → $P(F\mid S)=\frac{0.08}{0.08+0.18}=4/13\approx30.8\%$. Rare states make even good detectors imprecise.
- **Selected coin:** fair coin A or coin B ($p=3/4$), each w.p. 1/2; see HHH → $P(B\mid HHH)=27/35$; next-head prob $=\frac{27}{35}\cdot\frac34+\frac{8}{35}\cdot\frac12=97/140$.

### Key points
- **Conditional independence ≠ independence.** Tosses of the selected coin are independent *given the coin*, but unconditionally correlated because they share the hidden coin ($\mathrm{Cov}=\mathrm{Var}(\Theta)=1/64$). See [[total-expectation-variance]].
- Predict with the **posterior**, not the prior.

### Connections
- **Builds on:** [[probability-rules-counting]].
- **Extends to:** [[beta-bernoulli-conjugacy]] — continuous-parameter version.
- **Contrast with:** [[maximum-likelihood]] (no prior) and [[hypothesis-testing]] (a p-value is $P(\text{data}\mid H_0)$-type, not $P(H_0\mid\text{data})$).
- **Finance link:** signal precision vs base rate → [[backtest-pitfalls]].

<a id="beta-bernoulli-conjugacy"></a>

## Beta–Bernoulli Conjugacy
<!-- section: beta-bernoulli-conjugacy | prerequisites: [conditional-probability-bayes, distributions-reference] | related: [maximum-likelihood, ridge-regression] | sources: [src-squarepoint-dqa-workbook] | tags: [bayes, conjugate-prior, shrinkage] -->

### Formulas
$$\theta\sim\mathrm{Beta}(a,b)\ \Rightarrow\ \theta\mid D\sim\mathrm{Beta}(a+h,\ b+t),\qquad P(H_{\text{next}}\mid D)=\frac{a+h}{a+b+h+t}$$
$$\frac{a+h}{a+b+n}=\underbrace{\frac{a+b}{a+b+n}}_{\text{prior weight}}\frac{a}{a+b}+\underbrace{\frac{n}{a+b+n}}_{\text{data weight}}\frac{h}{n}$$

**Variables:**

- $\theta$ unknown head probability
- $a,b>0$ prior pseudo-counts
- $h$ heads, $t$ tails, $n=h+t$

### Key points
- Uniform prior = Beta(1,1). After HHH: Beta(4,1), predictive $4/5$ (Laplace's rule of succession).
- Posterior mean is a **weighted average** of prior mean and MLE $h/n$ → prior washes out as $n$ grows.
- Different model from "choose between two specific coins" (discrete prior).

### Connections
- **Builds on:** [[conditional-probability-bayes]], [[distributions-reference]] (Beta pdf/mean).
- **Contrast with:** [[maximum-likelihood]] — MLE $h/n$, MAP (mode), posterior mean all differ.
- **Same idea as:** [[ridge-regression]] — Gaussian prior ⇒ shrinkage toward prior mean.
