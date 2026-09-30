---
id: probability-bayes
title: "Probability & Bayes' Theorem"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# Probability & Bayes' Theorem

This chapter sets up the rules for combining probabilities and for updating them when information arrives. Every later statistical and pricing argument is built from these two steps: count (or measure) outcomes, then condition.

**Prerequisites:** none.

**Leads to:** [[distributions-reference]] (named distributions), [[expectation-linearity-indicators]] (expectations), [[beta-bernoulli-conjugacy]] (Bayesian estimation), [[hypothesis-testing]] (frequentist contrast).

**Sections:** [[probability-rules-counting]] · [[conditional-probability-bayes]]

<a id="probability-rules-counting"></a>

## Probability Rules & Counting
<!-- section: probability-rules-counting | prerequisites: [] | related: [conditional-probability-bayes, expectation-linearity-indicators] | sources: [src-squarepoint-dqa-workbook] | tags: [counting, complement, inclusion-exclusion] -->

The basic rules: add probabilities of unions (subtracting the overlap), use complements for "at least one", and count arrangements with permutations and combinations.

### Formulas
$$P(A\cup B)=P(A)+P(B)-P(A\cap B),\qquad P(A^c)=1-P(A)$$
$$P(n,k)=\frac{n!}{(n-k)!},\qquad \binom{n}{k}=\frac{n!}{k!\,(n-k)!}$$
$$P(\text{at least one})=1-(1-p)^n$$

**Variables:**

- $A,B$ events
- $A^c$ complement of $A$
- $P(n,k)$ number of ordered selections of $k$ items from $n$
- $\binom nk$ number of unordered selections of $k$ items from $n$
- $n$ number of items, or of independent trials
- $k$ number of items chosen
- $p$ per-trial probability (independent trials)

### Key points
- **Mutually exclusive ≠ independent.** Two exclusive events with positive probability are *dependent*: one rules out the other.
- Sampling **with** replacement gives independent draws; **without** replacement gives dependent draws. E.g. two aces without replacement: $\frac{4}{52}\cdot\frac{3}{51}=\frac{1}{221}$.
- At least one six in four rolls: $1-(5/6)^4\approx 0.5177$.
- Before using a ratio of counts, check the elementary outcomes are **equally likely**.

### Connections
- **Used by:** [[conditional-probability-bayes]] (conditioning is "restrict the sample space, renormalise"), [[expectation-linearity-indicators]] (indicator tricks often replace hard counting), [[distributions-reference]].

<a id="conditional-probability-bayes"></a>

## Conditional Probability & Bayes' Theorem
<!-- section: conditional-probability-bayes | prerequisites: [probability-rules-counting] | related: [beta-bernoulli-conjugacy, total-expectation-variance, maximum-likelihood, hypothesis-testing, bayesianized-p-value] | sources: [src-squarepoint-dqa-workbook] | tags: [bayes, base-rate, independence] -->

Conditioning on an event restricts attention to the outcomes where it happened and renormalises. Bayes' theorem turns "probability of the data given a hypothesis" into "probability of the hypothesis given the data".

### Formulas
$$P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(D)=\sum_j P(D\mid H_j)P(H_j)$$
$$P(H_i\mid D)=\frac{P(D\mid H_i)P(H_i)}{\sum_j P(D\mid H_j)P(H_j)},\qquad \frac{P(H_1\mid D)}{P(H_0\mid D)}=\frac{P(H_1)}{P(H_0)}\cdot\frac{P(D\mid H_1)}{P(D\mid H_0)}$$

**Variables:**

- $A,B$ events, $P(B)>0$
- $H_i$ disjoint hypotheses covering all cases
- $D$ observed data
- $P(H_i)$ prior probability of $H_i$
- $P(D\mid H_i)$ likelihood of the data under $H_i$
- $P(D)$ evidence (the normaliser, from the law of total probability)
- $P(H_i\mid D)$ posterior probability of $H_i$

The last formula reads: **posterior odds = prior odds × likelihood ratio**.

### Worked examples
- **Signal & base rate:** a favourable state occurs 10% of the time; a signal fires 80% of the time when the state is favourable and 20% otherwise. Then $P(F\mid S)=\frac{0.8\times0.1}{0.8\times0.1+0.2\times0.9}=\frac{0.08}{0.08+0.18}=4/13\approx30.8\%$. Rare states make even good detectors imprecise.
- **Selected coin:** pick a fair coin A or a biased coin B ($P(H)=3/4$), each with probability 1/2, and observe HHH. Then $P(B\mid HHH)=\frac{27/64}{27/64+8/64}=27/35$, and the probability that the next toss is a head is $\frac{27}{35}\cdot\frac34+\frac{8}{35}\cdot\frac12=97/140$.

### Key points
- **Conditional independence ≠ independence.** Tosses of the selected coin are independent *given the coin*, but unconditionally correlated because they share the hidden coin ($\mathrm{Cov}=\mathrm{Var}(\Theta)=1/64$, where $\Theta$ is the head probability of the selected coin). See [[total-expectation-variance]].
- Predict with the **posterior**, not the prior.

### Connections
- **Builds on:** [[probability-rules-counting]].
- **Extends to:** [[beta-bernoulli-conjugacy]] (continuous-parameter version), [[bayesianized-p-value]] (posterior probability of a null hypothesis).
- **Contrast:** [[maximum-likelihood]] (no prior) and [[hypothesis-testing]] (a p-value is a $P(\text{data}\mid H_0)$-type quantity, not $P(H_0\mid\text{data})$).
- **Finance link:** signal precision vs base rate → [[backtest-pitfalls]].
