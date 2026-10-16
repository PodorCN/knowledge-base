# AGENTS.md — how to work on this knowledge base

Instructions for any AI agent (Claude, Codex, Gemini, subagents, …) that adds, edits, or reorganises material here.
**Read this whole file before making any edit.** Assume future subagents will follow your structure literally: write clean, canonical, contradiction-free notes.

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

1. **Only put in what the user gives you (or explicitly asks you to add).** Do not add unrequested filler,
   long-winded introductions, or repetitive summaries. Reformatting for readability is fine; changing or inventing content is not.
2. **Read the whole library before adding anything, then add in the right place. Never start something new
   alongside what exists.** New material almost always belongs inside an existing section; parallel
   notes on the same idea make the library messy and hard to reorganise later. Concretely:
   - Read `maps/` (all chapters), then read in full every chapter and section that touches the topic,
     and `grep -ril` the key terms across `topics/` (and `questions/` for questions).
   - **Extend an existing section** when the idea is already covered, even partially: add a `###`
     sub-heading inside it, merge overlapping bullets instead of repeating them, and keep **one single canonical version** of
     each formula across the entire wiki.
   - Add a **new section** to an existing chapter only if no section covers the idea; place it next to
     the sections it depends on and update the chapter's `**Sections:**` line.
   - Create a **new chapter** only when no chapter fits, and never a new group or track unless the user asks.
   - Before editing, tell the user where each piece will go (which chapter / section, extend or new).
3. **Everything is written in English**, even when the user's material is in Chinese: translate
   faithfully, don't summarise or embellish. Keep the user's numbers, tables, references and **(自己推理)** marks.

## 0d. Target Audience & Quality Bar (Master's + 2 YoE Quant / Quant Dev)

The reader of this wiki is a **quant researcher / quant developer with a Master's degree and ~2 years of industry experience** preparing for technical interviews. Every section must be calibrated to this exact persona:

1. **No formula-free stubs on core technical topics.** A 3-bullet summary with no formula or algorithm does not pass a 2-YoE interview. Every technical section must state the exact mathematical formula, SDE, PDE scheme, estimator, or algorithm, followed by a complete `**Variables:**` block (`- $symbol$ meaning`) and concrete interview takeaways (when it works, when it breaks, and why alternatives were rejected).
2. **No CS101 / intro-textbook micro-sections.** Do not create standalone top-level `##` sections for elementary syntax (e.g. what a ternary operator `?:` or `=>` arrow is). Group basic syntax reminders into a single compact cheatsheet section using `alias: [...]` and `<a id="...">` anchors so top-level navigation stays focused on high-signal architecture, memory/concurrency, and numerical engineering.
3. **Single Source of Truth (Zero Cross-Chapter Duplication):**
   - **Formulas & Definitions** live in the **tool/metric chapter** (e.g. `signal-metrics.md` owns the equations for `IC`, `Rank IC`, `ICIR`, `Hit Rate`, `Fundamental Law`, `Turnover`, and `Cost Drag`).
   - **Workflow & Protocol chapters** (e.g. `signal-evaluation.md`, `portfolio-construction-process.md`) explain *how to interpret, stress-test, and make decisions* with those metrics and **link** to `[[section-id]]` instead of re-deriving the same equations and `**Variables:**` blocks.
   - **Case-study chapters** (e.g. `carry-stock-bond-timing.md`) present the specific economic hypothesis, data audit, and empirical results of that case study, linking back to the protocol and metric chapters.
4. **Strict Anti-Patterns (NEVER DO THESE):**
   - **NEVER write defensive or pedantic disclaimer prose.** Do not write sentences like *"This is a definition, not a theorem that X is the best metric"* or *"The formula is only a mechanical identity, not an economic law that guarantees profit."* State what the formula computes, what assumptions it requires, and the exact failure mode when those assumptions break (e.g., *"When $h > 1$ overlaps, naive $\sqrt{T}$ inflates $t$-stats by $\approx\sqrt{h}$; use Newey–West or $N_{\text{eff}}$"*).
   - **NEVER use mechanical string-replacement scripts (`inbox/*.py`) to bulk-insert boilerplate disclaimers into Markdown files.** Edit thoughtfully and read the surrounding prose.
   - **NEVER leave `(verify)`, `(cited from memory — verify)`, or `(not individually verified)` placeholders in `topics/`.** Verify every citation, equation, and function signature before writing it into `topics/`. If something cannot be verified, omit the unverified claim or ask the user.
   - **NEVER leave conflicting numbers for the same empirical case study across different chapters.** If two runs exist (e.g. a registered baseline run with `auto_adjust=True` giving `Rank IC = +0.0252` and an unadjusted-close check `auto_adjust=False` giving `Rank IC = +0.0423`), label both columns explicitly side by side in the table and reference them consistently everywhere.
   - **NEVER use raw Unicode Greek letters (`μ, Σ, σ, ρ, λ`) in prose when referring to mathematical variables.** Always use LaTeX math mode (`$\mu, \Sigma, \sigma, \rho, \lambda$`).
   - **NEVER delete or rename a section ID or alias.** If you merge section `foo-bar` into `baz-qux`, add `alias: [foo-bar]` to the `<!-- section: baz-qux | alias: [foo-bar] | ... -->` metadata comment AND keep `<a id="foo-bar"></a>` inside the merged section so all `[[foo-bar]]` links and local question banks continue to resolve with 0 errors. Never declare the same `section:` or `alias:` ID in two different places.

## 1. Structure

```
home
├── Foundations  → prob-stats · stochastic-finance
├── Buy-side     → signal-research · portfolio-construction
├── Sell-side    → black-scholes · pricing · risk-management
└── Engineering  → quant-dev
```

Tracks and chapters are in **reading order**: a section's `prerequisites` must come earlier in this order
(the build warns otherwise). If Section A wants to reference Section B that appears *later* in the reading order, put `B` in `related:`, **never** in `prerequisites:`. Symbols follow the **Notation & conventions**
table in `maps/home.md`; a chapter that needs local symbols defines them in its introduction.

Levels: **Group → Track → Chapter → Section**.

| Level | Where it lives | Notes |
|---|---|---|
| Group | `maps/map-foundations.md`, `map-buyside.md`, `map-sellside.md`, `map-engineering.md` | fixed, 4 groups (also listed in `GROUPS` in `scripts/viewer_template.html`) |
| Track | `maps/map-<track>.md` | fixed, 8 tracks; lists its chapters in reading order |
| Chapter | `topics/<chapter-id>.md` | one complete document per topic |
| Section | a block inside a chapter | one idea; has an anchor so `[[section-id]]` jumps to it |
| Question | `## Q017:` block in `questions/qb-*.md` | links to the sections it tests; **local only** (git-ignored) |
| Source | `sources/src-*.md` note + raw file in `sources/pdfs/` | **local only** (git-ignored), not shown in the wiki |

## 2. How to classify new material

Ask in this order:

1. **Which interview is it for?** Asked in any quant interview (probability, statistics, basic
   finance) → **Foundations**. Finding signals or building portfolios → **Buy-side**.
   Stochastic calculus, pricing, modelling or hedging derivatives → **Sell-side**.
   Programming / quant dev → **Engineering** (read last).
2. **Which track?**

| Track | Put here |
|---|---|
| `prob-stats` | probability, distributions, expectation/variance, puzzles, estimation, hypothesis tests, linear algebra, calculus / Taylor / mental math |
| `stochastic-finance` | returns, no-arbitrage, forwards, bonds, option payoffs / bounds / put–call parity / binomial & static replication (track title: "Finance Foundations") |
| `signal-research` | regression (OLS, Fama–MacBeth), ML (shrinkage, tree ensembles), time series, validation/leakage, signals, IC / alpha, multi-asset risk premia & macro signals, research process & backtests |
| `portfolio-construction` | Sharpe, win rate / expectancy, exposure, diversification, optimisation (Lagrange/KKT, constraints, infeasibility), risk contribution/budgeting, position sizing, the construction process (mandate/TE, covariance estimation, transaction costs, validation) |
| `pricing` | numerical methods (root finding, PDE finite differences, Monte Carlo), implied vol, vol surface construction, local/stochastic/jump/SABR vol; exotic options, structured products, delta one (track title: "Pricing") |
| `black-scholes` | Brownian motion, Itô, GBM, Ornstein–Uhlenbeck / mean reversion, martingales, risk-neutral pricing; Black–Scholes PDE/formula, N(d1) vs N(d2), Black-76, American exercise; **Greeks** (own chapter) (track title: "Black–Scholes") |
| `risk-management` | hedging, pin risk, scenarios, VaR/ES & coherent risk measures, model risk (Greeks themselves live in the `black-scholes` track) |
| `quant-dev` | OOP, design patterns, C#/.NET, MATLAB (vs Python, interop, performance, memory model, config), portfolio optimisation in MATLAB, pricing-app architecture, releases, reconciliation, streaming/rolling algorithms & coding questions |

3. **Which chapter?** Pick the existing chapter below whose subject fits. Only create a new chapter for a
   genuinely new topic (and list it in the track map).
4. **New section or existing section?** Search first: `grep -ril "<keyword>" topics/`. If a section
   already covers the idea, add the new material there. Otherwise add a new section to the chapter.

Current chapters and question banks:

| Track | Chapters (reading order) | Question banks |
|---|---|---|
| `prob-stats` | `calculus-mental-math`, `probability-distributions`, `moments-covariance`, `puzzles-markov`, `estimation-testing`, `statistical-testing` | `qb-probability`, `qb-statistics-inference` |
| `stochastic-finance` | `no-arbitrage-finance-basics`, `fixed-income-bonds`, `no-arbitrage-parity` | `qb-finance-foundations` |
| `quant-dev` | `oop-design`, `csharp-dotnet`, `matlab-quant-dev` | `qb-quant-dev-engineering` |
| `signal-research` | `linear-regression`, `ml-regularisation`, `time-series-validation`, `signal-metrics`, `signal-evaluation`, `alpha-forecasting`, `multi-asset-signals`, `carry-stock-bond-timing` | `qb-regression-ml`, `qb-research-judgment` |
| `portfolio-construction` | `measuring-performance`, `portfolio-optimisation`, `risk-budgeting-position-sizing`, `portfolio-construction-process` | `qb-portfolio-performance` |
| `black-scholes` | `stochastic-calculus`, `black-scholes`, `black-scholes-call-derivation`, `greeks-sensitivities` | `qb-stochastic-calculus`, `qb-options-bs-greeks` |
| `pricing` | `numerical-methods`, `implied-volatility-skew`, `vol-surface-construction-chapter`, `volatility-models`, `exotic-options`, `structured-products-delta-one` | `qb-vol-surface`, `qb-exotics-structured` |
| `risk-management` | `hedging`, `risk-control-governance` | `qb-risk-management` |

Section ids are permanent (local question banks link to them): move sections between chapters freely,
but never rename or delete a section id.

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

One-paragraph overview of what the chapter covers and why.

**Prerequisites:** [[portfolio-variance-diversification]], [[time-series-momentum]].

**Leads to:** [[fx-carry-spot-slide]].

**Sections:** [[risk-contribution]] · [[risk-budgeting]] · [[signal-to-weight]]

<a id="risk-budgeting"></a>

## Risk Budgeting (Bruder & Roncalli 2012)
<!-- section: risk-budgeting | prerequisites: [risk-contribution] | related: [signal-to-weight] | sources: [src-signal-to-weight] | tags: [risk-parity] -->

One or two sentences stating the idea of the section.

### Formula
$$RC_i(w)=w_i\frac{(\Sigma w)_i}{\sigma(w)}=b_i\cdot\sigma(w)$$

**Variables:**

- $w_i$ weight of asset $i$
- $\Sigma$ covariance matrix of asset returns
- $\sigma(w) = \sqrt{w^\top \Sigma w}$ portfolio volatility
- $b_i$ risk budget of asset $i$ ($\sum_i b_i = 1$)
- $RC_i(w)$ risk contribution of asset $i$

### Key points
- …

### Connections
- **Builds on:** [[risk-contribution]]
```

Rules:
- **Chapter intro:** after `# Title`, one overview paragraph, then `**Prerequisites:**` and `**Leads to:**` lines
  (links to sections in other chapters), then the `**Sections:**` line. Local notation goes in the intro.
- **Section layout, always in this order:** a 1–3 sentence statement of the idea → `### Formula` / `### Definition` with `**Variables:**` → `### Key points` → `### Worked example` (if any) → `### Connections` with `**Builds on:**` / `**Used by:**` / `**Related:**` / `**Contrast:**`.
- **Every symbol in a display formula (`$$...$$`) MUST appear in its `**Variables:**` list**, written `- $symbol$ meaning` (the viewer turns the list into a "where" table, and `scripts/check_variables.py` checks it automatically). Don't put another bullet list directly after `**Variables:**`; add a bold label such as `**Notes:**` or a `###` heading between them.
- The `<a id>` line, the `## ` title and the `<!-- section: … -->` comment go together, in that order;
  the anchor id must equal `section:`. Section ids are kebab-case and unique across the repo.
- `prerequisites` ("you need X first") and `related` in the comment create the links shown in the wiki.
  Link across chapters and tracks whenever the material connects.
- Inside a section use `###` for sub-headings, never `##`. Update the `**Sections:**` line when adding a section.
- Keep formulas with their variables, one variable per list item (`- $symbol$ meaning`).
- Every bold label (`**Variables:**`, `**Example:**`, `**Interview takeaway:**`) starts its own paragraph (blank line before it).
- Math: `$inline$`, `$$display$$`. Keep any **(自己推理)** marks that appear in the user's material.

The wiki typesets this like course notes automatically: numbered chapters/sections/equations, boxed
`### Formula` / `### Definition` blocks, individual display equations in custom subsections, `### Worked example` /
`**Example:**` as an Example box, `### Connections` as "See also", and variables as a "where" table.

### Question (`questions/qb-*.md`)

```markdown
## Q017: <question text in English>
**Category:** Asset Allocation
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

#### Interview preparation: extract, classify and format

- Identify the actual question in pasted material and put only that question in the numbered heading.
  Separate the answer from surrounding chat, praise and presentation instructions.
- Give every question a concise `**Category:**` based on its subject. Reuse an existing category when
  it fits, such as **Asset Allocation**, Fixed Income, Portfolio Risk or Derivatives; do not place
  unrelated questions in Asset Allocation or create a new track for each category.
- Remove decorative stars/emoji, timing estimates (for example, "Approximately 1 Minute"),
  redundant "Interview Answer" headings, and quotation marks enclosing the whole answer.
  This cleanup is authorised formatting, not a change to the financial meaning. Keep the raw original in `inbox/`.
- Preserve the substantive question and answer. Do not invent extra explanations or shorten the answer
  unless requested. Split the answer into readable paragraphs or lists where appropriate.
- The preparation reader groups questions by category, displays each question as a prominent heading,
  and separates the answer with generous spacing. Keep answers visible for reading. Source and section-link
  metadata belongs in the Markdown files, not between the question and its answer.
- Use `tags: [interview, interview-preparation]` on preparation banks. Rebuild both the wiki and the
  standalone local handout; never hand-edit generated HTML. Check desktop and mobile readability.
- Preparation navigation is **group → Interview Preparation → named study chapter**. A preparation
  bank's title is its study chapter (for example, Inflation / Recession Scenario), while each question's
  category remains its subject (for example, Asset Allocation). Reuse permanent bank/question IDs.
- When the user requests study notes, organise a concise overview, the existing numbered question and
  answer, a scenario comparison, mechanisms, limitations and a final recall checklist. Explain the
  reasoning instead of copying the chat. In the bank introduction, put the overview before
  `<!-- study-notes -->` and the detailed Markdown notes after it; keep numbered questions after the
  notes. The build displays overview → questions → notes and renders tables in the offline handout.
  These notes stay in the ignored preparation bank. Link existing foundations instead of duplicating
  them as new public chapters. Store raw chat retrievals and any retrieval limitations in `inbox/` and `sources/`.

### Source (`sources/src-*.md`)
One short note per document: title, file path, and the list of sections it fed. Raw PDF in `sources/pdfs/`.

## 4. Workflow for adding or editing material

1. Save the raw file in `sources/pdfs/` (or text in `inbox/`); these are git-ignored and never uploaded.
   Create `sources/src-<slug>.md`.
2. Read the library (rule 2), classify each piece (section 2), then extend an existing section or add a new
   one. Check section 0d to ensure zero cross-chapter duplication, no defensive disclaimer prose, and complete mathematical & variable definitions.
3. Add the questions to the track's question bank with `**Topics:**` links and the next free number
   (the build prints it). Check first that the question isn't already there.
4. Build and check (on Windows, if `python3` is the Windows Store stub, use `& "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe"`):
   - `python3 scripts/check_variables.py` must report **0 unexplained symbols** across all modified chapters.
   - `python3 scripts/build_graph.py --strict` must report **0 errors and 0 warnings**.
   - Before every published update, increment the patch number in `VERSION` (for example, `1.20` → `1.21`);
     the build injects it into the viewer.
5. Commit the notes and the regenerated `docs/`.
6. **The website follows `main`.** GitHub Pages serves `docs/` from the `main` branch. When the user OKs an
   upload (rule 0), merge the finished work into `main` (bring `main` into your working branch first and
   resolve any conflicts, then rebuild `docs/`) and push `main`; a push that doesn't reach `main` doesn't
   update the site.

## 5. Where the questions show up

- `docs/index.html` (uploaded) contains no questions and no sources.
- `local/index.html` (git-ignored) has everything, including each section's questions. Open it locally.
- Optional: `KB_QUESTIONS_PASSWORD='…' python3 scripts/build_graph.py` encrypts the questions inside
  `local/index.html`. Never write the password into any file, commit message or chat log.

## 6. Build outputs

The build also warns when a section's `prerequisites` entry comes later in the reading order (tracks as listed in
`maps/home.md`, chapters as listed in each track map); keep it at 0 warnings.

`scripts/build_graph.py` validates links and writes the public `docs/` site and the local-only `local/`
site (a self-contained wiki: sidebar menu, chapter reader, "On this page" rail, chapter graph).
Don't edit generated files by hand.
