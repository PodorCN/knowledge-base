---
id: calculus-mental-math
title: "Mathematical Toolkit: Series, Linear Algebra & Mental Math"
type: topic
domain: prob-stats
sources: [src-quant-finance-study-notes, src-squarepoint-dqa-workbook]
---
# Mathematical Toolkit: Series, Linear Algebra & Mental Math

This chapter collects the tools used by every later chapter: Taylor expansions, the exponential function and compounding, fast mental arithmetic with logarithms, complex exponents, and the matrix facts behind covariance matrices.

**Prerequisites:** none; this is the starting chapter.

**Leads to:** [[jensens-inequality]] and [[ito-lemma]] (second-order Taylor terms), [[returns-simple-log]] and [[discounting-compounding]] (compounding), [[pca]] and [[mean-variance-optimization]] (eigen-decomposition of $\Sigma$).

**Sections:** [[taylor-expansions]] · [[limit-definition-e]] · [[power-estimation]] · [[mental-math-techniques]] · [[complex-exponent-i-i]] · [[eigen-svd-psd]]

<a id="taylor-expansions"></a>

## Taylor Expansions (and where they show up in finance)
<!-- section: taylor-expansions | prerequisites: [] | related: [power-estimation, returns-simple-log, bond-duration, greeks, ito-lemma, black-scholes-formula, mean-variance-optimization, jensens-inequality] | sources: [src-quant-finance-study-notes] | tags: [taylor, approximation, second-order, convexity] -->

A smooth function is approximated near a point by its value, slope and curvature there. Almost every approximation in this wiki is a first- or second-order Taylor expansion.

### Formula
$$f(x)\approx f(a)+f'(a)(x-a)+\frac{f''(a)}{2}(x-a)^2$$

**Variables:**

- $f$ smooth function being approximated
- $x$ point at which $f$ is evaluated
- $a$ expansion point
- $f'(a),f''(a)$ first and second derivatives of $f$ at $a$

### Standard expansions (small $x$)

| Function | Expansion |
|---|---|
| $e^x$ | $1+x+x^2/2+x^3/6$ |
| $\ln(1+x)$ | $x-x^2/2+x^3/3$ |
| $\sqrt{1+x}$ | $1+x/2-x^2/8$ |
| $1/(1-x)$ | $1+x+x^2+\cdots$ (only for $\lvert x\rvert<1$) |
| $\sin x$ | $x-x^3/6$ |
| $\cos x$ | $1-x^2/2$ |

### Worked examples
- **$\sqrt{26}$:** first pull out the nearest perfect square, $\sqrt{26}=5\sqrt{1+1/25}$, so $x=0.04$: $5(1+0.02-0.0002)=5.099$ (true value 5.0990).
- **$\lim_{x\to0}\frac{\sin x-x}{x^3}$:** $\sin x=x-x^3/6+O(x^5)$, so the limit is $-\tfrac16$. This is faster than applying L'Hôpital's rule three times.

### Finance applications
Each item is developed in the linked section; the notation is the one used there.

- **Log vs simple return:** $r=\ln(1+R)\approx R-R^2/2$, hence $E[r]\approx\mu-\sigma^2/2$ (volatility drag) → [[returns-simple-log]].
- **Duration + convexity:** $\Delta P/P\approx-D_{mod}\Delta y+\tfrac12\mathcal C(\Delta y)^2$ → [[bond-duration]].
- **Delta–gamma P&L:** $\Delta V\approx\Delta\,\delta S+\tfrac12\Gamma(\delta S)^2+\Theta\,\delta t$. A delta-hedged long-gamma position earns on big moves, pays theta as rent, and profits when realised vol exceeds implied → [[greeks]], [[gamma-theta-pnl]].
- **Itô's lemma** is a second-order Taylor expansion in which $(dW)^2=dt$ is not negligible; it gives $d\ln S=(\mu-\sigma^2/2)dt+\sigma dW$ → [[ito-lemma]].
- **ATM call:** $N(d)\approx\tfrac12+d/\sqrt{2\pi}$, so $C\approx0.4\,S\sigma\sqrt T$ → [[black-scholes-formula]].
- **Certainty equivalent:** $CE\approx\mu-\tfrac12A\sigma^2$ → [[mean-variance-optimization]].

### One thread (自己推理)
- **Concave function + second-order Taylor → the expectation is penalised by variance** (Jensen): the log return loses $\sigma^2/2$, Itô loses $\sigma^2/2$, utility loses $A\sigma^2/2$ → [[jensens-inequality]].
- **Convexity makes the second-order term positive:** bond convexity, option gamma.

### Connections
- **Used by:** [[power-estimation]], [[mental-math-techniques]], [[jensens-inequality]], [[ito-lemma]], [[bond-duration]], [[greeks]].

<a id="limit-definition-e"></a>

## Limit Definition of eˣ & Continuous Compounding
<!-- section: limit-definition-e | prerequisites: [taylor-expansions] | related: [discounting-compounding, power-estimation] | sources: [src-quant-finance-study-notes] | tags: [limits, e, continuous-compounding] -->

The exponential function can be defined either as a limit of repeated compounding or as a power series. The limit form is exactly continuous compounding in finance.

### Formula
$$e^x=\lim_{n\to\infty}\Big(1+\frac xn\Big)^n,\qquad e=\lim_{n\to\infty}\Big(1+\frac1n\Big)^n,\qquad e^x=\sum_{k=0}^\infty\frac{x^k}{k!}=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots$$

**Variables:**

- $x$ any real (or complex) number
- $n$ number of sub-periods, taken to infinity
- $k$ summation index
- $k!$ factorial of $k$

### Finite-$n$ error
$$\Big(1+\frac xn\Big)^n\approx e^x\cdot e^{-x^2/(2n)}$$

**Variables:**

- $x$ total growth exponent
- $n$ finite number of compounding steps

**Notes:**

- **Why it converges:** $n\ln(1+x/n)\approx n\big(x/n-x^2/(2n^2)\big)=x-x^2/(2n)\to x$.
- The correction $x^2/(2n)$ comes from the second-order term of $\ln(1+x/n)$, so finite $n$ is always **slightly below** $e^x$.
- Example: $0.99^{100}\approx e^{-1}e^{-0.005}\approx0.366$ ✓ (see [[power-estimation]]).

### Continuous compounding
$$\lim_{n\to\infty}\Big(1+\frac rn\Big)^{nT}=e^{rT}$$

**Variables:**

- $r$ annual interest rate
- $n$ compounding periods per year
- $T$ horizon in years

| Frequency | $n$ | Value of 1 after $r=10\%$, $T=1$ |
|---|---|---|
| Annual | 1 | 1.1000 |
| Quarterly | 4 | 1.1038 |
| Monthly | 12 | 1.1047 |
| Daily | 365 | 1.1052 |
| Continuous | ∞ | $e^{0.1}$ = 1.1052 |

### Interview answer
"e^x is defined as the limit of (1 + x/n)^n as n goes to infinity. Intuitively, you split growth at rate x into n tiny steps and compound them. In finance, that's exactly continuous compounding: (1 + r/n)^(nT) → e^(rT). Equivalently, e^x is the Taylor series Σ x^k/k!."

### Connections
- **Builds on:** [[taylor-expansions]].
- **Used by:** [[discounting-compounding]] (finance conventions), [[power-estimation]] (same finite-$n$ error).

<a id="power-estimation"></a>

## Estimating "Weird Powers" (0.99¹⁰⁰, 1.1¹⁰, e^π vs π^e)
<!-- section: power-estimation | prerequisites: [taylor-expansions] | related: [limit-definition-e, mental-math-techniques, returns-simple-log, jensens-inequality] | sources: [src-quant-finance-study-notes] | tags: [mental-math, logarithm, compounding] -->

Any power can be turned into an exponential of a product, and the logarithm of a number close to 1 is easy to expand. One trick therefore handles all such questions.

### Formula
$$a^b=e^{\,b\ln a},\qquad \ln(1+x)\approx x-\frac{x^2}{2},\qquad e^y\approx1+y+\frac{y^2}{2}$$

**Variables:**

- $a$ base
- $b$ exponent
- $x$ distance of the base from 1, $a=1+x$ (smaller $x$ → more accurate)
- $y$ small number used to correct around a known value of $e$

### Worked example: $0.99^{100}$
1. $\ln0.99\approx-0.01-0.00005=-0.01005$
2. $\times100=-1.005$
3. $e^{-1.005}=e^{-1}\cdot e^{-0.005}\approx0.3679\times0.995\approx0.366$ (true value 0.36603)

**Interview answer:** "I'd write it as e^(100·ln 0.99). ln(0.99) is about −0.01, so the exponent is about −1, giving roughly 1/e ≈ 0.37. With the second-order term, ln(0.99) ≈ −0.01005, so the exponent is −1.005 and the answer is slightly below 1/e — about 0.366."

### Quick reference

| Expression | Transform | Result | True value |
|---|---|---|---|
| $0.99^{100}$ | $e^{-1.005}$ | ≈ 0.366 | 0.3660 |
| $1.01^{100}$ | $e^{0.995}$ | ≈ 2.705 | 2.7048 |
| $0.9^{10}$ | $\ln0.9\approx-0.1054\to e^{-1.054}$ | ≈ 0.349 | 0.3487 |
| $1.1^{10}$ | $\ln1.1\approx0.0953\to e^{0.953}$ | ≈ 2.59 | 2.5937 |
| $1.05^{20}$ | $\ln1.05\approx0.0488\to e^{0.976}$ | ≈ 2.65 | 2.6533 |
| $e^\pi$ vs $\pi^e$ | compare $\pi$ vs $e\ln\pi$ | $e^\pi$ larger | 23.14 vs 22.46 |

When $x$ is not small (e.g. 0.1) the second-order term is required: $1.1^{10}$ with only the first order gives $e=2.718$, 5% off.

### $e^\pi$ vs $\pi^e$
$$f(x)=\frac{\ln x}{x},\qquad f'(x)=\frac{1-\ln x}{x^2}$$

**Variables:**

- $f$ auxiliary function on $x>0$
- $f'$ its derivative

$f'(x)=0$ at $x=e$, so $f$ peaks at $x=e$ → $f(e)>f(\pi)$, i.e. $\frac{1}{e}>\frac{\ln\pi}{\pi}$ → $\pi>e\ln\pi$ → **$e^\pi>\pi^e$**.

### Finance links
- Falling 1% a day for 100 days leaves ~37%.
- **Rule of 72:** doubling time $\approx\ln2/r\approx0.693/r$ (72 is used because it divides more evenly).
- **Volatility drag:** +1% and −1% alternating 100 times gives $(1.01\times0.99)^{50}=0.9999^{50}\approx0.995\ne1$ ([[returns-simple-log]]).

### Connections
- **Builds on:** [[taylor-expansions]].
- **Same idea as:** [[limit-definition-e]] (finite-$n$ error $e^{-x^2/(2n)}$).
- **Used by:** [[mental-math-techniques]].

<a id="mental-math-techniques"></a>

## Mental Math in the Interview (three tricks)
<!-- section: mental-math-techniques | prerequisites: [taylor-expansions] | related: [power-estimation, complex-exponent-i-i] | sources: [src-quant-finance-study-notes] | tags: [mental-math, anchors, logarithm] -->

Exponentials and logarithms can be computed in your head by combining a few memorised anchor values with a first- or second-order correction.

### ① Memorise anchors

| Log | Value | Use in reverse |
|---|---|---|
| $\ln2$ | 0.69 | $e^{0.69}=2$ |
| $\ln3$ | 1.10 | $e^{1.1}=3$ |
| $\ln5$ | 1.61 | $e^{1.61}=5$ |
| $\ln10$ | 2.30 | $e^{2.3}=10$ |
| 1 | 1 | $e=2.718,\ 1/e=0.368$ |
| 0.5 | 0.5 | $e^{0.5}=1.65,\ e^{-0.5}=0.607$ |

Other constants: $e^{-1.5}=0.223$, $e^2=7.389$, $\sqrt2=1.414$.

**Split the exponent into a sum of anchors:** $1.8=0.69+1.1$ → $e^{1.8}\approx2\times3=6$ (true 6.05).

### ② First/second order for the small remainder
$$e^\delta\approx1+\delta+\frac{\delta^2}{2},\qquad \ln(1+x)\approx x-\frac{x^2}{2}+\frac{x^3}{3}$$

**Variables:**

- $\delta$ leftover exponent after removing anchors (first order is usually enough when $|\delta|<0.1$)
- $x$ distance of the number from 1 ($|x|\le0.01$: first order; 0.05–0.1: add the second order)

### ③ Multiply by subtracting
$$A\times(1-\delta)=A-A\delta$$

**Variables:**

- $A$ anchor value
- $\delta$ small correction

### Worked examples

| Expression | Steps | Answer |
|---|---|---|
| $e^{-1.57}$ | anchor $\ln0.2=0.69-2.30=-1.61$; difference $+0.04$ → $0.2\times1.04$ | 0.208 ✓ |
| $0.99^{100}$ | exponent $-1.005$; $0.368-0.368\times0.005$ | 0.366 ✓ |
| $1.1^{10}$ | $\ln1.1\approx0.1-0.005+0.0003=0.0953$; $2.718-2.718\times0.046$ | 2.593 ✓ |
| $1.05^{20}$ | exponent $0.976$; $2.718-2.718\times0.024$ | 2.653 ✓ |

### Speaking rhythm (自己推理)
1. **State the method:** "I'll rewrite it as e to the power of 100 times ln 0.99."
2. **Rough answer first:** "ln 0.99 is about −0.01, so roughly e^(−1), about 0.37."
3. **Then correct:** "The second-order term makes the exponent −1.005, so slightly less — about 0.366."

The rough answer passes; the correction earns extra credit. If you can't compute it exactly, say "slightly below/above because…": getting the direction right is enough.

### Drill values

| Expression | Value |
|---|---|
| $e^{0.1}$ | 1.105 |
| $e^{1.4}$ ($=2\times2\times e^{0.02}$) | ≈ 4.06 |
| $e^3$ ($=e^{2.3}\times e^{0.7}$) | ≈ 20.1 |
| $0.95^{20}$ | ≈ 0.358 |
| $2^{10}$ vs $e^7$ | 1024 vs ≈ 1097 |

### Connections
- **Builds on:** [[taylor-expansions]].
- **Applied in:** [[power-estimation]], [[complex-exponent-i-i]] ($e^{-1.57}$).

<a id="complex-exponent-i-i"></a>

## Computing iⁱ (Euler's formula, complex logarithm)
<!-- section: complex-exponent-i-i | prerequisites: [mental-math-techniques] | related: [power-estimation] | sources: [src-quant-finance-study-notes] | tags: [complex-numbers, euler, complex-log, multi-valued] -->

A classic interview question: write $i$ in polar form with Euler's formula, raise it to the power $i$, and evaluate the result mentally. The answer is a real number.

### Formula
$$e^{i\theta}=\cos\theta+i\sin\theta\ \Rightarrow\ i=e^{i\pi/2},\qquad i^i=\big(e^{i\pi/2}\big)^i=e^{i\cdot i\pi/2}=e^{-\pi/2}$$

**Variables:**

- $i$ imaginary unit, $i^2=-1$
- $\theta$ argument (angle in the complex plane); $i$ lies on the positive imaginary axis, so $\theta=\pi/2$

**Number:** $e^{-\pi/2}=e^{-1.5708}\approx0.2079$ (mentally: $e^{-1.5}\approx0.223$, × $e^{-0.07}\approx0.93$ → 0.208). **$i^i$ is real, ≈ 0.208.**

### Multi-valuedness (bonus point)
$$i=e^{i(\pi/2+2\pi k)}\Rightarrow i^i=e^{-\pi/2-2\pi k},\qquad z^w=e^{w\ln z},\ \ \ln z=\ln|z|+i(\arg z+2\pi k)$$

**Variables:**

- $k$ any integer; $k=0$ gives the principal value $e^{-\pi/2}$
- $z$ complex base
- $w$ complex exponent
- $|z|$ modulus of $z$ ($|i|=1\Rightarrow\ln|i|=0$)
- $\arg z$ principal argument of $z$

### Interview answer
"I'd use Euler's formula. Since i sits on the unit circle at angle π/2, I can write i = e^(iπ/2). Raising that to the power i gives e^(i·iπ/2) = e^(−π/2), which is about 0.208 — surprisingly, a real number. Strictly speaking, complex exponentiation is multi-valued, because the argument of i is π/2 plus any multiple of 2π. So the full answer is e^(−π/2 − 2πk) for integer k, and e^(−π/2) is the principal value."

### Follow-ups

| Follow-up | Key point |
|---|---|
| Why is it real? | $i\cdot i=-1$ turns "rotation" into "scaling" |
| Is $(i^i)^i=i^{i\cdot i}$? | RHS $=i^{-1}=-i$; LHS $=e^{-i\pi/2}=-i$ (equal by coincidence for principal values). In general $(z^a)^b\ne z^{ab}$ for complex numbers because the logarithm is multi-valued |
| Estimate without calculator? | $\pi/2\approx1.57$, slightly beyond 1.5, so slightly below $e^{-1.5}\approx0.22$ → ≈ 0.21 |

### Connections
- **Mental arithmetic for $e^{-1.57}$:** [[mental-math-techniques]].

<a id="eigen-svd-psd"></a>

## Eigen-decomposition, SVD & PSD Matrices
<!-- section: eigen-svd-psd | prerequisites: [] | related: [pca, multicollinearity, portfolio-variance-diversification, mean-variance-optimization, variance-covariance-correlation] | sources: [src-squarepoint-dqa-workbook] | tags: [linear-algebra] -->

Covariance matrices, regression design matrices and optimisers are all analysed through eigenvalues and singular values. These are the facts used later.

### Definitions
$$Av=\lambda v,\qquad v^\top Av\ge0\ \ \forall v\ \ (\text{PSD}),\qquad X=UDV^\top\ \ (\text{SVD})$$

**Variables:**

- $A$ square matrix
- $v$ eigenvector (for PSD: any vector)
- $\lambda$ eigenvalue
- $X$ any rectangular matrix (e.g. a design matrix)
- $U,V$ orthogonal matrices
- $D$ diagonal matrix of singular values of $X$

### Key points
- A real symmetric matrix has an orthonormal eigenbasis.
- **PSD** (positive semi-definite) ⇔ all eigenvalues ≥ 0.
- A covariance matrix $\Sigma$ is PSD because $v^\top\Sigma v=\mathrm{Var}(v^\top X)\ge0$ for a random vector $X$ ([[variance-covariance-correlation]]).
- A matrix is invertible ⇔ it has full rank.
- Small singular values ⇒ unstable least squares (the inverse amplifies noise in those directions).

### Connections
- **Used by:** [[pca]] (eigenvectors of $\Sigma$), [[multicollinearity]] (small eigenvalues of $X^\top X$), [[portfolio-variance-diversification]] (valid correlation matrices), [[mean-variance-optimization]] (inverting $\Sigma$ amplifies small-eigenvalue noise).
