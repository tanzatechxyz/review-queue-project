from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AppSettings(Base):
    __tablename__ = "app_settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    root_folder: Mapped[str] = mapped_column(String(1024), nullable=False)
    supported_extensions_csv: Mapped[str] = mapped_column(String(512), nullable=False)
    watched_threshold_percent: Mapped[int] = mapped_column(Integer, default=95, nullable=False)
    sort_priority_csv: Mapped[str] = mapped_column(String(128), default="filename,metadata,filesystem", nullable=False)
    auto_advance_on_done: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auto_advance_on_end: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    generate_thumbnails: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    thumbnail_interval_seconds: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    thumbnail_width: Mapped[int] = mapped_column(Integer, default=480, nullable=False)
    current_video_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class ScanJob(Base):
    __tablename__ = "scan_jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    scanned_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    added_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    removed_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    renamed_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_details: Mapped[str | None] = mapped_column(Text, nullable=True)


class Video(Base):
    __tablename__ = "videos"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    rel_path: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False)
    abs_path: Mapped[str] = mapped_column(String(4096), nullable=False)
    filename: Mapped[str] = mapped_column(String(1024), nullable=False)
    extension: Mapped[str] = mapped_column(String(32), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mtime_ns: Mapped[int] = mapped_column(BigInteger, nullable=False)
    birth_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    modified_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    content_fingerprint: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    path_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    thumbnail_path: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    filename_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    filesystem_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    derived_sort_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    derived_sort_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    review_state: Mapped[str] = mapped_column(String(32), index=True, default="queued", nullable=False)
    bookmarked: Mapped[bool] = mapped_column(Boolean, index=True, default=False, nullable=False)
    playback_position_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    last_interaction_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    watch_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_missing: Mapped[bool] = mapped_column(Boolean, index=True, default=False, nullable=False)
    missing_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
