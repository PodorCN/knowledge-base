---
id: multi-asset-signals
title: "Multi-Asset Signals"
type: topic
domain: signal-research
sources: [src-quant-finance-study-notes]
---
# Multi-Asset Signals

This chapter applies the signal toolkit across asset classes. It starts with the structural risk premia that systematic strategies harvest, describes the risk-on/risk-off regime that makes them move together, and then walks through two model designs: a relative-value long/short equity-index model and the FX carry–spot–slide model.

**Prerequisites:** [[capm-alpha-beta]], [[ic-contribution]], [[forward-pricing]], [[variance-covariance-correlation]].

**Leads to:** [[portfolio-variance-diversification]] (why premia are combined), [[risk-budgeting]] (weighting components), [[carry-stock-bond-timing]] (a full carry case study).

**Sections:** [[structural-risk-premia]] · [[risk-on-risk-off]] · [[relative-value-long-short]] · [[fx-carry-spot-slide]]

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
