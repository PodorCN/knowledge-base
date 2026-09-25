# AGENTS.md — how to work on this knowledge base

Instructions for any AI agent (Claude, Codex, …) that adds or reorganises material here.
Read this whole file before editing.

## 0. The rules that matter most

0. **Never upload without the user's explicit OK.** No `git push`, no publishing pages or artifacts, no
   creating repositories, until the user says OK for that specific upload. Local edits and local commits are fine.
0b. **Sources are never uploaded.** Everything the user hands over as raw material (PDFs, documents,
   screenshots, pasted text, chat exports) and the `sources/src-*.md` notes about it live only in
   `sources/` or `inbox/`. Both folders are in `.gitignore` and must stay there; the build also strips
   source nodes and references from `docs/`. Only the finished notes (`topics/`, `questions/`, `maps/`)
   and the tooling get uploaded. Never `git add -f` them, never move raw files elsewhere in the repo,
   and never publish them anywhere, even when the user says OK to upload the rest.
0c. **Interview questions are never uploaded.** `questions/` is git-ignored, and the public site in `docs/`
   is built without any questions. The user studies them in `local/index.html` (git-ignored), which the
   build writes alongside. Never add question text anywhere that gets uploaded (notes, examples, commit messages).

1. **Only put in what the user gives you.** Do not add explanations, intros, summaries, examples or
   "helpful" extra content beyond the user's material unless the user explicitly asks. Keep it concise.
   Reformatting for readability is fine; changing or adding content is not.
2. **Read the whole library before adding anything, then add in the right place. Never start something new
   alongside what exists.** New material almost always belongs inside an existing section; parallel
   notes on the same idea make the library messy and hard to reorganise later. Concretely:
   - Read `maps/` (all chapters), then read in full every chapter and section that touches the topic,
     and `grep -ril` the key terms across `topics/` (and `questions/` for questions).
   - **Extend an existing section** when the idea is already covered, even partially: add a `###`
     sub-heading inside it, merge overlapping bullets instead of repeating them, and keep one version of
     each formula.
   - Add a **new section** to an existing chapter only if no section covers the idea; place it next to
     the sections it depends on and update the chapter's `**Sections:**` line.
   - Create a **new chapter** only when no chapter fits, and never a new group or track unless the user asks.
   - Before editing, tell the user where each piece will go (which chapter / section, extend or new).
3. **Everything is written in English**, even when the user's material is in Chinese: translate
   faithfully, don't summarise or embellish. Keep the user's numbers, tables, references and **(自己推理)** marks.

## 1. Structure

```
home
├── Foundations  → prob-stats · stochastic-finance
├── Buy-side     → signal-research · portfolio-construction
└── Sell-side    → pricing · black-scholes · quant-models · risk-management · quant-dev
```

Levels: **Group → Track → Chapter → Section**.

| Level | Where it lives | Notes |
|---|---|---|
| Group | `maps/map-foundations.md`, `map-buyside.md`, `map-sellside.md` | fixed, 3 groups |
| Track | `maps/map-<track>.md` | fixed, 9 tracks; lists its chapters in reading order |
| Chapter | `topics/<chapter-id>.md` | one complete document per topic |
| Section | a block inside a chapter | one idea; has an anchor so `[[section-id]]` jumps to it |
| Question | `## Q017:` block in `questions/qb-*.md` | links to the sections it tests; **local only** (git-ignored) |
| Source | `sources/src-*.md` note + raw file in `sources/pdfs/` | **local only** (git-ignored), not shown in the wiki |

## 2. How to classify new material

Ask in this order:

1. **Which interview is it for?** Asked in any quant interview (probability, statistics, stochastic
   calculus, basic finance) → **Foundations**. Finding signals or building portfolios → **Buy-side**.
   Pricing, modelling, hedging or building derivatives systems → **Sell-side**.
2. **Which track?**

| Track | Put here |
|---|---|
| `prob-stats` | probability, distributions, expectation/variance, puzzles, estimation, hypothesis tests, linear algebra |
| `stochastic-finance` | Brownian motion, Itô, GBM, risk-neutral pricing, returns, no-arbitrage, forwards, bonds |
| `signal-research` | regression, ML, time series, validation/leakage, signals, alpha, backtests, research process |
| `portfolio-construction` | Sharpe, diversification, optimisation, risk contribution/budgeting, position sizing |
| `pricing` | option payoffs, parity, replication, exotic options, structured products, delta one |
| `black-scholes` | Black–Scholes PDE/formula, N(d1) vs N(d2), Black-76, American exercise; **Greeks** (own chapter) |
| `quant-models` | implied vol, vol surface construction, local/stochastic vol, numerical methods |
| `risk-management` | hedging, pin risk, scenarios, VaR/ES, model risk (Greeks themselves live in the `black-scholes` track) |
| `quant-dev` | OOP, design patterns, C#/.NET, pricing-app architecture, releases, reconciliation, coding questions |

3. **Which chapter?** Pick the existing chapter below whose subject fits. Only create a new chapter for a
   genuinely new topic (and list it in the track map).
4. **New section or existing section?** Search first: `grep -ril "<keyword>" topics/`. If a section
   already covers the idea, add the new material there. Otherwise add a new section to the chapter.

Current chapters and question banks:

| Track | Chapters (reading order) | Question banks |
|---|---|---|
| `prob-stats` | `probability-bayes`, `distributions`, `moments-covariance`, `puzzles-markov`, `estimation-testing` | `qb-probability`, `qb-statistics-inference` |
| `stochastic-finance` | `stochastic-calculus`, `no-arbitrage-finance-basics` | `qb-finance-foundations`, `qb-stochastic-calculus` |
| `signal-research` | `linear-regression`, `ml-regularisation`, `time-series-validation`, `signals-research-process` | `qb-regression-ml`, `qb-research-judgment` |
| `portfolio-construction` | `measuring-performance`, `portfolio-optimisation`, `risk-budgeting-position-sizing` | `qb-portfolio-performance` |
| `pricing` | `no-arbitrage-parity`, `exotic-options`, `structured-products-delta-one` | `qb-exotics-structured` |
| `black-scholes` | `black-scholes`, `black-scholes-call-derivation`, `greeks-sensitivities` | `qb-options-bs-greeks` |
| `quant-models` | `implied-volatility-skew`, `vol-surface-construction-chapter`, `volatility-models`, `numerical-methods` | `qb-vol-surface` |
| `risk-management` | `hedging`, `risk-control-governance` | `qb-risk-management` |
| `quant-dev` | `oop-design`, `csharp-dotnet`, `production-coding` | `qb-quant-dev-engineering` |

## 3. Formats

### Chapter (`topics/<chapter-id>.md`, see `templates/topic.md`)

```markdown
---
id: risk-budgeting-position-sizing   # = filename, kebab-case, must not equal any section id
title: "Risk Budgeting & Position Sizing"
type: topic
domain: portfolio-construction       # the track
sources: [src-signal-to-weight]
---
# Risk Budgeting & Position Sizing

**Sections:** [[risk-contribution]] · [[risk-budgeting]] · [[signal-to-weight]]

<a id="risk-budgeting"></a>

## Risk Budgeting (Bruder & Roncalli 2012)
<!-- section: risk-budgeting | prerequisites: [risk-contribution] | related: [signal-to-weight] | sources: [src-signal-to-weight] | tags: [risk-parity] -->

$$RC_i(w)=w_i\frac{(\Sigma w)_i}{\sigma(w)}=TE_i\cdot\sigma(w)$$

**Variables:**

- $w_i$ weight of asset $i$
- $TE_i$ risk budget of asset $i$

### Key points
- …

### Connections
- **Builds on:** [[risk-contribution]]
```

Rules:
- The `<a id>` line, the `## ` title and the `<!-- section: … -->` comment go together, in that order;
  the anchor id must equal `section:`. Section ids are kebab-case and unique across the repo.
- `prerequisites` ("you need X first") and `related` in the comment create the links shown in the wiki.
  Link across chapters and tracks whenever the material connects.
- Inside a section use `###` for sub-headings, never `##`. Update the `**Sections:**` line when adding a section.
- Keep formulas with their variables, one variable per list item (`- $symbol$ meaning`).
- Every bold label (`**Variables:**`, `**Example:**`) starts its own paragraph (blank line before it).
- Math: `$inline$`, `$$display$$`. Keep any **(自己推理)** marks that appear in the user's material.

The wiki typesets this like course notes automatically: numbered chapters/sections/equations, boxed
`### Formula` / `### Definition` blocks, individual display equations in custom subsections, `### Worked example` /
`**Example:**` as an Example box, `### Connections` as "See also", and variables as a "where" table.

### Question (`questions/qb-*.md`)

```markdown
## Q017: <question text in English>
**Topics:** [[section-id]] · [[another-section-id]]
**Seen in:** [[src-some-source]]

**Answer.** …
```

- Every question has a permanent number in its heading: `## Q017: …`. Numbers never change and are never
  reused; a new question takes the next free number (the build prints it). Deleting a question leaves a gap.
- Questions are in **English**, with the answer from the user's material.
- `**Topics:**` must link the sections the question tests; that is how it appears under those sections.
- If the question already exists, add the new source to `**Seen in:**` instead of duplicating it.
- `**Seen in:**` is kept in the files but hidden in the wiki.

### Source (`sources/src-*.md`)
One short note per document: title, file path, and the list of sections it fed. Raw PDF in `sources/pdfs/`.

## 4. Workflow for adding material

1. Save the raw file in `sources/pdfs/` (or text in `inbox/`); these are git-ignored and never uploaded.
   Create `sources/src-<slug>.md`.
2. Read the library (rule 2), classify each piece (section 2), then extend an existing section or add a new
   one. Only the user's content, in English.
3. Add the questions to the track's question bank with `**Topics:**` links and the next free number
   (the build prints it). Check first that the question isn't already there.
4. Build and check: `python3 scripts/build_graph.py --strict` must report **0 errors**.
   Before every published update, increment the patch number in `VERSION` (for example, `1.01` → `1.02`);
   the build injects it into the viewer.
5. Commit the notes and the regenerated `docs/`.

## 5. Where the questions show up

- `docs/index.html` (uploaded) contains no questions and no sources.
- `local/index.html` (git-ignored) has everything, including each section's questions. Open it locally.
- Optional: `KB_QUESTIONS_PASSWORD='…' python3 scripts/build_graph.py` encrypts the questions inside
  `local/index.html`. Never write the password into any file, commit message or chat log.

## 6. Build outputs

`scripts/build_graph.py` validates links and writes the public `docs/` site and the local-only `local/`
site (a self-contained wiki: sidebar menu, chapter reader, "On this page" rail, chapter graph).
Don't edit generated files by hand.
