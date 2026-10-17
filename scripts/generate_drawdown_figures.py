#!/usr/bin/env python3
"""Regenerate the drawdown figures in Signal Evaluation (Check 5).

Requires numpy and matplotlib. Run from any directory:
    python scripts/generate_drawdown_figures.py

Figure 1 reuses the predictive 5 bps strategy from generate_signal_figures.py.
Figure 2 is a Monte Carlo of maximum drawdown for strategies of known Sharpe
ratio with the same volatility (iid normal weekly returns, fixed seed).
"""
from pathlib import Path
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MaxNLocator

import generate_signal_figures as base

OUT = base.OUT
SEED, SIMS, WEEKS = 20261019, 4000, 520
BLUE, ORANGE, PURPLE, CRIMSON, GREY, INK = "#1874ad", "#c76525", "#7a5aa6", "#b8325a", "#777777", "#28323b"


def episode(value):
    """Peak, trough and recovery week of the maximum drawdown."""
    peak_curve = np.maximum.accumulate(value)
    dd = value / peak_curve - 1
    trough = int(dd.argmin())
    peak = int(np.argmax(value[:trough + 1]))
    after = np.nonzero(value[trough:] >= value[peak])[0]
    recovery = int(trough + after[0]) if len(after) else None
    return peak_curve, dd, peak, trough, recovery


def anatomy_figure(results):
    _, _, _, runs, _ = base.simulate()
    value = runs["good"]["value"]
    hwm, dd, peak, trough, recovery = episode(value)
    years = np.arange(len(value)) / 52
    results["anatomy"] = dict(peak_week=peak, trough_week=trough, recovery_week=recovery,
                              max_drawdown=float(dd.min()), peak_value=float(value[peak]),
                              trough_value=float(value[trough]),
                              fall_weeks=trough - peak,
                              recover_weeks=None if recovery is None else recovery - trough)

    fig, (top, bot) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained",
                                   height_ratios=[1.6, 1])
    fig.suptitle("Where a drawdown comes from: the gap between capital and its running peak",
                 fontsize=13, color=INK)
    top.plot(years, hwm, color=GREY, ls="--", lw=1.6, label="Running peak (high-water mark)")
    top.plot(years, value, color=BLUE, lw=2, label="Capital V_t (predictive signal, 5 bps)")
    top.fill_between(years, value, hwm, where=value < hwm, color=BLUE, alpha=.15, lw=0)
    for wk, name, dy in [(peak, "peak", 14), (trough, "trough", -22)]:
        top.scatter(years[wk], value[wk], color=INK, s=28, zorder=3)
        top.annotate(f"{name} {value[wk]:.2f}", (years[wk], value[wk]), xytext=(-6, dy),
                     textcoords="offset points", ha="right", fontsize=10, color=INK)
    if recovery is not None:
        top.scatter(years[recovery], value[recovery], color=INK, s=28, zorder=3)
        top.annotate("back to peak", (years[recovery], value[recovery]), xytext=(6, -16),
                     textcoords="offset points", fontsize=10, color=INK)
    top.set_ylabel("Capital (start = 1)")
    top.legend(frameon=False, fontsize=9.5, loc="upper left")
    top.grid(axis="y", color="#e5e9ec", lw=.7)

    bot.fill_between(years, dd, 0, color=BLUE, alpha=.25, lw=0)
    bot.plot(years, dd, color=BLUE, lw=1.4)
    bot.axhline(0, color="#65717b", lw=.8)
    end = recovery if recovery is not None else len(value) - 1
    y_bar = dd.min() * 1.18
    bot.annotate("", (years[peak], y_bar), (years[end], y_bar),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    bot.text((years[peak] + years[end]) / 2, y_bar * 1.06,
             f"underwater {(end - peak) / 52:.1f} yrs", ha="center", va="top", fontsize=10, color=INK)
    bot.annotate(f"Max DD {dd.min():.0%}", (years[trough], dd.min()), xytext=(-8, 0),
                 textcoords="offset points", ha="right", va="center", fontsize=10, color=INK)
    bot.set_ylim(dd.min() * 1.45, 0.02)
    bot.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    bot.set_ylabel("DD_t")
    bot.set_xlabel("Years of weekly trading")
    bot.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    bot.grid(axis="y", color="#e5e9ec", lw=.7)
    fig.savefig(OUT / "drawdown-anatomy.svg", metadata={"Date": None})
    plt.close(fig)
    return float(runs["good"]["net"].std() * np.sqrt(52)), float(dd.min())


def expected_dd_figure(results, vol, observed):
    rng = np.random.default_rng(SEED)
    sharpes = [(0.25, PURPLE, ":"), (0.5, ORANGE, "--"), (1.0, BLUE, "-"), (1.5, CRIMSON, "-.")]
    grid = np.linspace(0, .6, 301)
    fig, ax = plt.subplots(figsize=(9, 4.6), layout="constrained")
    ax.set(title=f"How deep should a 10-year drawdown be? Monte Carlo, {vol:.1%} annual volatility",
           xlabel="Maximum drawdown over 10 years (worse to the right)",
           ylabel="Probability of a drawdown at least this deep")
    results["expected_dd"] = dict(vol=vol, sims=SIMS, weeks=WEEKS, seed=SEED, observed=observed, by_sharpe={})
    for sr, color, ls in sharpes:
        mu, sd = sr * vol / 52, vol / np.sqrt(52)
        r = rng.normal(mu, sd, size=(SIMS, WEEKS))
        v = np.cumprod(1 + r, axis=1)
        v = np.concatenate([np.ones((SIMS, 1)), v], axis=1)
        mdd = -(v / np.maximum.accumulate(v, axis=1) - 1).min(axis=1)
        exceed = (mdd[None, :] >= grid[:, None]).mean(axis=1)
        ax.plot(grid, exceed, color=color, ls=ls, lw=2,
                label=f"Sharpe {sr}: median {np.median(mdd):.0%}, 1-in-10 worse than {np.quantile(mdd, .9):.0%}")
        results["expected_dd"]["by_sharpe"][str(sr)] = dict(
            median=float(np.median(mdd)), p90=float(np.quantile(mdd, .9)),
            p_worse_than_observed=float((mdd >= -observed).mean()),
            p_at_least_10pct=float((mdd >= .10).mean()))
    ax.axvline(-observed, color=INK, lw=1, ls=":")
    ax.annotate(f"predictive signal's\nactual Max DD {observed:.0%}", (-observed, .93), xytext=(6, 0),
                textcoords="offset points", fontsize=10, color=INK, va="top")
    ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.grid(color="#e5e9ec", lw=.7)
    ax.set_xlim(0, .6)
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    fig.savefig(OUT / "expected-max-drawdown.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 13,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "svg.hashsalt": "drawdown-figures-20261019",
                         "axes.edgecolor": "#b9c2ca", "text.color": INK,
                         "axes.labelcolor": INK, "figure.facecolor": "white"})
    results = {}
    vol, observed = anatomy_figure(results)
    expected_dd_figure(results, vol, observed)
    (OUT / "drawdown-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
