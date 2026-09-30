---
id: structured-products-delta-one
title: "Structured Products"
type: topic
domain: pricing
sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep]
---
# Structured Products

Structured notes are packages of a bond and options sold to investors; delta-one products are the linear instruments dealers use to fund and hedge them. This chapter starts with delta-one (pure carry), builds up the note families from simple to complex — principal-protected notes, reverse convertibles, worst-of payoffs — culminating in the autocallable case study, and ends with swaptions, the rates option embedded in callable notes.

**Prerequisites:** [[forward-pricing]], [[static-replication]], [[digital-options]], [[barrier-options]], [[portfolio-variance-diversification]], [[black-76]].

**Leads to:** [[model-risk-governance]] (reserves), [[pricing-app-architecture]] (product features).

**Sections:** [[delta-one-products]] · [[principal-protected-note]] · [[reverse-convertible]] · [[worst-of-correlation]] · [[autocallables]] · [[swaptions]]

<a id="delta-one-products"></a>

## Delta One Products (futures, TRS, dividend swaps)
<!-- section: delta-one-products | prerequisites: [forward-pricing] | related: [implied-forward-regression, autocallables, relative-value-long-short] | sources: [src-rbc-quantdev-prep] | tags: [delta-one, trs, dividend-swap, repo] -->

Delta-one products move one-for-one with the underlying. Pricing them is mostly **carry**: funding, dividends and borrow.

### Definitions
Products moving 1:1 with the underlying:

- Futures, forwards
- Total return swaps (TRS)
- ETFs, index arbitrage
- Dividend swaps / futures
- Stock loan / repo

### Key points
- **TRS:** one leg pays the total return (price + dividends), the other pays funding (CORRA/SOFR + spread) → synthetic exposure.
- **Implied dividends / borrow:** backed out from futures or put–call parity; the desk marks them ([[implied-forward-regression]]). Options and delta-one **must use the same forward**, or parity breaks.
- Dividend futures hedge the dividend risk left by [[autocallables]] (March 2020: 2020 dividends traded at ~55% of model).

### Connections
- **Builds on:** [[forward-pricing]]. **Implied via:** [[implied-forward-regression]].
- **Execution leg of:** [[relative-value-long-short]].

<a id="principal-protected-note"></a>

## Principal-Protected Note (PPN)
<!-- section: principal-protected-note | prerequisites: [static-replication, discounting-compounding] | related: [reverse-convertible, digital-options] | sources: [src-rbc-quantdev-prep] | tags: [structured-notes, participation-rate] -->

**PPN = zero-coupon bond (guarantees the principal) + call (or call spread) on the index.** What is left of the note price after buying the bond is spent on the option.

### Formula
$$\text{Participation}=\frac{\text{Note price}-\text{ZCB price}}{\text{Option price}}$$

**Variables:**

- $\text{Participation}$ share of the index upside the investor receives
- $\text{Note price}$ issue price of the note
- $\text{ZCB price}$ price of the zero-coupon bond that returns the principal ([[discounting-compounding]])
- $\text{Option price}$ price of the call (or call spread) per unit of participation

### Key points
- Higher rates → cheaper ZCB → more budget → **higher** participation.
- Higher vol → dearer option → **lower** participation.
- The same "budget buys payoff" logic as the digital payout ratio $\mathcal Q$ in [[digital-options]].

### Connections
- **Builds on:** [[static-replication]]. **Sibling:** [[reverse-convertible]].

<a id="reverse-convertible"></a>

## Reverse Convertible
<!-- section: reverse-convertible | prerequisites: [barrier-options] | related: [autocallables, principal-protected-note, worst-of-correlation] | sources: [src-rbc-quantdev-prep] | tags: [structured-notes, yield-enhancement] -->

**Reverse convertible = bond + short (down-and-in) put.** The investor sells downside protection and is paid through an enhanced coupon.

### Key points
- The investor sells the put and receives an enhanced coupon.
- Adding early-redemption digitals and contingent-coupon digitals turns it into an autocallable ([[autocallables]]).

### Connections
- **Builds on:** [[barrier-options]]. **Contrast:** [[principal-protected-note]] (investor buys the option instead of selling it).

<a id="worst-of-correlation"></a>

## Worst-of Payoffs & Correlation Risk
<!-- section: worst-of-correlation | prerequisites: [portfolio-variance-diversification, barrier-options] | related: [autocallables, reverse-convertible, digital-options, quanto-options] | sources: [src-rbc-quantdev-prep, src-vol-surface-exotics-notes] | tags: [worst-of, correlation, dispersion] -->

A worst-of payoff depends on the worst performer in a basket, so its value depends on correlation: lower correlation means more dispersion and a lower worst performer.

### Key points
- The investor **sells** the desk a worst-of down-and-in put and **receives** worst-of coupon/autocall digitals.
- **Lower correlation** → more dispersion → the worst is lower → the put is worth **more** and the digitals **less** → low-correlation baskets pay higher headline coupons.
- The desk is long the put and short the digitals; both lose value as ρ rises ⇒ the **desk is short correlation** ("The dealer, conversely, is short correlation" — Risk.net). It was hurt in Q1 2020 when markets moved in unison. (The long-put/short-digital breakdown is 自己推理; the direction matches the sources.)
- Example: correlations −0.1 → note −2.94 per 1,000; a single index instead of the worst-of → 1026.3 (the worst-of is cheaper, which funds the coupon).

### Connections
- **Diversification maths:** [[portfolio-variance-diversification]]. **Products:** [[autocallables]], [[reverse-convertible]].

<a id="autocallables"></a>

## Autocallables (worst-of, RBC case study)
<!-- section: autocallables | prerequisites: [digital-options, barrier-options, worst-of-correlation, reverse-convertible] | related: [local-stochastic-volatility, monte-carlo-pricing, delta-one-products, volatility-skew, model-risk-governance] | sources: [src-vol-surface-exotics-notes, src-rbc-quantdev-prep] | tags: [autocallable, structured-notes, dividends, rbc] -->

An autocallable combines everything in this chapter: a bond, a short down-and-in put, and digitals for the coupons and for early redemption, usually on the worst of several indices. Its price depends on skew, correlation, dividends and funding, and it is valued by Monte Carlo under LSV.

### Structure
- A coupon (often contingent, with memory).
- **Early redemption** if the (worst-of) underlying ≥ the autocall level on an observation date.
- At maturity, if below the knock-in barrier, the investor takes the equity loss.

**Decomposition:** bond + short down-and-in put + autocall digitals + coupon digitals ([[reverse-convertible]], [[digital-options]], [[barrier-options]]).

### RBC 424B2 case (public facts)
DJIA / Nasdaq-100 / S&P 500 worst-of, 3y (Feb 2029); monthly contingent coupon of 6.25 per 1,000 (7.5% p.a.) if all ≥ 60%; monthly autocall from Feb 2027 if all ≥ 100%; principal loss if the worst < 60% at maturity. Estimated value 937.50–987.50 per 1,000; underwriting 0.15%.

### Desk workflow (inferred)
Mark surfaces → calibrate LSV per underlier, mark correlations, imply dividends → MC in C++ (Greeks by AAD/bumps) → reserves (model, barrier & digital overhedges, correlation, dividends), verify vs consensus → hedge Δ with futures, vega with vanillas, dividends with dividend futures → recycle correlation / long-dated vol → discount at the internal funding rate.

### Worked example: MC results (the source's assumptions, not RBC's)

| per 1,000 | Flat ATM vols | Downside vols +6 pts |
|---|---|---|
| Note value | 1007.7 | 958.5 |
| P(autocall) | 67.8% | 64.3% |
| P(principal loss) | 8.3% | 16.5% |

A flat vol values the note **above par** — wrong: the investor is short a deep OTM put priced in the steep skew ([[volatility-skew]]).

### Sensitivities → what the issuer holds
Vols +1 pt: −7.45 (the issuer is long vol); correlation −0.1: −2.94; dividends +0.5%: −2.80 (the issuer is long dividends); discounting at $r$ instead of $r$ + 60 bp: +10.10.

After Δ-hedging, issuers are **short delta, long vol, long dividends, short correlation**, with awkward gamma near barriers/triggers. March 2020: 2020 dividends traded at ~55% of model and 2021 at ~70% → big losses on dividend hedges.

### Why the estimated value < 1,000
The issue price covers underwriting, hedging cost and structuring margin; the estimated value uses the internal funding rate and mid hedge terms.

### Connections
- **Components:** [[digital-options]], [[barrier-options]], [[worst-of-correlation]]. **Model:** [[local-stochastic-volatility]] + [[monte-carlo-pricing]].
- **Dividend hedge:** [[delta-one-products]]. **Reserves:** [[model-risk-governance]].

<a id="swaptions"></a>

## Swaptions (and why an equity desk cares)
<!-- section: swaptions | prerequisites: [black-76] | related: [sabr, autocallables] | sources: [src-rbc-quantdev-prep] | tags: [swaption, callable-notes, rates] -->

A payer swaption is an option to enter a swap paying a fixed rate. It is priced with Black-76 on the forward swap rate, with the annuity playing the role of the discount factor.

### Formula
$$PS=A\,\big[F\,N(d_1)-K\,N(d_2)\big],\qquad A=\sum_i\tau_i\,P(0,t_i)$$

**Variables:**

- $PS$ payer swaption price
- $A$ annuity (PV01)
- $F$ forward swap rate
- $K$ strike rate
- $d_1,d_2$ as in [[black-76]], with $\sigma$ the Black vol and $T$ the option expiry
- $\tau_i$ accrual fractions of the swap's fixed leg
- $P(0,t_i)$ discount factors to the payment dates $t_i$

### Key points
- Rates desks quote **normal (Bachelier) vol** because rates can be negative → [[sabr]].
- **Equity desk link (自己推理):** issuer-callable structured notes embed a **Bermudan receiver swaption** owned by the issuer, hedged with rates; long-dated equity products carry rho / equity–rates correlation. Or "equity swaptions" = options on a TRS. Ask which is meant in the interview.

### Connections
- **Builds on:** [[black-76]]. **Smile model:** [[sabr]].
