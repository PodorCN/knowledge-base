#!/usr/bin/env python3
"""Regenerate the timing-curve and underwater figures in Signal Metrics.

Requires numpy and matplotlib. Run from any directory:
    python scripts/generate_timing_figures.py

Teaching figures only: one simulated weekly spread market with a fixed seed;
signal strength and crash sizes are illustrative choices. The carry-like sleeve's drift is set so its final value matches
the skilled signal's, to show two equal-return paths.
"""
from pathlib import Path
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter, NullFormatter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures" / "signal-metrics"
SEED, WEEKS, H = 20261018, 520, 4
BLUE, ORANGE, PURPLE, CRIMSON, GREY, INK = "#1874ad", "#c76525", "#7a5aa6", "#b8325a", "#777777", "#28323b"


def simulate():
    rng = np.random.default_rng(SEED)
    r = 0.0005 + 0.02 * rng.standard_t(5, size=WEEKS + H) / np.sqrt(5 / 3)   # weekly spread return
    fwd = np.array([r[t + 1:t + 1 + H].sum() for t in range(WEEKS)])          # 4-week forward label
    nxt = r[1:WEEKS + 1]                                                       # next-week return
    skill = 0.16 * fwd / fwd.std() + np.sqrt(1 - 0.16**2) * rng.normal(size=WEEKS)
    w_skill = np.clip(np.clip(skill, -2, 2) / 2, -1, 1)
    w_noise = np.clip(np.clip(rng.normal(size=WEEKS), -2, 2) / 2, -1, 1)

    def curve(ret):
        v = np.r_[1.0, np.cumprod(1 + ret)]
        return v, v / np.maximum.accumulate(v) - 1

    lines = {
        "hold": nxt * 1.0,                    # always +1 on the spread
        "skill": w_skill * nxt,
        "noise": w_noise * nxt,
        "bug": w_skill * fwd,                 # WRONG: compounds overlapping 4-week labels weekly
    }
    # Carry-like sleeve: steady small gains plus three sharp crash episodes.
    crash = np.zeros(WEEKS)
    for start, depth, weeks in [(110, -.16, 4), (290, -.24, 6), (440, -.12, 3)]:
        crash[start:start + weeks] = depth / weeks
    base = 0.0025 * rng.normal(size=WEEKS) + crash
    target = np.log(curve(lines["skill"])[0][-1])
    lo, hi = 0.0, 0.01
    for _ in range(60):                       # bisection on drift so final values match
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if np.log(curve(base + mid)[0][-1]) < target else (lo, mid)
    lines["carry"] = base + (lo + hi) / 2

    stats = {}
    curves = {}
    for k, ret in lines.items():
        v, dd = curve(ret)
        under = np.r_[dd < 0, False]
        runs, n = [], 0
        for u in under:
            n = n + 1 if u else (runs.append(n) or 0)
        curves[k] = (v, dd)
        stats[k] = dict(final_value=float(v[-1]), annualised_return=float(v[-1] ** (52 / WEEKS) - 1),
                        max_drawdown=float(dd.min()), longest_underwater_weeks=int(max(runs)),
                        annualised_vol=float(ret.std() * np.sqrt(52)))
    stats["skill_rank_ic_vs_fwd"] = float(np.corrcoef(np.argsort(np.argsort(skill)),
                                                      np.argsort(np.argsort(fwd)))[0, 1])
    return curves, stats


def canvas(title, ylabel, height=4.6):
    fig, ax = plt.subplots(figsize=(9, height), layout="constrained")
    ax.set(title=title, xlabel="Years of weekly rebalancing", ylabel=ylabel)
    ax.grid(axis="y", color="#e5e9ec", linewidth=.7)
    ax.set_axisbelow(True)
    return fig, ax


STYLE = {
    "skill": (BLUE, "-", 2.2, "Skilled signal"),
    "carry": (ORANGE, "-", 2.0, "Carry-like (same final value)"),
    "hold": (GREY, "--", 1.6, "Buy and hold the spread"),
    "noise": (PURPLE, ":", 2.0, "Noise signal"),
    "bug": (CRIMSON, "-.", 1.8, "Bug: overlapping 4-week returns"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 13,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "svg.hashsalt": "timing-curves-20261018",
                         "axes.edgecolor": "#b9c2ca", "text.color": INK,
                         "axes.labelcolor": INK, "figure.facecolor": "white"})
    curves, stats = simulate()
    years = np.arange(WEEKS + 1) / 52

    fig, ax = canvas("Timing curves V_t: same market, five ways to trade it (log scale)",
                     "Capital, starting at 1 (log scale)")
    for k in ["bug", "skill", "carry", "hold", "noise"]:
        color, ls, lw, label = STYLE[k]
        s = stats[k]
        ax.plot(years, curves[k][0], color=color, ls=ls, lw=lw,
                label=f"{label}: {s['annualised_return']:+.1%}/yr")
    ax.set_yscale("log")
    ax.set_yticks([0.8, 1, 1.25, 1.5, 2, 2.5, 3])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.axhline(1, color="#b9c2ca", lw=.8)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.set_xlim(0, WEEKS / 52)
    fig.savefig(OUT / "timing-curves.svg", metadata={"Date": None})
    plt.close(fig)

    fig, ax = canvas("Underwater curves DD_t: how deep and how long below the last peak",
                     "Drawdown from running peak", height=5.2)
    for k in ["hold", "noise", "carry", "skill"]:
        color, ls, lw, label = STYLE[k]
        s = stats[k]
        ax.plot(years, curves[k][1], color=color, ls=ls, lw=lw,
                label=f"{label}: max {s['max_drawdown']:.0%}, "
                      f"longest {s['longest_underwater_weeks'] / 52:.1f} yrs under")
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.axhline(0, color="#65717b", lw=.8)
    fig.legend(frameon=False, fontsize=9.5, loc="outside lower center", ncol=2)
    ax.set_xlim(0, WEEKS / 52)
    fig.savefig(OUT / "underwater-curves.svg", metadata={"Date": None})
    plt.close(fig)

    stats["seed"] = SEED
    (OUT / "timing-results.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
