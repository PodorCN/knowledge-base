---
id: structured-products-delta-one
title: "Structured Products & Delta One"
type: topic
domain: pricing
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep]
---
# Structured Products & Delta One

**Sections:** [[autocallables]] · [[reverse-convertible]] · [[principal-protected-note]] · [[worst-of-correlation]] · [[swaptions]] · [[delta-one-products]]

<a id="autocallables"></a>

## Autocallables (worst-of, RBC case study)
<!-- section: autocallables | prerequisites: [digital-options, barrier-options, worst-of-correlation] | related: [local-stochastic-volatility, monte-carlo-pricing, reverse-convertible, delta-one-products, volatility-skew, model-risk-governance] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [autocallable, structured-notes, dividends, rbc] -->

**Structure:**

- Coupon (often contingent, with memory).
- **Early redemption** if the (worst-of) underlying ≥ autocall level on an observation date.
- At maturity, if below the knock-in barrier, investor takes the equity loss.

**Decomposition:** bond + short down-and-in put + autocall digitals + coupon digitals.

### RBC 424B2 case (public facts)
DJIA / Nasdaq-100 / S&P 500 worst-of, 3y (Feb 2029); monthly contingent coupon $6.25/$1,000 (7.5% p.a.) if all ≥ 60%; monthly autocall from Feb 2027 if all ≥ 100%; principal loss if worst < 60% at maturity. Estimated value $937.50–$987.50; underwriting 0.15%.

### Desk workflow (inferred)
Mark surfaces → calibrate LSV per underlier, mark correlations, imply dividends → MC in C++ (Greeks by AAD/bumps) → reserves (model, barrier & digital overhedges, correlation, dividends), verify vs consensus → hedge Δ with futures, vega with vanillas, dividends with div futures → recycle correlation / long-dated vol → discount at internal funding rate.

### MC results (source's assumptions, not RBC's)
| per $1,000 | Flat ATM vols | Downside vols +6 pts |
|---|---|---|
| Note value | 1007.7 | 958.5 |
| P(autocall) | 67.8% | 64.3% |
| P(principal loss) | 8.3% | 16.5% |

Flat vol values the note **above par** — wrong: investor is short a deep OTM put priced in the steep skew ([[volatility-skew]]).

### Sensitivities → what the issuer holds
Vols +1pt: −7.45 (issuer long vol); corr −0.1: −2.94; divs +0.5%: −2.80 (issuer long dividends); discount at r instead of r+60bp: +10.10.
After Δ-hedging, issuers are **short delta, long vol, long dividends, short correlation**; awkward gamma near barriers/triggers. March 2020: 2020 dividends traded ~55% of model, 2021 ~70% → big losses on dividend hedges.

### Why estimated value < $1,000
Issue price covers underwriting, hedging cost, structuring margin; value uses internal funding rate & mid hedge terms.

### Connections
- **Components:** [[digital-options]], [[barrier-options]], [[worst-of-correlation]]. **Model:** [[local-stochastic-volatility]] + [[monte-carlo-pricing]].
- **Sibling:** [[reverse-convertible]]. **Dividend hedge:** [[delta-one-products]].

<a id="reverse-convertible"></a>

## Reverse Convertible
<!-- section: reverse-convertible | prerequisites: [barrier-options] | related: [autocallables, principal-protected-note, worst-of-correlation] | sources: [src-rbc-quantdev-prep] | tags: [structured-notes, yield-enhancement] -->

**= bond + short (down-and-in) put.**

- Investor sells the put and receives an enhanced coupon.
- Adding early-redemption digitals and contingent coupon digitals turns it into an [[autocallables]].

<a id="principal-protected-note"></a>

## Principal-Protected Note (PPN)
<!-- section: principal-protected-note | prerequisites: [static-replication, discounting-compounding] | related: [reverse-convertible, digital-options] | sources: [src-rbc-quantdev-prep] | tags: [structured-notes, participation-rate] -->

**= zero-coupon bond (guarantees principal) + call (or call spread) on the index.**

$$\text{Participation}=\frac{\text{Note price}-\text{ZCB price}}{\text{Option price}}$$
- Higher rates → cheaper ZCB → more budget → **higher** participation.
- Higher vol → dearer option → **lower** participation.
- Same "budget buys payoff" logic as the digital payout ratio Q in [[digital-options]].

<a id="worst-of-correlation"></a>

## Worst-of Payoffs & Correlation Risk
<!-- section: worst-of-correlation | prerequisites: [portfolio-variance-diversification, barrier-options] | related: [autocallables, reverse-convertible, digital-options] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [worst-of, correlation, dispersion] -->

Payoff depends on the worst performer in a basket.

- Investor **sells** the desk a worst-of down-and-in put and **receives** worst-of coupon/autocall digitals.
- **Lower correlation** → more dispersion → worst is lower → put worth **more**, digitals worth **less** → low-correlation baskets pay higher headline coupons.
- Desk is long the put, short the digitals; both lose value as ρ rises ⇒ **desk is short correlation** ("The dealer, conversely, is short correlation" — Risk.net). Hurt in Q1 2020 when markets moved in unison. (Long-put/short-digital breakdown is 自己推理; direction matches sources.)
- Example: correlations −0.1 → note −2.94 per $1,000; single index instead of worst-of → 1026.3 (worst-of cheaper, funds the coupon).

### Connections
- **Diversification maths:** [[portfolio-variance-diversification]]. **Products:** [[autocallables]], [[reverse-convertible]].

<a id="swaptions"></a>

## Swaptions (and why an equity desk cares)
<!-- section: swaptions | prerequisites: [black-76] | related: [sabr, autocallables] | sources: [src-rbc-quantdev-prep] | tags: [swaption, callable-notes, rates] -->

$$PS=A\,[F\,N(d_1)-K\,N(d_2)],\qquad d_{1,2}=\frac{\ln(F/K)\pm\tfrac12\sigma^2T}{\sigma\sqrt T},\qquad A=\sum_i\tau_iP(0,t_i)$$

**Variables:**

- $PS$ payer swaption
- $A$ annuity (PV01)
- $F$ forward swap rate
- $K$ strike rate
- σ Black vol
- $T$ option expiry
- $\tau_i$ accrual fractions
- $P(0,t_i)$ discount factors

- Rates desks quote **normal (Bachelier) vol** because rates can be negative → [[sabr]].
- **Equity desk link (自己推理):** issuer-callable structured notes embed a **Bermudan receiver swaption** owned by the issuer, hedged with rates; long-dated equity products carry rho / equity–rates correlation. Or "equity swaptions" = options on a TRS. Ask which in the interview.

<a id="delta-one-products"></a>

## Delta One Products (futures, TRS, dividend swaps)
<!-- section: delta-one-products | prerequisites: [forward-pricing] | related: [implied-forward-regression, autocallables] | sources: [src-rbc-quantdev-prep] | tags: [delta-one, trs, dividend-swap, repo] -->

**Products moving 1:1 with the underlying:**

- Futures, forwards
- Total return swaps
- ETFs, index arbitrage
- Dividend swaps/futures
- Stock loan/repo

Pricing is mostly **carry**: funding, dividends, borrow.

- **TRS:** one leg pays total return (price + dividends), other pays funding (CORRA/SOFR + spread) → synthetic exposure.
- **Implied dividends / borrow:** back out from futures or put–call parity; the desk marks them. Options and delta-one **must use the same forward** or you get parity breaks.
- Dividend futures hedge the dividend risk left by [[autocallables]] (March 2020: 2020 dividends traded ~55% of model).

### Connections
- **Builds on:** [[forward-pricing]]. **Implied via:** [[implied-forward-regression]].
