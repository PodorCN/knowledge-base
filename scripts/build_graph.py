#!/usr/bin/env python3
"""Build the knowledge graph from the Markdown vault.

Reads maps/, topics/, questions/ and sources/, validates links and frontmatter,
and writes:
  docs/graph.json   - nodes + links (for other tools)
  docs/index.html   - self-contained interactive viewer (data inlined, works offline)

Usage:
  python3 scripts/build_graph.py            # build, print warnings
  python3 scripts/build_graph.py --strict   # exit 1 on broken links / schema errors

Outputs:
  docs/index.html   public site (uploaded): no sources, no interview questions
  local/index.html  local-only site (git-ignored): includes interview questions
Optionally KB_QUESTIONS_PASSWORD='...' encrypts the questions in local/index.html (AES-256-GCM,
key from PBKDF2-SHA256). Never commit the password.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import sys
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTE_DIRS = ["maps", "topics", "questions", "sources"]
TEMPLATE = ROOT / "scripts" / "viewer_template.html"
VERSION_FILE = ROOT / "VERSION"
OUT_DIR = ROOT / "docs"      # uploaded: no sources, no questions
LOCAL_DIR = ROOT / "local"   # git-ignored: includes interview questions

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
QUESTION_HEADING = re.compile(r"^## Q(\d{3,})?:\s*(.+)$", re.M)

# When the same pair of nodes is linked several ways, keep the most meaningful type.
EDGE_PRIORITY = ["prerequisite", "related", "tests", "contains", "source", "mention", "domain"]
VALID_TYPES = {"topic", "map", "question-bank", "source"}

# A topic document is split into sections; each section is a "concept" node you can link to.
#   <a id="risk-budgeting"></a>
#
#   ## Risk Budgeting ...
#   <!-- section: risk-budgeting | prerequisites: [a, b] | related: [c] | sources: [src-x] | tags: [t] -->
SECTION = re.compile(r'^<a id="([a-z0-9-]+)"></a>\s*\n## (.+?)\n<!-- section: (.*?) -->', re.M)


def parse_section_meta(text: str) -> dict:
    meta = {}
    for part in text.split("|"):
        if ":" not in part:
            continue
        key, _, val = part.partition(":")
        val = val.strip()
        meta[key.strip()] = [v.strip() for v in val.strip("[]").split(",") if v.strip()] if val.startswith("[") else val
    return meta


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-")


def parse_note(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(raw)
    if not m:
        return None, raw
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2)


def embed_note_figures(body: str, note_path: Path) -> str:
    """Inline finished figures so both generated viewers remain portable.

    Only assets/figures is eligible: raw sources and interview material must
    never be copied into a public page through an image reference.
    """
    figure_root = (ROOT / "assets" / "figures").resolve()
    media_types = {".svg": "image/svg+xml", ".png": "image/png",
                   ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                   ".webp": "image/webp"}

    def inline(match):
        alt, reference = match.groups()
        if reference.startswith(("https://", "http://", "data:")):
            return match.group(0)
        figure = (note_path.parent / reference).resolve()
        if not figure.is_relative_to(figure_root):
            raise ValueError("local figures must live in assets/figures")
        media_type = media_types.get(figure.suffix.lower())
        if not media_type:
            raise ValueError(f"unsupported figure format: {figure.suffix}")
        if not figure.is_file():
            raise ValueError(f"missing figure: {reference}")
        encoded = base64.b64encode(figure.read_bytes()).decode("ascii")
        return f"![{alt}](data:{media_type};base64,{encoded})"

    return re.sub(r"!\[([^\]\n]*)\]\(([^)\n]+)\)", inline, body)


ONE_LINER = re.compile(r"\*\*In one line:\*\*\s*(.+)")


def summarize(body: str, limit: int = 180) -> str:
    """One-line summary: the '**In one line:**' sentence, else the first prose paragraph."""
    m = ONE_LINER.search(body)
    text = m.group(1) if m else ""
    if not text:
        for line in body.splitlines():
            line = line.strip()
            if line and not line.startswith(("#", "$", "|", "-", "*", "`", ">", "1.")):
                text = line
                break
    text = WIKILINK.sub(lambda w: w.group(1), text).replace("**", "")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


PBKDF2_ITERATIONS = 310_000


def lock_questions(graph: dict, password: str) -> dict:
    """Replace question text with ciphertext; question ids become opaque hashes."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    rename, secret = {}, {}
    for n in graph["nodes"]:
        if n["type"] != "question":
            continue
        bank = n["id"].split("/")[0]
        new_id = f"{bank}/q-{hashlib.sha256(n['id'].encode()).hexdigest()[:12]}"
        rename[n["id"]] = new_id
        secret[new_id] = {"title": n["title"], "content": n["content"]}
        n.update(id=new_id, title="Locked exercise", content="", locked=True)
    for link in graph["links"]:
        link["source"] = rename.get(link["source"], link["source"])
        link["target"] = rename.get(link["target"], link["target"])
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS, dklen=32)
    ct = AESGCM(key).encrypt(iv, json.dumps(secret, ensure_ascii=False).encode(), None)
    b64 = lambda b: base64.b64encode(b).decode()
    graph["locked"] = {"salt": b64(salt), "iv": b64(iv), "ct": b64(ct), "iter": PBKDF2_ITERATIONS}
    return graph


def write_site(graph: dict, out_dir: Path) -> None:
    out_dir.mkdir(exist_ok=True)
    (out_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    if TEMPLATE.exists():
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+", version):
            raise ValueError(f"VERSION must look like MAJOR.MINOR, got {version!r}")
        payload = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
        html = (TEMPLATE.read_text(encoding="utf-8")
                .replace("__KB_VERSION__", version)
                .replace("/*__GRAPH_DATA__*/null", payload))
        head = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
        (out_dir / "index.html").write_text(head + html, encoding="utf-8")


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value]


def write_interview_handout(graph: dict, password: str) -> None:
    """Write a script-free reading copy from the local preparation banks."""
    output = LOCAL_DIR / "interview-preparation.html"
    if password:
        output.unlink(missing_ok=True)
        return
    banks = [n for n in graph["nodes"]
             if n["type"] == "question-bank" and "interview-preparation" in n["tags"]]
    if not banks:
        output.unlink(missing_ok=True)
        return
    import markdown

    by_id = {n["id"]: n for n in graph["nodes"]}

    def render(text: str, contents: bool = False) -> str:
        text = WIKILINK.sub(lambda m: by_id.get(m.group(1), {}).get("title", m.group(1)), text)
        renderer = markdown.Markdown(extensions=["tables", "fenced_code", "toc"], extension_configs={"toc": {"toc_depth": "2-2"}})
        html = renderer.convert(text)
        if contents:
            html = '<nav class="study-nav" aria-label="Study notes contents">' + renderer.toc + '</nav>' + html
        return html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    sections = []
    for bank in banks:
        overview, _, notes = re.sub(r"^# .*\n?", "", bank["content"]).partition("<!-- study-notes -->")
        cards = []
        questions = [n for n in graph["nodes"] if n["type"] == "question" and n["id"].split("/")[0] == bank["id"]]
        for q in questions:
            body = re.sub(r"^## Q\d+:.*\n?", "", q["content"])
            body = re.sub(r"^\*\*(?:Category|Topics|Seen in):\*\*.*\n?", "", body, flags=re.M)
            body = re.sub(r"\*\*Answer\.\*\*\s*", "", body).strip()
            cards.append(f'<article><span class="number">{escape(q["category"])} · {escape(q["qno"])}</span>'
                         f'<h3>{escape(q["title"])}</h3><div class="answer">{render(body)}</div></article>')
        sections.append(f'<section id="{escape(bank["id"])}"><h2 class="chapter-title">{escape(bank["title"])}</h2>'
                        f'<div class="lead">{render(overview)}</div>{"".join(cards)}'
                        f'<div class="study-notes">{render(notes, contents=bool(notes.strip()))}</div></section>')
    css = """*{box-sizing:border-box}body{margin:0;background:#f6f5f1;color:#24322f;font-family:Georgia,serif}
main{max-width:900px;margin:auto;padding:64px 36px 90px}header{margin-bottom:60px}header p{font:13px/1.5 system-ui;color:#63716b;letter-spacing:.1em;text-transform:uppercase}
h1{font-size:38px;line-height:1.2;margin:16px 0}.chapter-title{font-size:31px;line-height:1.3;margin:0 0 20px}.lead{font-size:18px;line-height:1.8;color:#58665e;margin-bottom:34px}
article{padding:36px 40px 40px;background:#fff;border:1px solid #e1e5de;border-radius:10px;margin-bottom:32px}
.number{font:12px/1.5 system-ui;color:#7b8881}h3{font-size:30px;line-height:1.35;font-weight:600;margin:12px 0 30px;overflow-wrap:break-word}
.answer{border-top:1px solid #e3e7e0;padding-top:10px;font-size:18px;line-height:1.85}.answer p{margin:20px 0}.answer p:last-child{margin-bottom:0}
.study-notes{font-size:17px;line-height:1.85}.study-notes h2{font:600 24px/1.4 Georgia,serif;color:#2a5141;margin:48px 0 22px;padding-top:24px;border-top:1px solid #dce2d9}.study-notes h3{font:600 20px/1.5 Georgia,serif;margin:30px 0 16px}.study-notes li{margin:10px 0}.study-notes a{color:#326b61;overflow-wrap:anywhere}
.table-wrap{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font:14px/1.65 system-ui;background:#fff}th,td{text-align:left;vertical-align:top;padding:14px 16px;border:1px solid #dce2d9;min-width:155px}th{background:#edf1ea;font-weight:600}nav{font:14px/1.6 system-ui;margin:26px 0}nav a{color:#326b61}
.study-nav{padding:18px 22px;background:#edf1ea;border-radius:8px}.study-nav ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 20px}.study-nav li{margin:0}
@media(max-width:600px){main{padding:32px 18px 48px}header{margin-bottom:38px}h1{font-size:30px}article{padding:26px 22px}h3{font-size:25px}.answer{font-size:17px}}
@media print{body{background:white}main{padding:0;max-width:none}article{break-inside:avoid;border:0;padding:20px 0}}"""
    output.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                      '<meta name="viewport" content="width=device-width, initial-scale=1">'
                      '<title>Interview Preparation</title><style>' + css + '</style></head>'
                      '<body><main><header><p>Buy-side</p><h1>Interview Preparation</h1>'
                      '<nav>' + ' · '.join(f'<a href="#{escape(b["id"])}">{escape(b["title"])}</a>' for b in banks)
                      + '</nav></header>'
                      + "".join(sections) + '</main></body></html>\n', encoding="utf-8")


def main() -> int:
    strict = "--strict" in sys.argv
    errors: list[str] = []
    warnings: list[str] = []

    nodes: dict[str, dict] = {}
    aliases: dict[str, str] = {}  # merged section id -> canonical section id
    qnumbers: dict[str, str] = {}
    raw_edges: list[tuple[str, str, str]] = []  # (source, target, type)
    link_sites: list[tuple[str, str]] = []  # (from node, target) for broken-link checks

    for folder in NOTE_DIRS:
        for path in sorted((ROOT / folder).glob("*.md")):
            rel = path.relative_to(ROOT).as_posix()
            meta, body = parse_note(path)
            if meta is None:
                errors.append(f"{rel}: missing YAML frontmatter")
                continue
            try:
                body = embed_note_figures(body, path)
            except ValueError as exc:
                errors.append(f"{rel}: {exc}")
            nid = meta.get("id")
            if nid != path.stem:
                errors.append(f"{rel}: id '{nid}' must equal filename '{path.stem}'")
                nid = path.stem
            ntype = meta.get("type")
            if ntype not in VALID_TYPES:
                errors.append(f"{rel}: type '{ntype}' not in {sorted(VALID_TYPES)}")
            if nid in nodes:
                errors.append(f"{rel}: duplicate id '{nid}'")

            node = {
                "id": nid,
                "title": meta.get("title", nid),
                "type": ntype,
                "domain": meta.get("domain", ""),
                "tags": as_list(meta.get("tags")),
                "path": rel,
                "content": body.strip(),
                "summary": summarize(body),
                "topic": meta.get("topic", ""),
            }

            if ntype == "topic":
                # Split the document into sections; the part before the first section is the intro.
                matches = list(SECTION.finditer(body))
                intro = body[: matches[0].start()] if matches else body
                node["summary"] = summarize(re.sub(r"^# .*$", "", intro, flags=re.M))
                node["sections"] = []
                for target in WIKILINK.findall(intro):
                    link_sites.append((nid, target.strip()))
                    raw_edges.append((nid, target.strip(), "mention"))
                for i, sm in enumerate(matches):
                    end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
                    sid, stitle, smeta = sm.group(1), sm.group(2).strip(), parse_section_meta("section: " + sm.group(3))
                    block = body[sm.start():end].strip()
                    if smeta.get("section") != sid:
                        errors.append(f"{rel}: section anchor '{sid}' does not match its comment '{smeta.get('section')}'")
                    if sid in nodes or sid in aliases:
                        errors.append(f"{rel}: duplicate section id '{sid}'")
                    nodes[sid] = {
                        "id": sid, "title": stitle, "type": "concept", "domain": node["domain"],
                        "tags": as_list(smeta.get("tags")), "path": rel, "content": block,
                        "summary": summarize(block), "topic": nid,
                    }
                    for aid in as_list(smeta.get("alias")):
                        if aid in nodes or aid in aliases:
                            errors.append(f"{rel}: duplicate alias id '{aid}'")
                        aliases[aid] = sid
                    node["sections"].append(sid)
                    raw_edges.append((nid, sid, "contains"))
                    for target in WIKILINK.findall(block):
                        link_sites.append((sid, target.strip()))
                        raw_edges.append((sid, target.strip(), "mention"))
                    for field, etype in (("prerequisites", "prerequisite"), ("related", "related"), ("sources", "source")):
                        for target in as_list(smeta.get(field)):
                            link_sites.append((sid, target))
                            raw_edges.append((sid, target, etype))
                if not matches:
                    warnings.append(f"{rel}: topic has no sections")
            elif ntype == "question-bank":
                # Split the bank into one node per "## Q:" block.
                matches = list(QUESTION_HEADING.finditer(body))
                node["content"] = body[: matches[0].start()].strip() if matches else body.strip()
                for i, qm in enumerate(matches):
                    end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
                    block = body[qm.start():end].strip()
                    qnum, qtext = qm.group(1), qm.group(2).strip()
                    if not qnum:
                        errors.append(f"{rel}: question '{qtext[:50]}…' has no number (write '## Q<next>: …')")
                        qnum = "000"
                    qid = f"{nid}/q{qnum}"
                    if f"Q{qnum}" in qnumbers:
                        errors.append(f"{rel}: duplicate question number Q{qnum} (also in {qnumbers[f'Q{qnum}']})")
                    qnumbers[f"Q{qnum}"] = rel
                    category = re.search(r"^\*\*Category:\*\*[ \t]*(.+)$", block, re.M)
                    nodes[qid] = {
                        "id": qid,
                        "title": qtext,
                        "type": "question",
                        "qno": f"Q{qnum}",
                        "category": category.group(1).strip() if category else "General",
                        "domain": node["domain"],
                        "tags": [],
                        "path": rel,
                        "content": block,
                    }
                    raw_edges.append((nid, qid, "contains"))
                    for target in WIKILINK.findall(block):
                        target = target.strip()
                        link_sites.append((qid, target))
                        raw_edges.append((qid, target, "tests"))
                    if "**Topics:**" not in block:
                        warnings.append(f"{rel}: question '{qtext[:50]}…' has no **Topics:** line")
            else:
                for target in WIKILINK.findall(body):
                    target = target.strip()
                    link_sites.append((nid, target))
                    raw_edges.append((nid, target, "mention"))

            for field, etype in (("prerequisites", "prerequisite"), ("related", "related"), ("sources", "source")):
                for target in as_list(meta.get(field)):
                    link_sites.append((nid, target))
                    raw_edges.append((nid, target, etype))

            nodes[nid] = node

    for aid in aliases:
        if aid in nodes:
            errors.append(f"{nodes[aid]['path']}: id '{aid}' is also declared as an alias")
    # Links to a merged section point at the section that now holds it.
    raw_edges = [(aliases.get(s, s), aliases.get(t, t), ty) for s, t, ty in raw_edges]

    # Domain membership edges (concept -> its map).
    map_ids = {n["id"] for n in nodes.values() if n["type"] == "map"}
    for n in list(nodes.values()):
        if n["type"] in ("topic", "question-bank") and n["domain"]:
            mid = f"map-{n['domain']}"
            if mid in map_ids:
                raw_edges.append((n["id"], mid, "domain"))
            else:
                errors.append(f"{n['path']}: domain '{n['domain']}' has no map '{mid}.md'")

    # Every topic document must be listed in its track map.
    for n in nodes.values():
        if n["type"] != "topic":
            continue
        track_map = nodes.get(f"map-{n['domain']}")
        if track_map and f"[[{n['id']}]]" not in track_map["content"]:
            errors.append(f"{n['path']}: topic is not listed in map-{n['domain']}.md")

    # Reading order: tracks as listed in home.md, chapters as listed in each track map.
    # A section's prerequisites must appear earlier in that order.
    home = nodes.get("home")
    if home:
        position: dict[str, int] = {}
        for mid in WIKILINK.findall(home["content"]):
            track_map = nodes.get(mid.strip())
            if not track_map or track_map.get("domain") in ("", None):
                continue
            for tid in WIKILINK.findall(track_map["content"]):
                topic = nodes.get(tid.strip())
                if topic and topic["type"] == "topic":
                    for sid in topic.get("sections", []):
                        position.setdefault(sid, len(position))
        for s, t, ty in raw_edges:
            if ty == "prerequisite" and s in position and t in position and position[t] > position[s]:
                warnings.append(f"{nodes[s]['path']}: prerequisite [[{t}]] of '{s}' comes later in the reading order")

    # Broken links. Source notes (sources/) are local-only, so a missing src-* note is not an error.
    for src, target in link_sites:
        if target not in nodes and target not in aliases and not target.startswith(("src-", "qb-")):
            errors.append(f"{nodes[src]['path']}: broken link [[{target}]] (in {src})")

    # Deduplicate edges: one edge per unordered pair, keep highest-priority type.
    best: dict[tuple[str, str], tuple[str, str, str]] = {}
    for s, t, ty in raw_edges:
        if s == t or s not in nodes or t not in nodes:
            continue
        key = tuple(sorted((s, t)))
        cur = best.get(key)
        if cur is None or EDGE_PRIORITY.index(ty) < EDGE_PRIORITY.index(cur[2]):
            best[key] = (s, t, ty)
    links = [{"source": s, "target": t, "type": ty} for s, t, ty in best.values()]

    degree = {nid: 0 for nid in nodes}
    for link in links:
        if link["type"] != "domain":
            degree[link["source"]] += 1
            degree[link["target"]] += 1
    for nid, n in nodes.items():
        n["degree"] = degree[nid]
        if n["type"] == "concept" and degree[nid] == 0:
            warnings.append(f"{n['path']}: orphan concept (no links)")

    all_nodes = list(nodes.values())

    # Public site (docs/, uploaded): no sources and no interview questions.
    hidden = {n["id"] for n in all_nodes if n["type"] in ("source", "question", "question-bank")}
    public_nodes = []
    for n in all_nodes:
        if n["id"] in hidden:
            continue
        n = dict(n)
        n["content"] = re.sub(r" \| sources: \[[^\]]*\]", "", n["content"])
        n["content"] = re.sub(r"\s*\*\*Questions:\*\*[^\n]*", "", n["content"])
        n["content"] = re.sub(r"\[\[(src|qb)-[^\]]*\]\]", "", n["content"])
        public_nodes.append(n)
    public_links = [l for l in links if l["source"] not in hidden and l["target"] not in hidden]
    write_site({"nodes": public_nodes, "links": public_links, "aliases": aliases}, OUT_DIR)

    # Local site (local/, git-ignored): everything except sources, for the user's own study.
    local_nodes = [n for n in all_nodes if n["type"] != "source"]
    local_links = [l for l in links if nodes[l["source"]]["type"] != "source" and nodes[l["target"]]["type"] != "source"]
    local_graph = {"nodes": local_nodes, "links": local_links, "aliases": aliases}
    password = os.environ.get("KB_QUESTIONS_PASSWORD", "")
    if password:
        local_graph = lock_questions(local_graph, password)
        print("questions: encrypted with KB_QUESTIONS_PASSWORD in local/index.html")
    write_site(local_graph, LOCAL_DIR)
    write_interview_handout(local_graph, password)
    print(f"wrote {OUT_DIR.name}/index.html (public, no questions) and {LOCAL_DIR.name}/index.html (local only, with questions)")

    if qnumbers:
        print(f"questions: {len(qnumbers)} numbered, next free number Q{max(int(k[1:]) for k in qnumbers) + 1:03d}")
    counts: dict[str, int] = {}
    for n in nodes.values():
        counts[n["type"]] = counts.get(n["type"], 0) + 1
    print("nodes:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())), f"| links={len(links)}")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if (strict and errors) else 0


if __name__ == "__main__":
    sys.exit(main())
