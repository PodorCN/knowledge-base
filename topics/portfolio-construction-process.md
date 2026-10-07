---
id: portfolio-construction-process
title: "The Portfolio Construction Process"
type: topic
domain: portfolio-construction
sources: [src-portopt-pm-interview]
---
# The Portfolio Construction Process

A desk turns forecasts into trades through a fixed sequence of stages. The signal stage (alpha) lives in the signal-research track and the optimiser itself in [[mean-variance-optimization]] and the rest of Portfolio Optimisation; this chapter covers everything around them: the pipeline as a whole, the mandate and tracking-error budget, the risk model (covariance estimation), transaction costs and rebalancing, and how to prove that the optimiser adds value.

**Prerequisites:** [[mean-variance-optimization]], [[lagrange-kkt-duality]], [[eigen-svd-psd]], [[grinold-alpha]], [[backtest-pitfalls]].

**Leads to:** [[risk-measures]] (realised tracking error and IR), [[hedging]].

**Sections:** [[portfolio-construction-pipeline]] · [[mandate-tracking-error]] · [[covariance-estimation]] · [[transaction-costs-no-trade]] · [[portfolio-validation-attribution]]

Notation for this chapter: $w$ target weights, $w_0$ current weights, $b$ benchmark weights, $\alpha$ expected (excess or residual) returns, $\Sigma$ covariance matrix, $\gamma$ risk aversion, $N$ number of assets, $T$ number of observations.

<a id="portfolio-construction-pipeline"></a>

## The Pipeline: Nine Stages from Mandate to Attribution
<!-- section: portfolio-construction-pipeline | prerequisites: [mean-variance-optimization] | related: [mandate-tracking-error, covariance-estimation, transaction-costs-no-trade, portfolio-validation-attribution, grinold-alpha, constraints-shadow-prices] | sources: [src-portopt-pm-interview] | tags: [process, portfolio-construction, interview] -->

Portfolio optimisation in production is a pipeline, not a formula. Each stage feeds the next, and skipping one produces a characteristic failure.

### The stages

| # | Stage | What you decide | What breaks if you skip it | Section |
|---|---|---|---|---|
| 1 | **Mandate and objective** | Absolute return or benchmark-relative? TE budget, leverage, gross/net limits, horizon | You optimise the wrong objective very precisely | [[mandate-tracking-error]] |
| 2 | **Universe** | Investable assets: liquidity screens, borrow availability, restricted lists | The optimiser loves illiquid names because their "risk" looks low | — |
| 3 | **Alpha / expected returns** | Signals → scores → return forecasts, scaled correctly | Raw z-scores fed in as returns give absurd sizes | [[grinold-alpha]] |
| 4 | **Risk model** | Factor model or shrunk covariance; the horizon of the estimate | $\Sigma^{-1}$ blows up the noise | [[covariance-estimation]] |
| 5 | **Transaction-cost model** | Spread, commissions, market impact, borrow cost | Paper alpha eaten by turnover | [[transaction-costs-no-trade]] |
| 6 | **Optimisation** | Objective + constraints → solver (QP / SOCP) | Corner solutions, infeasibility | [[mean-variance-optimization]], [[optimiser-infeasibility]] |
| 7 | **Post-optimisation checks** | Risk decomposition, factor exposures, concentration, liquidity (days to trade out) | You find out what you hold only after it hurts | [[risk-contribution]], [[portfolio-validation-attribution]] |
| 8 | **Implementation and rebalancing** | When to trade, no-trade bands, execution schedule | Churn | [[transaction-costs-no-trade]] |
| 9 | **Attribution and feedback** | Was the P&L alpha, factors or costs? Recalibrate | You never learn which stage failed | [[portfolio-validation-attribution]] |

### Formula: the canonical single-period problem
$$\max_{w}\ \ \alpha^\top w\;-\;\frac{\gamma}{2}\,(w-b)^\top\Sigma\,(w-b)\;-\;\kappa^\top|w-w_0|\;-\;\lambda\,\text{TC}(w-w_0)\quad\text{s.t. } Aw\le c$$

**Variables:**

- $w$ target weights; $w_0$ current weights
- $b$ benchmark weights ($b=0$ for an absolute-return book)
- $\alpha$ vector of expected (excess / residual) returns
- $\Sigma$ covariance matrix from the risk model
- $\gamma$ risk aversion
- $\kappa$ per-asset linear cost (half-spread + commission); $|w-w_0|$ taken element by element
- $\text{TC}(\cdot)$ non-linear market-impact cost; $\lambda$ its weight (cost aversion)
- $A,c$ linear constraints (budget, sector/factor neutrality, position limits)

### Key points
- A senior analyst's job is to say *why the optimiser's answer is wrong* before it trades: most failures come from stages 3–5 (inputs), not from the solver.
- How to write this as a QP in practice (splitting $|w-w_0|$ into buys and sells): [[matlab-custom-portfolio-optimization]].

### Connections
- **Builds on:** [[mean-variance-optimization]].
- **Detail of each stage:** the sections of this chapter; [[grinold-alpha]] (stage 3); [[constraints-shadow-prices]] (stage 6).

<a id="mandate-tracking-error"></a>

## Mandate, Tracking Error & Information Ratio
<!-- section: mandate-tracking-error | prerequisites: [portfolio-construction-pipeline, information-coefficient] | related: [risk-measures, constraints-shadow-prices, grinold-alpha] | sources: [src-portopt-pm-interview] | tags: [tracking-error, information-ratio, benchmark, mandate] -->

A benchmark-relative mandate optimises **active** weights $w-b$ against an ex-ante tracking-error budget. Expected active return is the information ratio times the tracking error taken.

### Formula
$$TE=\sqrt{(w-b)^\top\Sigma\,(w-b)},\qquad IR=\frac{E[r_p-r_b]}{TE},\qquad E[r_p-r_b]=IR\times TE$$

**Variables:**

- $w$ portfolio weights; $b$ benchmark weights; $w-b$ active weights
- $\Sigma$ covariance matrix
- $TE$ ex-ante annualised tracking error (% per year)
- $r_p,r_b$ portfolio and benchmark returns (per year)
- $IR$ information ratio (per year)

### Worked example
TE budget 4%, IR = 0.5 → expected active return $0.5\times4\%=$ **2% per year**.

### Key points
- The fundamental law links IR to signal skill and breadth: $IR\approx IC\sqrt{BR}$ ([[information-coefficient]]).
- The TE constraint's shadow price is the optimal IR: one more percent of TE budget buys about $IR^*\times1\%$ of alpha ([[constraints-shadow-prices]]).
- Realised TE and IR (measured after the fact from returns) are in [[risk-measures]]; this section is the ex-ante, model-based version.

### Connections
- **Builds on:** [[portfolio-construction-pipeline]] (stage 1), [[information-coefficient]].
- **Related:** [[risk-measures]], [[constraints-shadow-prices]].

<a id="covariance-estimation"></a>

## The Risk Model: Sample Covariance, Shrinkage & Factor Models
<!-- section: covariance-estimation | prerequisites: [eigen-svd-psd, variance-covariance-correlation, mean-variance-optimization] | related: [pca, ridge-regression, constraints-shadow-prices, optimiser-infeasibility, black-litterman] | sources: [src-portopt-pm-interview] | tags: [covariance, risk-model, ledoit-wolf, marchenko-pastur, factor-model, shrinkage] -->

The optimiser needs $\Sigma^{-1}$, but only an estimate of $\Sigma$ is available. With fewer observations than assets the sample covariance is singular: some portfolios had exactly zero variance in-sample, and the optimiser treats them as arbitrage. Even with more data than assets, the smallest eigenvalues are biased down. Shrinkage and factor models fix both problems.

### Definition: the sample covariance matrix
$$S=\frac{1}{T-1}\sum_{t=1}^{T}(r_t-\bar r)(r_t-\bar r)^\top,\qquad \mathrm{rank}(S)\le T-1$$

**Variables:**

- $S$ $N\times N$ sample covariance matrix (the estimate of the true $\Sigma$)
- $r_t$ $N\times1$ return vector in period $t$, $t=1,\dots,T$
- $\bar r=\frac1T\sum_tr_t$ sample mean vector
- $T$ number of observations (e.g. 250 trading days); $N$ number of assets (e.g. 500)

**Why the rank bound:** each $(r_t-\bar r)(r_t-\bar r)^\top$ is an outer product of rank 1; $T$ of them have rank at most $T$; the deviations sum to zero, so they are linearly dependent and the rank is at most $T-1$. $T$ days give only $T-1$ independent "snapshots" of how the assets move together. With $N=500$, $T=250$: rank ≤ 249, leaving at least $500-249=251$ independent portfolios that look riskless in-sample. Same idea as a regression with more parameters than data points: two points always lie on a line.

### Worked example: a "riskless" portfolio (3 stocks, 3 days; numbers illustrative, computed)

| Day | A | B | C |
|---|---|---|---|
| 1 | +1 | +2 | 0 |
| 2 | −1 | 0 | +2 |
| 3 | 0 | −2 | −2 |
| Mean | 0 | 0 | 0 |

Returns in %. Dividing by $T-1=2$:

$$S=\begin{pmatrix}1&1&-1\\1&4&2\\-1&2&4\end{pmatrix},\qquad w=(2,-1,1):\ \ Sw=0,\ \ w^\top Sw=0$$

**Variables:**

- $S$ sample covariance of A, B, C (e.g. $S_{AA}=(1+1+0)/2=1$, $S_{AB}=(2+0+0)/2=1$)
- $w$ portfolio: long 2 A, short 1 B, long 1 C

The portfolio's return $2r_A-r_B+r_C$ is $0$ on every day, so its sample variance is 0 and $S$ is **singular** (rank 2) — no inverse. In reality the combination is not riskless; it happened to cancel on these 3 days.

**What the optimiser does:** a zero-risk portfolio with any positive expected return looks like infinite Sharpe, so MVO puts unlimited leverage on it — or the solver fails because $S^{-1}$ doesn't exist ([[optimiser-infeasibility]], "dual infeasible").

### Even with $T>N$: eigenvalue bias (Marchenko–Pastur)
If the true correlation matrix is the identity (every eigenvalue 1), the eigenvalues of the pure-noise sample correlation matrix spread over

$$\big[(1-\sqrt q)^2,\ (1+\sqrt q)^2\big],\qquad q=\frac NT$$

**Variables:**

- $q$ ratio of assets to observations

**Example (computed):** $N=500$, $T=1000$, $q=0.5$ → roughly $[0.086,\ 2.91]$ although every true eigenvalue is 1. The optimiser hunts for exactly the lucky low-variance directions (selection bias): it believes that portfolio's vol is $\sqrt{0.086}\approx0.29$ of the truth, so realised risk comes in about **3.4× higher** than predicted. $\Sigma^{-1}$ amplifies these directions — the "error maximiser" of [[mean-variance-optimization]].

**Notes:**

- Real stock data has true structure (a strong market factor), so the exact numbers differ; the direction of the bias is the same.

### Fix 1: Ledoit–Wolf shrinkage
$$\hat\Sigma=\delta F+(1-\delta)S$$

**Variables:**

- $\hat\Sigma$ shrunk estimate
- $S$ sample covariance (unbiased, noisy)
- $F$ structured target (biased, stable): e.g. constant correlation, single-factor model, or the diagonal of variances
- $\delta\in[0,1]$ shrinkage intensity; Ledoit–Wolf give an analytical formula minimising expected (Frobenius) estimation error

**Example (computed):** in the 3-stock case with $F=\mathrm{diag}(1,4,4)$ and $\delta=0.5$, the magic portfolio's variance becomes $0.5\times0+0.5\times(2^2\cdot1+1^2\cdot4+1^2\cdot4)=6$: no longer riskless, and $\hat\Sigma$ is invertible. In correlation terms: a sample correlation of 0.9 against an average of 0.3, shrunk with $\delta=0.5$, becomes 0.6. A bias–variance trade-off, the same idea as [[ridge-regression]].

### Fix 2: factor model
The factor model $\Sigma=BFB^\top+D$ is defined in [[eigen-svd-psd]] ($B$ exposures, $F$ factor covariance, $D$ diagonal specific variances, $K$ factors).

| Method | Parameters to estimate | $N=500$, $K=10$ |
|---|---|---|
| Sample covariance | $N(N+1)/2$ | 125,250 |
| Factor model | $K(K+1)/2+NK+N$ | 55 + 5,000 + 500 = 5,555 |

**Why it fixes both problems:**

1. Far fewer numbers to estimate, so less noise.
2. No portfolio can look riskless: every stock carries specific risk $D_i>0$, so any non-zero $w$ has variance at least $\sum_iw_i^2D_i>0$.

### Alpha–risk misalignment (Lee & Stefek 2008)
**Symptom:** the optimiser keeps building a big position in an odd combination of stocks that looks low-risk.

**Cause:** part of the alpha lies outside the span of the risk model's factors. The optimiser prices that part only by the small specific variance $D$, treats it as nearly risk-free and levers it up. The other usual cause is an underestimated small eigenvalue.

**Fixes:**

- Add an "alpha factor" to the risk model, or penalise the component of $\alpha$ the factors don't span.
- Constrain exposure along the misaligned direction.
- Inspect the eigen-portfolios behind the position ([[pca]]).

(Reference cited from memory — verify.)

### Interview answer
*"No. With 250 observations the sample covariance has rank at most 249, so for 500 stocks it is singular: hundreds of long-short portfolios had exactly zero variance in-sample and the optimiser would treat them as arbitrage. Even with more data than assets, the smallest eigenvalues are biased down and the optimiser loads onto exactly those directions, so realised risk comes in well above predicted. I'd use a factor risk model, or Ledoit–Wolf shrinkage toward a structured target."*

### Connections
- **Builds on:** [[eigen-svd-psd]] (rank, PSD, factor model), [[variance-covariance-correlation]].
- **Used by:** [[mean-variance-optimization]], [[black-litterman]] ($\Sigma$ input), [[portfolio-construction-pipeline]] (stage 4).
- **Related:** [[ridge-regression]] (shrinkage), [[constraints-shadow-prices]] (constraints as implicit shrinkage), [[optimiser-infeasibility]] (unbounded problems).

<a id="transaction-costs-no-trade"></a>

## Transaction Costs, No-Trade Bands & Rebalancing
<!-- section: transaction-costs-no-trade | prerequisites: [mean-variance-optimization, lagrange-kkt-duality, exposure-neutrality] | related: [matlab-custom-portfolio-optimization, lasso-elastic-net, portfolio-construction-pipeline, optimiser-infeasibility] | sources: [src-portopt-pm-interview] | tags: [transaction-costs, market-impact, square-root-law, no-trade-region, rebalancing, garleanu-pedersen] -->

Linear costs (spread, commission) create a no-trade band: trade only when the marginal alpha beats the marginal cost, and then only to the edge of the band. Market impact grows faster than linearly in trade size, so the optimiser spreads trades out. Across periods, trade partially toward an aim portfolio.

### Formula: linear costs, one asset
$$\max_w\ \alpha w-\frac{\gamma}{2}\sigma^2w^2-\kappa\,|w-w_0|\ \Rightarrow\ w^{\text{new}}=\begin{cases}\bar w-\dfrac{\kappa}{\gamma\sigma^2}, & w_0<\bar w-\dfrac{\kappa}{\gamma\sigma^2}\ \text{(buy to the lower edge)}\\[2mm] w_0, & w_0\ \text{inside the band (no trade)}\\[2mm] \bar w+\dfrac{\kappa}{\gamma\sigma^2}, & w_0>\bar w+\dfrac{\kappa}{\gamma\sigma^2}\ \text{(sell to the upper edge)}\end{cases}$$

**Variables:**

- $w$ target position (weight); $w_0$ current position
- $\alpha$ expected return over the same horizon as $\kappa$
- $\sigma$ volatility; $\gamma$ risk aversion
- $\kappa$ linear cost per unit of weight traded (half-spread + commission, [[exposure-neutrality]])
- $\bar w=\alpha/(\gamma\sigma^2)$ the cost-free optimum

**Derivation:** $|w-w_0|$ has a kink at $w_0$, so use the subgradient. A trade is worth it only if the marginal gain $|\alpha-\gamma\sigma^2w_0|$ exceeds $\kappa$; when buying, the last unit's marginal gain equals $\kappa$: $\alpha-\gamma\sigma^2w=\kappa\Rightarrow w=\bar w-\kappa/(\gamma\sigma^2)$. The same KKT logic as [[lagrange-kkt-duality]], at a kink.

### Worked example (自己推理; numbers illustrative, computed)
$\alpha=4\%$, $\sigma=20\%$, $\gamma=5$ → $\gamma\sigma^2=0.2$, $\bar w=20\%$. With $\kappa=0.4\%$ the band half-width is $0.004/0.2=2\%$: no-trade region $[18\%,22\%]$.

- Current position 10% → buy only up to **18%**, not 20%.
- Current position 19% → **don't trade**.

### Reading it
- Linear costs make you trade **to the edge of the band**, never to the ideal point.
- Band width ∝ $\kappa/(\gamma\sigma^2)$: higher cost or lower risk → wider band.
- It is an L1 penalty — the same mechanism that makes lasso sparse ([[lasso-elastic-net]]): for many assets the optimal trade is exactly 0. In a QP, split $|w-w_0|$ into buys and sells ([[matlab-custom-portfolio-optimization]]).

### Market impact: the square-root law
$$\text{impact per share}\approx Y\,\sigma_d\sqrt{\frac{Q}{V}},\qquad \text{total cost}\propto Q\cdot\sqrt Q=Q^{3/2}$$

**Variables:**

- $Y$ constant, empirically of order 1 (calibrate on your own fills; cited from memory — verify)
- $\sigma_d$ daily volatility
- $Q$ shares traded; $V$ average daily volume (ADV)

**Example (computed):** $\sigma_d=2\%$: trading 1% of ADV costs about $2\%\times\sqrt{0.01}=20$ bp; 10% of ADV about $2\%\times\sqrt{0.1}\approx63$ bp. A 10× larger trade costs about 3.2× more per share.

**Notes:**

- $|\Delta w_i|^{3/2}$ is **convex**, so the problem stays efficiently solvable (power cone / SOCP).
- Unlike linear costs it penalises **large** trades: the optimiser moves part of the way each period.
- The cost term is often multiplied by a cost aversion $\lambda>1$ tuned in backtests — the cost model has errors too, so overestimating is safer.

### Multi-period: Gârleanu & Pedersen (2013)
*Dynamic Trading with Predictable Returns and Transaction Costs* (qualitative form; check the paper for exact coefficients):

$$x_t=x_{t-1}+\tau\,(\text{aim}_t-x_{t-1}),\qquad 0<\tau<1$$

**Variables:**

- $x_t$ holdings in period $t$
- $\text{aim}_t$ aim portfolio: a weighted average of the **current and expected future** Markowitz portfolios
- $\tau$ trading speed: smaller with higher costs, larger with higher risk aversion

**Notes:**

- **Trade partially toward the aim**, not all the way at once.
- **Aim in front of the target:** slow-decaying signals (value) get more weight in the aim than fast ones (short-term reversal), which fade before the position is built.
- A single-period optimiser re-solved daily is dragged around by fast signals and generates wasted turnover.

### Connections
- **Builds on:** [[mean-variance-optimization]], [[lagrange-kkt-duality]] (subgradient / KKT at a kink), [[exposure-neutrality]] (bid–ask cost).
- **Related:** [[lasso-elastic-net]] (L1 sparsity), [[matlab-custom-portfolio-optimization]] (implementation), [[optimiser-infeasibility]] (turnover caps vs drift).

<a id="portfolio-validation-attribution"></a>

## Does the Optimiser Add Value? Validation & Attribution
<!-- section: portfolio-validation-attribution | prerequisites: [backtest-pitfalls, sharpe-ratio, portfolio-construction-pipeline] | related: [covariance-estimation, transaction-costs-no-trade, risk-contribution, minimum-variance-portfolio, risk-budgeting] | sources: [src-portopt-pm-interview] | tags: [validation, 1-over-n, bias-statistic, attribution, out-of-sample] -->

An optimiser earns its place only if it beats simple baselines out-of-sample, net of costs. Estimation error often eats the theoretical gain: sample-based mean–variance frequently fails to beat 1/N.

### Benchmarks to beat

| Baseline | Needs | Section |
|---|---|---|
| 1/N (equal weight) | nothing | — |
| Signal-proportional weights | signal only | [[signal-to-weight]] |
| Inverse-vol / risk parity | vols (and correlations) | [[risk-budgeting]] |
| Global minimum variance | $\Sigma$ only | [[minimum-variance-portfolio]] |

**DeMiguel, Garlappi & Uppal (2009),** *Optimal Versus Naive Diversification*, Review of Financial Studies: 14 optimisation models generally failed to beat 1/N out-of-sample; for 25 assets, sample-based MVO would need about 3,000 months of data to beat it (cited from memory — verify the figures before quoting).

### Formula: risk-model bias statistic
$$b=\mathrm{std}_t\!\left(\frac{r_t}{\hat\sigma_{t-1}}\right)\approx1$$

**Variables:**

- $r_t$ realised portfolio return in period $t$
- $\hat\sigma_{t-1}$ risk model's ex-ante volatility forecast made at $t-1$ for period $t$
- $b$ bias statistic: ≈ 1 if forecasts are right; $b>1$ means risk is under-forecast (e.g. realised vol 30% above predicted in a de-grossing gives $b\approx1.3$)

### Key points
- Compare **net of costs**, walk-forward, never in-sample ([[backtest-pitfalls]]).
- Report turnover, realised vs ex-ante risk (the bias statistic), and attribution split into **alpha / factors / costs** — otherwise you never learn which pipeline stage failed.
- Post-optimisation checks before trading: risk decomposition ([[risk-contribution]]), factor exposures, concentration, liquidity (days to trade out).

### Connections
- **Builds on:** [[backtest-pitfalls]], [[sharpe-ratio]], [[portfolio-construction-pipeline]] (stages 7 and 9).
- **Related:** [[covariance-estimation]] (why realised risk exceeds predicted), [[transaction-costs-no-trade]], [[minimum-variance-portfolio]], [[risk-budgeting]].
