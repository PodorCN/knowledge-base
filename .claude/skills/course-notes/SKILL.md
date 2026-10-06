---
name: course-notes
description: Turn raw material (PDF, HTML course notes, pasted text, chat notes) into course-notes-level sections of this knowledge base, or bring an existing section up to that standard. Use whenever material is added to topics/, or the user says a page "doesn't meet the wiki standard", variables are unexplained, or a concept (e.g. Rank IC) needs more explanation.
---

# Course-notes standard for this wiki

AGENTS.md is the rulebook (placement, upload rules, formats). This skill is the **quality bar** on top of
it: a reader who knows only the sections listed as prerequisites must be able to follow every line.

## 1. Before writing

1. Read AGENTS.md, `maps/` and every chapter touching the topic; `grep -ril` the key terms in `topics/`.
2. Split the material into ideas and map each one: **extend** an existing section (add a `###` sub-heading)
   or **new** section (only if nothing covers it). Generic tools (a statistic, a test, a leakage rule) go
   to the section that owns the tool; the material's own story (theory, case study) goes in its chapter.
3. Tell the user the placement list before editing.

## 2. The bar each section must clear

| Check | What "done" looks like |
|---|---|
| Statement | 1–3 sentences: what the idea is and what question it answers |
| Every symbol defined | Every symbol in every `$$…$$` is in the `**Variables:**` list right after it, with **units** (%, trading days, per year) and **sign / range** where it matters ($IC\in[-1,1]$, $DD_t\le0$) |
| Indices and timing | Say what $i$, $j$, $t$ run over and **when** each quantity is known (signal at $t$, return $t\to t+h$) |
| Jargon unpacked | Every named statistic (Rank IC, ICIR, n_eff, drawdown, turnover…) has a formula or a link to the section that defines it; never a bare name |
| Reading it | A "Reading it" / `**Notes:**` paragraph: how to interpret values, benchmarks, what high/low means |
| Why, not just what | For each design choice: what → why → what was rejected (a table works well) |
| Worked example | Small numbers the reader can redo by hand; check every number by computing it (python), never by eye |
| Pitfalls | When it breaks, and what a naive version gets wrong |
| Connections | `**Builds on:**` / `**Used by:**` / `**Related:**` links in both directions; metadata `prerequisites` only to earlier sections |

Content you add beyond the user's material (derivations, examples, explanations the user asked for) must be
standard and correct; mark genuine own inference **(自己推理)**. Keep numbers, tables, references and
(自己推理) marks from the source. Figures cannot be embedded: summarise what each figure shows in one line.

## 3. Verify

```bash
python3 scripts/check_variables.py topics/<chapter>.md   # unexplained formula symbols (advisory; read each hit)
python3 scripts/build_graph.py --strict                  # must be 0 errors, 0 warnings
```

Then open `local/index.html` (or screenshot it with Playwright) and check the new sections render: boxed
formulas, "where" tables, no raw `$`. Commit locally; upload only after the user's explicit OK (AGENTS.md rule 0).
