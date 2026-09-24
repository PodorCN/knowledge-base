# Knowledge Base 🧠

A personal knowledge graph for quant / derivatives / statistics interview prep.
Notes are plain Markdown chapters whose sections link to what they build on.

Organised by interview type:

```
Home
├── Foundations → Prob & Stats · Stochastic calc & Finance basics
├── Buy-side    → Signal research · Portfolio construction
└── Sell-side   → Pricing · Black–Scholes · Quant models · Risk management · Quant dev
```

Under each track: **chapters** (`topics/*.md`), each one complete document on a topic, split into sections you can link to and jump between. Interview questions are kept locally and are not part of this repository.

## Ways to browse

1. **Wiki site**: open `docs/index.html` (works offline) or enable GitHub Pages
   (Settings → Pages → Deploy from branch → `/docs`). Menu on the left (group → track → chapter),
   the chapter in the middle, and "On this page"
   plus builds-on / leads-to chapters on the right. The graph is one click away.
2. **Obsidian** (recommended for editing): *Open folder as vault* → this repo. Graph view,
   backlinks and `[[wikilinks]]` work without extra setup.
3. **GitHub**: start at [`maps/home.md`](maps/home.md).

## Adding material

- Drop a PDF into `inbox/` (or send it to Claude) and ask it to ingest it. Claude follows
  the workflow in [`AGENTS.md`](AGENTS.md): it reuses existing concepts, adds only new ones,
  and wires the links.
- Rebuild the graph with `python3 scripts/build_graph.py`; add `--strict` to fail on broken links.

## Current contents

See [`maps/home.md`](maps/home.md). Rules for AI agents adding material: [`AGENTS.md`](AGENTS.md).
