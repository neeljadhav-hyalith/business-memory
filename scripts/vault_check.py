#!/usr/bin/env python3
"""vault_check: read-only size and structure check for a business-memory vault.

Usage:
  python vault_check.py <vault_folder> [--skill path/to/SKILL.md]

Reads the caps from the CAPS table in SKILL.md (their only home), then checks:
the size of 00-state.md and every operating card against its cap, rows over
their word caps, rows untouched too long, 2 versions of a file side by side,
router pointers that name a version or match no file, and cards no router row
reaches. Prints 1 table, worst first, and the counts. Changes nothing.
Exit code 1 if anything FAILs.
MIT licence. Built by Neel Jadhav, Hyalith AI (hyalith.ai/resources)."""
import argparse, datetime, os, re, sys

VER = re.compile(r"_v\d+(?:\.\d+)?(?=\.[A-Za-z0-9]+$)")
ROW_ID = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9-]+$")
rows = []

def rec(status, where, check, found=""):
    rows.append((status, where, check, found))

def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

def load_caps(skill_path):
    caps = {}
    for line in read(skill_path).splitlines():
        m = re.match(r"\|\s*`(\w+)`\s*\|[^|]*\|\s*([\d,]+)\s*\|", line)
        if m:
            caps[m.group(1)] = int(m.group(2).replace(",", ""))
    need = ["state_item_words", "state_next_words", "state_file_bytes", "card_bytes", "headroom_bytes", "ageing_days"]
    missing = [k for k in need if k not in caps]
    if missing:
        sys.exit(f"CAPS table in {skill_path} is missing: {', '.join(missing)}")
    return caps

def size_check(path, label, cap, headroom):
    n = os.path.getsize(path)
    if n > cap:
        rec("FAIL", label, "Size over cap", f"{n:,} of {cap:,} bytes ({n / cap:.1f}x)")
    elif cap - n < headroom:
        rec("WARN", label, "Size near cap", f"{n:,} of {cap:,} bytes, {cap - n} left")
    return n

def table_rows(text):
    """Yield (header_cells, row_cells) for every Markdown table row whose first cell is a row id."""
    header = None
    for line in text.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if cells and ROW_ID.match(cells[0]):
            yield header, cells

def col(header, *names):
    for i, h in enumerate(header):
        if any(h.startswith(n) for n in names):
            return i
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--skill", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SKILL.md"))
    a = ap.parse_args()
    root = os.path.abspath(a.vault)
    ctx = os.path.join(root, "Context")
    if not os.path.isdir(ctx):
        sys.exit(f"No Context folder in {root}")
    caps = load_caps(a.skill)
    head = caps["headroom_bytes"]
    today = datetime.date.today()

    # every file, split live and archived
    live, archived, md_total = [], 0, 0
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        rel_d = os.path.relpath(d, root)
        in_arch = any(p.lower() in ("_archive", "00_archive", "_to_delete") for p in rel_d.split(os.sep))
        for f in files:
            if f.lower().endswith(".md"):
                md_total += 1
            if in_arch:
                archived += 1
            else:
                live.append(os.path.relpath(os.path.join(d, f), root))

    # 1. the state file
    state_p = os.path.join(ctx, "00-state.md")
    n_rows, status_count = 0, {}
    if not os.path.isfile(state_p):
        rec("FAIL", "Context\\00-state.md", "File missing")
    else:
        size_check(state_p, "Context\\00-state.md", caps["state_file_bytes"], head)
        for header, cells in table_rows(read(state_p)):
            n_rows += 1
            rid = cells[0]
            ci, cn, cs, cm = col(header, "item"), col(header, "next"), col(header, "status"), col(header, "moved")
            if cs is not None and cs < len(cells):
                status_count[cells[cs]] = status_count.get(cells[cs], 0) + 1
            for c, key, name in ((ci, "state_item_words", "item"), (cn, "state_next_words", "next / blocker")):
                if c is not None and c < len(cells):
                    w = len(cells[c].split())
                    if w > caps[key]:
                        rec("WARN", rid, f"Row {name} over cap", f"{w} words, cap {caps[key]}")
            if cm is not None and cm < len(cells):
                m = re.search(r"\d{4}-\d{2}-\d{2}", cells[cm])
                st = cells[cs].upper() if cs is not None and cs < len(cells) else ""
                if m and st not in ("CONFIRM", "PARKED"):
                    age = (today - datetime.date.fromisoformat(m.group(0))).days
                    if age >= caps["ageing_days"]:
                        rec("WARN", rid, "Row untouched", f"{age} days, move to CONFIRM")

    # 2. settled: no cap, size is a trend line
    settled_p = os.path.join(ctx, "00-settled.md")
    if not os.path.isfile(settled_p):
        rec("FAIL", "Context\\00-settled.md", "File missing")

    # 3. cards and side-by-side versions in Context
    cards, stems = [], {}
    for rel in live:
        if not rel.startswith("Context" + os.sep):
            continue
        name = os.path.basename(rel)
        if VER.search(name):
            stem = VER.sub("", re.sub(r"^\d{4}-\d{2}-\d{2}_", "", name))
            stems.setdefault((os.path.dirname(rel), stem), []).append(name)
        if re.search(r"card_v\d", name):
            cards.append(rel)
            size_check(os.path.join(root, rel), rel, caps["card_bytes"], head)
    for (d, stem), names in stems.items():
        # dated files that all carry the same version are separate records, not 2 versions
        if len({VER.search(n).group(0) for n in names}) > 1:
            rec("FAIL", d or "Context", "2 versions side by side", f"{len(names)} files for {stem}: retire the lower")

    # 4. router pointers
    index_p = os.path.join(ctx, "00-index.md")
    if not os.path.isfile(index_p):  # accept another 00-*index*.md name
        alt = sorted(f for f in os.listdir(ctx) if re.match(r"00-.*index.*\.md$", f))
        if alt:
            index_p = os.path.join(ctx, alt[0])
    router_rows = 0
    if not os.path.isfile(index_p):
        rec("FAIL", "Context\\00-index.md", "File missing")
    else:
        idx = read(index_p)
        in_router = False
        for line in idx.splitlines():
            if line.startswith("|") and not re.match(r"^\|\s*-", line):
                if in_router:
                    router_rows += 1
                in_router = True
            elif not line.startswith("|"):
                in_router = False
        names_live = [os.path.basename(p) for p in live]
        idx_name = "Context\\" + os.path.basename(index_p)
        patterns = []
        for ptr in re.findall(r"`([^`]+\.(?:md|csv|xlsx|txt))`", idx):
            base = os.path.basename(ptr.replace("\\", "/"))
            if "<" in base or "YYYY" in base:
                continue  # a naming template for a new file, not a pointer
            if "*" not in base and VER.search(base):
                rec("WARN", idx_name, "Pointer names a version", f"{base}: use a pattern")
            if "*" in base:
                rx = re.compile("^" + ".*".join(re.escape(p) for p in base.split("*")) + "$", re.I)
                patterns.append(rx)
                if not any(rx.match(n) for n in names_live):
                    rec("FAIL", idx_name, "Pointer matches no file", base)
        for rel in cards:
            stem = VER.sub("", re.sub(r"^\d{4}-\d{2}-\d{2}_", "", os.path.basename(rel)))
            stem = os.path.splitext(stem)[0]
            if stem not in idx and not any(rx.match(os.path.basename(rel)) for rx in patterns):
                rec("WARN", rel, "Card not in the router", "add a row with a pattern pointer")

    # report
    order = {"FAIL": 0, "WARN": 1, "OK": 2}
    rows.sort(key=lambda r: order.get(r[0], 3))
    print("| Result | Where | Check | Found |\n|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    fails = sum(r[0] == "FAIL" for r in rows)
    warns = sum(r[0] == "WARN" for r in rows)
    st = ", ".join(f"{v} {k}" for k, v in sorted(status_count.items(), key=lambda x: -x[1]))
    print()
    print(f"Markdown files: {md_total:,} | live files: {len(live):,} | archived files: {archived:,}")
    print(f"Open rows: {n_rows}" + (f" ({st})" if st else "") + f" | router rows: {router_rows} | cards: {len(cards)}")
    if os.path.isfile(state_p):
        print(f"00-state.md: {os.path.getsize(state_p):,} of {caps['state_file_bytes']:,} bytes")
    if os.path.isfile(settled_p):
        print(f"00-settled.md: {os.path.getsize(settled_p):,} bytes (no cap, trend only)")
    print(f"{fails} failures, {warns} warnings")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
