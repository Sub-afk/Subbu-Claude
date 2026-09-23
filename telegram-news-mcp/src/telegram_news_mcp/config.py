"""Settings loaded from environment variables (optionally via a .env file)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

_TME_LINK = re.compile(r"^(?:https?://)?(?:t\.me|telegram\.me)/(?P<name>[A-Za-z0-9_+]+)/?$")


def load_dotenv(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE lines; existing env vars win."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def parse_group_ref(ref: str) -> str | int:
    """Normalise a group reference.

    Returns an int for numeric ids, "@username" for usernames / public t.me
    links, a full "https://t.me/+hash" link for private invite links (Telethon
    resolves those for groups you have already joined), or the raw string,
    which is treated as a group title.
    """
    ref = ref.strip()
    if re.fullmatch(r"-?\d+", ref):
        return int(ref)
    match = _TME_LINK.match(ref)
    if match:
        name = match.group("name")
        if name.startswith("+"):
            return "https://t.me/" + name
        return "@" + name
    if ref.startswith("@"):
        return ref
    return ref


def parse_topics(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


@dataclass
class Settings:
    api_id: int
    api_hash: str
    session_path: Path
    download_dir: Path
    default_group: str | None = None
    topics: list[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv(Path(os.environ.get("TG_NEWS_ENV_FILE", ".env")).expanduser())
        missing = [k for k in ("TG_API_ID", "TG_API_HASH") if not os.environ.get(k)]
        if missing:
            raise RuntimeError(
                f"Missing {', '.join(missing)}. Create an app at https://my.telegram.org "
                "and set these in your environment or .env file."
            )
        base = Path("~/.telegram-news-mcp").expanduser()
        session = Path(os.environ.get("TG_SESSION", base / "session")).expanduser()
        downloads = Path(os.environ.get("NEWS_DOWNLOAD_DIR", base / "downloads")).expanduser()
        return cls(
            api_id=int(os.environ["TG_API_ID"]),
            api_hash=os.environ["TG_API_HASH"],
            session_path=session,
            download_dir=downloads,
            default_group=os.environ.get("TG_NEWS_GROUP") or None,
            topics=parse_topics(os.environ.get("NEWS_TOPICS")),
        )
