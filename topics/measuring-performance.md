---
id: measuring-performance
title: "Performance"
type: topic
domain: portfolio-construction
sources: [src-squarepoint-dqa-workbook]
---
# Performance

Before building portfolios we need to measure them. This chapter covers the Sharpe ratio and its statistical pitfalls, the information ratio and when to use it instead, why a high win rate says little about profitability, and how gross/net exposure and neutrality describe a long-short book.

**Prerequisites:** [[returns-simple-log]], [[variance-covariance-correlation]], [[hypothesis-testing]], [[stationarity-ar1]], [[capm-alpha-beta]].

**Leads to:** [[portfolio-variance-diversification]], [[marginal-sharpe-improvement]], [[risk-measures]] (tail measures beyond σ).

**Sections:** [[sharpe-ratio]] · [[information-ratio]] · [[win-rate-expectancy]] · [[exposure-neutrality]]

<a id="sharpe-ratio"></a>

## Sharpe Ratio (annualisation, leverage, pitfalls)
<!-- section: sharpe-ratio | prerequisites: [variance-covariance-correlation, returns-simple-log, hypothesis-testing] | related: [multiple-testing, stationarity-ar1, portfolio-variance-diversification, marginal-sharpe-improvement, risk-measures, effective-sample-size] | sources: [src-squarepoint-dqa-workbook] | tags: [sharpe, annualisation, performance] -->

The Sharpe ratio is mean excess return per unit of volatility. It scales with the square root of the horizon only when returns are uncorrelated, and its sample estimate is a t-statistic in disguise.

### Formulas
$$SR=\frac{E[R-r_f]}{\sigma(R-r_f)},\qquad SR_h=\sqrt h\,SR_1,\qquad t=\sqrt n\,\widehat{SR}_{\text{period}}$$
$$\mathrm{Var}\Big(\sum_{t=1}^hZ_t\Big)=h\,\sigma^2+2\sum_{k=1}^{h-1}(h-k)\,\gamma_k$$

**Variables:**

- $R$ strategy return per period; $r_f$ risk-free return per period
- $Z_t=R_t-r_{f,t}$ excess return in period $t$, with variance $\sigma^2$
- $SR_1$ one-period Sharpe ratio; $SR_h$ Sharpe ratio over $h$ periods
- $h$ number of periods aggregated (e.g. 252 days for annualising daily data)
- $n$ number of observations in the sample
- $\widehat{SR}_{\text{period}}$ estimated per-period Sharpe ratio
- $\gamma_k$ autocovariance of $Z$ at lag $k$

### Worked examples
- Daily $\mu$ = 0.1%, $\sigma$ = 2% → daily SR 0.05 → annual ≈ $0.05\sqrt{252}\approx0.794$.
- Daily SR 0.1 over 100 days → $t=\sqrt{100}\times0.1=1$, even though the annualised SR ≈ 1.59.

### Key points
- $\sqrt h$ scaling needs **uncorrelated, stationary, summed** returns. Positive autocorrelation makes the $\gamma_k$ terms positive, so naive annualisation **overstates** the SR ([[effective-sample-size]]).
- **Leverage** by $k>0$ leaves the SR unchanged ($k\mu/k\sigma$) in a frictionless world, but raises drawdown and ruin risk.
- A high SR can mislead: few observations, selection ([[multiple-testing]]), stale prices, short-option (negative-skew) payoffs, ignored costs, regime change.

### Connections
- **Is a t-stat in disguise:** [[hypothesis-testing]]; inflated by [[multiple-testing]]; autocorrelation from [[stationarity-ar1]].
- **Portfolio level:** [[portfolio-variance-diversification]], [[marginal-sharpe-improvement]]. **Beyond σ:** [[risk-measures]].
- **Benchmark-relative version:** [[information-ratio]].

<a id="information-ratio"></a>

## Information Ratio vs Sharpe Ratio
<!-- section: information-ratio | prerequisites: [sharpe-ratio, capm-alpha-beta, fundamental-law-active-management] | related: [eval-statistical-significance, mandate-tracking-error, risk-measures, marginal-sharpe-improvement] | sources: [] | tags: [information-ratio, tracking-error, active-return, benchmark, sharpe] -->

The information ratio (IR) is the Sharpe ratio of the **active** return: mean outperformance of a benchmark per unit of tracking error. The Sharpe ratio judges a portfolio against cash; the IR judges a manager against the benchmark they were hired to beat.

### Formula
$$IR=\frac{E[R_p-R_b]}{\sigma(R_p-R_b)}=\frac{E[A]}{TE},\qquad \widehat{IR}_{\text{ann}}=\sqrt{P}\,\frac{\bar A}{s_A}$$

**Variables:**

- $IR$ information ratio (dimensionless, per year when annualised)
- $R_p$ portfolio return per period
- $R_b$ benchmark return per period (e.g. S&P 500, Bloomberg US Aggregate)
- $A=R_p-R_b$ active return per period
- $TE=\sigma(R_p-R_b)$ tracking error: standard deviation of active return
- $\widehat{IR}_{\text{ann}}$ annualised sample IR
- $P$ number of periods per year ($12$ for monthly data, $252$ for daily)
- $\bar A$ sample mean of active return per period
- $s_A$ sample standard deviation of active return per period

**Notes:**

- The Sharpe ratio $SR = E[R_p-r_f]/\sigma(R_p-r_f)$ ([[sharpe-ratio]]) is the special case with the risk-free rate as the benchmark. So for a market-neutral fund benchmarked to cash, $IR = SR$.
- Annualising with $\sqrt{P}$ needs uncorrelated active returns, the same caveat as for the Sharpe ratio.
- **Ex ante vs ex post:** this section measures *realised* IR from returns. The *forecast* IR of a strategy is $IR \approx IC\sqrt{BR}\cdot TC$ ([[fundamental-law-active-management]]), and a mandate turns IR into an alpha target via $E[A] = IR \times TE$ ([[mandate-tracking-error]]).

### Residual IR: removing hidden beta
If the portfolio's beta to the benchmark is not 1, $R_p - R_b$ contains benchmark exposure, not skill. A beta-1.3 fund in a rising market shows positive "active return" with no stock-picking at all. The residual (appraisal) version regresses out the benchmark first:

$$R_p-r_f=\alpha+\beta\,(R_b-r_f)+\varepsilon,\qquad IR_{\text{res}}=\frac{\alpha}{\sigma(\varepsilon)}$$

**Variables:**

- $R_p, R_b$ portfolio and benchmark return per period
- $r_f$ risk-free return per period
- $\alpha$ residual return (Jensen's alpha) per period ([[capm-alpha-beta]])
- $\beta$ portfolio beta to the benchmark
- $\varepsilon$ residual return, uncorrelated with the benchmark by construction
- $IR_{\text{res}}$ residual information ratio (appraisal ratio)

With $\beta = 1$ the two definitions coincide. Use $IR_{\text{res}}$ whenever beta drifts away from 1.

### How IR and Sharpe combine
A benchmark-tracking portfolio plus an uncorrelated active bet is a two-asset portfolio. Scaling the active bet optimally gives the highest Sharpe ratio achievable:

$$SR_{\max}^{2}=SR_b^{2}+IR_{\text{res}}^{2},\qquad \sigma_A^{*}=\frac{IR_{\text{res}}}{SR_b}\,\sigma_b$$

**Variables:**

- $SR_{\max}$ highest Sharpe ratio reachable by holding the benchmark plus the active bet at the optimal size
- $SR_b$ Sharpe ratio of the benchmark
- $IR_{\text{res}}$ residual information ratio of the active bet
- $\sigma_A^{*}$ active risk (tracking error) that achieves $SR_{\max}$
- $\sigma_b$ benchmark volatility

**Why:** the maximum Sharpe ratio of uncorrelated assets satisfies $SR_{\max}^2 = \mu^\top\Sigma^{-1}\mu = \sum_i (\mu_i/\sigma_i)^2$, and the benchmark and the residual bet are uncorrelated by construction. This is the "Pythagorean" relation in the CFA Level II reading *Analysis of Active Portfolio Management*.

**Reading it:** IR is the quantity a manager controls; SR is what the investor ends up with. Any positive $IR_{\text{res}}$ raises the achievable SR, and **IR does not change with leverage of the active bet**, while the SR of the total portfolio does.

### Worked example
Fund return $9\%$, benchmark $7\%$, risk-free $3\%$, benchmark volatility $15\%$, tracking error $4\%$, beta $1$, active return uncorrelated with the benchmark:

- **Benchmark:** $SR_b = (7-3)/15 = 0.267$.
- **Fund IR:** $IR = (9-7)/4 = 0.50$.
- **Fund Sharpe:** $\sigma_p = \sqrt{15^2+4^2} = 15.52\%$, so $SR_p = (9-3)/15.52 = 0.387$.
- **Best possible Sharpe with this skill:** $SR_{\max} = \sqrt{0.267^2+0.5^2} = 0.567$, reached at $\sigma_A^* = (0.5/0.267)\times15\% = 28.1\%$ tracking error.

In practice the TE budget is far below $28\%$ because the true IR is uncertain and the client caps active risk ([[mandate-tracking-error]]).

### Is the IR statistically real?
An annualised IR is a $t$-statistic per square-root year, like the Sharpe ratio: $t \approx \widehat{IR}_{\text{ann}}\sqrt{Y}$, where $Y$ is the number of years of (uncorrelated) active returns.

- $IR = 0.5$ over 5 years gives $t = 0.5\sqrt5 = 1.12$, which fails even the $1.5$ screen ([[eval-statistical-significance]]).
- Reaching $t = 2$ at $IR = 0.5$ takes $(2/0.5)^2 = 16$ years.
- **Benchmarks:** Grinold & Kahn (*Active Portfolio Management*, 2000) put a top-quartile active manager at about $IR \approx 0.5$ and an exceptional one at about $1.0$. Most managers sit near zero after fees.

### When to use which
- **Use Sharpe** when the investor's alternative is cash, or when judging a whole portfolio: hedge funds, market-neutral and stat-arb books, CTAs and global macro, a total pension fund.
- **Use IR** when there is an agreed, investable benchmark and the question is the manager's value added: long-only equity and bond mandates, enhanced index, portable alpha.
- **Use both** for a benchmarked fund: IR to judge the manager, SR to judge what the investor's total holding earns.
- **IR is only as good as the benchmark:** a benchmark that is too easy (different style, sector or credit quality) manufactures a high IR without skill. Check that the benchmark is investable, specified in advance and matches the mandate.

### By asset class
- **Equities, long-only active:** IR against the policy index (e.g. S&P 500, MSCI ACWI). Use residual IR or a style benchmark for funds with a persistent size, value or beta tilt, otherwise the factor premium shows up as "skill". Long-only constraints cap achievable IR through the transfer coefficient ([[fundamental-law-active-management]]).
- **Equity market-neutral / stat arb:** the benchmark is cash, so report the Sharpe ratio (here $IR = SR$). Also report net exposure and factor betas ([[exposure-neutrality]]), since a "neutral" book with residual beta is not neutral.
- **Fixed income, benchmarked:** IR against the bond index (e.g. Bloomberg US Aggregate). A structural overweight of credit or longer duration earns a steady spread premium in calm markets and loses it in sell-offs. That looks like a high IR with a hidden short-crisis exposure. Measure residual IR against duration and spread-duration factors, and look at the active drawdown in stress periods **(自己推理)**.
- **Global macro, CTA, FX and commodity absolute-return:** no natural benchmark, so use the Sharpe ratio, with a peer index only for comparison. Their returns are far from normal: trend-following is positively skewed and carry or short-vol is negatively skewed. Pair SR with drawdown and expected shortfall ([[risk-measures]]) and the win/loss payoff profile ([[eval-directional-hit-rate]]).
- **Multi-asset / balanced:** SR for the total fund versus cash. IR of the active layer (tactical tilts) against the strategic policy mix (e.g. 60/40), so allocation skill is separated from the policy's own risk premium.
- **Private and illiquid assets:** appraisal-based returns are smoothed, which understates volatility and tracking error, so both SR and IR look too high. Unsmooth the returns or use public-market equivalents before comparing (stale-price pitfall in [[sharpe-ratio]]).

### Pitfalls
- **Closet indexing:** a tiny TE makes IR large even when the alpha in dollars is negligible. Report $E[A]$ and TE alongside IR.
- **Negative ratios:** with negative active return, a *higher* TE makes IR less negative. Do not rank losing managers by IR.
- **Fees:** quote IR net of fees; a gross IR of $0.5$ with $1\%$ fees on $4\%$ TE becomes $0.25$.

### Connections
- **Builds on:** [[sharpe-ratio]], [[capm-alpha-beta]], [[fundamental-law-active-management]].
- **Used by:** [[mandate-tracking-error]], [[risk-measures]], [[marginal-sharpe-improvement]].
- **Related:** [[eval-statistical-significance]] ($t$-hurdles), [[exposure-neutrality]].

<a id="win-rate-expectancy"></a>

## Win Rate vs Expected Value
<!-- section: win-rate-expectancy | prerequisites: [expectation-linearity-indicators] | related: [risk-measures, sharpe-ratio] | sources: [src-squarepoint-dqa-workbook] | tags: [expectancy] -->

The profitability of a trade depends on the sizes of wins and losses, not only on how often it wins.

### Formula
$$E[\Pi]=p\,g-(1-p)\,\ell-c$$

**Variables:**

- $E[\Pi]$ expected profit per trade
- $p$ probability of a win
- $g$ gain on a win
- $\ell$ loss on a loss
- $c$ cost per trade

### Worked example
90% win rate, +1 on wins and −20 on losses (no costs) → $0.9\times1-0.1\times20=0.9-2=-1.1$ per trade.

### Key points
- A high win rate ≠ positive expectation (typical of short-option strategies).

### Connections
- **Builds on:** [[expectation-linearity-indicators]].
- **Related:** [[sharpe-ratio]], [[risk-measures]].

<a id="exposure-neutrality"></a>

## Gross/Net Exposure, Neutrality & Trading Costs
<!-- section: exposure-neutrality | prerequisites: [capm-alpha-beta] | related: [win-rate-expectancy, relative-value-long-short] | sources: [src-squarepoint-dqa-workbook] | tags: [long-short, beta-neutral, bid-ask] -->

Gross exposure measures total capital at risk, net exposure the directional tilt. Being neutral in one sense (dollars) does not make a book neutral in another (beta, sector, style).

### Formulas
$$\text{Gross}=\sum_i|w_i|,\qquad \text{Net}=\sum_iw_i$$

**Variables:**

- $w_i$ portfolio weight of asset $i$ (negative for shorts)

### Key points
- Dollar-neutral ≠ beta-neutral (the long and short legs may have different betas); sector, style and nonlinear exposures can remain.
- Bid–ask spread: crossing costs the half-spread relative to the mid. 1 bp = 0.0001.

### Connections
- **Builds on:** [[capm-alpha-beta]].
- **Used by:** [[relative-value-long-short]] (beta-adjusted notionals).
