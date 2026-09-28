---
id: calculus-mental-math
title: "Calculus, Complex Exponents & Mental Math"
type: topic
domain: prob-stats
sources: [src-quant-finance-study-notes]
---
# Calculus, Complex Exponents & Mental Math

**Sections:** [[complex-exponent-i-i]] · [[power-estimation]] · [[limit-definition-e]] · [[mental-math-techniques]] · [[taylor-expansions]]

<a id="complex-exponent-i-i"></a>

## Computing iⁱ (Euler's formula, complex logarithm)
<!-- section: complex-exponent-i-i | prerequisites: [] | related: [power-estimation, mental-math-techniques] | sources: [src-quant-finance-study-notes] | tags: [complex-numbers, euler, complex-log, multi-valued] -->

### Formula
$$e^{i\theta}=\cos\theta+i\sin\theta\ \Rightarrow\ i=e^{i\pi/2},\qquad i^i=\big(e^{i\pi/2}\big)^i=e^{i\cdot i\pi/2}=e^{-\pi/2}$$

**Variables:**

- $\theta$ argument (angle in the complex plane); $i$ is on the positive imaginary axis → $\theta=\pi/2$

**Number:** $e^{-\pi/2}=e^{-1.5708}\approx0.2079$ (mental: $e^{-1.5}\approx0.223$, × $e^{-0.07}\approx0.93$ → 0.208). **$i^i$ is real, ≈ 0.208.**

### Multi-valuedness (bonus point)
$$i=e^{i(\pi/2+2\pi k)}\Rightarrow i^i=e^{-\pi/2-2\pi k},\qquad z^w=e^{w\ln z},\ \ \ln z=\ln|z|+i(\arg z+2\pi k)$$

**Variables:**

- $k$ any integer; $k=0$ → principal value $e^{-\pi/2}$
- $z$ complex base
- $w$ complex exponent
- $|z|$ modulus ($|i|=1\Rightarrow\ln|i|=0$)
- $\arg z$ principal argument

### Answer template (~30 s)
"I'd use Euler's formula. Since i sits on the unit circle at angle π/2, I can write i = e^(iπ/2). Raising that to the power i gives e^(i·iπ/2) = e^(−π/2), which is about 0.208 — surprisingly, a real number. Strictly speaking, complex exponentiation is multi-valued, because the argument of i is π/2 plus any multiple of 2π. So the full answer is e^(−π/2 − 2πk) for integer k, and e^(−π/2) is the principal value."

### Follow-ups

| Follow-up | Key point |
|---|---|
| Why is it real? | $i\cdot i=-1$ turns "rotation" into "scaling" |
| Is $(i^i)^i=i^{i\cdot i}$? | RHS $=i^{-1}=-i$; LHS $=e^{-i\pi/2}=-i$ (equal by coincidence for principal values). In general $(z^a)^b\ne z^{ab}$ for complex numbers because log is multi-valued |
| Estimate without calculator? | $\pi/2\approx1.57$, slightly below $e^{-1.5}\approx0.22$ → ≈ 0.21 |

### Connections
- **Mental arithmetic for $e^{-1.57}$:** [[mental-math-techniques]].

<a id="power-estimation"></a>

## Estimating "Weird Powers" (0.99¹⁰⁰, 1.1¹⁰, e^π vs π^e)
<!-- section: power-estimation | prerequisites: [taylor-expansions] | related: [limit-definition-e, mental-math-techniques, returns-simple-log, jensens-inequality] | sources: [src-quant-finance-study-notes] | tags: [mental-math, logarithm, compounding] -->

### One trick for all
$$a^b=e^{\,b\ln a},\qquad \ln(1+x)\approx x-\frac{x^2}{2},\qquad e^y\approx1+y+\frac{y^2}{2}$$

**Variables:**

- $a$ base
- $b$ exponent
- $x$ distance of the base from 1 (smaller → more accurate)
- $y$ small number used to correct around a known value of $e$

### Worked example: $0.99^{100}$
1. $\ln0.99\approx-0.01-0.00005=-0.01005$
2. $\times100=-1.005$
3. $e^{-1.005}=e^{-1}\cdot e^{-0.005}\approx0.3679\times0.995\approx0.366$ (true 0.36603)

"I'd write it as e^(100·ln 0.99). ln(0.99) is about −0.01, so the exponent is about −1, giving roughly 1/e ≈ 0.37. With the second-order term, ln(0.99) ≈ −0.01005, so the exponent is −1.005 and the answer is slightly below 1/e — about 0.366."

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

- $f$ auxiliary function, $x>0$

$f$ peaks at $x=e$ → $f(e)>f(\pi)$ → **$e^\pi>\pi^e$**.

### Finance links
- Falling 1% a day for 100 days → ~37% left.
- **Rule of 72:** doubling time $\approx\ln2/r\approx0.693/r$ (72 divides more evenly).
- **Volatility drag:** +1%/−1% alternating 100 times → $(1.01\times0.99)^{50}=0.9999^{50}\approx0.995\ne1$ ([[returns-simple-log]]).

### Connections
- **Builds on:** [[taylor-expansions]]. **Same idea as:** [[limit-definition-e]] (finite-$n$ error $e^{-x^2/(2n)}$).

<a id="limit-definition-e"></a>

## Limit Definition of eˣ & Continuous Compounding
<!-- section: limit-definition-e | prerequisites: [] | related: [discounting-compounding, power-estimation, taylor-expansions] | sources: [src-quant-finance-study-notes] | tags: [limits, e, continuous-compounding] -->

### Formula
$$e^x=\lim_{n\to\infty}\Big(1+\frac xn\Big)^n,\qquad e=\lim_{n\to\infty}\Big(1+\frac1n\Big)^n,\qquad e^x=\sum_{k=0}^\infty\frac{x^k}{k!}=1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots$$

**Variables:**

- $x$ any real (or complex) number
- $n$ number of sub-periods → ∞
- $k$ summation index; $k!$ factorial

### Finite-$n$ error
$$\Big(1+\frac xn\Big)^n\approx e^x\cdot e^{-x^2/(2n)}$$

- $x^2/(2n)$ comes from the 2nd-order term of $\ln(1+x/n)$ → finite $n$ is always **slightly below** $e^x$.
- e.g. $0.99^{100}\approx e^{-1}e^{-0.005}\approx0.366$ ✓
- **Why it converges:** $n\ln(1+x/n)\approx n\big(x/n-x^2/(2n^2)\big)=x-x^2/(2n)\to x$.

### Continuous compounding
$$\lim_{n\to\infty}\Big(1+\frac rn\Big)^{nT}=e^{rT}$$

**Variables:**

- $r$ annual rate
- $n$ compounding periods per year
- $T$ years

| Frequency | n | $1 after r = 10%, T = 1 |
|---|---|---|
| Annual | 1 | 1.1000 |
| Quarterly | 4 | 1.1038 |
| Monthly | 12 | 1.1047 |
| Daily | 365 | 1.1052 |
| Continuous | ∞ | $e^{0.1}$ = 1.1052 |

"e^x is defined as the limit of (1 + x/n)^n as n goes to infinity. Intuitively, you split growth at rate x into n tiny steps and compound them. In finance, that's exactly continuous compounding: (1 + r/n)^(nT) → e^(rT). Equivalently, e^x is the Taylor series Σ x^k/k!."

### Connections
- **Finance conventions:** [[discounting-compounding]].

<a id="mental-math-techniques"></a>

## Mental Math in the Interview (three tricks)
<!-- section: mental-math-techniques | prerequisites: [taylor-expansions] | related: [power-estimation, complex-exponent-i-i] | sources: [src-quant-finance-study-notes] | tags: [mental-math, anchors, logarithm] -->

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

- $\delta$ leftover after removing anchors (first order is usually enough when $|\delta|<0.1$)
- $x$ distance from 1 ($|x|\le0.01$ first order; 0.05–0.1 add the second order)

### ③ Multiply by subtracting
$$A\times(1-\delta)=A-A\delta$$

**Variables:**

- $A$ anchor value
- $\delta$ small correction

### Worked examples

| Expression | Steps | Answer |
|---|---|---|
| $e^{-1.57}$ | anchor $\ln0.2=0.69-2.30=-1.61$; diff $+0.04$ → $0.2\times1.04$ | 0.208 ✓ |
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

<a id="taylor-expansions"></a>

## Taylor Expansions (and where they show up in finance)
<!-- section: taylor-expansions | prerequisites: [] | related: [power-estimation, returns-simple-log, bond-duration, greeks, ito-lemma, black-scholes-formula, mean-variance-optimization, jensens-inequality] | sources: [src-quant-finance-study-notes] | tags: [taylor, approximation, second-order, convexity] -->

### Formula
$$f(x)\approx f(a)+f'(a)(x-a)+\frac{f''(a)}{2}(x-a)^2$$

**Variables:**

- $a$ expansion point
- $f',f''$ 1st / 2nd derivatives

| Function | Expansion (small $x$) |
|---|---|
| $e^x$ | $1+x+x^2/2+x^3/6$ |
| $\ln(1+x)$ | $x-x^2/2+x^3/3$ |
| $\sqrt{1+x}$ | $1+x/2-x^2/8$ |
| $1/(1-x)$ | $1+x+x^2+\cdots$ (only $\lvert x\rvert<1$) |
| $\sin x$ | $x-x^3/6$ |
| $\cos x$ | $1-x^2/2$ |

### Worked examples
- **$\sqrt{26}$:** $\sqrt{26}=5\sqrt{1+1/25}$, $x=0.04$: $5(1+0.02-0.0002)=5.099$ (true 5.0990). Trick: first pull out the nearest perfect square.
- **$\lim_{x\to0}\frac{\sin x-x}{x^3}$:** $\sin x=x-x^3/6+O(x^5)$ → limit $=-\tfrac16$. Faster than applying L'Hôpital three times.

### Finance applications
- **Log vs simple return:** $r=\ln(1+R)\approx R-R^2/2$, $E[r]\approx\mu-\sigma^2/2$ (volatility drag) → [[returns-simple-log]].
- **Duration + convexity:** $\Delta P/P\approx-D_{mod}\Delta y+\tfrac12C(\Delta y)^2$ → [[bond-duration]].
- **Delta–gamma P&L:** $\Delta V\approx\Delta\,\delta S+\tfrac12\Gamma(\delta S)^2+\Theta\,\delta t$; delta-hedged, long gamma earns on big moves, pays theta rent, profits when realised vol > implied → [[greeks]], [[gamma-theta-pnl]].
- **Itô's lemma** = second-order Taylor with $(dW)^2=dt$ not negligible; $d\ln S=(\mu-\sigma^2/2)dt+\sigma dW$ → [[ito-lemma]].
- **ATM call:** $N(d)\approx\tfrac12+d/\sqrt{2\pi}$ → $C\approx0.4\,S\sigma\sqrt T$ → [[black-scholes-formula]].
- **Certainty equivalent:** $CE\approx\mu-\tfrac12A\sigma^2$ → [[mean-variance-optimization]].

### One thread (自己推理)
- **Concave function + second-order Taylor → the expectation is penalised by variance** (Jensen): log return loses $\sigma^2/2$, Itô loses $\sigma^2/2$, utility loses $A\sigma^2/2$ → [[jensens-inequality]].
- **Convexity makes the second-order term positive:** bond convexity, option gamma.
