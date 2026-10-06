---
id: signal-weighting
title: "Signal Weighting"
type: topic
domain: signal-research
sources: []
---
# Signal Weighting

Once several signals pass their tests, they must be combined into one score. This chapter compares the four ways of setting the weights (equal weight, equal risk, IC-weighted, model-fitted), explains why equal weight is so hard to beat (estimation error, DeMiguel, Garlappi & Uppal 2009), and covers what to do with highly correlated signals: drop one, or merge them into one theme.

Reliability note from the source material: the summary is based on general knowledge of the literature and of industry practice, not on a fresh search or a fresh reading of each paper. Treat firm-level details as general industry practice, not quotes, and exact figures as approximate. The AQR details come from search summaries of their papers; only the abstract-level summary of Lichtendahl & Winkler (2020) was used.

**Prerequisites:** [[information-coefficient]], [[ic-contribution]], [[estimator-properties]], [[multicollinearity]].

**Leads to:** [[mean-variance-optimization]] (the same estimation-error problem for asset weights), [[black-litterman]] (confidence per view), [[risk-budgeting]] (equal-risk weighting), [[carry-stock-bond-timing]].

**Sections:** [[signal-weighting-schools]] · [[equal-weight-estimation-error]] · [[correlated-signals-drop-or-merge]]

<a id="signal-weighting-schools"></a>

## Four Ways to Weight Signals
<!-- section: signal-weighting-schools | prerequisites: [information-coefficient, ic-contribution] | related: [equal-weight-estimation-error, correlated-signals-drop-or-merge, black-litterman, risk-budgeting, grinold-alpha, timing-signal-evaluation] | sources: [] | tags: [signal-combination, equal-weight, ic-weighting, forecast-combination, themes] -->

There are basically four schools for weighting signals in a composite, and the simple ones win more often than you'd expect.

### Definition

| Approach | How weights are set | Who uses it | Catch |
|---|---|---|---|
| 1. Equal weight | Every surviving signal gets the same share | Most asset-allocation papers; index providers | Ignores that some signals are better |
| 2. Equal risk | Scale each signal so each contributes the same volatility, then equal weight | AQR-style multi-signal funds | Still assumes signals are equally good |
| 3. IC-weighted | More weight to signals that predicted better in the past, less to ones that overlap | Grinold & Kahn; Qian, Hua & Sorensen; equity quant desks | Needs a lot of data to measure "better" |
| 4. Model-fitted | A regression or machine-learning model picks the weights | Stock-selection quant shops | Needs thousands of assets |

### What the papers say
- **Equal weight is very hard to beat.** DeMiguel, Garlappi & Uppal (2009) tested 14 "optimal" weighting methods against a plain 1/N split and none beat it consistently. They estimated you'd need about 3,000 months of data for an optimised split of 25 assets to pull ahead ([[equal-weight-estimation-error]]).
- **Averaging forecasts beats picking the best one.** Rapach, Strauss & Zhou (2010) took 15 stock-market predictors that each failed out of sample on their own. A simple equal average of the 15 forecasts worked. Forecasters call this the **"combination puzzle"**: fitted weights keep losing to the plain average.
- **The classic multi-signal papers just use 50/50.** Asness, Moskowitz & Pedersen (2013) combine value and momentum half and half, with no optimisation.
- **The IC-weighted formula exists but is aimed at stock picking.** Qian, Hua & Sorensen's method weights each signal by its average IC ([[information-coefficient]]), penalised for unstable IC and for overlap with other signals. It works when you score 500 to 3,000 stocks each month, because each month gives a precise IC reading.

### What practitioners do
- **Asset-allocation teams** usually group signals into 3 to 5 themes (valuation, trend, carry, macro, sentiment). They equal-weight inside a theme and equal-weight or judgment-weight across themes. Grouping stops five momentum variants from outvoting one value signal ([[correlated-signals-drop-or-merge]]).
- **Multi-factor index providers** such as MSCI target equal exposure to each factor.
- **Equity quant desks** are the ones that do tilt weights by trailing IC, often over a rolling 1 to 3 year window. Even there, many shrink the result halfway back to equal weight.
- **Black–Litterman users** set a confidence level per view instead of a weight, which is the same idea as IC-weighting ([[black-litterman]]); this is what the `BL_IC_SAA` / `BL_IC_TAA` settings do ([[carry-case-diagnosis]]).

### Application: stock–bond timing
- Stock/bond timing is the hardest case: it is **one bet per month, not 500**. That puts it firmly in approaches 1 and 2, the same place the asset-allocation papers and TAA desks end up. Approaches 3 and 4 are built for stock-picking breadth that this project does not have (breadth: [[information-coefficient]]).
- One practitioner idea worth borrowing is **theme grouping**. The sector layer has four momentum-type signals (`momentum`, `risk_adj_momentum`, `residual_momentum`, `ma_energy`). Treating them as one "momentum" theme with one shared weight is closer to how desks do it than giving each its own slot.

### Connections
- **Builds on:** [[information-coefficient]], [[ic-contribution]] (weighting schemes for a composite).
- **Related:** [[equal-weight-estimation-error]], [[correlated-signals-drop-or-merge]], [[risk-budgeting]] (equal risk), [[black-litterman]] (confidence per view), [[grinold-alpha]].

<a id="equal-weight-estimation-error"></a>

## Why Equal Weight Is Hard to Beat: Estimation Error (DeMiguel, Garlappi & Uppal 2009)
<!-- section: equal-weight-estimation-error | prerequisites: [signal-weighting-schools, estimator-properties] | related: [mean-variance-optimization, bias-variance-tradeoff, minimum-variance-portfolio, information-coefficient] | sources: [] | tags: [1-over-n, estimation-error, demiguel-garlappi-uppal, naive-diversification] -->

DeMiguel, Garlappi & Uppal (2009) don't quite claim equal weight is the best method. Their claim is narrower: the smarter methods are better in theory, but nobody has enough data to make them work in practice.

### Their explanation: estimation error
Any "optimal" weighting needs two inputs: how much each asset will return, and how the assets move together. Both have to be guessed from history, and the guesses are bad.

**Example:** (illustration, not from the paper) take an asset that truly returns 8% a year with 20% volatility. After 10 years of data, your estimate of its return is uncertain by about ±6% ($20\%/\sqrt{10}\approx6.3\%$). So you cannot tell an 8% asset from a 4% one or a 12% one.

The optimiser then makes this worse. It treats the guesses as facts and piles into whatever looks best, which is often just the asset that got lucky in the sample ([[mean-variance-optimization]]). Equal weight uses no guesses at all, so it has zero error of this kind.

| | Loss |
|---|---|
| Equal weight | Loses a little by not being the ideal mix |
| Optimised weights | Lose a lot from acting on wrong inputs |

In their data, the second loss was bigger than the first (the same trade-off as [[bias-variance-tradeoff]]).

### What they actually showed
- **The test:** 14 methods against equal weight, on 7 datasets, using 5 or 10 years of monthly history to set the weights each time.
- **In-sample vs real life:** on the US sector dataset, the optimised portfolio looked about twice as good as equal weight on paper (monthly Sharpe roughly 0.38 vs 0.19). Run forward on data it hadn't seen, it fell to roughly 0.08, well below equal weight.
- **Methods built to fix the problem also failed.** They tested versions that shrink the estimates, ignore returns altogether, or ban short positions. These did better than the raw optimiser but still did not beat equal weight consistently.
- **How much data would be enough:** about 3,000 months (250 years) for 25 assets, and about 6,000 months for 50.

### When optimising does win
They list three conditions:

1. A very long history to estimate from.
2. Few assets, so fewer numbers to guess.
3. The ideal mix is far better than equal weight, so there is a big prize to win.

Their test portfolios were already diversified baskets, which makes the prize small. That is one reason equal weight looked so strong.

### Pushback from later papers
- **Kritzman, Page & Turkington (2010)** argued that with longer histories and sensible inputs, optimisation does beat equal weight.
- **Kirby & Ostdiek (2012)** argued the test setup was tilted in favour of equal weight, and that simple rules based only on volatility can beat it.

Both agree on the underlying point: forecasts of returns are too noisy to drive weights. That is the part that carries over to signals, since an IC is a measure of return-forecasting skill and is just as noisy ([[information-coefficient]]).

### Connections
- **Builds on:** [[signal-weighting-schools]], [[estimator-properties]].
- **Related:** [[mean-variance-optimization]] (estimation error in asset weights), [[minimum-variance-portfolio]] (ignores returns), [[bias-variance-tradeoff]].

<a id="correlated-signals-drop-or-merge"></a>

## Highly Correlated Signals: Drop One or Merge Them?
<!-- section: correlated-signals-drop-or-merge | prerequisites: [signal-weighting-schools, multicollinearity] | related: [timing-signal-evaluation, ic-contribution, multiple-testing, pca] | sources: [] | tags: [forecast-combination, redundancy, lichtendahl-winkler, factor-zoo, themes] -->

A common rule is "drop one of any pair that is highly correlated". The forecasting paper's reason is that a near-copy adds nothing and steals votes. Practitioners agree with the problem but usually fix it differently: they merge near-copies into one signal instead of deleting one.

### What the paper says (Lichtendahl & Winkler 2020)
They studied the M4 forecasting competition, where the winning entry combined 9 methods. Their argument:

- Combining works because errors cancel. Two forecasts that make different mistakes average out to something better than either.
- A near-copy makes the same mistakes, so there is nothing to cancel. Adding a worse method whose errors are highly correlated with a better one is "redundant and can degrade" the combination.
- The reverse also holds: a worse method whose errors run opposite to a better one can still improve the average.

They screened out the weak and the highly correlated methods, averaged the rest, and got almost the same accuracy as the 9-method winner with fewer bad misses.

### Two effects
**Noise reduction** (illustration): averaging two signals with equal noise $\sigma$ and noise correlation $\rho$ leaves noise

$$\sigma_{\text{avg}}=\sigma\sqrt{\frac{1+\rho}{2}}$$

**Variables:**

- $\sigma$ noise (standard deviation) of each signal on its own
- $\rho$ correlation between the two signals' noise
- $\sigma_{\text{avg}}$ noise of the equal-weight average

| | Noise reduction from averaging two signals |
|---|---|
| Unrelated signals (correlation 0) | about 29% |
| Near-copies (correlation 0.9) | about 2.5% |

**Vote-stealing:** with two momentum look-alikes and one value signal at 1/3 each, momentum controls 2/3 of the decision even though you only have two real ideas.

### What practitioners do
They agree on the diagnosis but mostly do not drop. The common practice is to **average the look-alikes into one composite, then give the composite one vote.**

- **AQR** builds its value signal from several measures at once (book-to-price, earnings-to-price, cash-flow-to-price and others; one source says up to 25). Their stated reasons: averaging correlated measures cancels measurement noise, and when several versions of an idea all work, that is evidence the idea is real and not a fluke of one formula.
- **Multi-factor desks** then weight by theme (value, momentum, quality, and so on), not by individual measure, which solves the vote-stealing problem.
- **Academic factor research leans toward dropping.** Feng, Giglio & Xiu (2020) tested the hundreds of published stock factors and found most are redundant once the existing ones are accounted for ([[multiple-testing]]).

| Camp | Fix | Good when |
|---|---|---|
| Forecasting paper | Drop the weaker one of the pair | You can tell which one is weaker |
| Practitioners | Average them into one, give it one vote | You can't tell which one is weaker |

### Application: stock–bond timing
- The protocol's rule is the paper's version: correlation above 0.7, keep the one with the higher t-stat ([[timing-signal-evaluation]]). The weak spot is "higher t-stat". The sector signals had t-stats of 1.21, 0.70, 0.69 and 0.26, which are too close and too noisy to rank reliably. Picking the "better" one is close to a coin flip.
- Recommended switch to the practitioner version for the sector layer: average the four momentum-style signals (`momentum`, `risk_adj_momentum`, `residual_momentum`, `ma_energy`) into one momentum score and give that one score a single weight alongside the other themes.

### References
- Lichtendahl & Winkler (2020), "Why do some combinations perform better than others?"
- Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere"
- AQR, "Looking for the Intuition Underlying Multi-Factor Stock Selection"
- AQR, "Long-Only Style Investing: Don't Just Mix, Integrate"
- Feng, Giglio & Xiu (2020), "Taming the Factor Zoo"

### Connections
- **Builds on:** [[signal-weighting-schools]], [[multicollinearity]] (correlated regressors).
- **Related:** [[timing-signal-evaluation]] (the 0.7 independence rule), [[ic-contribution]] (contribution depends on correlations), [[multiple-testing]] (factor zoo), [[pca]].
