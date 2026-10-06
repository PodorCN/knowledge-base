---
id: multi-asset-signals
title: "Multi-Asset Signals"
type: topic
domain: signal-research
sources: [src-quant-finance-study-notes, src-carry-course-notes]
---
# Multi-Asset Signals

This chapter applies the signal toolkit across asset classes. It starts with the structural risk premia that systematic strategies harvest, describes the risk-on/risk-off regime that makes them move together, and then walks through model designs: a relative-value long/short equity-index model, carry defined uniformly across asset classes with a full case study of stock–bond relative-carry timing, and the FX carry–spot–slide model.

**Prerequisites:** [[capm-alpha-beta]], [[ic-contribution]], [[timing-signal-evaluation]], [[effective-sample-size]], [[forward-pricing]], [[variance-covariance-correlation]].

**Leads to:** [[portfolio-variance-diversification]] (why premia are combined), [[risk-budgeting]] (weighting components).

**Sections:** [[structural-risk-premia]] · [[risk-on-risk-off]] · [[relative-value-long-short]] · [[carry-across-assets]] · [[stock-bond-carry-case-study]] · [[fx-carry-spot-slide]]

<a id="structural-risk-premia"></a>

## Structural Risk Premia
<!-- section: structural-risk-premia | prerequisites: [capm-alpha-beta] | related: [risk-on-risk-off, fx-carry-spot-slide, realized-volatility, portfolio-variance-diversification] | sources: [src-quant-finance-study-notes] | tags: [risk-premia, factor-investing, alternative-risk-premia] -->

Structural risk premia are persistent, systematic excess returns that come from **structural features** of markets (the economy, investor behaviour, market mechanics), not from skill or timing. Investors are paid for bearing risks that are inherent to the structure.

### Definitions

| Premium | Why it exists |
|---|---|
| Equity risk premium | Equity holders bear more risk than bondholders |
| Term premium | Compensation for duration / rate risk |
| Credit premium | Compensation for default risk |
| Volatility risk premium | Implied vol is systematically above realised; option sellers are paid |
| Value, momentum, carry, low vol | Behavioural biases, constraints, risk compensation |

### Key points
- **Sources of persistence:** regulatory constraints (e.g. insurers as forced sellers), behavioural biases (overpaying for lottery-like payoffs), the risk–return trade-off.
- **In practice:** systematic strategies harvest several premia together ("alternative risk premia" / factor investing) because they have low correlation with each other and with traditional assets.

### Connections
- **Builds on:** [[capm-alpha-beta]].
- **Volatility risk premium:** [[realized-volatility]]. **Carry premium in FX:** [[fx-carry-spot-slide]]. **Why combine them:** [[portfolio-variance-diversification]].

<a id="risk-on-risk-off"></a>

## Risk-On / Risk-Off (RORO)
<!-- section: risk-on-risk-off | prerequisites: [variance-covariance-correlation] | related: [portfolio-variance-diversification, structural-risk-premia, fx-carry-spot-slide] | sources: [src-quant-finance-study-notes] | tags: [regimes, cross-asset-correlation, sentiment] -->

Markets alternate between risk appetite and risk aversion, and in the risk-off state most risky assets fall together.

### Definitions

| | Risk-on | Risk-off |
|---|---|---|
| Mood | Optimism, appetite for return | Fear, capital preservation |
| Favoured assets | Equities, HY, EM debt, commodities, high-beta FX | UST, Bunds, gold, USD, JPY, CHF |
| Vol | Low | Spikes |
| Credit spreads | Tighten | Widen |
| Correlations | Normal | **Rise: assets move together** |

### Key points
- In risk-off episodes **diversification breaks down** because one factor (de-risking) dominates ([[portfolio-variance-diversification]]: a common ρ sets a floor on portfolio variance).
- Watch VIX, credit spreads and cross-asset correlations.
- RORO has become more pronounced since 2008 (central-bank policy, algorithmic trading, interconnected markets). It is a spectrum, not two buckets.

### Connections
- **Builds on:** [[variance-covariance-correlation]].
- **Crash risk of carry:** [[fx-carry-spot-slide]].

<a id="relative-value-long-short"></a>

## Relative-Value Long/Short Equity Index Model
<!-- section: relative-value-long-short | prerequisites: [capm-alpha-beta, ic-contribution] | related: [exposure-neutrality, delta-one-products, research-workflow] | sources: [src-quant-finance-study-notes] | tags: [relative-value, pairs, beta-hedging, index] -->

A model design that forecasts the relative return of two related equity indices or baskets and trades the spread beta-neutrally.

### Model steps
1. **Universe:** pairs/baskets with economic logic: S&P 500 vs Russell 2000, MSCI Europe vs EM, tech vs energy.
2. **Signals for relative performance:**
   - Macro: growth differentials, rate sensitivity, inflation exposure
   - Valuation: relative P/E, P/B, earnings-yield spreads
   - Momentum: relative price trend over several look-backs
   - Flows & positioning: fund flows, futures positioning, short interest
   - Vol & correlation regime
3. **Composite signal:** a weighted blend (static or dynamic; regression / ML / Bayesian) forecasting the relative return over the horizon ([[ic-contribution]]).
4. **Risk:** **beta-adjust** the notionals (not dollar-neutral) to remove common market beta ([[exposure-neutrality]]); monitor spread vol, drawdowns, correlation stability.
5. **Execution:** futures / ETFs / swaps; roll costs, dividend differentials, funding ([[delta-one-products]]).

### Connections
- **Builds on:** [[capm-alpha-beta]] (beta), [[ic-contribution]] (composite).
- **Process:** [[research-workflow]].

<a id="carry-across-assets"></a>

## Carry Across Asset Classes & Stock–Bond Relative Carry
<!-- section: carry-across-assets | prerequisites: [forward-pricing, structural-risk-premia] | related: [fx-carry-spot-slide, stock-bond-carry-case-study, time-series-momentum, cross-validation-leakage] | sources: [src-carry-course-notes] | tags: [carry, koijen-moskowitz-pedersen-vrugt, dividend-yield, fed-model, stock-bond-timing] -->

Carry is the return an asset earns if its price does not move. It is observable **ex ante** with no pricing model, so it can be defined uniformly across asset classes; for timing stocks against bonds, the financing leg cancels and relative carry is dividend yield minus the 10-year yield.

### Formula
Koijen, Moskowitz, Pedersen & Vrugt (2018, *Journal of Financial Economics*):

$$r_{t+1}=C_t+E_t[\Delta P]+\text{shock}_{t+1}$$

**Variables:**

- $r_{t+1}$ return of the (futures) position from $t$ to $t+1$
- $C_t$ carry: the return if the price never moves, known at $t$
- $E_t[\Delta P]$ expected price change given information at $t$
- $\text{shock}_{t+1}$ unexpected part of the return

### Carry by asset and the relative carry

$$C^{E}_t\approx DY_t-r_f,\qquad C^{B}_t\approx y^{10}_t-r_f,\qquad C^{E}_t-C^{B}_t=DY_t-y^{10}_t$$

**Variables:**

- $C^{E}_t$, $C^{B}_t$ equity and bond carry
- $DY_t$ dividend yield of the equity index (%)
- $y^{10}_t$ 10-year government bond yield (%)
- $r_f$ financing (short) rate, the same for both legs, so it cancels in the difference

**Reading it:** high relative carry means equities pay more to hold than bonds → tilt to equity. This is also the dividend-yield variant of the **Fed model**, so carry belongs to the value family without being a price-reversal signal: it finds cheapness in *yields*, not in *past price paths*.

### Key points
- Empirically carry predicts returns in time series and cross section across equities, bonds, commodities, credit and options; timing strategies that buy when carry is above its historical mean earn average Sharpe ratios near 0.6 at monthly rebalancing.
- **Ideal vs feasible inputs:** ideal = futures-implied *forward* yields; feasible public proxies = trailing-twelve-month cash distributions / price for equities and the constant-maturity 10-year nominal yield for bonds.
- **No look-ahead:** distributions enter on their ex-dates (knowable then and no earlier), are summed by calendar month, and any day uses only past month ends ([[cross-validation-leakage]]).

**Code:** trailing-12-month dividend yield of SPY (`div` = cash distributions indexed by ex-date, `px` = daily close):

```python
monthly_div = div.resample("ME").sum()       # specials can't spike a daily series
ttm = monthly_div.rolling(12).sum()          # annualise, remove seasonality
yld = (ttm / px.resample("ME").last() * 100).dropna()   # DY_t in %
```

The signal itself is then one subtraction after aligning the daily 10-year yield (`^TNX`, %) onto the month ends: `(div_yield - y10).rename("equity_bond_carry")` (alignment code in [[cross-validation-leakage]]).
- **Know your proxy error:** since the 1990s US firms have shifted payout from dividends to buybacks, so dividend yield structurally **understates** shareholder yield; trailing and forward carry can disagree for years.
- **Timing rule:** compare carry with its own history, an expanding z-score capped at ±2 ([[time-series-momentum]]): $z=+2$ → full position, $z=0$ → flat.

### Connections
- **Builds on:** [[forward-pricing]], [[structural-risk-premia]].
- **Used by:** [[stock-bond-carry-case-study]]. **FX version:** [[fx-carry-spot-slide]].

<a id="stock-bond-carry-case-study"></a>

## Case Study: Timing US Stocks vs Bonds with Relative Carry
<!-- section: stock-bond-carry-case-study | prerequisites: [carry-across-assets, timing-signal-evaluation, effective-sample-size, cross-validation-leakage] | related: [information-coefficient, multiple-testing, research-workflow, backtest-pitfalls, grinold-alpha, black-litterman] | sources: [src-carry-course-notes] | tags: [case-study, carry, pre-registration, overlap, quantile-sort] -->

A pre-registered test of relative carry ($DY-y^{10}$) as a weekly stocks-vs-bonds timing signal. The sign matches theory but the effect is statistically indistinguishable from zero and the quintile shape contradicts linear sizing, so the candidate fails; the diagnosis points mainly at the measurement (dividend-only yield), not the theory.

### Design
- **Score:** trailing S&P 500 dividend yield minus the 10-year yield, expanding z-score capped at ±2, sign +1 (high favours equity).
- **Target:** 21-trading-day return of the equity basket minus the bond basket, sampled on the last trading day of each week.
- **Window:** weeks whose forward window ends before 2018: 574 usable weeks, Oct 2006 – Nov 2017.
- **Pass rule (frozen in advance):** $IC>0$ and $t\ge1.5$.
- **Registration:** the candidate is one entry in the portfolio config, inside the TAA layer next to two other tactical signals (HY-minus-IG credit appetite, bond time-series momentum). `side` says which asset a high value favours ("equity" adds to the equity-vs-bond score, "bond" subtracts):

```python
"equity_bond_carry": {
    "func": equity_bond_carry,
    "data": {"div_yield": "div_yield", "ten_year": "us10y"},
    "weight": 1 / 3, "side": "equity",
},
```

### Protocol: what, why, and what was rejected
Every choice was fixed before results were viewed.

| | What | Why | Rejected |
|---|---|---|---|
| A | **Dividend leg:** Cash distributions of an S&P 500 tracker by ex-date, summed by calendar month; trailing 12 months / month-end price, % | Monthly: distributions arrive quarterly with specials, daily yields spike on noise. 12 months: annualises and removes seasonality. Ex-dates + month-end: knowable on the ex-date and no earlier | Linear interpolation between month ends (draws the next month end into today: look-ahead) |
| B | **Bond leg:** 10-year nominal close, daily, % (same series as the existing term-spread signal) | No new plumbing, no inconsistent vintages | A longer source (FRED daily 10-year, back to the 1960s): swapping data mid-research is a new registration; recorded as the first upgrade for a round two. Cost: the equity-index feed caps history at 20 years, so the joint sample starts around 2006 |
| C | **Baskets:** Equal-weight, daily-rebalanced index per sleeve (11 sector funds; 4 bond funds), from long-history US originals converted at spot FX; in code `(1 + prices[labels].pct_change().mean(axis=1).dropna()).cumprod()`, assets join once they have prices | The neutral, tradable proxy for "the asset class", matching the sleeves the portfolio tilts | The traded (Canadian) funds: they start in 2025, too short to calibrate |
| D | **Alignment:** Union of calendars + forward-fill onto trading days | Forward-fill invents no information | Interpolation or resampling touching future month ends |
| E | **Normalisation:** Expanding z-score vs own past, cap ±2, sign after | The paper's rule "above vs below the historical mean" in volatility units; expanding = no extra parameter; cap = no single freak observation | Rolling window (one more parameter to overfit). Disclosed wart: alignment before normalisation, so the 20-observation minimum counts trading days, and 2006–2008 z-scores rest on thin history |
| F | **Sampling:** Weekly (last trading day); 21-trading-day forward | Daily drowns in microstructure noise and quintuples overlap; monthly starves the sample; weekly = the live rebalancing clock. 21 days = the paper's one-month holding period, exact | Calendar months (wobble with holidays) |
| G | **Clean splits:** A week is in the selection window only if its whole forward window ends before 2018; straddling weeks belong to neither side | No leakage across the boundary ([[cross-validation-leakage]]) | Assigning straddlers to one side |
| H | **Rank IC:** Spearman over the 574 score/forward pairs | Fat-tailed returns: one crash week would own a Pearson coefficient; linearity checked separately by the quintile sort | Pearson |
| I | **Overlap:** $n_{\text{eff}}\approx574/4.2\approx137$ ([[effective-sample-size]]) | Neighbouring 21-day windows share 16 days | Naive $n=574$ (≈2× too large a $t$) |
| J | **Quintiles & curve:** 5 buckets (≈115 weeks each); positions $\mathrm{clip}(z/2,\pm1)$ held one week; gross; rolling 52-week IC; yearly IC with ≥10 weeks | See [[timing-signal-evaluation]] | — |
| K | **Sealed data:** Nothing after the boundary is loaded, not for a quick look or debugging | Results stay sealed until their round | — (only the input history, without forwards or statistics, is displayed, as a live dashboard would) |

### Results

| Statistic | Result | Reading |
|---|---|---|
| Rank IC | +0.0252 | Right sign, negligible size |
| $t$ (overlap-adjusted) | +0.29 | 5× below the bar: noise |
| Hit rate | 56% | Uninformative, near a coin flip |
| Timing curve, annualised | +1.6% | Faintly positive, gross of costs |
| Worst drawdown | −27.7% | |
| Autocorrelation of the score | 0.95 | Slow-moving; nearly free to trade |

Average next-21-day equity-minus-bond return by score quintile:

| Q1 (low) | Q2 | Q3 | Q4 | Q5 (high) |
|---|---|---|---|---|
| −0.26% | +0.73% | +1.32% | +0.63% | −0.09% |

**Notes:**

- The quintiles hump: the strongest buy signals (Q5) lost money, so linear sizing puts the largest positions where returns are worst.
- Figures in the original notes (not reproduced here): raw carry and its z-score compress after 2008 (the zero-rate era pins both legs); rolling 52-week IC flips sign around zero; no single regime carries the result (no "crisis alpha"); the decile-mean line bends down at the right end.

**Verdict: fail.** By the pre-committed rule the candidate stops here; later data stays sealed.

**In the portfolio:** the TAA layer as a whole measured IC −0.009 (vs next 21 trading days, weekly samples; SAA layer +0.083), so its weight in the equity-vs-bond score is set to zero and its Black–Litterman IC to 0 ([[grinold-alpha]], [[black-litterman]]); the signals are still computed for the research pages:

```python
L1_TE_WEIGHTS = {"saa": 1.0, "taa": 0.0}   # TAA IC ~0
BL_IC_TAA = 0.0
```

### Worked example
**Effective N and the IC needed for $t=1.5$** (574 overlapping weeks, 21-day horizon):

$$m=\frac{21}{5}=4.2,\qquad n_{\text{eff}}=\frac{574}{4.2}\approx137,\qquad t\approx IC\sqrt{n_{\text{eff}}-2}=0.0252\sqrt{135}\approx0.29,\qquad IC_{\text{needed}}\approx\frac{1.5}{\sqrt{135}}\approx0.13$$

**Variables:**

- $m$ overlap ratio (horizon / sampling step, in trading days)
- $n_{\text{eff}}$ effective number of independent observations
- $t$ overlap-adjusted t-statistic of the IC
- $IC$ observed rank IC (0.0252)
- $IC_{\text{needed}}$ smallest IC that reaches $t=1.5$

### Diagnosis: four suspects, ranked
1. **Mismeasured equity leg.** 2006–2017 coincides with the buyback boom; dividend-only carry understates shareholder yield for the whole sample. Measurement error, not theory error; adding buyback yield is the one fix that could change the answer.
2. **Single-series power.** ~140 independent observations need $IC\approx0.13$ for $t\ge1.5$, a level only one established signal in this literature reaches. A Sharpe-0.6 effect averaged across many assets can shrink to 0.025 on one line.
3. **Horizon mismatch.** A monthly, slow-moving spread tested on 21-day forwards is the harshest possible exam. Lengthening the window is one line of code but changes the registered design: a new round with the $t\ge3$ bar.
4. **Variance drought.** The zero-rate era pinned both legs: with no spread movement there is nothing to time. This explains rather than excuses, and suggests a rerun on post-2022 high-rate data.

### Key points
- Carry = hold-return difference; the financing rate cancels, leaving dividend yield minus bond yield.
- Proxies must be ex ante and dated by publication; trailing ≠ forward, and buybacks bias dividend-only measures.
- Judge timing by overlap-adjusted $t$, quintile shape, timing curve with drawdown, turnover, independence and sealed out-of-sample data, never by IC alone.
- Fix pass/fail rules before results; a failed candidate with clean discipline is a result, not a waste.
- Theory survives: the tested object was one monthly, single-asset, trailing proxy, not carry itself.

### Connections
- **Builds on:** [[carry-across-assets]], [[timing-signal-evaluation]], [[effective-sample-size]], [[cross-validation-leakage]].
- **Related:** [[information-coefficient]] (rank IC), [[multiple-testing]] (the $t\ge3$ round-two hurdle), [[research-workflow]].

<a id="fx-carry-spot-slide"></a>

## FX CSS Model (Carry, Spot, Slide)
<!-- section: fx-carry-spot-slide | prerequisites: [forward-pricing, time-series-momentum] | related: [structural-risk-premia, risk-on-risk-off, risk-budgeting, ic-contribution] | sources: [src-quant-finance-study-notes] | tags: [fx, carry, uip, momentum, valuation, roll-down] -->

The expected return of an FX position is decomposed as **Carry** + **Expected spot move** + **Slide (roll-down)**, and each component is forecast by its own family of signals.

### Carry
- Income from the interest-rate differential; it shows up in the forward points (the high-yield currency's forward trades at a discount to spot, so you earn the differential if spot is unchanged; cf. [[forward-pricing]]).
- E.g. long BRL vs JPY earns the Brazil–Japan short-rate spread.
- **Uncovered interest-rate parity fails empirically** → high-carry currencies don't depreciate enough → carry pays on average.
- Crash risk in risk-off: "picking up pennies in front of a steamroller" ([[risk-on-risk-off]]).
- Refinements: real-rate carry, term-structure carry, vol/tail-risk-adjusted carry.

### Spot

| Family | Signals | Horizon |
|---|---|---|
| Valuation | PPP, BEER (productivity, terms of trade, NFA), REER z-scores | Very slow; long-run anchor |
| Momentum / trend | MA crossovers, time-series momentum (1–12m), cross-sectional momentum | Works when carry fails (risk-off trends) |
| Macro fundamentals | Current account, fiscal, growth differential, policy divergence, commodity terms of trade | Regression / factor / ML |
| Flows & positioning | CFTC positioning, bank flows, option skew | Crowding / reversal risk |

### Slide (roll-down)
- As a 3m forward ages into a 2m forward, it rolls along the forward curve.
- Carry = the **level** of the forward points; slide = the **slope/shape** of the forward term structure.
- Slide adds return in steep curves and little or negative return in flat/inverted curves. It matters most for longer forwards rolled early and for fixed-income overlays.

### Putting it together
- Compute each component per currency → z-score → rank (cross-sectional) or composite per pair.
- Weighting: pure carry, equal weight, or **risk parity across components** ([[risk-budgeting]]).
- **Interactions:** carry and momentum are negatively correlated (calm vs trending markets); valuation is roughly orthogonal; slide correlates with carry but adds curve information.
- Risk overlay: vol targeting, drawdown controls, correlation monitoring, liquidity filters.

### Connections
- **Builds on:** [[forward-pricing]]. **Momentum leg:** [[time-series-momentum]]. **Premium view:** [[structural-risk-premia]]. **Carry in general:** [[carry-across-assets]].
