"""MCP server: fetch the latest news PDF from a Telegram group and help the client curate it.

The server does the mechanical work (find, download, extract, index). The
curating itself - picking what matters and summarising it - is done by the
model in the MCP client (Claude Desktop, Claude Code, ...), guided by the
`curate_news` prompt.
"""

from __future__ import annotations

import functools
import logging

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from telethon.errors import RPCError

from . import pdf_text
from .config import Settings
from .telegram_client import NewsTelegram

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=True)

server = MCPServer(
    name="telegram-news",
    instructions=(
        "Reads news PDFs posted in the user's Telegram news group. Typical flow: "
        "get_latest_news_pdf -> read_news_pages for the pages that matter -> write a curated brief. "
        "Use search_news for specific topics. This server never sends Telegram messages."
    ),
)

_tg: NewsTelegram | None = None
_current_pdf_id: str | None = None


def friendly_errors(fn):
    """Pass anticipated failures (setup, lookup, Telegram API) to the model as readable tool errors."""

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except (ValueError, RuntimeError, FileNotFoundError, RPCError) as exc:
            raise ToolError(str(exc) or type(exc).__name__) from exc

    return wrapper


def tg() -> NewsTelegram:
    global _tg
    if _tg is None:
        _tg = NewsTelegram(Settings.from_env())
    return _tg


async def _load(pdf_id: str | None) -> tuple[str, pdf_text.ExtractedPdf]:
    pdf_id = pdf_id or _current_pdf_id
    if not pdf_id:
        raise ValueError("No PDF loaded yet. Call get_latest_news_pdf first, or pass a pdf_id.")
    path = await tg().download_by_id(pdf_id)
    return pdf_id, pdf_text.extract_pdf(path)


@server.tool(annotations=READ_ONLY)
@friendly_errors
async def list_groups(query: str | None = None, limit: int = 30) -> list[dict]:
    """List Telegram groups/channels you have joined, optionally filtered by a title substring.

    Use this to find the exact title or id of your news group.
    """
    return await tg().list_groups(query, limit)


@server.tool(annotations=READ_ONLY)
@friendly_errors
async def list_news_pdfs(group: str | None = None, limit: int = 10) -> list[dict]:
    """List the most recent PDF files posted in the news group (newest first).

    group: title, @username, t.me link or numeric id. Defaults to TG_NEWS_GROUP.
    """
    return [p.as_dict() for p in await tg().recent_pdfs(group, limit)]


@server.tool(annotations=READ_ONLY)
@friendly_errors
async def get_latest_news_pdf(
    group: str | None = None,
    pdf_id: str | None = None,
    headlines_per_page: int = 8,
) -> dict:
    """Download the newest news PDF from the group (or a specific pdf_id) and return a page-by-page overview.

    The overview lists likely headlines per page plus hits for the user's
    NEWS_TOPICS, so you can decide which pages to read in full with
    read_news_pages. The downloaded PDF becomes the "current" one for other tools.
    """
    global _current_pdf_id
    client = tg()
    if pdf_id:
        meta = {"pdf_id": pdf_id}
        path = await client.download_by_id(pdf_id)
    else:
        recent = await client.recent_pdfs(group, limit=1)
        if not recent:
            raise ValueError("No PDF found in the last 200 documents of that group.")
        meta = recent[0].as_dict()
        path = await client.download(recent[0])
    pdf = pdf_text.extract_pdf(path)
    _current_pdf_id = meta["pdf_id"]

    result = {
        **meta,
        "local_path": str(path),
        "page_count": pdf.page_count,
        "user_topics": client.settings.topics,
        "pages": pdf_text.overview(pdf, client.settings.topics, headlines_per_page),
    }
    if pdf.looks_scanned:
        result["warning"] = (
            "Most pages have no extractable text, so this PDF is probably scanned images. "
            "Run OCR on it first (for example `ocrmypdf in.pdf out.pdf`), or open local_path directly."
        )
    return result


@server.tool(annotations=READ_ONLY)
@friendly_errors
async def read_news_pages(
    start_page: int,
    end_page: int | None = None,
    pdf_id: str | None = None,
    max_chars: int = 40_000,
) -> dict:
    """Return the full extracted text of pages start_page..end_page (1-based, inclusive) of the current PDF.

    Output is capped at max_chars; if truncated, call again from the next page.
    """
    pdf_id, pdf = await _load(pdf_id)
    end_page = end_page or start_page
    text, truncated = pdf_text.read_pages(pdf, start_page, end_page, max_chars)
    return {"pdf_id": pdf_id, "page_count": pdf.page_count, "truncated": truncated, "text": text}


@server.tool(annotations=READ_ONLY)
@friendly_errors
async def search_news(query: str, pdf_id: str | None = None, limit: int = 15) -> dict:
    """Search the current news PDF. Every word in query must appear in a matching paragraph."""
    pdf_id, pdf = await _load(pdf_id)
    return {"pdf_id": pdf_id, "query": query, "matches": pdf_text.search(pdf, query, limit=limit)}


@server.prompt()
def curate_news(topics: str = "", length: str = "about 10 items") -> str:
    """Build today's curated news brief from the latest PDF in the Telegram news group."""
    focus = f"Prioritise these interests: {topics}." if topics else (
        "Prioritise the interests in `user_topics` returned by the tool, if any."
    )
    return f"""Create my curated news brief from today's news PDF.

1. Call `get_latest_news_pdf`. Note the date and file name.
2. From the page overview, choose the pages most likely to hold significant stories
   (front page, national, international, economy/business, science & tech, editorials). {focus}
3. Read those pages with `read_news_pages` (a few pages per call). Use `search_news` for follow-ups.
4. Write the brief, {length}:
   - Group by section (Top stories, India/National, World, Economy & Business, Science & Tech, Opinion, Other).
   - For each item: a bold one-line headline, 2-3 sentences on what happened and why it matters,
     and the page number in brackets, e.g. [p. 7].
   - Merge duplicate coverage of the same story. Skip ads, classifieds, horoscopes and puzzles.
   - Report only what the PDF says; don't add outside facts. Flag anything that reads like opinion.
5. End with "Worth reading in full" - 2-3 pieces with page numbers.
"""


def main() -> None:
    logging.basicConfig(level=logging.INFO)  # logs go to stderr; stdout is the MCP channel
    server.run("stdio")


if __name__ == "__main__":
    main()
