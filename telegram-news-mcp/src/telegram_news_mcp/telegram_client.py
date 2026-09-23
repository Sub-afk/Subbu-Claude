"""Thin read-only wrapper around Telethon for finding and downloading news PDFs."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument

from .config import Settings, parse_group_ref

CONNECT_TIMEOUT_S = 30


@dataclass
class PdfMessage:
    chat_id: int
    message_id: int
    date: datetime
    file_name: str
    size_bytes: int
    caption: str

    @property
    def pdf_id(self) -> str:
        """Stable id used for the cached file name and for later tool calls."""
        return f"{self.chat_id}_{self.message_id}"

    def as_dict(self) -> dict:
        return {
            "pdf_id": self.pdf_id,
            "file_name": self.file_name,
            "date": self.date.isoformat(),
            "size_mb": round(self.size_bytes / 1_048_576, 2),
            "caption": self.caption[:300],
        }


def _safe_name(name: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", name.removesuffix(".pdf").removesuffix(".PDF"))[:80]
    return (stem or "news") + ".pdf"


class NewsTelegram:
    def __init__(self, settings: Settings):
        self.settings = settings
        settings.session_path.parent.mkdir(parents=True, exist_ok=True)
        settings.download_dir.mkdir(parents=True, exist_ok=True)
        self.client = TelegramClient(str(settings.session_path), settings.api_id, settings.api_hash)
        self._lock = asyncio.Lock()
        self._connected = False

    async def ensure_connected(self) -> None:
        async with self._lock:
            if self._connected:
                return
            try:
                await asyncio.wait_for(self.client.connect(), timeout=CONNECT_TIMEOUT_S)
            except (asyncio.TimeoutError, OSError) as exc:
                raise RuntimeError(
                    f"Could not reach Telegram within {CONNECT_TIMEOUT_S}s ({exc!r}). "
                    "Check your internet connection or proxy."
                ) from exc
            if not await self.client.is_user_authorized():
                await self.client.disconnect()
                raise RuntimeError(
                    "Telegram session is not logged in. Run `telegram-news-login` once in a "
                    "terminal, then restart the MCP server."
                )
            self._connected = True

    async def list_groups(self, query: str | None, limit: int) -> list[dict]:
        await self.ensure_connected()
        out = []
        async for dialog in self.client.iter_dialogs():
            if not (dialog.is_group or dialog.is_channel):
                continue
            if query and query.lower() not in (dialog.name or "").lower():
                continue
            username = getattr(dialog.entity, "username", None)
            out.append(
                {
                    "title": dialog.name,
                    "id": dialog.id,
                    "username": f"@{username}" if username else None,
                    "type": "channel" if dialog.is_channel and not dialog.is_group else "group",
                }
            )
            if len(out) >= limit:
                break
        return out

    async def resolve_group(self, group: str | None):
        await self.ensure_connected()
        ref = group or self.settings.default_group
        if not ref:
            raise ValueError("No group given and TG_NEWS_GROUP is not set.")
        parsed = parse_group_ref(ref)
        if isinstance(parsed, int) or parsed.startswith(("@", "https://")):
            return await self.client.get_entity(parsed)
        # Otherwise treat it as a title: exact match first, then a unique substring match.
        partial = []
        async for dialog in self.client.iter_dialogs():
            if not (dialog.is_group or dialog.is_channel):
                continue
            if (dialog.name or "").casefold() == parsed.casefold():
                return dialog.entity
            if parsed.casefold() in (dialog.name or "").casefold():
                partial.append(dialog)
        if len(partial) == 1:
            return partial[0].entity
        if partial:
            names = ", ".join(repr(d.name) for d in partial[:10])
            raise ValueError(f"Group title {parsed!r} is ambiguous: {names}. Use the exact title or id.")
        raise ValueError(f"No joined group or channel matches {parsed!r}. Try the list_groups tool.")

    async def recent_pdfs(self, group: str | None, limit: int, scan: int = 200) -> list[PdfMessage]:
        entity = await self.resolve_group(group)
        found: list[PdfMessage] = []
        async for msg in self.client.iter_messages(entity, limit=scan, filter=InputMessagesFilterDocument):
            f = msg.file
            if f is None:
                continue
            name = f.name or ""
            if f.mime_type != "application/pdf" and not name.lower().endswith(".pdf"):
                continue
            found.append(
                PdfMessage(
                    chat_id=msg.chat_id,
                    message_id=msg.id,
                    date=msg.date,
                    file_name=name or f"message_{msg.id}.pdf",
                    size_bytes=f.size or 0,
                    caption=msg.message or "",
                )
            )
            if len(found) >= limit:
                break
        return found

    def local_path(self, pdf: PdfMessage) -> Path:
        return self.settings.download_dir / f"{pdf.pdf_id}_{_safe_name(pdf.file_name)}"

    def find_cached(self, pdf_id: str) -> Path | None:
        matches = sorted(self.settings.download_dir.glob(f"{pdf_id}_*.pdf"))
        return matches[0] if matches else None

    async def download(self, pdf: PdfMessage) -> Path:
        path = self.local_path(pdf)
        if path.is_file() and path.stat().st_size == pdf.size_bytes:
            return path
        msg = await self.client.get_messages(pdf.chat_id, ids=pdf.message_id)
        if msg is None:
            raise ValueError(f"Message {pdf.message_id} no longer exists.")
        tmp = path.with_suffix(".part")
        await self.client.download_media(msg, file=str(tmp))
        tmp.replace(path)
        return path

    async def download_by_id(self, pdf_id: str) -> Path:
        cached = self.find_cached(pdf_id)
        if cached:
            return cached
        chat_id, _, message_id = pdf_id.rpartition("_")
        await self.ensure_connected()
        msg = await self.client.get_messages(int(chat_id), ids=int(message_id))
        if msg is None or msg.file is None:
            raise ValueError(f"No document found for pdf_id {pdf_id!r}.")
        pdf = PdfMessage(
            chat_id=int(chat_id),
            message_id=int(message_id),
            date=msg.date,
            file_name=msg.file.name or f"message_{message_id}.pdf",
            size_bytes=msg.file.size or 0,
            caption=msg.message or "",
        )
        return await self.download(pdf)
