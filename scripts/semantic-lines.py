#!/usr/bin/env python3
"""Reflow Markdown prose to one sentence per line (semantic line breaks).

Usage:
    scripts/semantic-lines.py FILE [FILE...]        rewrite files in place
    scripts/semantic-lines.py --check FILE [...]    exit 1 if any line holds 2+ sentences

Leaves headings, lists, block quotes' markers, code fences, tables and HTML
comments (TODO markers) untouched. Paragraph breaks (blank lines) are kept.
Rendered Markdown looks identical: single newlines inside a paragraph render as spaces.
"""
import re
import sys

ABBREV = {"mr", "mrs", "ms", "dr", "st", "jr", "sr", "prof", "vs", "etc", "mt", "ft", "no", "e.g", "i.e"}
# sentence end: . ! ? or ellipsis, optionally followed by closing quotes/brackets
# or emphasis markers (*text.* or _text._), then whitespace, then something that
# can start a sentence (possibly opening with quotes/brackets/emphasis)
SPLIT_RE = re.compile(r'([.!?…]+["\'”’)\]*_]*)\s+(?=["\'“‘(\[*_]*[A-Z0-9])')


def split_sentences(text):
    parts, last = [], 0
    for m in SPLIT_RE.finditer(text):
        word = re.findall(r"([A-Za-z.]+)[.]$", text[last:m.end(1)].split(" ")[-1])
        if word and word[0].lower().rstrip(".") in ABBREV:
            continue
        if word and re.fullmatch(r"(?:[A-Z]\.)*[A-Z]", word[0]):
            continue  # initials: "J. R. Smith", "T.S. Eliot"
        parts.append(text[last:m.end(1)].strip())
        last = m.end()
    parts.append(text[last:].strip())
    return [p for p in parts if p]


def is_structural(line):
    s = line.lstrip()
    return (not s or s.startswith(("#", "|", "```", "~~~", "<!--", "---", "- ", "* ", "+ ", ">"))
            or re.match(r"\d+[.)] ", s) is not None)


def reflow(text):
    out, para, in_fence, in_comment = [], [], False, False

    def flush():
        if para:
            out.extend(split_sentences(" ".join(l.strip() for l in para)))
            para.clear()

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith(("```", "~~~")):
            flush(); in_fence = not in_fence; out.append(line); continue
        if in_fence or in_comment:
            out.append(line)
            if in_comment and "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            flush(); out.append(line)
            in_comment = "-->" not in s
            continue
        if is_structural(line):
            flush(); out.append(line); continue
        para.append(line)
    flush()
    return "\n".join(out)


def main(argv):
    check = "--check" in argv
    files = [a for a in argv if a != "--check"]
    if not files:
        print(__doc__); return 2
    bad = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        new = reflow(text)
        if check:
            if new != text:
                bad += 1
                print(f"{f}: not one-sentence-per-line")
        elif new != text:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(new)
            print(f"reflowed {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
