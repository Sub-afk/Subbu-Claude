"""Helpers to read a factsheet portfolio table out of a PDF page using word positions.

Each holding's percentage is used as an anchor: name and industry text lines are attached to
the first percentage at or just below them (factsheets print the percentage on the last line of
a wrapped row). Totals are checked by the caller against the subtotal printed on the page."""
import re

import pdfplumber

NUM = re.compile(r"^-?\d{1,3}\.\d{2}%?$")


def _words(chars, gap=1.6):
    """Group characters into words ourselves: some factsheets interleave the character
    stream of neighbouring rows, which breaks pdfplumber's own word grouping."""
    rows = {}
    for c in chars:
        key = next((k for k in rows if abs(k - c["top"]) < 1.5), c["top"])
        rows.setdefault(key, []).append(c)
    words = []
    for top, cs in rows.items():
        cur = None
        for c in sorted(cs, key=lambda c: c["x0"]):
            if c["text"].isspace():
                cur = None
                continue
            if cur and c["x0"] - cur["x1"] <= gap:
                cur["text"] += c["text"]
                cur["x1"] = c["x1"]
            else:
                cur = {"text": c["text"], "x0": c["x0"], "x1": c["x1"], "top": top}
                words.append(cur)
    return words


def _lines(words):
    rows = {}
    for w in sorted(words, key=lambda w: (round(w["top"]), w["x0"])):
        key = next((k for k in rows if abs(k - w["top"]) < 2.5), w["top"])
        rows.setdefault(key, []).append(w)
    return sorted((k, " ".join(x["text"] for x in sorted(v, key=lambda x: x["x0"]))) for k, v in rows.items())


def read_block(pdf_path, page_no, name_x, pct_x, y, ind_x=None, tol=6.0, nearest=False):
    """Return [(name, industry, pct)] for one column block.
    name_x/pct_x/ind_x are (x0, x1) ranges in PDF points, y is (top, bottom)."""
    with pdfplumber.open(pdf_path) as pdf:
        words = _words(pdf.pages[page_no - 1].chars)
    inside = lambda w, xr: xr[0] <= w["x0"] < xr[1] and y[0] <= w["top"] < y[1]
    anchors = sorted((w["top"], float(w["text"].rstrip("%"))) for w in words
                     if inside(w, pct_x) and NUM.match(w["text"]))
    out = [[[], [], p] for _, p in anchors]

    def attach(xr, slot):
        for top, text in _lines([w for w in words if inside(w, xr)]):
            if nearest:  # tightly spaced tables: closest percentage wins, ties go to the one below
                idx = min(range(len(anchors)), key=lambda i: (abs(anchors[i][0] - top), anchors[i][0] < top)) if anchors else None
            else:
                idx = next((i for i, (at, _) in enumerate(anchors) if at >= top - tol), None)
            if idx is not None:
                out[idx][slot].append(text)

    attach(name_x, 0)
    if ind_x:
        attach(ind_x, 1)
    return [(" ".join(n).replace("•", "").strip(), " ".join(i).strip(), p) for n, i, p in out]


def read_sectioned(pdf_path, page_no, columns, y, header_font, current=None):
    """For factsheets (ICICI Prudential) that print a bold industry header row followed by
    its holdings, one row per line. Returns [(name, industry, pct)] for holdings only and
    [(industry, pct)] for the headers so the caller can check the sums."""
    with pdfplumber.open(pdf_path) as pdf:
        chars = pdf.pages[page_no - 1].chars
    holdings, headers = [], []
    for x0, x1 in columns:
        cs = [c for c in chars if x0 <= c["x0"] < x1 and y[0] <= c["top"] < y[1]]
        pending = ""  # first line of a holding name that wraps onto the next line
        for top, line in sorted(_group_lines(cs).items()):
            text = _join(line).strip()
            m = re.match(r"^(.*?)\s*(-?\d+\.\d+)%$", text)
            if not m:
                pending = (pending + " " + text.replace("•", "").strip()).strip()
                continue
            name, pct = (pending + " " + m.group(1).replace("•", "").strip()).strip(), float(m.group(2))
            pending = ""
            first = next(c for c in line if c["text"].isalpha())
            if header_font in first["fontname"]:
                current = name
                headers.append((name, pct))
            else:
                holdings.append((name, current or "", pct))
    return holdings, headers, current


def _join(line):
    out, prev = "", None
    for c in line:
        if prev is not None and c["x0"] - prev["x1"] > 1.2 and not c["text"].isspace() and not out.endswith(" "):
            out += " "
        out += c["text"]
        prev = c
    return out


def _group_lines(chars):
    rows = {}
    for c in sorted(chars, key=lambda c: c["x0"]):
        key = next((k for k in rows if abs(k - c["top"]) < 1.5), c["top"])
        rows.setdefault(key, []).append(c)
    return rows
