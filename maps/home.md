---
id: home
title: Home — Knowledge Map
type: map
domain: ""
tags: [index]
---
# Home — Knowledge Map

- **[[map-foundations]]**: [[map-prob-stats]] · [[map-stochastic-finance]]
- **[[map-buyside]]**: [[map-signal-research]] · [[map-portfolio-construction]]
- **[[map-sellside]]**: [[map-black-scholes]] · [[map-pricing]] · [[map-risk-management]] · [[map-quant-dev]]

## How to read this wiki

Chapters are numbered in reading order: every section is placed after the sections it builds on, and each chapter opens with its prerequisites and what it leads to. Foundations are needed by both sides; the Buy-side and Sell-side groups can be read independently after the Foundations. Inside a section the layout is always the same: a short statement of the idea, the **Formula** or **Definition** with a table of its variables, **Key points**, a **Worked example** where one exists, and **See also** links. Marks such as **(自己推理)** (own reasoning) and ✏️ (a corrected number) are kept from the original notes.

## Notation & conventions

Symbols below have the same meaning everywhere; a chapter that needs a local symbol defines it in its introduction or in the section's variable table.

| Symbol | Meaning |
|---|---|
| $\mathbb P$, $\mathbb Q$, $\mathbb Q^S$ | real-world, risk-neutral and stock-numeraire probability measures; $E^{\mathbb Q}[\cdot]$ expectation under $\mathbb Q$ |
| $N(\cdot)$, $\phi(\cdot)$ | standard normal CDF and density |
| $\ln$ | natural logarithm |
| $\mathbf 1_A$, $x^+$ | indicator of event $A$; $\max(x,0)$ |
| $t$, $T$, $\tau$ | current time, maturity (years), time to maturity $\tau=T-t$ (formulas at $t=0$ use $T$) |
| $r$, $q$, $D$ | continuously compounded risk-free rate, continuous dividend yield (incl. borrow where stated), discount factor $D=e^{-r\tau}$ |
| $\mathrm{Div}_i$ | cash dividend with ex-date $t_i$ |
| $S_t$, $F$, $K$ | spot price, forward price for delivery at $T$ ($F=S_0e^{(r-q)T}$), strike |
| $k$, $\omega$ | log-moneyness $k=\ln(K/F)$; total implied variance $\omega=\sigma^2T$ |
| $C$, $P$, $V$, $h$ | call price, put price, generic derivative value, payoff function |
| $\sigma$, $\sigma_{\text{imp}}$, $\sigma_{\text{real}}$ | volatility; implied and realised volatility |
| $\Delta$, $\Gamma$, $\mathcal V$, $\Theta$, $\mathrm{Rho}$ | delta, gamma, vega, theta, rho |
| $\mu$, $W_t$, $\mathcal F_t$ | real-world drift / expected return, Brownian motion, information at $t$ |
| $R_t$, $r_t$, $r_f$ | simple return, log return, risk-free return per period |
| $n$, $\bar X$, $s$ | sample size, sample mean, sample standard deviation |
| $y$, $X$, $\beta$, $\varepsilon$, $e$, $p$ | regression response, design matrix, coefficients, errors, residuals, number of coefficients (incl. intercept) |
| $\rho$, $\Sigma$ | correlation, covariance matrix |
| $w$, $\mu$, $\sigma_p$, $\gamma$ | portfolio weights, expected excess returns, portfolio volatility, risk aversion |
| $SR$, $IR$, $IC$ | Sharpe ratio, information ratio, information coefficient |
| $s_{i,t}$, $z_i$, $b_i$ | signal of asset $i$ at $t$, cross-sectional z-score, risk budget |

Bonds use $P$ (price), $M$ (face value), $c$ (annual coupon) and $y$ (yield) inside their chapter.
