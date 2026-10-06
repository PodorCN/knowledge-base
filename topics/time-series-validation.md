---
id: time-series-validation
title: "Time Series"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook, src-rbc-gam-quantdev-notes, src-carry-course-notes]
---
# Time Series

Financial data arrive in time order and are serially dependent. This chapter defines stationarity through the AR(1) model, shows how autocorrelation shrinks the effective sample size, and sets out how to validate a model on time-ordered data without leaking future information.

**Prerequisites:** [[variance-covariance-correlation]], [[lln-clt]], [[bias-variance-tradeoff]].

**Leads to:** [[sharpe-ratio]] (annualisation under autocorrelation), [[information-coefficient]], [[backtest-pitfalls]], [[research-workflow]].

**Sections:** [[stationarity-ar1]] · [[effective-sample-size]] · [[cross-validation-leakage]]

<a id="stationarity-ar1"></a>

## Stationarity & AR(1)
<!-- section: stationarity-ar1 | prerequisites: [variance-covariance-correlation] | related: [effective-sample-size, robust-standard-errors, sharpe-ratio, markov-chains] | sources: [src-squarepoint-dqa-workbook] | tags: [time-series, random-walk, spurious-regression] -->

A weakly stationary series has a constant mean, constant finite variance, and autocovariances that depend only on the lag. The AR(1) model is the simplest stationary process — and becomes a non-stationary random walk when its coefficient reaches 1.

### Definition
Weak stationarity: $E[X_t]$ constant, $\mathrm{Var}(X_t)$ finite and constant, $\mathrm{Cov}(X_t,X_{t-k})=\gamma_k$ depends only on the lag $k$.

### Formula
$$X_t=c+\varphi X_{t-1}+\varepsilon_t,\ \ |\varphi|<1:\qquad E[X_t]=\frac{c}{1-\varphi},\qquad \mathrm{Var}(X_t)=\frac{\sigma_\varepsilon^2}{1-\varphi^2},\qquad \rho_k=\varphi^k$$

**Variables:**

- $X_t$ value of the series at time $t$
- $c$ constant
- $\varphi$ AR coefficient
- $\varepsilon_t$ iid innovations with variance $\sigma_\varepsilon^2$
- $\gamma_k$ lag-$k$ autocovariance
- $\rho_k=\gamma_k/\gamma_0$ lag-$k$ autocorrelation

### Key points
- $\varphi=1$: random walk, non-stationary → regressing unrelated price **levels** on each other gives spurious "relationships".
- A stable-looking plot is not proof of stationarity.

### Connections
- **Consequences:** [[effective-sample-size]], [[robust-standard-errors]], Sharpe annualisation in [[sharpe-ratio]].
- **Contrast:** [[markov-chains]] (discrete-state stationarity).

<a id="effective-sample-size"></a>

## Effective Sample Size under Autocorrelation
<!-- section: effective-sample-size | prerequisites: [stationarity-ar1, lln-clt] | related: [sharpe-ratio, regression-invariances, bootstrap, information-coefficient] | sources: [src-squarepoint-dqa-workbook, src-carry-course-notes] | tags: [autocorrelation, standard-error] -->

With positively autocorrelated observations the sample mean is noisier than $\sigma^2/n$ suggests: $n$ correlated observations carry the information of fewer independent ones.

### Formula
$$\mathrm{Var}(\bar X)=\frac{\sigma^2}{n}\Big[1+2\sum_{k=1}^{n-1}\Big(1-\frac kn\Big)\rho_k\Big],\qquad n_{\text{eff}}\approx\frac{n}{1+2\sum_{k\ge1}\rho_k}\ \overset{\text{AR(1)}}{=}\ n\,\frac{1-\varphi}{1+\varphi}$$

**Variables:**

- $\bar X$ sample mean of $n$ observations
- $\sigma^2$ variance of one observation
- $\rho_k$ lag-$k$ autocorrelation
- $n_{\text{eff}}$ effective (independent-equivalent) sample size
- $\varphi$ AR(1) coefficient

### Key points
- $\varphi=0.5$ → $n_{\text{eff}}\approx n/3$. Negative dependence can give $n_{\text{eff}}>n$.
- 1,000 stocks on one date ≠ 1,000 independent observations (a common shock) → cluster or block methods.

### Overlapping forward returns
Sampling more often than the forecast horizon makes consecutive forward windows share days, so one market event (e.g. the 2008 crash) sits inside many "independent" observations at once. The standard correction divides the sample by the overlap ratio:

$$m=\frac{h}{\Delta},\qquad n_{\text{eff}}\approx\frac{n}{m},\qquad \text{shared days between neighbours}=h-\Delta$$

**Variables:**

- $h$ forward horizon in trading days
- $\Delta$ sampling step in trading days ($\Delta=5$ for weekly sampling)
- $m$ overlap ratio: how many sampling steps one forward window spans
- $n$ number of sampled dates
- $n_{\text{eff}}$ effective number of independent observations

**Why $n/m$:** a forward return built from $m$ iid steps has lag-$k$ autocorrelation $\rho_k=1-k/m$ for $k<m$ (and 0 beyond), so $1+2\sum_{k=1}^{m-1}(1-k/m)=m$ in the formula above (exact for integer $m$). **(自己推理)**: this derivation is added to explain the rule; the course notes state the rule only.

**Example:** weekly sampling, $h=21$: $m=21/5=4.2$; neighbouring windows share $21-5=16$ days; 574 weeks → $n_{\text{eff}}\approx574/4.2\approx137$. A naive t-statistic using 574 would be about $\sqrt{4.2}\approx2$ times too large: with a large IC that inflation is the difference between a false discovery and an honest negative. Every t-statistic, backtest Sharpe and "significant" result stands or falls on whether overlap was corrected.

### Connections
- **Builds on:** [[stationarity-ar1]], [[lln-clt]].
- **Applies to:** [[sharpe-ratio]] (autocorrelated returns), [[regression-invariances]] (duplicated rows), [[bootstrap]] (block version), [[information-coefficient]] (t-statistic of an IC with overlapping forwards).

<a id="cross-validation-leakage"></a>

## Validation, Walk-Forward CV & Leakage
<!-- section: cross-validation-leakage | prerequisites: [bias-variance-tradeoff] | related: [backtest-pitfalls, stationarity-ar1, research-workflow, effective-sample-size] | sources: [src-squarepoint-dqa-workbook, src-rbc-gam-quantdev-notes, src-carry-course-notes] | tags: [walk-forward, purging, leakage, point-in-time] -->

Model selection needs data the model has not seen. With time series the split must respect time order, and any use of future information ("leakage") makes the validation meaningless.

### Key points
- **Train** fits parameters; **validation** picks hyper-parameters; **test** is touched once. Re-using the test set turns it into validation.
- Time series: **walk-forward** (train on the past, test on the next window, roll forward). **Purge / gap** overlapping label windows.

### Leakage checklist
- Random splits with overlapping labels.
- Training labels extending into the validation period.
- Standardising or selecting features using future data.
- Revised (not point-in-time) economic data.
- Trading at a close you couldn't have observed before deciding.
- Interpolating a monthly series between month ends: it draws the **next** month end into today. Forward-fill instead (each day inherits the latest known value; it invents no information).

**Code:** aligning a daily series (10-year yield) onto monthly dates point-in-time: union of both calendars → forward-fill (only past values flow forward) → keep the target dates.

```python
y10 = ten_year.reindex(div_yield.index.union(ten_year.index)).ffill().reindex(div_yield.index)
```

### Clean train/test boundary with overlapping forwards
A sample date belongs to the earlier (selection) window only if its **entire** forward window ends before the boundary; dates whose forward window straddles the boundary belong to **neither** side. A forward return spanning the boundary cannot be attributed to either regime, and assigning it to one side leaks the other side's information. Every layer (signal calibration, tests) uses the same rule, so all are graded on the same dates. In code the evaluation sample is the intersection with the selection weeks, after dropping dates before the score has history:

```python
df = pd.DataFrame({"z": z.reindex(weeks_all), "fwd": fwd.reindex(weeks_all)}).dropna()
df = df[df["z"] != 0]                         # before the signal has history
df = df.loc[df.index.intersection(sel)]       # sel = weeks whose forward window ends before SELECT_END
```
 Data after the boundary is not loaded at all until its round ("sealed"), not even for a quick look or debugging.

### Point-in-time join (no look-ahead)
Join each price date to the latest fundamental record that was already **available** on that date:

```python
merged = pd.merge_asof(prices.sort_values("date"), fund.sort_values("available_date"),
                       left_on="date", right_on="available_date", by="ticker", direction="backward")
```

### Connections
- **Builds on:** [[bias-variance-tradeoff]].
- **Main cause of:** [[backtest-pitfalls]]. **Part of:** [[research-workflow]].
