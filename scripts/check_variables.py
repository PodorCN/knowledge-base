#!/usr/bin/env python3
"""Flag formula symbols that no **Variables:** list explains.

Advisory lint for the course-notes standard (AGENTS.md section 3): every symbol
in a display formula must appear in the section's variable list. Heuristic, so
it can report false positives; read each hit before acting on it.

  python3 scripts/check_variables.py                      # all chapters
  python3 scripts/check_variables.py topics/foo.md ...    # selected chapters
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GREEK = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta", "vartheta",
    "kappa", "lambda", "mu", "nu", "xi", "rho", "sigma", "tau", "phi", "varphi", "chi", "psi",
    "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
}
# Letters that are almost always notation rather than variables.
IGNORE = {"d", "e", "i", "E", "P", "N"}
# Commands whose argument is a word/operator, not a symbol.
WORD_CMDS = r"\\(?:text|mathrm|operatorname|textbf|mathbf|mathbb|mathcal|qquad|quad|left|right|big|Big|bigg|Bigg)"


def symbols(tex: str) -> set[str]:
    tex = re.sub(WORD_CMDS + r"\{[^{}]*\}", " ", tex)
    tex = re.sub(r"_\{[^{}]*\}|_\\?\w", " ", tex)  # drop subscripts: base symbol is enough
    tex = re.sub(r"\^\{[^{}]*\}|\^\\?\w", " ", tex)
    out = {g for g in re.findall(r"\\([A-Za-z]+)", tex) if g in GREEK}
    tex = re.sub(r"\\[A-Za-z]+", " ", tex)
    out |= {c for c in re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", tex) if c not in IGNORE}
    return out


def explained(var_text: str) -> set[str]:
    found: set[str] = set()
    var_text = var_text.replace("\\$", "")  # escaped dollar signs are currency, not math
    for math in re.findall(r"\$([^$]+)\$", var_text):
        found |= symbols(math)
    return found


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    hits: list[str] = []
    for sec in re.split(r"\n(?=<a id=\")", text)[1:]:
        sid = re.match(r'<a id="([^"]+)"', sec).group(1)
        var_text = "\n".join(re.findall(r"\*\*Variables:\*\*\n\n((?:- .*\n?)+)", sec))
        known = explained(var_text) | explained(text.split("<a id=")[0])  # chapter intro notation
        for formula in re.findall(r"\$\$(.+?)\$\$", sec, flags=re.S):
            missing = sorted(symbols(formula) - known)
            if missing:
                hits.append(f"{path.relative_to(ROOT)} [{sid}]: {', '.join(missing)}  in  {formula.strip()[:70]}")
    return hits


def main() -> int:
    paths = [Path(p).resolve() for p in sys.argv[1:]] or sorted((ROOT / "topics").glob("*.md"))
    hits = [h for p in paths for h in check(p)]
    for h in hits:
        print(h)
    print(f"{len(hits)} formula(s) with unexplained symbols")
    return 0


if __name__ == "__main__":
    sys.exit(main())
