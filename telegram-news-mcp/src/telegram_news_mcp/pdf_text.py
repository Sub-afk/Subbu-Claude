"""PDF text extraction plus cheap heuristics that help an LLM navigate a newspaper PDF.

A newspaper PDF can be 20-60 pages and several hundred thousand characters,
which is too much to hand to a model in one go. So we extract once, cache the
result as JSON, and expose three views: a per-page overview (likely headlines),
full text for a page range, and keyword search.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from pypdf import PdfReader

# Pages with fewer extractable characters than this are probably scanned images.
SCANNED_PAGE_CHARS = 40


@dataclass
class ExtractedPdf:
    source: str
    pages: list[str]

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def looks_scanned(self) -> bool:
        if not self.pages:
            return True
        empty = sum(1 for p in self.pages if len(p.strip()) < SCANNED_PAGE_CHARS)
        return empty / len(self.pages) > 0.6


def clean_text(text: str) -> str:
    text = text.replace("­", "")  # soft hyphens
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # re-join hyphenated line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(pdf_path: Path) -> ExtractedPdf:
    """Extract text from a PDF, caching the result next to it as <name>.json."""
    cache = pdf_path.with_suffix(".json")
    if cache.is_file() and cache.stat().st_mtime >= pdf_path.stat().st_mtime:
        data = json.loads(cache.read_text(encoding="utf-8"))
        return ExtractedPdf(**data)

    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(clean_text(page.extract_text() or ""))
        except Exception:  # a single malformed page shouldn't sink the whole paper
            pages.append("")
    extracted = ExtractedPdf(source=pdf_path.name, pages=pages)
    cache.write_text(json.dumps(asdict(extracted), ensure_ascii=False), encoding="utf-8")
    return extracted


def _is_headline(line: str) -> bool:
    line = line.strip()
    if not 15 <= len(line) <= 120:
        return False
    if line.endswith((",", ";")) or re.search(r"\b(page|continued|contd)\b\.?\s*\d*$", line, re.I):
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", line)
    if len(words) < 3:
        return False
    if line.isupper():
        return True
    # Title Case: most words longer than 3 letters start with a capital.
    long_words = [w for w in words if len(w) > 3]
    if long_words and sum(w[0].isupper() for w in long_words) / len(long_words) >= 0.75:
        return not line.endswith(".")
    return False


def headline_candidates(page_text: str, limit: int = 8) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for line in page_text.splitlines():
        if _is_headline(line):
            key = line.strip().lower()
            if key not in seen:
                seen.add(key)
                out.append(line.strip())
        if len(out) >= limit:
            break
    return out


def topic_hits(text: str, topics: list[str]) -> dict[str, int]:
    hits = {}
    for topic in topics:
        n = len(re.findall(rf"\b{re.escape(topic)}(?:s|es)?\b", text, re.I))  # allow plurals
        if n:
            hits[topic] = n
    return hits


def overview(pdf: ExtractedPdf, topics: list[str], headlines_per_page: int = 8) -> list[dict]:
    """One entry per page: likely headlines, a short opening snippet and topic hits."""
    rows = []
    for i, text in enumerate(pdf.pages, start=1):
        heads = headline_candidates(text, headlines_per_page)
        snippet = " ".join(text.split())[:240]
        rows.append(
            {
                "page": i,
                "chars": len(text),
                "headlines": heads,
                "opening": snippet if not heads else None,
                "topic_hits": topic_hits(text, topics),
            }
        )
    return rows


def read_pages(pdf: ExtractedPdf, start: int, end: int, max_chars: int) -> tuple[str, bool]:
    """Return text of pages [start, end] (1-based, inclusive) up to max_chars."""
    start = max(1, start)
    end = min(pdf.page_count, end)
    parts = []
    total = 0
    truncated = False
    for n in range(start, end + 1):
        chunk = f"=== Page {n} ===\n{pdf.pages[n - 1]}\n"
        if total + len(chunk) > max_chars:
            parts.append(chunk[: max(0, max_chars - total)])
            truncated = True
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts), truncated


def search(pdf: ExtractedPdf, query: str, context_chars: int = 400, limit: int = 15) -> list[dict]:
    """Case-insensitive search; every whitespace-separated term must appear in the paragraph."""
    terms = [t for t in query.lower().split() if t]
    if not terms:
        return []
    results = []
    for page_no, text in enumerate(pdf.pages, start=1):
        for para in re.split(r"\n\s*\n", text):
            flat = " ".join(para.split())
            low = flat.lower()
            if all(t in low for t in terms):
                idx = low.find(terms[0])
                lo = max(0, idx - context_chars // 2)
                results.append({"page": page_no, "excerpt": flat[lo : lo + context_chars]})
                if len(results) >= limit:
                    return results
    return results
