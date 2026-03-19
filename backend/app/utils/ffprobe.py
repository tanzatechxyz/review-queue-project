from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from dateutil import parser as date_parser
from app.utils.dates import ensure_utc


def ffprobe_available() -> bool:
    return shutil.which("ffprobe") is not None


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def probe_video(file_path: Path) -> tuple[float | None, datetime | None, str | None]:
    if not ffprobe_available():
        return None, None, "ffprobe not available"
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration:format_tags=creation_time,com.apple.quicktime.creationdate", "-of", "json", str(file_path)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        payload = json.loads(result.stdout or "{}")
        fmt = payload.get("format", {})
        duration_raw = fmt.get("duration")
        duration = float(duration_raw) if duration_raw is not None else None
        tags = fmt.get("tags", {}) or {}
        raw_date = tags.get("creation_time") or tags.get("com.apple.quicktime.creationdate")
        parsed_date = ensure_utc(date_parser.parse(raw_date)) if raw_date else None
        return duration, parsed_date, None
    except Exception as exc:
        return None, None, str(exc)


def generate_thumbnail(file_path: Path, output_path: Path, second: int, width: int) -> str | None:
    if not ffmpeg_available():
        return "ffmpeg not available"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-y", "-ss", str(second), "-i", str(file_path), "-frames:v", "1", "-vf", f"scale={width}:-1", str(output_path)]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        return None
    except subprocess.CalledProcessError as exc:
        return exc.stderr[-500:] if exc.stderr else str(exc)
