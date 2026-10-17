#!/usr/bin/env python3
"""Regenerate the t-statistic figures in Signal Evaluation (Check 2).

Requires numpy, scipy and matplotlib. Run from any directory:
    python scripts/generate_significance_figures.py

Teaching figures only: no market data, fixed seed chosen in advance.
"""
from pathlib import Path
import json

import numpy as np
from scipy import stats
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures" / "signal-evaluation"
SEED = 20261017
BLUE, GREY, ORANGE, INK, RULE = "#1874ad", "#777777", "#c76525", "#28323b", "#b9c2ca"

# Carry-study geometry: 574 weekly dates, 21-day forward returns, 5-day step.
N_WEEKS, H, STEP = 574, 21, 5
M = H / STEP
N_EFF = N_WEEKS / M
HURDLES = (1.5, 2.0, 3.0)


def canvas(title, ylabel, xlabel):
    fig, ax = plt.subplots(figsize=(9, 4.3), layout="constrained")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(axis="y", color="#e5e9ec", linewidth=.7)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", metadata={"Date": None})
    plt.close(fig)


def hurdle_figure(results):
    """Null vs alternative sampling distribution of t, cut at the hurdle."""
    ic_true, hurdle = 0.15, 1.5
    shift = ic_true * np.sqrt(N_EFF - 2)
    x = np.linspace(-3.5, 5.5, 600)
    null, alt = stats.norm.pdf(x), stats.norm.pdf(x, loc=shift)
    false_pos = stats.norm.sf(hurdle)
    power = stats.norm.sf(hurdle - shift)
    results["hurdle_figure"] = dict(ic_true=ic_true, n_eff=N_EFF, mean_t_alt=shift,
                                    false_positive=false_pos, power=power)

    fig, ax = canvas("A t-hurdle splits pass from fail: false positives vs missed signals",
                     "Probability density", "t-statistic of the sample IC")
    ax.plot(x, null, color=GREY, ls="--", lw=2)
    ax.plot(x, alt, color=BLUE, lw=2)
    tail = x >= hurdle
    ax.fill_between(x[tail], null[tail], color=GREY, alpha=.35, hatch="//", lw=0)
    ax.fill_between(x[tail], alt[tail], color=BLUE, alpha=.18, lw=0)
    ax.axvline(hurdle, color=ORANGE, lw=2)
    for h in HURDLES[1:]:
        ax.axvline(h, color=ORANGE, lw=1, ls=":")
        ax.annotate(f"t* = {h:.1f}", (h, .445), xytext=(3, 0), textcoords="offset points",
                    color=INK, fontsize=10)
    ax.annotate(f"hurdle t* = {hurdle}", (hurdle, .445), xytext=(-3, 0), ha="right",
                textcoords="offset points", color=INK, fontsize=10, weight="bold")
    ax.annotate("Noise signal (true IC = 0)", (-0.2, stats.norm.pdf(-0.2)), xytext=(-150, 8),
                textcoords="offset points", color=INK, fontsize=10)
    ax.annotate(f"Real signal (true IC = {ic_true:.2f})", (shift + .6, stats.norm.pdf(.6)),
                xytext=(14, 4), textcoords="offset points", color=INK, fontsize=10)
    ax.annotate(f"False-positive rate {false_pos:.1%}\n(noise that passes)", (2.0, .03),
                xytext=(18, 40), textcoords="offset points", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=.8))
    ax.annotate(f"Power {power:.0%}\n(real signal that passes)", (2.6, .2),
                xytext=(40, 20), textcoords="offset points", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=.8))
    ax.set_ylim(0, .47)
    ax.set_xlim(-3.5, 5.5)
    save(fig, "t-hurdle")


def overlap_figure(results):
    """Pure-noise persistent score vs overlapping 21-day forward returns."""
    rng = np.random.default_rng(SEED)
    sims, phi = 4000, 0.95
    days = N_WEEKS * STEP + H
    naive, adjusted = np.empty(sims), np.empty(sims)
    starts = np.arange(N_WEEKS) * STEP
    for k in range(sims):
        daily = rng.normal(size=days)
        csum = np.r_[0, np.cumsum(daily)]
        fwd = csum[starts + H] - csum[starts]          # 21-day forward return from each week
        eps = rng.normal(size=N_WEEKS)
        score = np.empty(N_WEEKS)
        score[0] = eps[0] / np.sqrt(1 - phi**2)
        for t in range(1, N_WEEKS):                    # weekly AR(1) score, independent of returns
            score[t] = phi * score[t - 1] + eps[t]
        ic = np.corrcoef(score, fwd)[0, 1]
        naive[k] = ic * np.sqrt(N_WEEKS - 2)
        adjusted[k] = ic * np.sqrt(N_EFF - 2)
    results["overlap_figure"] = dict(
        sims=sims, score_phi=phi, n=N_WEEKS, m=M, n_eff=N_EFF,
        sd_naive_t=float(naive.std()), sd_adjusted_t=float(adjusted.std()),
        pass_naive_1_5=float((naive >= 1.5).mean()), pass_adjusted_1_5=float((adjusted >= 1.5).mean()),
        pass_naive_abs2=float((np.abs(naive) >= 2).mean()),
        pass_adjusted_abs2=float((np.abs(adjusted) >= 2).mean()))
    r = results["overlap_figure"]

    fig, ax = canvas("Pure noise looks significant when overlapping windows are counted as independent",
                     "Density", "t-statistic of the sample IC")
    bins = np.linspace(-7, 7, 57)
    ax.hist(naive, bins=bins, color=ORANGE, alpha=.55, density=True)
    ax.hist(adjusted, bins=bins, color=BLUE, alpha=.55, density=True)
    x = np.linspace(-7, 7, 400)
    ax.plot(x, stats.norm.pdf(x), color=GREY, ls="--", lw=1.6)
    ax.axvline(1.5, color=INK, lw=1, ls=":")
    ax.annotate("hurdle 1.5", (1.5, .36), xytext=(4, 0), textcoords="offset points",
                color=INK, fontsize=10)
    ax.annotate(f"Adjusted, n_eff = {N_EFF:.0f}: sd {r['sd_adjusted_t']:.2f},\n"
                f"{r['pass_adjusted_1_5']:.0%} of noise passes t ≥ 1.5",
                (-1.0, .30), xytext=(-215, 0), textcoords="offset points", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=.8))
    ax.annotate(f"Naive, n = {N_WEEKS}: sd {r['sd_naive_t']:.2f},\n"
                f"{r['pass_naive_1_5']:.0%} of noise passes t ≥ 1.5",
                (3.6, .045), xytext=(30, 45), textcoords="offset points", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=.8))
    ax.annotate("N(0,1): what a correct t\nlooks like under noise", (-2.3, stats.norm.pdf(-2.3)),
                xytext=(-150, 30), textcoords="offset points", color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=.8))
    ax.set_xlim(-7, 7)
    save(fig, "overlap-t-inflation")


def min_ic_figure(results):
    """Minimum sample IC needed to clear each hurdle, by effective sample size."""
    n = np.geomspace(30, 3000, 300)
    fig, ax = canvas("The smaller the effective sample, the larger the IC needed to pass",
                     "Minimum |IC| to clear the hurdle", "Effective sample size n_eff (log scale)")
    styles = {1.5: ("-", 2.2), 2.0: ("--", 1.8), 3.0: (":", 1.8)}
    for h in HURDLES:
        ls, lw = styles[h]
        ic_min = h / np.sqrt(n - 2)
        ax.plot(n, ic_min, color=BLUE, ls=ls, lw=lw)
        ax.annotate(f"t* = {h:.1f}", (40, h / np.sqrt(38)), xytext=(4, 6),
                    textcoords="offset points", color=INK, fontsize=10)
    need = 1.5 / np.sqrt(N_EFF - 2)
    for ic, label in [(0.0252, "Carry, baseline IC 0.025"), (0.0423, "Carry, unadjusted-close IC 0.042")]:
        ax.scatter([N_EFF], [ic], color=ORANGE, s=45, zorder=3)
        ax.annotate(label, (N_EFF, ic), xytext=(10, -4 if ic < .03 else 4),
                    textcoords="offset points", color=INK, fontsize=10)
    ax.scatter([N_EFF], [need], color=INK, s=30, zorder=3, marker="D")
    ax.annotate(f"needed at n_eff ≈ {N_EFF:.0f}: IC ≥ {need:.3f}", (N_EFF, need),
                xytext=(-10, -20), ha="right", textcoords="offset points", color=INK, fontsize=10)
    ax.set_xscale("log")
    ax.set_xticks([30, 100, 300, 1000, 3000], ["30", "100", "300", "1,000", "3,000"])
    ax.set_xlim(30, 3000)
    ax.set_ylim(0, .6)
    results["min_ic_figure"] = dict(n_eff=N_EFF, ic_min={str(h): h / np.sqrt(N_EFF - 2) for h in HURDLES})
    save(fig, "min-ic-vs-neff")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 13, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "none",
                         "svg.hashsalt": "signal-significance-20261017",
                         "axes.edgecolor": RULE, "text.color": INK, "hatch.color": GREY,
                         "axes.labelcolor": INK, "figure.facecolor": "white"})
    results = {"seed": SEED}
    hurdle_figure(results)
    overlap_figure(results)
    min_ic_figure(results)
    (OUT / "significance-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
