"""One-time interactive Telegram login. Creates the session file the MCP server reuses.

Run this in a normal terminal (not through the MCP client): Telegram sends a
login code to your Telegram app, and you may be asked for your 2FA password.
"""

from __future__ import annotations

import asyncio
import os

from telethon import TelegramClient

from .config import Settings


async def _login() -> None:
    settings = Settings.from_env()
    settings.session_path.parent.mkdir(parents=True, exist_ok=True)
    client = TelegramClient(str(settings.session_path), settings.api_id, settings.api_hash)
    await client.start()  # prompts for phone number, login code and 2FA password as needed
    me = await client.get_me()
    print(f"Logged in as {me.first_name} (@{me.username or 'no username'}).")

    session_file = settings.session_path.with_suffix(".session")
    if session_file.exists():
        os.chmod(session_file, 0o600)
        print(f"Session saved to {session_file} (permissions 600). Keep it private.")

    if settings.default_group:
        from .telegram_client import NewsTelegram

        tg = NewsTelegram(settings)
        tg.client = client
        tg._connected = True
        entity = await tg.resolve_group(None)
        title = getattr(entity, "title", None) or getattr(entity, "username", "?")
        pdfs = await tg.recent_pdfs(None, limit=3)
        print(f"TG_NEWS_GROUP resolved to: {title}. Recent PDFs found: {len(pdfs)}")
        for p in pdfs:
            print(f"  - {p.date:%Y-%m-%d %H:%M}  {p.file_name}")
    await client.disconnect()


def main() -> None:
    asyncio.run(_login())


if __name__ == "__main__":
    main()
