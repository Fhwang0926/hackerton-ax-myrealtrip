from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)

    def text(self) -> str:
        return " ".join(self.parts)


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def iso_now() -> str:
    return utc_now().isoformat()


def timestamp_slug() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def strip_html(value: str) -> str:
    parser = TextExtractor()
    parser.feed(value)
    text = parser.text() or re.sub(r"<[^>]+>", " ", value)
    return compact_whitespace(unescape(text))


def compact_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_date(value: str | None) -> str:
    if not value:
        return utc_now().date().isoformat()
    try:
        parsed = parsedate_to_datetime(value)
        return parsed.date().isoformat()
    except (TypeError, ValueError, IndexError, OverflowError):
        return value[:10]


def stable_id(*parts: str) -> str:
    joined = "|".join(part for part in parts if part)
    slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", joined).strip("-").lower()
    return slug[:120] or "item"


def truncate(value: str, length: int) -> str:
    if len(value) <= length:
        return value
    return value[: max(0, length - 1)].rstrip() + "…"
