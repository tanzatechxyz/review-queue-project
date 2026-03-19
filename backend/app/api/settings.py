from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import maybe_require_auth
from app.config import settings as env_settings
from app.db import get_db
from app.schemas import SettingsResponse, SettingsUpdateRequest
from app.services.scan_service import scan_manager
from app.services.settings_service import get_or_create_settings

router = APIRouter(prefix="/api/settings", tags=["settings"], dependencies=[Depends(maybe_require_auth)])


@router.get("", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)) -> SettingsResponse:
    settings = get_or_create_settings(db)
    return SettingsResponse(root_folder=settings.root_folder, supported_extensions=[item.strip() for item in settings.supported_extensions_csv.split(",") if item.strip()], watched_threshold_percent=settings.watched_threshold_percent, sort_priority=[item.strip() for item in settings.sort_priority_csv.split(",") if item.strip()], auto_advance_on_done=settings.auto_advance_on_done, auto_advance_on_end=settings.auto_advance_on_end, generate_thumbnails=settings.generate_thumbnails, thumbnail_interval_seconds=settings.thumbnail_interval_seconds, thumbnail_width=settings.thumbnail_width, current_video_id=settings.current_video_id)


@router.put("", response_model=SettingsResponse)
async def update_settings(payload: SettingsUpdateRequest, db: Session = Depends(get_db)) -> SettingsResponse:
    settings = get_or_create_settings(db)
    if payload.root_folder is not None: settings.root_folder = payload.root_folder
    if payload.supported_extensions is not None: settings.supported_extensions_csv = ",".join(sorted(set(item.lower() for item in payload.supported_extensions)))
    if payload.watched_threshold_percent is not None: settings.watched_threshold_percent = payload.watched_threshold_percent
    if payload.sort_priority is not None: settings.sort_priority_csv = ",".join(payload.sort_priority)
    if payload.auto_advance_on_done is not None: settings.auto_advance_on_done = payload.auto_advance_on_done
    if payload.auto_advance_on_end is not None: settings.auto_advance_on_end = payload.auto_advance_on_end
    if payload.generate_thumbnails is not None: settings.generate_thumbnails = payload.generate_thumbnails
    if payload.thumbnail_interval_seconds is not None: settings.thumbnail_interval_seconds = payload.thumbnail_interval_seconds
    if payload.thumbnail_width is not None: settings.thumbnail_width = payload.thumbnail_width
    if payload.current_video_id is not None: settings.current_video_id = payload.current_video_id
    db.add(settings); db.commit(); db.refresh(settings)
    if env_settings.scan_on_settings_save:
        await scan_manager.start_scan()
    return SettingsResponse(root_folder=settings.root_folder, supported_extensions=[item.strip() for item in settings.supported_extensions_csv.split(",") if item.strip()], watched_threshold_percent=settings.watched_threshold_percent, sort_priority=[item.strip() for item in settings.sort_priority_csv.split(",") if item.strip()], auto_advance_on_done=settings.auto_advance_on_done, auto_advance_on_end=settings.auto_advance_on_end, generate_thumbnails=settings.generate_thumbnails, thumbnail_interval_seconds=settings.thumbnail_interval_seconds, thumbnail_width=settings.thumbnail_width, current_video_id=settings.current_video_id)
