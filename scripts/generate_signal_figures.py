#!/usr/bin/env python3
"""Regenerate the synthetic worked example in Signal Evaluation.

Requires numpy and matplotlib. Run from any directory:
    python scripts/generate_signal_figures.py

These finished teaching figures contain no market data or interview material.
The fixed seed is chosen in advance; signals, sizing and costs are not fitted.
"""
from pathlib import Path
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MaxNLocator

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures" / "signal-evaluation"
SEED, WEEKS = 20261014, 520
BLUE, GREY, ORANGE = "#1874ad", "#777777", "#c76525"


def simulate():
    rng = np.random.default_rng(SEED)
    score = rng.normal(size=WEEKS)
    shock = rng.normal(size=WEEKS)
    noise = rng.normal(size=WEEKS)
    # Score is available first; the following week's outcome includes a new shock.
    target = 0.025 * (0.18 * score + np.sqrt(1 - 0.18**2) * shock)

    def backtest(s, cost):
        weight = np.clip(s / 2, -1, 1)
        traded = np.abs(weight - np.r_[0, weight[:-1]])
        gross = weight * target
        net = gross - cost * traded
        # A toy spread sleeve: cost is all-in per unit of spread exposure changed.
        # Initial entry is charged; no separate terminal liquidation is assumed.
        # Financing, borrow, price-driven weight drift and impact are not modelled.
        assert np.all(1 + net > 0)
        value = np.r_[1, np.cumprod(1 + net)]
        drawdown = value / np.maximum.accumulate(value) - 1
        return dict(net=net, value=value, drawdown=drawdown, traded=traded)

    def rank_ic(s):
        # Continuous simulated inputs have no ties.
        return float(np.corrcoef(np.argsort(np.argsort(s)),
                                 np.argsort(np.argsort(target)))[0, 1])

    runs = {"good": backtest(score, .0005), "noise": backtest(noise, .0005),
            "costly": backtest(score, .005), "gross": backtest(score, 0)}
    stats = {key: {"final_value": float(run["value"][-1]),
                   "annualised_return": float(run["value"][-1]**(52 / WEEKS) - 1),
                   "max_drawdown": float(run["drawdown"].min()),
                   "mean_weekly_turnover": float(run["traded"].mean())}
             for key, run in runs.items()}
    stats.update(seed=SEED, weeks=WEEKS, good_rank_ic=rank_ic(score),
                 noise_rank_ic=rank_ic(noise))
    return score, noise, target, runs, stats


def canvas(title, ylabel, xlabel="Years of weekly trading"):
    fig, ax = plt.subplots(figsize=(9, 4.3), layout="constrained")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(axis="y", color="#e5e9ec", linewidth=.7)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 14, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "none",
                         "svg.hashsalt": "signal-evaluation-20261014",
                         "axes.edgecolor": "#b9c2ca", "text.color": "#28323b",
                         "axes.labelcolor": "#28323b", "figure.facecolor": "white"})
    score, noise, target, runs, stats = simulate()
    years = np.arange(WEEKS + 1) / 52

    fig, ax = canvas("Same market, same sizing: three different outcomes",
                     "Capital (initial value = 1)")
    for key, color, style, label in [
        ("good", BLUE, "-", "Predictive / 5 bps"),
        ("noise", GREY, "--", "Noise / 5 bps"),
        ("costly", ORANGE, "-", "Same predictive signal / 50 bps")]:
        ax.plot(years, runs[key]["value"], color=color, ls=style, lw=2,
                label=f"{label}: {stats[key]['final_value']:.2f}")
    ax.axhline(1, color="#b9c2ca", lw=.8)
    ax.legend(frameon=False, fontsize=10)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    save(fig, "equity-curves")

    fig, ax = canvas("Predictive does not mean every forecast is correct",
                     "Next-week target return (%)", "Score known before the next week")
    for values, color, marker, name, metric in [
        (score, BLUE, "o", "Predictive", stats["good_rank_ic"]),
        (noise, GREY, "x", "Noise", stats["noise_rank_ic"])]:
        ax.scatter(values, target * 100, s=13, alpha=.22, color=color,
                   marker=marker, rasterized=True)
        slope, intercept = np.polyfit(values, target * 100, 1)
        xs = np.array([-2.5, 2.5])
        ax.plot(xs, intercept + slope * xs, color=color, lw=2,
                label=f"{name}: Rank IC {metric:+.2f}")
    ax.axhline(0, color="#b9c2ca", lw=.8)
    ax.legend(frameon=False)
    save(fig, "predictive-scatter")

    fig, ax = canvas("Higher scores should correspond to higher average returns",
                     "Mean next-week target return (%)", "Dates sorted into five score groups")
    x = np.arange(5)
    for values, offset, color, name in [(score, -.18, BLUE, "Predictive"),
                                       (noise, .18, GREY, "Noise")]:
        groups = np.array_split(np.argsort(values), 5)
        means = np.array([target[g].mean() for g in groups]) * 100
        se = np.array([target[g].std(ddof=1) / np.sqrt(len(g)) for g in groups]) * 100
        ax.bar(x + offset, means, width=.34, color=color, label=name)
        ax.errorbar(x + offset, means, yerr=1.96 * se, fmt="none",
                    ecolor="#39444c", elinewidth=.8, capsize=3)
    ax.set_xticks(x, ["Q1\nLowest", "Q2", "Q3", "Q4", "Q5\nHighest"])
    ax.axhline(0, color="#65717b", lw=.8)
    ax.legend(frameon=False)
    save(fig, "quantile-returns")

    fig, ax = canvas("A profitable strategy can still spend years below its peak",
                     "Drawdown from the running capital peak")
    for key, color, style, label in [
        ("good", BLUE, "-", "Predictive / 5 bps"),
        ("noise", GREY, "--", "Noise / 5 bps"),
        ("costly", ORANGE, "-", "Same predictive signal / 50 bps")]:
        ax.plot(years, runs[key]["drawdown"], color=color, ls=style, lw=1.7,
                label=f"{label}: worst {stats[key]['max_drawdown']:.1%}")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    ax.legend(frameon=False, loc="lower left", fontsize=10)
    save(fig, "drawdowns")

    fig, ax = canvas("Same predictive score: trading costs consume the edge",
                     "Mean annualised arithmetic return (%)", "All-in cost per unit of exposure traded")
    gross = runs["gross"]["net"].mean() * 52 * 100
    drag = np.array([0, .0005, .005]) * runs["good"]["traded"].mean() * 52 * 100
    ax.bar([0, 1, 2], [gross] * 3, width=.5, color=BLUE, label="Gross mean return")
    ax.bar([0, 1, 2], -drag, bottom=gross, width=.5, color=ORANGE,
           alpha=1, label="Subtract trading costs")
    net = gross - drag
    ax.scatter([0, 1, 2], net, color="#28323b", s=35, zorder=3, label="Net mean return")
    for k, value in enumerate(net):
        ax.annotate(f"Net {value:+.1f}%", (k, value), xytext=(0, -18),
                    textcoords="offset points", ha="center", fontsize=11)
    ax.set_xticks([0, 1, 2], ["0 bps", "5 bps", "50 bps"])
    ax.axhline(0, color="#65717b", lw=.8)
    low, high = min(0, float(net.min())), max(gross, float(net.max()))
    span = high - low
    ax.set_ylim(low - .22 * span, high + .18 * span)
    ax.legend(frameon=False, loc="lower left", fontsize=10)
    save(fig, "cost-drag")
    (OUT / "simulation-results.json").write_text(
        json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote five teaching figures to {OUT}")


if __name__ == "__main__":
    main()
