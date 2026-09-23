# telegram-news-mcp

An MCP server that opens your Telegram news group, downloads the most recent news PDF, and gives
your AI assistant (Claude Desktop, Claude Code, or any MCP client) what it needs to write a
**curated news brief** from it.

```
Telegram group ──► newest PDF ──► download + text extraction (cached)
                                        │
                  page overview (headlines + your topics) ──► Claude picks pages
                                        │
                        read_news_pages / search_news ──► curated brief
```

This server does the mechanical work: it finds the PDF, downloads it, extracts the text and
indexes it. The **model in your client does the curating**, so you don't need a separate AI API
key. The `curate_news` prompt tells it how to write the brief.

It is **read-only**. It never sends, deletes or marks messages in Telegram.

## Tools

| Tool | What it does |
|---|---|
| `list_groups(query?)` | Lists the groups and channels you've joined, so you can find the exact name or id |
| `list_news_pdfs(group?, limit?)` | Lists recent PDFs in the group, newest first |
| `get_latest_news_pdf(group?, pdf_id?)` | Downloads the newest PDF (or a specific one) and returns a page-by-page overview: likely headlines, plus how often each of your `NEWS_TOPICS` appears |
| `read_news_pages(start_page, end_page?)` | Returns the full text of a page range, with a size cap |
| `search_news(query)` | Keyword search across the current PDF |

**Prompt:** `curate_news(topics?, length?)` runs the whole flow and returns a brief grouped by
section, with page numbers.

## Setup

### 1. Get Telegram API credentials
1. Go to <https://my.telegram.org>, log in with your phone number and open **API development tools**.
2. Create an app (any name works). Copy the **api_id** and **api_hash**.

> The server logs in as **you** (a Telegram "user client", via [Telethon](https://docs.telethon.dev)),
> not as a bot. That's why it can read any group you're a member of, without an admin having to
> add a bot.

### 2. Install
```bash
cd telegram-news-mcp
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env    # then edit .env
```

In `.env`, set `TG_API_ID`, `TG_API_HASH` and `TG_NEWS_GROUP`. The group can be given as its
exact title, `@username`, a `t.me` link or its numeric id. `NEWS_TOPICS` is optional.

### 3. Log in once (in a normal terminal)
```bash
telegram-news-login
```
Telegram sends a code to your Telegram app. Enter it, plus your 2FA password if you have one. The
script saves a session file and checks that it can see PDFs in `TG_NEWS_GROUP`.

### 4. Connect it to your AI client

**Claude Code**
```bash
claude mcp add telegram-news --env TG_NEWS_ENV_FILE=/absolute/path/to/telegram-news-mcp/.env \
  -- /absolute/path/to/telegram-news-mcp/.venv/bin/telegram-news-mcp
```

**Claude Desktop**: add this to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "telegram-news": {
      "command": "/absolute/path/to/telegram-news-mcp/.venv/bin/telegram-news-mcp",
      "env": { "TG_NEWS_ENV_FILE": "/absolute/path/to/telegram-news-mcp/.env" }
    }
  }
}
```
(On Windows the command is `...\\.venv\\Scripts\\telegram-news-mcp.exe`.)

### 5. Use it
> "Give me today's curated news from my Telegram news PDF, focus on economy and tech."

or run the `curate_news` prompt from your client's prompt/slash menu.

## Notes and limits

- **Scanned PDFs.** Some newspaper PDFs are just page images with no text layer. The overview
  flags these (`warning`). Run OCR on them first, for example `ocrmypdf in.pdf out.pdf`.
- **Multi-column layouts.** Text extraction can interleave the columns of a newspaper page. The
  model usually untangles this, but headline detection is a heuristic, so treat the overview as a
  map rather than a table of contents.
- **Caching.** PDFs and their extracted text are cached in `NEWS_DOWNLOAD_DIR`, so repeat calls
  don't download again. Delete old files whenever you like.
- **Security.** The `.session` file gives **full access to your Telegram account**. Keep it
  private (the login script sets its permissions to `600`), never commit it, and revoke it from
  Telegram → Settings → Devices if it leaks.
- **Copyright.** Newspaper PDFs shared in Telegram groups are often redistributed without the
  publisher's permission. Keep the briefs for your own use.
- **Telegram rules.** Using your own account through the official API is allowed. Heavy
  automation can trigger flood limits, and this server only makes a handful of calls per brief.

## Development
```bash
pip install -e '.[dev]'
pytest
```
