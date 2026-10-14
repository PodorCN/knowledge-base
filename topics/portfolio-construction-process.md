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
- Realised TE and IR (measured after the fact from returns) are in [[risk-measures]]; this section is the ex-ante, model-based version.

### Worked example

An illustrative investor has USD 10 million, a ten-year horizon, USD 400,000 of known payments over the next year and a 3% annual real return target net of fees. At assumed inflation of 2%, the corresponding nominal net target is **1.03 × 1.02 − 1 = 5.06%**. The known payments equal **4% of starting assets**, before adding any liquidity buffer. That 4% cash requirement is separate from the return target; it is not automatically an extra 4% return requirement.

Specify a liquid payment reserve and stress buffer first, then assess how much risk the remaining assets can bear. The long horizon alone does not justify putting the whole portfolio into private assets. Separately, for a benchmark-relative mandate, a TE budget of 4% and expected IR of 0.5 imply expected active return of **0.5 × 4% = 2% per year**; neither return is guaranteed.

### Connections
- **Builds on:** [[portfolio-construction-pipeline]] (stage 1), [[information-coefficient]].
- **Related:** [[risk-measures]], [[constraints-shadow-prices]].
- **Used by:** [[capital-market-assumptions]], [[strategic-multi-asset-allocation]], [[robust-allocation-refinement]].

<a id="capital-market-assumptions"></a>

## Step 2: Forward-Looking Capital Market Assumptions
<!-- section: capital-market-assumptions | prerequisites: [mandate-tracking-error, portfolio-variance-diversification, structural-risk-premia] | related: [covariance-estimation, black-litterman, carry-across-assets, strategic-multi-asset-allocation] | sources: [src-multi-asset-portfolio-framework] | tags: [capital-market-assumptions, expected-returns, multi-asset, scenarios] -->

Capital market assumptions (CMAs) describe expected returns, volatilities, correlations and scenario behaviour for each investable asset class. They are forward-looking estimates over a stated horizon, with uncertainty, rather than a ranking of recent winners.

### Definition

A usable CMA set specifies the estimation date, investment horizon, base currency, currency-hedging policy, total-versus-excess return convention and treatment of fees. Estimates must be internally consistent across assets and with the mandate.

### Key points

| Asset class | Starting point for expected return | Main qualifications |
|---|---|---|
| Equities | Income yield, sustainable earnings growth and an explicit valuation-change assumption | Avoid extrapolating recent multiple expansion; be consistent about inflation, buybacks and per-share growth |
| Government bonds | Starting yield, cash-flow reinvestment and the assumed path of the yield curve | Yield is an anchor, not a guaranteed holding-period return; duration creates mark-to-market risk ([[bond-duration]]) |
| Credit | Government bond return plus spread income, less expected defaults, recoveries, migration and costs | A high quoted spread is not all excess return; credit risk can overlap with equity risk |
| Real assets | Rental or operating income, growth, valuation changes and financing costs; for commodity futures, collateral return, spot changes and roll effects | Inflation sensitivity depends on the asset, financing and shock; property and infrastructure remain exposed to real rates |
| Alternatives | Identify the underlying strategy, economic risk premium and manager contribution, then subtract fees and financing | Private equity, private credit, market-neutral strategies and trend following are not one homogeneous exposure |
| Cash | Short-rate and reinvestment assumptions in the liability currency | Low price volatility does not remove inflation or long-run reinvestment risk |

Use long historical samples to understand behaviour, current yields and valuations to anchor starting conditions, and economic reasoning to judge what can persist. Do not use a short sample mean as a precise long-run forecast; [[mean-variance-optimization]] explains why mean estimates are especially noisy. [[black-litterman]] provides one way to combine a prior with views and confidence.

For the risk assumptions, align return frequency, calendars, currency treatment and horizons. Model the exposures the investor will actually hold: unhedged foreign bonds include FX risk, while a hedged estimate must reflect hedging costs. Appraisal-based private-asset returns can look artificially smooth; low reported volatility and correlation need not imply low economic risk. Detailed covariance estimation belongs in [[covariance-estimation]].

Evaluate at least a base case, stronger growth, recession/disinflation, an inflation shock and a liquidity shock. Specify joint changes in growth, inflation, rates, spreads and market liquidity; do not combine individually convenient assumptions that are economically inconsistent. Scenario results are conditional outcomes, not probabilities unless probabilities have been explicitly modelled.

### Worked example

Suppose illustrative annual **excess-return** assumptions are 5% for equities and 1% for government bonds, with annual volatilities of 16% and 6% and zero correlation. Using the formulas in [[portfolio-variance-diversification]], a 60/40 allocation has expected excess return **3.4%** and volatility **9.90%**. Compare an absolute nominal target with expected total return on a consistent basis, not directly with this excess return.

Keeping the volatilities and weights fixed but changing correlation to +0.5 raises modelled volatility to **11.00%**. This is a sensitivity check, not an estimate that correlation will become +0.5; a full stress test would also change volatilities, asset returns and liquidity together.

### Connections

- **Builds on:** [[mandate-tracking-error]], [[portfolio-variance-diversification]], [[structural-risk-premia]].
- **Used by:** [[strategic-multi-asset-allocation]], [[robust-allocation-refinement]].
- **Related:** [[covariance-estimation]], [[black-litterman]], [[carry-across-assets]] (carry is one return component, not the entire forecast).

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

<a id="strategic-multi-asset-allocation"></a>

## Step 3: Strategic Asset Allocation & Risk-Factor Diversification
<!-- section: strategic-multi-asset-allocation | prerequisites: [capital-market-assumptions, covariance-estimation, risk-contribution, risk-budgeting] | related: [risk-on-risk-off, portfolio-variance-diversification, robust-allocation-refinement, bond-duration] | sources: [src-multi-asset-portfolio-framework] | tags: [strategic-allocation, multi-asset, diversification, factors] -->

Strategic asset allocation (SAA) is the long-run combination of asset classes designed to meet the mandate. Diversification depends on the underlying economic exposures and their joint behaviour, as well as on the number of asset-class labels.

### Definition

The **strategic allocation** sets policy weights and permitted ranges. **Tactical asset allocation** takes shorter-term deviations based on views, within delegated risk limits. **Security or manager selection** chooses how each allocation is implemented. Keeping these decisions distinct makes their risks and results easier to attribute.

### Key points

| Sleeve | Intended portfolio role | Exposure to check |
|---|---|---|
| Global equities | Long-run growth and participation in corporate profits | Growth, equity beta, geography, sectors, valuation and FX |
| High-quality government bonds | Contractual income, liability matching and possible recession protection | Duration, real rates, inflation and sovereign quality; nominal bonds can lose during an inflation shock |
| Investment-grade and high-yield credit | Income and credit risk premium | Spread and default risk, duration and liquidity; high yield often shares growth exposure with equities |
| Inflation-linked bonds and real assets | Exposure suited to inflation-linked needs and selected real cash flows | Linker real-rate duration; property financing and valuations; commodity-specific supply and demand |
| Alternative strategies | Additional return sources or risk diversification where supported by evidence | Hidden equity or credit beta, leverage, short-volatility exposure, manager risk and redemption terms |
| Cash and short-term instruments | Payments, collateral and capacity to rebalance under stress | Currency matching, counterparty exposure and inflation erosion |

Start from the required roles: fund liabilities and liquidity, then allocate the risk-bearing capital among return sources. Assess global equity diversification by region, sector and style; assess bonds by duration, issuer quality and currency rather than treating every bond as defensive. A policy benchmark should represent this long-run allocation, not be chosen afterward to flatter realised results.

Look through fund labels to **risk factors**: equity/growth risk, nominal and real-rate duration, credit spreads, inflation, currency, liquidity and style premia such as value, momentum and carry ([[structural-risk-premia]]). A portfolio with public equities, private equity, high-yield bonds and private credit may still make one large bet on growth and easy financing. A market-neutral label likewise does not establish neutrality to all factors ([[exposure-neutrality]]).

Use asset and factor risk contributions to identify concentration ([[risk-contribution]]). Factor exposures show sensitivity to a driver; risk contributions additionally depend on driver volatility and covariance. Equal capital weights therefore do not imply equal risk, and asset-level risk parity does not automatically imply factor-level diversification.

Test the combination across regimes. Government duration can help in a recession with falling inflation, yet nominal bonds and equities can both fall when inflation pushes rates up. The risk-on/risk-off framework ([[risk-on-risk-off]]) is useful, but correlations and the identity of the defensive assets depend on the shock. No asset is a universal hedge.

### Worked example

With the illustrative 60/40 equity–government-bond allocation, volatilities of 16% and 6%, and zero correlation from [[capital-market-assumptions]], weighted volatilities are **9.6%** and **2.4%**. Applying [[risk-contribution]], equities contribute **94.12% of portfolio volatility risk** and bonds **5.88%**. The allocation is balanced by capital far more than by modelled risk.

Under the same two-asset assumptions, equal risk contributions would require equity weight **6 / (16 + 6) = 27.27%** and bond weight **72.73%**. This illustrates risk budgeting, not a recommended allocation: expected return, liability needs, duration concentration and financing constraints must still be checked. Adding an illiquid equity fund would not automatically solve the original growth-risk concentration.

### Connections

- **Builds on:** [[capital-market-assumptions]], [[covariance-estimation]], [[risk-contribution]], [[risk-budgeting]].
- **Used by:** [[robust-allocation-refinement]], [[transaction-costs-no-trade]], [[portfolio-validation-attribution]].
- **Related:** [[risk-on-risk-off]], [[bond-duration]], [[structural-risk-premia]].

<a id="robust-allocation-refinement"></a>

## Step 4: Robust Optimisation & Allocation Refinement
<!-- section: robust-allocation-refinement | prerequisites: [strategic-multi-asset-allocation, mean-variance-optimization, constraints-shadow-prices, risk-budgeting] | related: [black-litterman, covariance-estimation, transaction-costs-no-trade, portfolio-validation-attribution, optimiser-infeasibility] | sources: [src-multi-asset-portfolio-framework] | tags: [robustness, optimisation, uncertainty, risk-budgeting] -->

Optimisation refines a policy allocation into feasible weights, using an objective aligned with the mandate. The useful result is an allocation whose behaviour remains acceptable under uncertain inputs and realistic trading conditions, rather than a precise maximum built on fragile estimates.

### Definition

**Constrained mean–variance optimisation** trades expected return against risk within a feasible set ([[mean-variance-optimization]]). **Risk budgeting** instead sets desired risk contributions and solves for the weights ([[risk-budgeting]]). Both need a credible risk model; they express different starting objectives rather than interchangeable definitions of an optimal portfolio.

### Key points

| Approach | When it helps | Main limitation and safeguard |
|---|---|---|
| Constrained mean–variance | Credible return forecasts and a clear risk–return trade-off | Sensitive to means and covariance; shrink inputs and impose economically justified limits |
| Risk budgeting | The investor can state desired risk shares more confidently than expected returns | Avoids estimating means but still depends on covariance; can concentrate capital in low-volatility duration assets |
| Black–Litterman | A defensible prior plus explicit investment views | The prior, covariance and view confidence remain assumptions; inspect the resulting tilts ([[black-litterman]]) |
| Simple policy or equal-weight baseline | Transparent comparison requiring few estimated inputs | Ignores some economic differences; use it to establish whether added complexity earns its cost |

The operational objective in [[portfolio-construction-pipeline]] already includes return, risk and trading costs. For an absolute mandate use total portfolio risk; for a benchmark-relative mandate use active risk but retain any required total-risk controls. For a liability-aware mandate also test funding and cash-flow outcomes: an asset-only variance minimum may not minimise the investor's shortfall risk.

Translate the IPS into constraints: budget and allocation ranges, concentration, leverage, factor exposures, liquidity, turnover and permitted instruments. Separate binding legal or contractual limits from preferences. Soft penalties can express preferences, but should never silently relax a binding investment restriction. If constraints conflict, diagnose the conflict using [[optimiser-infeasibility]].

Address **estimation uncertainty** by shrinking covariance ([[covariance-estimation]]), using cautious return estimates or a prior, and solving under alternative assumptions. Constraints and turnover penalties can stabilise weights ([[constraints-shadow-prices]], [[transaction-costs-no-trade]]). Inspect how much the recommendation changes when expected returns, correlations, costs and starting weights are perturbed; a large weight change from a small forecast change needs an economic explanation.

Address **implementation uncertainty** by including spreads, impact, fees, taxes where applicable, financing and currency hedging on consistent horizons. A one-off trading cost must not be compared directly with an annual expected benefit without allowing for the intended holding period. Private assets also need commitment schedules, capital-call reserves, redemption restrictions and uncertain exit values; a daily turnover constraint alone cannot describe them.

Compare feasible candidates on expected net return, risk contributions, concentration, stress losses, liquidity and stability. Optimisation does not eliminate the trade-offs: the highest estimated Sharpe portfolio may violate the spending objective or require a degree of forecast confidence that the investor does not have.

### Worked example

Suppose a small increase in the estimated return of one equity region moves a candidate allocation from 40% to 80% in that region. Re-estimate with a more cautious return, apply the agreed concentration cap, and compare against the original policy allocation. If the supposed advantage disappears after plausible estimation changes or trading costs, the extreme tilt is poorly supported; a high in-sample objective value alone does not justify it.

The 27.27/72.73 equal-risk allocation in [[strategic-multi-asset-allocation]] is another candidate to assess, not a final answer. It can diversify the two modelled asset risks while leaving an unacceptable concentration in nominal duration or an insufficient expected return. Record which mandate requirements determine the final choice.

### Connections

- **Builds on:** [[strategic-multi-asset-allocation]], [[mean-variance-optimization]], [[constraints-shadow-prices]], [[risk-budgeting]].
- **Used by:** [[transaction-costs-no-trade]], [[portfolio-validation-attribution]].
- **Related:** [[black-litterman]], [[covariance-estimation]], [[optimiser-infeasibility]].

<a id="transaction-costs-no-trade"></a>

## Step 5: Implementation, Transaction Costs & Rebalancing
<!-- section: transaction-costs-no-trade | prerequisites: [mean-variance-optimization, lagrange-kkt-duality, exposure-neutrality] | related: [matlab-custom-portfolio-optimization, lasso-elastic-net, portfolio-construction-pipeline, optimiser-infeasibility] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [transaction-costs, market-impact, square-root-law, no-trade-region, rebalancing, garleanu-pedersen] -->

Linear costs (spread, commission) create a no-trade band: trade only when the marginal alpha beats the marginal cost, and then only to the edge of the band. Market impact grows faster than linearly in trade size, so the optimiser spreads trades out. Across periods, trade partially toward an aim portfolio.

### Key points: putting the allocation into the market

Choose instruments for the intended exposure, all-in costs, capacity and operational requirements. ETFs or pooled funds may be suitable for liquid beta; direct bonds can support cash-flow matching; futures and currency forwards can efficiently adjust exposures but require margin, collateral, rolls and funding. Manager selection adds fees, style drift and due-diligence considerations. Verify the exposures after choosing the instrument, not just its marketing category.

Before trading, check mandate compliance, cash and collateral, current holdings, risk contributions, liquidity and executable trade sizes. Plan execution around market depth and participation limits. Where implementing gradually, monitor the temporary allocation and transition risk as well as the final target. Reconcile positions and cash after execution and compare realised costs with the estimates.

### Rebalancing policy

| Rule | Purpose | Trade-off |
|---|---|---|
| Calendar review | Assess drift and assumptions on a regular schedule | Review need not mean trade; automatic full resets can create unnecessary costs |
| Weight bands | Trade when a sleeve leaves its agreed allocation range | Responds to drift, but the band width must reflect costs and mandate limits |
| Risk or liquidity triggers | Respond to excessive factor concentration, risk contributions, collateral needs or insufficient liquid reserves | These can require action even when capital weights remain close to target |
| Cash-flow rebalancing | Direct contributions, distributions and withdrawals toward restoring the allocation | Reduces trading, but cash flows may be insufficient to correct a breach |

Specify both the trigger and the destination: rebalance to the target, to the permitted boundary or part of the way, depending on the rule and costs. Distinguish **rebalancing back to policy** from **changing policy** after a revised mandate or structural assumption; a market fall alone does not establish that the strategic allocation is wrong.

**Example (illustrative, computed):** a 60/40 portfolio with equities up 20% and bonds unchanged drifts to equity weight **0.72 / 1.12 = 64.29%**, assuming no cash flows. A 55–65% equity band would not trigger on weights alone; a risk or collateral trigger might still do so. The no-trade model below explains why costs can justify tolerating some deviation.

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

## Step 5 Continued: Monitoring, Stress Tests & Attribution
<!-- section: portfolio-validation-attribution | prerequisites: [backtest-pitfalls, sharpe-ratio, portfolio-construction-pipeline] | related: [covariance-estimation, transaction-costs-no-trade, risk-contribution, minimum-variance-portfolio, risk-budgeting] | sources: [src-portopt-pm-interview, src-multi-asset-portfolio-framework] | tags: [validation, 1-over-n, bias-statistic, attribution, out-of-sample] -->

Monitoring checks whether the implemented portfolio still serves the mandate and whether the assumptions remain credible. An optimiser earns its place through out-of-sample evidence, net of costs; estimation error often eats the theoretical gain, so sample-based mean–variance can fail to beat 1/N.

### Key points: the ongoing monitoring dashboard

| Monitor | Interpretation and response |
|---|---|
| Performance against objectives and policy benchmark | Separate market movements, policy allocation, tactical tilts, manager/security selection and implementation costs; compare on the same currency and fee basis |
| Forecast versus realised risk | Compare volatility and tracking error with forecasts; persistent under-forecasting calls for risk-model review, not simply a larger risk budget |
| Asset and factor risk contributions | Identify changes in equity, duration, spread, inflation, FX and style concentration; weights can stay constant while risk changes ([[risk-contribution]]) |
| Drawdown, tail loss and stress losses | Check the investor's loss capacity and shortfall exposure using [[risk-measures]] and explicit scenarios; volatility alone does not summarise the tails |
| Liquidity and collateral | Track available cash, cash-flow coverage, redemption terms and time to liquidate under stressed market depth; include future capital calls |
| Costs and implementation | Check turnover, realised slippage, fees, financing and hedge costs against assumptions; reconcile holdings with the intended exposures |
| Governance | Set reporting frequency, breach thresholds, responsible decision makers and an escalation procedure; record changes to assumptions and policy |

Review assumptions and policy on a planned schedule, with event-driven checks for material changes in liabilities, liquidity or market structure. Respond to breaches using the agreed rules; do not continually retune weights to the latest winning backtest.

### Stress testing across economic environments

| Scenario | Joint shocks to consider | Portfolio question |
|---|---|---|
| Recession with disinflation | Equities fall, credit spreads widen, government yields may fall | Does high-quality duration offset enough growth risk to preserve required liquidity? |
| Inflation shock | Nominal yields rise, equity valuations compress, stock–bond correlation may turn positive | How much protection comes from inflation-linked exposure after allowing for real-rate moves? |
| Credit and liquidity crisis | Spreads widen, market depth falls, redemptions and collateral needs increase | Can the portfolio fund obligations without distressed sales? |
| Currency shock | Liability currency appreciates or depreciates and hedging costs change | Does the currency policy protect the obligations it was designed to cover? |
| Persistent range-bound markets | Trend signals reverse frequently and trading costs accumulate | Can an alternative sleeve endure its own adverse environment? |

Use historical episodes to understand known combinations and hypothetical shocks for risks absent from the sample. Shocks should be joint and internally plausible. Revalue instruments with nonlinear payoffs rather than extrapolating a small-move sensitivity ([[scenario-risk-grids]]). A **reverse stress test** starts with a failure, such as an unmanageable funding shortfall, and asks which combination of market and liquidity shocks could produce it; it does not estimate that event's probability.

**Example (illustrative, computed):** if equities lose 15% and nominal government bonds lose 10% over the same stress horizon, the 60/40 portfolio loses **0.6 × 15% + 0.4 × 10% = 13%**, before costs, rebalancing and cash flows. This is a conditional single-period loss, not a forecast, an annual volatility or a maximum drawdown estimate. Check whether the investor can absorb it and still meet payments, including any collateral needs.

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
