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
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTE_DIRS = ["maps", "topics", "questions", "sources"]
TEMPLATE = ROOT / "scripts" / "viewer_template.html"
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
        payload = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
        html = TEMPLATE.read_text(encoding="utf-8").replace("/*__GRAPH_DATA__*/null", payload)
        head = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
        (out_dir / "index.html").write_text(head + html, encoding="utf-8")


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value]


def main() -> int:
    strict = "--strict" in sys.argv
    errors: list[str] = []
    warnings: list[str] = []

    nodes: dict[str, dict] = {}
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
                    if sid in nodes:
                        errors.append(f"{rel}: duplicate section id '{sid}'")
                    nodes[sid] = {
                        "id": sid, "title": stitle, "type": "concept", "domain": node["domain"],
                        "tags": as_list(smeta.get("tags")), "path": rel, "content": block,
                        "summary": summarize(block), "topic": nid,
                    }
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
                    nodes[qid] = {
                        "id": qid,
                        "title": qtext,
                        "type": "question",
                        "qno": f"Q{qnum}",
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

    # Broken links. Source notes (sources/) are local-only, so a missing src-* note is not an error.
    for src, target in link_sites:
        if target not in nodes and not target.startswith(("src-", "qb-")):
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
    write_site({"nodes": public_nodes, "links": public_links}, OUT_DIR)

    # Local site (local/, git-ignored): everything except sources, for the user's own study.
    local_nodes = [n for n in all_nodes if n["type"] != "source"]
    local_links = [l for l in links if nodes[l["source"]]["type"] != "source" and nodes[l["target"]]["type"] != "source"]
    local_graph = {"nodes": local_nodes, "links": local_links}
    password = os.environ.get("KB_QUESTIONS_PASSWORD", "")
    if password:
        local_graph = lock_questions(local_graph, password)
        print("questions: encrypted with KB_QUESTIONS_PASSWORD in local/index.html")
    write_site(local_graph, LOCAL_DIR)
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
