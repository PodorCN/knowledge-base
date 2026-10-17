---
id: portfolio-construction-process
title: "The Portfolio Construction Process"
type: topic
domain: portfolio-construction
sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework]
---
# The Portfolio Construction Process

Building a diversified multi-asset portfolio starts with the investor's objectives and ends with an implemented, monitored allocation. This chapter develops five steps: define objectives and constraints, form capital market assumptions, set a strategic allocation, refine it with robust optimisation or risk budgeting, and implement and monitor it. The nine-stage production pipeline below gives the operational detail behind that framework; the underlying optimisation and risk-contribution formulas live in their own linked sections.

**Prerequisites:** [[mean-variance-optimization]], [[lagrange-kkt-duality]], [[eigen-svd-psd]], [[grinold-alpha]], [[backtest-pitfalls]].

**Leads to:** [[risk-measures]] (realised tracking error and IR), [[hedging]].

**Sections:** [[portfolio-construction-pipeline]] · [[mandate-tracking-error]] · [[capital-market-assumptions]] · [[covariance-estimation]] · [[strategic-multi-asset-allocation]] · [[robust-allocation-refinement]] · [[transaction-costs-no-trade]] · [[portfolio-validation-attribution]]

Notation for this chapter: $w$ target weights, $w_0$ current weights, $b$ benchmark weights, $\alpha$ expected (excess or residual) returns, $\Sigma$ covariance matrix, $\gamma$ risk aversion, $N$ number of assets, $T$ number of observations.

<a id="portfolio-construction-pipeline"></a>

## The Pipeline: Nine Stages from Mandate to Attribution
<!-- section: portfolio-construction-pipeline | prerequisites: [mean-variance-optimization] | related: [mandate-tracking-error, covariance-estimation, transaction-costs-no-trade, portfolio-validation-attribution, grinold-alpha, constraints-shadow-prices] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [process, portfolio-construction, interview] -->

Portfolio optimisation in production is a pipeline, not a formula. Each stage feeds the next, and skipping one produces a characteristic failure.

### Key points: the five-step multi-asset framework

| Step | Main decision | Concrete output | Detail |
|---|---|---|---|
| 1. Objectives and constraints | What must the portfolio achieve, and what can the investor withstand? | An investment policy statement with return, risk, horizon, liquidity and liability requirements | [[mandate-tracking-error]] |
| 2. Capital market assumptions | What can each investable asset class plausibly deliver? | Forward-looking return, volatility and correlation estimates, with uncertainty and economic scenarios | [[capital-market-assumptions]], [[covariance-estimation]] |
| 3. Strategic allocation | Which combination of assets and economic exposures serves the mandate? | Long-run target weights, allocation ranges and risk budgets | [[strategic-multi-asset-allocation]] |
| 4. Robust refinement | How should the allocation change after allowing for estimation error and implementation frictions? | Feasible, stable weights tested against simple alternatives | [[robust-allocation-refinement]] |
| 5. Implementation and monitoring | How will the portfolio be traded, maintained and reviewed? | Instrument selection, execution and rebalancing rules, risk reporting and escalation responsibilities | [[transaction-costs-no-trade]], [[portfolio-validation-attribution]] |

The objective is a robust portfolio that meets the investor's needs across plausible market environments. Maximising a historical backtested return is not a substitute for specifying those needs. The strategic allocation is the long-run anchor; shorter-term tactical views must fit within its delegated limits.

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

## Step 1: Investment Objectives, Constraints & the Mandate
<!-- section: mandate-tracking-error | prerequisites: [portfolio-construction-pipeline, information-coefficient] | related: [risk-measures, constraints-shadow-prices, grinold-alpha] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [tracking-error, information-ratio, benchmark, mandate] -->

The mandate defines success before any asset weights are chosen. A benchmark-relative mandate optimises **active** weights $w-b$ against an ex-ante tracking-error budget, while an absolute-return or liability-aware investor also needs explicit limits on total risk and cash-flow shortfalls.

### Definition: the investment policy statement

An **investment policy statement (IPS)** records the investor's objectives, investable universe, binding constraints and decision responsibilities. A return aspiration becomes actionable only when its horizon, currency, fee basis and acceptable risks are stated.

### Key points

| Item | What to establish | Why it changes the portfolio |
|---|---|---|
| Return objective | Nominal or real; total or excess return; gross or net of fees and taxes; long-run compound growth or one-period expectation | A historical arithmetic mean cannot directly establish an achievable compound spending target |
| Risk tolerance and capacity | Willingness to accept losses versus financial ability to absorb them; volatility, drawdown and shortfall tolerances | A willing investor may still lack the capacity to take risk when near-term withdrawals are large |
| Horizon | Both the long-run investment horizon and the dates of intermediate obligations | A ten-year horizon does not make money needed next quarter available for illiquid investments |
| Liquidity | Withdrawals, benefit payments, capital calls, collateral and a stress buffer | Forced sales and margin calls can make an otherwise sensible allocation fail |
| Liabilities | Timing, currency, inflation linkage and interest-rate sensitivity | Pension or insurance assets should be judged partly against the obligations they must fund |
| Benchmark | Policy benchmark, absolute objective or liability-relative measure; permitted tracking error | Low tracking error can coexist with a large absolute loss when the benchmark falls |
| Other constraints | Position and asset-class limits, leverage, derivatives, tax, legal restrictions and any stated investment exclusions | These determine which candidate portfolios are actually feasible |

For liabilities, distinguish **hedging assets**, chosen to match obligation cash flows or sensitivities, from **return-seeking assets**, chosen to improve long-run funding. Duration matching reduces local rate sensitivity; it does not eliminate inflation, credit, curve-shape or cash-flow mismatch risk (see [[bond-duration]]).

If the return needed to fund the objectives is inconsistent with the risk and liquidity limits, report the conflict. Revise the spending plan, funding, horizon or agreed risk capacity before choosing weights; the optimiser cannot make an infeasible mandate achievable.

### Formula
$$TE=\sqrt{(w-b)^\top\Sigma\,(w-b)},\qquad IR=\frac{E[r_p-r_b]}{TE},\qquad E[r_p-r_b]=IR\times TE$$

**Variables:**

- $w$ portfolio weights; $b$ benchmark weights; $w-b$ active weights
- $\Sigma$ covariance matrix
- $TE$ ex-ante annualised tracking error (% per year)
- $r_p,r_b$ portfolio and benchmark returns (per year)
- $IR$ information ratio (per year)

**Notes:**

- The fundamental law links IR to signal skill and breadth: $IR\approx IC\sqrt{BR}$ ([[information-coefficient]]).
- The TE constraint's shadow price is the optimal IR: one more percent of TE budget buys about $IR^*\times1\%$ of alpha ([[constraints-shadow-prices]]).
- Realised IR (measured after the fact from returns), its residual version and IR vs Sharpe are in [[information-ratio]]; realised TE is in [[risk-measures]]. This section is the ex-ante, model-based version.

### Worked example

An institutional endowment has USD 10 million, a 10-year horizon, USD 400,000 of scheduled distributions over the next year (4% of starting assets), and a 3% annual real return target net of fees. At 2% expected inflation, the required nominal net compound return is $1.03 \times 1.02 - 1 = \mathbf{5.06\%/\text{yr}}$.
- **Liquidity carving:** Carve out the 4% near-term distribution plus a stress cash buffer in short-duration bills first; only the remaining capital can bear illiquidity or equity drawdown risk.
- **Benchmark-relative translation:** For an active mandate with tracking-error budget $TE = 4\%$ and target $IR = 0.50$, expected active return is $E[r_p - r_b] = 0.50 \times 4\% = \mathbf{2.0\%/\text{yr}}$.

### Connections
- **Builds on:** [[portfolio-construction-pipeline]] (stage 1), [[information-coefficient]].
- **Related:** [[risk-measures]], [[constraints-shadow-prices]].
- **Used by:** [[capital-market-assumptions]], [[strategic-multi-asset-allocation]], [[robust-allocation-refinement]].

<a id="capital-market-assumptions"></a>

## Step 2: Forward-Looking Capital Market Assumptions
<!-- section: capital-market-assumptions | prerequisites: [mandate-tracking-error, portfolio-variance-diversification, structural-risk-premia] | related: [covariance-estimation, black-litterman, carry-across-assets, strategic-multi-asset-allocation] | sources: [src-multi-asset-portfolio-framework] | tags: [capital-market-assumptions, expected-returns, multi-asset, scenarios] -->

Capital market assumptions (CMAs) specify forward-looking expected returns, volatilities, correlations, and scenario payoffs for each investable asset class over the mandate horizon, anchored by current yields and structural building blocks rather than trailing sample means.

### Definition

A consistent CMA set fixes the estimation date, horizon, base currency, FX-hedging policy, excess-vs-total return convention, and fee basis across all asset classes.

### Key points

| Asset class | Forward-looking building blocks | Key adjustments & pitfalls |
|---|---|---|
| **Equities** | Cash payout yield (dividends + net buybacks) + real earnings growth + inflation + valuation multiple reversion | Do not extrapolate recent P/E expansion; adjust payout yield for net share issuance/buybacks ([[carry-across-assets]]). |
| **Government bonds** | Starting yield-to-maturity + roll-down + expected yield-curve shift reinvestment | Starting yield anchors 7–10yr nominal returns, but duration creates mark-to-market loss when rates rise ([[bond-duration]]). |
| **Credit (IG / HY)** | Government bond return + credit spread − $\text{PD}\times\text{LGD}$ (expected default + downgrade migration loss) − illiquidity cost | Quoted spread is an upper bound, not expected excess return; HY spread widens sharply during equity selloffs. |
| **Real assets** | Net operating income yield + inflation pass-through − cap-rate expansion and leverage financing cost | Levered real estate and infrastructure carry heavy real-rate duration exposure in rising-rate regimes. |
| **Alternatives** | Underlying factor risk premia + idiosyncratic manager alpha − management/performance fees and financing spread | Decompose private equity/credit into levered public beta + illiquidity premium; unsmooth appraisal returns before estimating $\Sigma$. |
| **Cash** | Expected path of central-bank policy rate in the liability currency | Zero mark-to-market volatility, but high reinvestment and inflation erosion risk over long horizons. |

### Worked example

Suppose forward excess-return CMAs are $\mu_E = 5.0\%$ ($\sigma_E = 16\%$) for equities and $\mu_B = 1.0\%$ ($\sigma_B = 6\%$) for government bonds:
- Under baseline correlation $\rho_{EB} = 0.0$, a 60/40 portfolio has expected excess return $0.6(5\%) + 0.4(1\%) = \mathbf{3.40\%}$ and volatility $\sqrt{(0.6\times 16\%)^2 + (0.4\times 6\%)^2} = \sqrt{92.16 + 5.76}\% = \mathbf{9.90\%}$ ([[portfolio-variance-diversification]]).
- Under an inflation-shock regime where stock–bond correlation flips to $\rho_{EB} = +0.50$, portfolio volatility jumps to $\sqrt{97.92 + 2(0.5)(9.6)(2.4)}\% = \mathbf{11.00\%}$ even before accounting for higher standalone volatilities.

### Connections

- **Builds on:** [[mandate-tracking-error]], [[portfolio-variance-diversification]], [[structural-risk-premia]].
- **Used by:** [[strategic-multi-asset-allocation]], [[robust-allocation-refinement]].
- **Related:** [[covariance-estimation]], [[black-litterman]], [[carry-across-assets]].

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
- $N$ number of assets; $T$ number of observations

**Example (computed):** $N=500$, $T=1000$, $q=0.5$ → roughly $[0.086,\ 2.91]$ although every true eigenvalue is 1. The optimiser hunts for exactly the lucky low-variance directions (selection bias): it believes that portfolio's vol is $\sqrt{0.086}\approx0.29$ of the truth, so realised risk comes in about **3.4× higher** than predicted. $\Sigma^{-1}$ amplifies these directions — the "error maximiser" of [[mean-variance-optimization]].

**Notes:**

- Real stock data has true structure (a strong market factor), so the exact numbers differ; the direction of the bias is the same.

### Fix 1: Ledoit–Wolf shrinkage
$$\hat\Sigma=\delta F+(1-\delta)S$$

**Variables:**

- $\hat\Sigma$ shrunk estimate
- $S$ sample covariance (unbiased, noisy)
- $F$ structured target (biased, stable): e.g. constant correlation, single-factor model, or the diagonal of variances
- $\delta\in[0,1]$ shrinkage intensity; Ledoit & Wolf (2004, *Journal of Multivariate Analysis*) give an analytical formula minimising expected Frobenius estimation error

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

**Cause:** part of the alpha lies outside the span of the risk model's factors ($\alpha = B\alpha_F + \alpha_\perp$). The optimiser prices the orthogonal component $\alpha_\perp$ only by the small specific variance $D$, treats an unmodelled common factor as diversifiable idiosyncratic noise, and levers it up (Lee & Stefek 2008, *"Do Risk Factors Eat Alpha?"*, *Journal of Portfolio Management*, 34(4), 12–24).

**Fixes:**

- Add the missing systematic driver (or an explicit "alpha factor") to the risk model, or penalise the residual component $\alpha_\perp$ not spanned by $B$.
- Constrain exposure along the misaligned direction.
- Inspect the eigen-portfolios behind the position ([[pca]]).

### Interview answer
*"No. With 250 observations the sample covariance has rank at most 249, so for 500 stocks it is singular: hundreds of long-short portfolios had exactly zero variance in-sample and the optimiser would treat them as arbitrage. Even with more data than assets, the smallest eigenvalues are biased down and the optimiser loads onto exactly those directions, so realised risk comes in well above predicted. I'd use a factor risk model, or Ledoit–Wolf shrinkage toward a structured target."*

### Connections
- **Builds on:** [[eigen-svd-psd]] (rank, PSD, factor model), [[variance-covariance-correlation]].
- **Used by:** [[mean-variance-optimization]], [[black-litterman]] ($\Sigma$ input), [[portfolio-construction-pipeline]] (stage 4).
- **Related:** [[ridge-regression]] (shrinkage), [[constraints-shadow-prices]] (constraints as implicit shrinkage), [[optimiser-infeasibility]] (unbounded problems).

<a id="strategic-multi-asset-allocation"></a>

## Step 3: Strategic Asset Allocation & Risk-Factor Diversification
<!-- section: strategic-multi-asset-allocation | prerequisites: [capital-market-assumptions, covariance-estimation, risk-contribution, risk-budgeting] | related: [risk-on-risk-off, portfolio-variance-diversification, robust-allocation-refinement, bond-duration] | sources: [src-multi-asset-portfolio-framework] | tags: [strategic-allocation, multi-asset, diversification, factors] -->

Strategic asset allocation (SAA) establishes long-run policy weights and risk budgets across asset classes, while tactical asset allocation (TAA) takes bounded deviations within delegated tracking-error limits. True diversification requires looking through asset-class labels to underlying **macroeconomic risk factors**.

### Asset sleeves vs underlying factor exposures

| Sleeve | Primary Portfolio Role | Underlying Factor Exposures to Audit |
|---|---|---|
| **Global equities** | Long-run real growth & corporate profit participation | Growth beta, equity vol, valuation duration, FX |
| **Nominal government bonds** | Deflation/recession hedge & liability duration matching | Real rates, breakeven inflation (loses alongside equities in supply/inflation shocks, [[risk-on-risk-off]]) |
| **IG & HY credit** | Carry & credit risk premium | Corporate default/spread beta ($\sim 0.5\text{–}0.7$ correlated with equity drawdown + illiquidity) |
| **TIPS & real assets** | Inflation protection & real cash-flow matching | Real-rate duration (TIPS), cap-rate/financing sensitivity (REITs/infrastructure), spot supply shocks (commodities) |
| **Liquid alternatives / Trend** | Uncorrelated alpha & convex crisis diversification | Hidden equity/credit beta, short-volatility tail skew, leverage financing risk |
| **Cash & T-bills** | Liquidity reserve, margin collateral & dry powder | Reinvestment risk, negative real carry under high inflation |

### Capital weights vs risk contributions (60/40 vs Risk Parity)
Using the 2-asset CMAs from [[capital-market-assumptions]] ($\sigma_E = 16\%, \sigma_B = 6\%, \rho_{EB} = 0$) and the Euler decomposition in [[risk-contribution]] ($\%RC_i = w_i^2 \sigma_i^2 / \sigma_p^2$ when $\rho=0$):
- **Traditional 60/40 capital allocation:** $w_E \sigma_E = 9.6\%$, $w_B \sigma_B = 2.4\%$, $\sigma_p = 9.90\%$. Equities account for $9.6^2 / (9.6^2 + 2.4^2) = \mathbf{94.12\%}$ of portfolio variance (and volatility risk contribution), while bonds contribute only **5.88%**.
- **Unlevered 2-asset Risk Parity ([[risk-budgeting]]):** Equalising risk contributions ($w_E \sigma_E = w_B \sigma_B$) sets $w_E = \frac{6}{16+6} = \mathbf{27.27\%}$ and $w_B = \mathbf{72.73\%}$. To restore equity-like expected returns without equity concentration, institutional risk-parity books apply portfolio-level leverage (via futures/repos) to the 27/73 mix—which introduces **funding liquidity risk** and **positive stock–bond correlation risk** (as in 2022 when both legs fell simultaneously).

### Connections

- **Builds on:** [[capital-market-assumptions]], [[covariance-estimation]], [[risk-contribution]], [[risk-budgeting]].
- **Used by:** [[robust-allocation-refinement]], [[transaction-costs-no-trade]], [[portfolio-validation-attribution]].
- **Related:** [[risk-on-risk-off]], [[bond-duration]], [[structural-risk-premia]].

<a id="robust-allocation-refinement"></a>

## Step 4: Robust Optimisation & Allocation Refinement
<!-- section: robust-allocation-refinement | prerequisites: [strategic-multi-asset-allocation, mean-variance-optimization, constraints-shadow-prices, risk-budgeting] | related: [black-litterman, covariance-estimation, transaction-costs-no-trade, portfolio-validation-attribution, optimiser-infeasibility] | sources: [src-multi-asset-portfolio-framework] | tags: [robustness, optimisation, uncertainty, risk-budgeting] -->

Choosing an allocation rule depends on which input you trust more: expected returns ($\mu$), the covariance matrix ($\Sigma$), or a market-equilibrium prior ($w_{\mathrm{eq}}$).

### Choosing the construction framework

| Framework | Required Inputs | When to Use | Primary Failure Mode & Safeguard |
|---|---|---|---|
| **Constrained MVO** ([[mean-variance-optimization]]) | $\alpha$ (or $\mu$), $\hat\Sigma$, linear/quadratic constraints | High-breadth cross-sectional signals or explicit active-risk mandates | Amplifies $\mu$ estimation error into corner weights; requires shrunk $\hat\Sigma$, Grinold scaling $\alpha = \sigma\cdot IC\cdot z$, and box/sector bounds ([[constraints-shadow-prices]]). |
| **Black–Litterman** ([[black-litterman]]) | Market-cap prior $\Pi = \gamma\Sigma w_{\mathrm{mkt}}$, views $P, Q$, uncertainty $\Omega$ | Multi-asset SAA/TAA with a few macro or relative views | Sensitive to $\tau$ and view confidence $\Omega$; audit implied posterior tilts against view conviction. |
| **Risk Budgeting / ERC** ([[risk-budgeting]]) | $\hat\Sigma$ and risk budgets $b_i$ (no $\mu$ required) | Strategic asset allocation when mean return forecasts have low power | Concentrates capital in low-vol duration assets; vulnerable to synchronous rate + equity selloffs. |
| **1/N or Policy Baseline** | Universe definition only | Benchmark baseline & sanity check | Ignores valuation and volatility shifts; any complex optimiser must beat $1/N$ net of costs out-of-sample. |

### Perturbation & sensitivity stress check
Before signing off on optimised weights $w^*$, perturb expected returns by $\pm 1\text{ SE}$ and correlations by $+0.20$:
- If a $+50\text{ bps}$ tweak to one regional equity forecast flips the allocation from $40\%$ to $80\%$, the solution is driven by near-collinear covariance directions rather than genuine alpha. Apply shrinkage ([[covariance-estimation]]), Bayesian prior pulling ([[black-litterman]]), or explicit concentration caps.

### Connections

- **Builds on:** [[strategic-multi-asset-allocation]], [[mean-variance-optimization]], [[constraints-shadow-prices]], [[risk-budgeting]].
- **Used by:** [[transaction-costs-no-trade]], [[portfolio-validation-attribution]].
- **Related:** [[black-litterman]], [[covariance-estimation]], [[optimiser-infeasibility]].

<a id="transaction-costs-no-trade"></a>

## Step 5: Implementation, Transaction Costs & Rebalancing
<!-- section: transaction-costs-no-trade | prerequisites: [mean-variance-optimization, lagrange-kkt-duality, exposure-neutrality] | related: [matlab-custom-portfolio-optimization, lasso-elastic-net, portfolio-construction-pipeline, optimiser-infeasibility] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [transaction-costs, market-impact, square-root-law, no-trade-region, rebalancing, garleanu-pedersen] -->

Linear costs (spread, commission) create a no-trade band: trade only when the marginal alpha beats the marginal cost, and then only to the edge of the band. Market impact grows faster than linearly in trade size, so the optimiser spreads trades out. Across periods, trade partially toward an aim portfolio.

### Rebalancing policy & drift triggers

| Rebalancing Rule | Mechanism | Trade-off |
|---|---|---|
| **Calendar schedule** | Review monthly/quarterly on a fixed clock | Predictable operations, but blind to intra-period crashes or unnecessary when drift is tiny. |
| **No-trade weight bands** | Trade only when $|w_i - w_i^*| > \Delta_i$ (and trade to the band edge, not the center) | Optimal under proportional transaction costs ($\Delta_i = \kappa_i / (\gamma\sigma_i^2)$). |
| **Risk / factor triggers** | Rebalance when active tracking error $TE$ or factor $\%RC$ breaches limit | Captures volatility spikes even when capital weights look unchanged. |
| **Cash-flow routing** | Direct inflows, dividends, and withdrawals toward underweight sleeves | Zero extra spread cost, though insufficient during large market dislocations. |

**Example (computed):** A 60/40 portfolio where equities rally $+20\%$ and bonds return $0\%$ drifts to equity weight $0.72 / 1.12 = \mathbf{64.29\%}$. Under a $\pm 5\%$ weight band ($[55\%, 65\%]$), no trade is triggered by capital weight alone, though if equity volatility simultaneously spiked from $16\%$ to $24\%$, a risk-contribution trigger would fire.

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

- $Y$ dimensionless impact constant of order unity ($Y \approx 0.5\text{–}1.0$, calibrated to execution fills; Almgren et al. 2005, *Risk*)
- $\sigma_d$ daily volatility
- $Q$ shares traded; $V$ average daily volume (ADV)

**Example (computed):** $\sigma_d=2\%$, $Y=1$: trading 1% of ADV costs about $2\%\times\sqrt{0.01}=20$ bp; 10% of ADV about $2\%\times\sqrt{0.1}\approx63$ bp. A 10× larger trade costs about 3.2× more per share.

**Notes:**

- $|\Delta w_i|^{3/2}$ is **convex**, so the problem stays efficiently solvable (power cone / SOCP).
- Unlike linear costs it penalises **large** trades: the optimiser moves part of the way each period.
- The cost term is often multiplied by a cost aversion $\lambda>1$ tuned in backtests — the cost model has errors too, so overestimating is safer.

### Multi-period: Gârleanu & Pedersen (2013)
*Dynamic Trading with Predictable Returns and Transaction Costs* (*Journal of Finance*, 68(6), 2309–2340):

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

## Step 5 Continued: Monitoring, Stress Tests & Attribution
<!-- section: portfolio-validation-attribution | prerequisites: [backtest-pitfalls, sharpe-ratio, portfolio-construction-pipeline] | related: [covariance-estimation, transaction-costs-no-trade, risk-contribution, minimum-variance-portfolio, risk-budgeting] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [validation, 1-over-n, bias-statistic, attribution, out-of-sample] -->

Post-trade monitoring reconciles ex-ante forecasts against realised risk, attributes active returns into factor vs idiosyncratic components, and tests whether complex optimisation beats simple heuristics net of costs out-of-sample.

### Ongoing monitoring & stress-testing matrix

| Regime / Diagnostic | Joint Shock / Metric | Portfolio Action & Governance |
|---|---|---|
| **Recession / Disinflation** | Equities $-20\%$, HY spreads $+300\text{ bps}$, nominal yields $-100\text{ bps}$ | Verify whether sovereign duration offsets growth and credit drawdowns without breaching liquidity reserves. |
| **Inflation / Rate Shock (2022-style)** | Nominal yields $+200\text{ bps}$, equities $-15\%$, $\rho_{EB} > +0.5$ | Standard 60/40 loses $0.6(-15\%) + 0.4(-10\%) = -13\%$ simultaneously; requires TIPS, commodities, or short-duration tilts. |
| **Liquidity & Collateral Stress** | Bid-ask spreads $3\times$, FX/futures variation margin calls, private capital calls | Run **reverse stress test**: find the smallest joint shock that exhausts unencumbered cash buffers. |
| **Performance Attribution** | Brinson allocation/selection (multi-asset) or factor + specific + cost decomposition (quant equity) | Separate whether P&L came from intended alpha, unhedged factor drift, or lower/higher execution slippage. |

### Benchmarks to beat

| Baseline | Needs | Section |
|---|---|---|
| 1/N (equal weight) | nothing | — |
| Signal-proportional weights | signal only | [[signal-to-weight]] |
| Inverse-vol / risk parity | vols (and correlations) | [[risk-budgeting]] |
| Global minimum variance | $\Sigma$ only | [[minimum-variance-portfolio]] |

**DeMiguel, Garlappi & Uppal (2009),** *"Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?"*, *Review of Financial Studies*, 22(5), 1915–1953: across 14 optimisation models and 7 empirical datasets, sample-based MVO generally failed to beat $1/N$ out-of-sample in Sharpe ratio or certainty-equivalent return; for $N = 25$ assets, sample MVO requires a critical estimation window of ~3,000 months (~250 years) to outperform $1/N$ (~6,000 months for $N = 50$).

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
