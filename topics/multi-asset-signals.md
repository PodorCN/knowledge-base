---
id: multi-asset-signals
title: "Multi-Asset Risk Premia & Macro Signals"
type: topic
domain: signal-research
sources: [src-quant-finance-study-notes]
---
# Multi-Asset Risk Premia & Macro Signals

**Sections:** [[structural-risk-premia]] · [[risk-on-risk-off]] · [[relative-value-long-short]] · [[fx-carry-spot-slide]]

<a id="structural-risk-premia"></a>

## Structural Risk Premia
<!-- section: structural-risk-premia | prerequisites: [capm-alpha-beta] | related: [risk-on-risk-off, fx-carry-spot-slide, realized-volatility, portfolio-variance-diversification] | sources: [src-quant-finance-study-notes] | tags: [risk-premia, factor-investing, alternative-risk-premia] -->

Persistent, systematic excess returns that come from **structural features** of markets (economy, investor behaviour, market mechanics), not from skill or timing. Investors are paid for bearing risks that are inherent to the structure.

| Premium | Why it exists |
|---|---|
| Equity risk premium | Equity holders bear more risk than bondholders |
| Term premium | Compensation for duration / rate risk |
| Credit premium | Compensation for default risk |
| Volatility risk premium | Implied vol systematically > realised; option sellers are paid |
| Value, momentum, carry, low vol | Behavioural biases, constraints, risk compensation |

### Key points
- **Sources of persistence:** regulatory constraints (e.g. insurers as forced sellers), behavioural biases (overpaying for lottery-like payoffs), risk–return trade-off.
- **In practice:** systematic strategies harvest several premia together ("alternative risk premia" / factor investing) because they have low correlation with each other and with traditional assets.

### Connections
- **Volatility risk premium:** [[realized-volatility]]. **Carry premium in FX:** [[fx-carry-spot-slide]]. **Why combine them:** [[portfolio-variance-diversification]].

<a id="risk-on-risk-off"></a>

## Risk-On / Risk-Off (RORO)
<!-- section: risk-on-risk-off | prerequisites: [variance-covariance-correlation] | related: [portfolio-variance-diversification, structural-risk-premia, fx-carry-spot-slide] | sources: [src-quant-finance-study-notes] | tags: [regimes, cross-asset-correlation, sentiment] -->

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
- RORO has become more pronounced since 2008 (central bank policy, algorithmic trading, interconnected markets). It is a spectrum, not two buckets.

<a id="relative-value-long-short"></a>

## Relative-Value Long/Short Equity Index Model
<!-- section: relative-value-long-short | prerequisites: [capm-alpha-beta] | related: [exposure-neutrality, ic-contribution, delta-one-products, research-workflow] | sources: [src-quant-finance-study-notes] | tags: [relative-value, pairs, beta-hedging, index] -->

1. **Universe:** pairs/baskets with economic logic: S&P 500 vs Russell 2000, MSCI Europe vs EM, tech vs energy.
2. **Signals for relative performance:**
   - Macro: growth differentials, rate sensitivity, inflation exposure
   - Valuation: relative P/E, P/B, earnings-yield spreads
   - Momentum: relative price trend over several lookbacks
   - Flows & positioning: fund flows, futures positioning, short interest
   - Vol & correlation regime
3. **Composite signal:** weighted blend (static or dynamic; regression / ML / Bayesian) forecasting relative return over the horizon ([[ic-contribution]]).
4. **Risk:** **beta-adjust** notionals (not dollar-neutral) to remove common market beta ([[exposure-neutrality]]); monitor spread vol, drawdowns, correlation stability.
5. **Execution:** futures / ETFs / swaps; roll costs, dividend differentials, funding ([[delta-one-products]]).

<a id="fx-carry-spot-slide"></a>

## FX CSS Model (Carry, Spot, Slide)
<!-- section: fx-carry-spot-slide | prerequisites: [forward-pricing] | related: [structural-risk-premia, risk-on-risk-off, time-series-momentum, risk-budgeting, ic-contribution] | sources: [src-quant-finance-study-notes] | tags: [fx, carry, uip, momentum, valuation, roll-down] -->

Expected return on an FX position ≈ **Carry** + **Expected spot move** + **Slide (roll-down)**.

### Carry
- Income from the rate differential; shows up in forward points (the high-yield currency's forward trades at a discount to spot, so you earn it if spot is unchanged; cf. [[forward-pricing]]).
- e.g. long BRL vs JPY earns the Brazil–Japan short-rate spread.
- **Uncovered interest rate parity fails empirically** → high-carry currencies don't depreciate enough → carry pays on average.
- Crash risk in risk-off: "picking up pennies in front of a steamroller" ([[risk-on-risk-off]]).
- Refinements: real-rate carry, term-structure carry, vol/tail-risk-adjusted carry.

### Spot

| Family | Signals | Horizon |
|---|---|---|
| Valuation | PPP, BEER (productivity, terms of trade, NFA), REER z-scores | Very slow; long-run anchor |
| Momentum / trend | MA crossovers, time-series momentum (1–12m), cross-sectional momentum | Works when carry fails (risk-off trends) |
| Macro fundamentals | Current account, fiscal, growth differential, policy divergence, commodity ToT | Regression / factor / ML |
| Flows & positioning | CFTC positioning, bank flows, option skew | Crowding / reversal risk |

### Slide (roll-down)
- As a 3m forward ages into a 2m forward, it rolls along the forward curve.
- Carry = **level** of forward points; slide = **slope/shape** of the forward term structure.
- Adds return in steep curves; little or negative in flat/inverted curves. Most relevant for longer forwards rolled early and FI overlays.

### Putting it together
- Compute each component per currency → z-score → rank (cross-sectional) or composite per pair.
- Weighting: pure carry, equal weight, or **risk parity across components** ([[risk-budgeting]]).
- **Interactions:** carry and momentum are negatively correlated (calm vs trending markets); valuation is roughly orthogonal; slide correlates with carry but adds curve information.
- Risk overlay: vol targeting, drawdown controls, correlation monitoring, liquidity filters.

### Connections
- **Builds on:** [[forward-pricing]]. **Momentum leg:** [[time-series-momentum]]. **Premium view:** [[structural-risk-premia]].
