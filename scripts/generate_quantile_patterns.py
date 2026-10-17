#!/usr/bin/env python3
"""Regenerate the quantile-shape small multiples in Signal Evaluation (Check 4).

Requires matplotlib. Run from any directory:
    python scripts/generate_quantile_patterns.py

Stylised shapes, except the hump panel, which plots the stock-bond carry
Select-period quintile means reported in the case study.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "figures" / "signal-evaluation"
BLUE, ORANGE, INK, RULE = "#1874ad", "#c76525", "#28323b", "#b9c2ca"

PATTERNS = [
    ("1. Monotonic staircase", "linear sizing fits", [-1, -.5, 0, .5, 1], []),
    ("2. Flat / noisy", "no skill: stop", [.1, -.15, .05, -.05, .1], []),
    ("3. Inverted staircase", "sign is backwards", [1, .5, 0, -.5, -1], [0, 4]),
    ("4. Hump (carry Select, actual %)", "extremes fail", [-.26, .73, 1.32, .63, -.09], [4]),
    ("5. One tail only", "only Q1 informative", [-1.2, 0, .05, 0, .1], []),
    ("6. Extremes only", "information at the tails", [-1, 0, 0, 0, 1], []),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.spines.left": False, "svg.fonttype": "none",
                         "svg.hashsalt": "quantile-patterns-20261017",
                         "axes.edgecolor": RULE, "text.color": INK,
                         "axes.labelcolor": INK, "figure.facecolor": "white"})
    fig, axes = plt.subplots(2, 3, figsize=(9, 5.2), layout="constrained")
    fig.suptitle("Mean forward return by score quintile: six shapes and what they say",
                 fontsize=13, color=INK)
    for ax, (title, note, values, flagged) in zip(axes.flat, PATTERNS):
        colors = [ORANGE if q in flagged else BLUE for q in range(5)]
        ax.bar(range(5), values, width=.7, color=colors)
        ax.axhline(0, color="#65717b", lw=.8)
        ax.set_title(f"{title}\n{note}", fontsize=10, loc="left", color=INK, linespacing=1.4)
        ax.set_xticks(range(5), ["Q1", "Q2", "Q3", "Q4", "Q5"])
        ax.set_yticks([])
        top = max(abs(v) for v in values) * 1.35
        ax.set_ylim(-top, top)
    fig.text(.5, -.01, "Q1 = lowest score, Q5 = highest score. Orange = the bucket where linear "
             "sizing puts its largest bet in the wrong direction.", ha="center", fontsize=9, color="#5b6670")
    fig.savefig(OUT / "quantile-patterns.svg", metadata={"Date": None}, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT / 'quantile-patterns.svg'}")


if __name__ == "__main__":
    main()
