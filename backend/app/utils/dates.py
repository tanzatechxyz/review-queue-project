from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable
from dateutil import parser as date_parser

FILENAME_PATTERNS = [
    re.compile(r"(?P<year>20\d{2}|19\d{2})[-_.](?P<month>0[1-9]|1[0-2])[-_.](?P<day>0[1-9]|[12]\d|3[01])"),
    re.compile(r"(?P<year>20\d{2}|19\d{2})(?P<month>0[1-9]|1[0-2])(?P<day>0[1-9]|[12]\d|3[01])"),
]


def ensure_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def parse_date_from_filename(filename: str) -> datetime | None:
    stem = filename.rsplit(".", 1)[0]
    for pattern in FILENAME_PATTERNS:
        match = pattern.search(stem)
        if match:
            try:
                return datetime(int(match.group("year")), int(match.group("month")), int(match.group("day")), tzinfo=timezone.utc)
            except ValueError:
                pass
    tokens = re.findall(r"\d{4}[-_.]?\d{2}[-_.]?\d{2}[ T]?\d{0,6}", stem)
    for token in tokens:
        try:
            return ensure_utc(date_parser.parse(token.replace("_", "-").replace(".", "-")))
        except Exception:
            continue
    return None


def choose_sort_date(priority: Iterable[str], filename_date: datetime | None, metadata_date: datetime | None, filesystem_date: datetime | None) -> tuple[datetime | None, str | None]:
    lookup = {"filename": filename_date, "metadata": metadata_date, "filesystem": filesystem_date}
    for source in priority:
        value = lookup.get(source)
        if value is not None:
            return ensure_utc(value), source
    for source, value in lookup.items():
        if value is not None:
            return ensure_utc(value), source
    return None, None
