from pathlib import Path

import pytest

from telegram_news_mcp import pdf_text
from telegram_news_mcp.config import parse_group_ref, parse_topics


def make_pdf(path: Path, pages: list[list[str]]) -> None:
    """Write a minimal text PDF (Helvetica, one line per string) without extra dependencies."""
    page_ids = []
    font_id = 3
    next_id = 4
    body_objs = {}
    for lines in pages:
        ops = ["BT", "/F1 11 Tf", "14 TL", "50 780 Td"]
        for line in lines:
            safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"({safe}) Tj T*")
        ops.append("ET")
        stream = "\n".join(ops).encode("latin-1")
        content_id, page_id = next_id, next_id + 1
        next_id += 2
        body_objs[content_id] = b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
        body_objs[page_id] = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] "
            b"/Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>" % (font_id, content_id)
        )
        page_ids.append(page_id)
    kids = " ".join(f"{p} 0 R" for p in page_ids).encode()
    body_objs[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    body_objs[2] = b"<< /Type /Pages /Kids [" + kids + b"] /Count %d >>" % len(page_ids)
    body_objs[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"

    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for oid in sorted(body_objs):
        offsets[oid] = len(out)
        out += b"%d 0 obj\n" % oid + body_objs[oid] + b"\nendobj\n"
    xref = len(out)
    n = max(body_objs) + 1
    out += b"xref\n0 %d\n0000000000 65535 f \n" % n
    for oid in range(1, n):
        out += b"%010d 00000 n \n" % offsets[oid]
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (n, xref)
    path.write_bytes(bytes(out))


@pytest.fixture
def paper(tmp_path: Path) -> Path:
    path = tmp_path / "-100123_45_daily.pdf"
    make_pdf(
        path,
        [
            [
                "RBI Holds Repo Rate Steady Amid Inflation Worries",
                "The central bank kept rates unchanged on Tuesday, citing food prices.",
                "Economists expect a cut later in the year if the monsoon is normal.",
            ],
            [
                "NEW DATA CENTRE POLICY TARGETS WATER USE",
                "The state will require closed-loop cooling for new AI data centres.",
                "Continued on page 7",
            ],
        ],
    )
    return path


def test_extract_and_cache(paper: Path):
    pdf = pdf_text.extract_pdf(paper)
    assert pdf.page_count == 2
    assert "central bank" in pdf.pages[0]
    assert not pdf.looks_scanned
    assert paper.with_suffix(".json").is_file()
    again = pdf_text.extract_pdf(paper)  # served from cache
    assert again.pages == pdf.pages


def test_overview_headlines_and_topics(paper: Path):
    pdf = pdf_text.extract_pdf(paper)
    rows = pdf_text.overview(pdf, ["inflation", "data centre", "cricket"])
    assert rows[0]["headlines"] == ["RBI Holds Repo Rate Steady Amid Inflation Worries"]
    assert rows[0]["topic_hits"] == {"inflation": 1}
    assert rows[1]["headlines"] == ["NEW DATA CENTRE POLICY TARGETS WATER USE"]
    assert rows[1]["topic_hits"] == {"data centre": 2}


def test_headline_rejects_sentences_and_jumps():
    assert not pdf_text._is_headline("The central bank kept rates unchanged on Tuesday.")
    assert not pdf_text._is_headline("Continued on page 7")
    assert not pdf_text._is_headline("Short")


def test_read_pages_truncates(paper: Path):
    pdf = pdf_text.extract_pdf(paper)
    text, truncated = pdf_text.read_pages(pdf, 1, 2, max_chars=10_000)
    assert "=== Page 1 ===" in text and "=== Page 2 ===" in text and not truncated
    text, truncated = pdf_text.read_pages(pdf, 1, 2, max_chars=50)
    assert truncated and len(text) == 50


def test_search(paper: Path):
    pdf = pdf_text.extract_pdf(paper)
    hits = pdf_text.search(pdf, "closed-loop cooling")
    assert [h["page"] for h in hits] == [2]
    assert pdf_text.search(pdf, "cricket") == []


def test_scanned_detection():
    assert pdf_text.ExtractedPdf("x.pdf", ["", " ", "short"]).looks_scanned


@pytest.mark.parametrize(
    "ref, expected",
    [
        ("-1001234567890", -1001234567890),
        ("@dailynews", "@dailynews"),
        ("https://t.me/dailynews", "@dailynews"),
        ("t.me/+AbCdEf123", "https://t.me/+AbCdEf123"),
        ("The Hindu Daily PDF", "The Hindu Daily PDF"),
    ],
)
def test_parse_group_ref(ref, expected):
    assert parse_group_ref(ref) == expected


def test_parse_topics():
    assert parse_topics(" AI, climate ,,India ") == ["AI", "climate", "India"]
    assert parse_topics(None) == []
