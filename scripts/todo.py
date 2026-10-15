#!/usr/bin/env python3
"""TODO marker tool for the fiction workbench.

Marker syntax (HTML comments, invisible when Markdown is rendered):

    <!-- TODO t3 [next]: directive -->        change the paragraph after the marker
    <!-- TODO t3 [prev]: directive -->        change the paragraph before the marker
    <!-- TODO t3 [insert]: directive -->      write new text at the marker
    <!-- TODO t3 [start]: directive -->       begin an explicit range ...
    <!-- TODO t3 [end] -->                    ... end of that range
    <!-- TODO: directive -->                  no id / no scope: scope = auto (the paragraphs either side)
    <!-- AGENT-Q t3: question -->             agent question left for the author

Subcommands:
    list [paths...]                    list open TODOs and AGENT-Qs (working tree)
    ids  [paths...]                    assign ids (never reused; numbering continues past git history)
    lint [--staged] [paths...]         reject malformed, duplicate, or unmatched markers
    check-resolved [paths...]          exit 1 if a TODO is neither resolved, awaiting an AGENT-Q answer,
                                       nor marked "Author: skip" in plan/todo-plan.md (working tree)
    check-ids t3,t4                    staged commit vs HEAD: each id must exist at HEAD and be gone from
                                       the index, or carry an AGENT-Q there (awaiting the author)
    check-scope BASE [HEAD]            every manuscript line changed BASE..HEAD must lie inside the scope
                                       of a TODO present at BASE
    check-scope --staged [--ids t3]    the same for the staged commit vs HEAD, optionally for named TODOs only
    check-markers-only --staged        staged manuscript changes may only add/remove/edit comment lines
                                       (for passes that may place TODO markers but never touch prose)
"""
import os
import re
import subprocess
import sys
from dataclasses import dataclass

SCOPES = ("next", "prev", "insert", "start", "end", "auto")
TODO_RE = re.compile(
    r"<!--\s*TODO(?:\s+(?P<id>t\d+))?\s*(?:\[(?P<scope>[a-z]+)\])?\s*:?\s*(?P<text>.*?)\s*-->",
    re.S,
)
Q_RE = re.compile(r"<!--\s*AGENT-Q\s+(?P<id>t\d+)\s*:?\s*(?P<text>.*?)\s*-->", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
DEFAULT_DIRS = ["manuscript"]
PLAN = "plan/todo-plan.md"


@dataclass
class Marker:
    path: str
    line: int      # 1-based line of marker start
    end_line: int  # 1-based line of marker end (multi-line comments)
    id: str
    scope: str
    text: str
    raw: str
    start: int
    end: int


# ---------------------------------------------------------------- reading text

def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check).stdout


def md_files(paths):
    paths = paths or DEFAULT_DIRS
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                out += [os.path.join(root, f) for f in sorted(files) if f.endswith(".md")]
        elif p.endswith(".md") and os.path.exists(p):
            out.append(p)
    return sorted(out)


def snapshot(rev):
    """{path: text} for manuscript/*.md at a revision; rev ':' means the index (staged)."""
    if rev == ":":
        names = git("ls-files", "--", "manuscript").split("\n")
    else:
        if subprocess.run(["git", "rev-parse", "-q", "--verify", f"{rev}^{{commit}}"],
                          capture_output=True).returncode:
            return {}
        names = git("ls-tree", "-r", "--name-only", rev, "--", "manuscript").split("\n")
    out = {}
    for n in names:
        if n.endswith(".md"):
            out[n] = git("show", f"{rev}{n}" if rev == ":" else f"{rev}:{n}")
    return out


def working():
    out = {}
    for f in md_files([]):
        with open(f, encoding="utf-8") as fh:
            out[f] = fh.read()
    return out


def parse(path, text=None):
    if text is None:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    todos, qs = [], []
    for m in TODO_RE.finditer(text):
        scope = (m.group("scope") or "auto").lower()
        todos.append(Marker(path, text.count("\n", 0, m.start()) + 1,
                            text.count("\n", 0, m.end()) + 1, m.group("id") or "",
                            scope, " ".join(m.group("text").split()), m.group(0),
                            m.start(), m.end()))
    for m in Q_RE.finditer(text):
        qs.append(Marker(path, text.count("\n", 0, m.start()) + 1,
                         text.count("\n", 0, m.end()) + 1, m.group("id"), "question",
                         " ".join(m.group("text").split()), m.group(0), m.start(), m.end()))
    return todos, qs


def plan_skips():
    """TODO ids the author marked `Author: skip` in plan/todo-plan.md."""
    try:
        with open(PLAN, encoding="utf-8") as fh:
            plan = fh.read()
    except OSError:
        return set()
    skips = set()
    for sec in re.split(r"^## ", plan, flags=re.M)[1:]:
        m = re.match(r"(t\d+)\b", sec)
        if m and re.search(r"^Author:\s*skip\b", sec, re.M | re.I):
            skips.add(m.group(1))
    return skips


# ---------------------------------------------------------------- list / ids / lint

def cmd_list(paths):
    total = 0
    for f in md_files(paths):
        todos, qs = parse(f)
        for t in todos:
            if t.scope == "end":
                continue
            total += 1
            bad = "" if t.scope in SCOPES else "  (!! unknown scope)"
            print(f"{t.id or '??':<5} {t.scope:<7} {f}:{t.line}  {t.text}{bad}")
        for q in qs:
            print(f"{q.id:<5} {'AGENT-Q':<7} {f}:{q.line}  {q.text}")
    if total == 0:
        print("No open TODOs.")
    return 0


def ids_in_history():
    """Every TODO/AGENT-Q id that ever appeared in git history, so ids are never reused."""
    patches = git("log", "--all", "-p", "--format=", "--", "manuscript", PLAN, check=False)
    trailers = git("log", "--all", "--format=%(trailers:key=Todo,valueonly,separator=%x2C)", check=False)
    return set(re.findall(r"(?:TODO|AGENT-Q)\s+(t\d+)", patches)) | set(re.findall(r"\bt\d+\b", trailers))


def cmd_ids(paths):
    files = md_files(paths)
    used = ids_in_history()
    for f in md_files([]) + files:
        todos, qs = parse(f)
        used |= {t.id for t in todos + qs if t.id}
    n = max([int(i[1:]) for i in used] + [0])
    changed = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        todos, _ = parse(f, text)
        pending_start = None
        # number in reading order, then substitute back-to-front so offsets stay valid
        edits = []
        for t in todos:
            if t.id or t.scope == "end":
                continue  # unnamed [end] markers get their [start]'s id below
            n += 1
            edits.append((t, f"<!-- TODO t{n} [{t.scope}]: {t.text} -->"))
        for t, new in reversed(edits):
            text = text[:t.start] + new + text[t.end:]
            changed += 1
        # second pass: give unnamed [end] markers the id of the preceding [start]
        todos, _ = parse(f, text)
        out, last = [], 0
        for t in todos:
            if t.scope == "start":
                pending_start = t.id
            if t.scope == "end" and not t.id and pending_start:
                out.append(text[last:t.start] + f"<!-- TODO {pending_start} [end] -->")
                last = t.end
                changed += 1
        out.append(text[last:])
        text = "".join(out)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(f"Assigned/normalized {changed} marker(s).")
    return 0


def lint_text(path, text):
    problems = []
    todos, _ = parse(path, text)
    seen, open_start = {}, None
    for t in todos:
        where = f"{path}:{t.line}"
        if t.scope not in SCOPES:
            problems.append(f"{where} unknown scope [{t.scope}]")
        if t.scope == "start":
            if open_start:
                problems.append(f"{where} [start] {t.id} opens before {open_start} is closed")
            open_start = t.id or "??"
        elif t.scope == "end":
            if not open_start:
                problems.append(f"{where} [end] without a matching [start]")
            elif t.id and open_start not in ("??", t.id):
                problems.append(f"{where} [end] {t.id} closes [start] {open_start}")
            open_start = None
        if t.id and t.scope != "end":
            if t.id in seen:
                problems.append(f"{where} duplicate id {t.id} (also {seen[t.id]})")
            seen[t.id] = where
    if open_start:
        problems.append(f"{path}: [start] {open_start} is never closed by [end]")
    stripped = COMMENT_RE.sub("", text)
    if "<!--" in stripped or "-->" in stripped:
        problems.append(f"{path}: unclosed or stray HTML comment delimiter")
    return problems


def cmd_lint(args):
    staged = "--staged" in args
    files = snapshot(":") if staged else {f: open(f, encoding="utf-8").read()
                                           for f in md_files([a for a in args if a != "--staged"])}
    problems = [p for f, t in sorted(files.items()) for p in lint_text(f, t)]
    if problems:
        print("TODO marker problems:\n  " + "\n  ".join(problems))
        return 1
    return 0


# ---------------------------------------------------------------- resolution

def cmd_check_resolved(paths):
    problems, skips = [], plan_skips()
    for f in md_files(paths):
        todos, qs = parse(f)
        qids = {q.id for q in qs}
        for t in todos:
            if t.scope == "end" or (t.id and (t.id in qids or t.id in skips)):
                continue
            problems.append(f"{f}:{t.line} TODO {t.id or '??'} unresolved, no AGENT-Q, not skipped in the plan")
    if problems:
        print("Unresolved TODOs:\n  " + "\n  ".join(problems))
        return 1
    print("Every TODO is resolved, awaiting an author answer (AGENT-Q), or skipped by the author.")
    return 0


def markers(snap):
    """{id: (path, line)} for open TODOs and {id} for AGENT-Qs in a snapshot."""
    todos, qids = {}, set()
    for f, text in snap.items():
        ts, qs = parse(f, text)
        todos.update({t.id: (f, t.line) for t in ts if t.id and t.scope != "end"})
        qids |= {q.id for q in qs}
    return todos, qids


def cmd_check_ids(ids):
    """Compare the staged commit with HEAD, never the working copy."""
    wanted = [i.strip() for i in ",".join(ids).split(",") if i.strip()]
    before, _ = markers(snapshot("HEAD"))
    after, qids = markers(snapshot(":"))
    problems = []
    for i in wanted:
        if i not in before:
            problems.append(f"{i}: no such open TODO at HEAD")
        elif i in after and i in qids:
            print(f"{i}: awaiting the author's answer (AGENT-Q) — not resolved")
        elif i in after:
            f, line = after[i]
            problems.append(f"{f}:{line} TODO {i} is still open in the staged text")
        else:
            print(f"{i}: resolved")
    if problems:
        print("\n".join(problems))
        return 1
    return 0


# ---------------------------------------------------------------- scope

def paragraph_bounds(lines, idx):
    """Return (start, end) 0-based inclusive bounds of the paragraph containing idx."""
    s = idx
    while s > 0 and lines[s - 1].strip():
        s -= 1
    e = idx
    while e < len(lines) - 1 and lines[e + 1].strip():
        e += 1
    return s, e


def para_after(lines, b):
    """1-based (start, end) of the paragraph after 1-based line b, or None."""
    i = b
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None
    s, e = paragraph_bounds(lines, i)
    return s + 1, e + 1


def para_before(lines, a):
    i = a - 2
    while i >= 0 and not lines[i].strip():
        i -= 1
    if i < 0:
        return None
    s, e = paragraph_bounds(lines, i)
    return s + 1, e + 1


def allowed_ranges(text, ids=None):
    """1-based inclusive line ranges in the BASE text that may change: each marker itself plus its scope.
    With ids, only those TODOs (and their AGENT-Qs) authorize changes."""
    lines = text.split("\n")
    todos, qs = parse("", text)
    ranges, starts = [], {}
    for t in todos + qs:
        if ids is not None and t.id not in ids:
            continue
        a, b = t.line, t.end_line
        # the marker itself, plus one blank line either side so removing it can tidy the spacing
        lo = a - 1 if a >= 2 and not lines[a - 2].strip() else a
        hi = b + 1 if b < len(lines) and not lines[b].strip() else b
        ranges.append((lo, hi))
        if t.scope == "next":
            p = para_after(lines, b)
            if p:
                ranges.append((a, p[1]))
        elif t.scope == "prev":
            p = para_before(lines, a)
            if p:
                ranges.append((p[0], b))
        elif t.scope == "start":
            starts[t.id] = a
        elif t.scope == "end" and t.id in starts:
            ranges.append((starts[t.id], b))
        elif t.scope == "auto":
            p, q = para_before(lines, a), para_after(lines, b)
            ranges.append((p[0] if p else a, q[1] if q else b))
    return ranges


def file_hunks(diff):
    """Yield (old_path, new_path, old_start, old_count, new_start, new_count) from a -U0 diff."""
    old = new = None
    in_header = False
    for row in diff.splitlines():
        if row.startswith("diff --git "):
            old = new = None
            in_header = True
        elif in_header and row.startswith("--- "):
            old = None if row == "--- /dev/null" else row[6:]
        elif in_header and row.startswith("+++ "):
            new = None if row == "+++ /dev/null" else row[6:]
        elif row.startswith("@@"):
            in_header = False
            m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", row)
            yield (old, new, int(m.group(1)), int(m.group(2) or 1),
                   int(m.group(3)), int(m.group(4) or 1))


def manuscript_diff(base, head):
    args = ["diff", "-U0", "-M", "--no-color"]
    args += ["--cached", base] if head == ":" else [base, head]
    return git(*args, "--", "manuscript")


def scope_violations(base, head, ids=None):
    base_snap = snapshot(base)
    out = []
    for old, new, o_start, o_count, n_start, n_count in file_hunks(manuscript_diff(base, head)):
        if old is None:
            out.append(f"{new}: new file is outside any TODO scope")
            continue
        if new is None:
            out.append(f"{old}: file deleted, outside any TODO scope")
            continue
        ranges = allowed_ranges(base_snap.get(old, ""), ids)
        inside = lambda n: any(lo <= n <= hi for lo, hi in ranges)
        if o_count == 0:
            # pure insertion after base line o_start: allowed at the edge of or inside a scope
            if not (inside(o_start) or inside(o_start + 1)):
                out.append(f"{old}: text inserted after base line {o_start}, outside any TODO scope")
            continue
        bad = [n for n in range(o_start, o_start + o_count) if not inside(n)]
        if bad:
            out.append(f"{old}: base line(s) {bad[0]}–{bad[-1]} changed outside "
                       f"{'the named TODO scope' if ids else 'any TODO scope'}")
    return out


def cmd_check_scope(args):
    ids = None
    if "--ids" in args:
        i = args.index("--ids")
        ids = {x.strip() for x in args[i + 1].split(",") if x.strip()}
        args = args[:i] + args[i + 2:]
    if "--staged" in args:
        base, head = "HEAD", ":"
    elif args:
        base, head = args[0], (args[1] if len(args) > 1 else "HEAD")
    else:
        print("usage: todo.py check-scope BASE [HEAD] | --staged [--ids t3,t4]")
        return 2
    warnings = scope_violations(base, head, ids)
    if warnings:
        print("Out-of-scope edits (revert them, or record each under Out-of-scope: in the commit body):")
        print("  " + "\n  ".join(warnings))
        return 1
    print("All manuscript edits fall inside TODO scopes.")
    return 0


def comment_only_lines(text):
    """1-based numbers of lines that are blank once HTML comments are removed."""
    blanked = COMMENT_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    return {i + 1 for i, l in enumerate(blanked.split("\n")) if not l.strip()}


def cmd_check_markers_only(_args):
    base_snap, idx_snap = snapshot("HEAD"), snapshot(":")
    out = []
    for old, new, o_start, o_count, n_start, n_count in file_hunks(manuscript_diff("HEAD", ":")):
        if old is None or new is None:
            out.append(f"{new or old}: file added or deleted")
            continue
        old_ok, new_ok = comment_only_lines(base_snap.get(old, "")), comment_only_lines(idx_snap.get(new, ""))
        if o_count and any(n not in old_ok for n in range(o_start, o_start + o_count)):
            out.append(f"{old}: prose changed near base line {o_start}")
        if n_count and any(n not in new_ok for n in range(n_start, n_start + n_count)):
            out.append(f"{new}: prose added near line {n_start}")
    if out:
        print("This pass may only add or change comment markers in manuscript/:\n  " + "\n  ".join(out))
        return 1
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    commands = {
        "list": cmd_list, "ids": cmd_ids, "lint": cmd_lint,
        "check-resolved": cmd_check_resolved, "check-ids": cmd_check_ids,
        "check-scope": cmd_check_scope, "check-markers-only": cmd_check_markers_only,
    }
    if cmd not in commands:
        print(f"unknown command: {cmd}\n{__doc__}")
        return 2
    return commands[cmd](rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
