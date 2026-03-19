from __future__ import annotations

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from app.auth import maybe_require_auth
from app.db import get_db
from app.models import Video
from app.schemas import QueueAdjacentResponse, QueueItemResponse, QueueJumpResponse
from app.services.queue_service import get_adjacent_video_ids, get_continue_video, jump_to_date, jump_to_position, set_current_video
from app.api.videos import to_detail

router = APIRouter(prefix="/api/queue", tags=["queue"], dependencies=[Depends(maybe_require_auth)])


@router.get("/continue", response_model=QueueItemResponse)
def continue_queue(request: Request, db: Session = Depends(get_db)) -> QueueItemResponse:
    request.state.db = db
    video = get_continue_video(db)
    if video is None: return QueueItemResponse(video=None)
    set_current_video(db, video.id)
    return QueueItemResponse(video=to_detail(video, request))


@router.get("/current", response_model=QueueItemResponse)
def current_queue_item(request: Request, db: Session = Depends(get_db)) -> QueueItemResponse:
    request.state.db = db
    video = get_continue_video(db)
    return QueueItemResponse(video=to_detail(video, request) if video else None)


@router.get("/adjacent/{video_id}", response_model=QueueAdjacentResponse)
def adjacent(video_id: str, view: str = Query(default="unfinished", pattern="^(all|unfinished|watched|skipped|bookmarked)$"), db: Session = Depends(get_db)) -> QueueAdjacentResponse:
    video = db.get(Video, video_id)
    if not video: raise HTTPException(status_code=404, detail="Video not found")
    previous_video_id, next_video_id = get_adjacent_video_ids(db, video, view=view)
    return QueueAdjacentResponse(previous_video_id=previous_video_id, next_video_id=next_video_id)


@router.get("/jump", response_model=QueueJumpResponse)
def jump(jump_date: date | None = None, position: int | None = Query(default=None, ge=1), view: str = Query(default="unfinished", pattern="^(all|unfinished|watched|skipped|bookmarked)$"), db: Session = Depends(get_db)) -> QueueJumpResponse:
    video = jump_to_date(db, jump_date, view=view) if jump_date is not None else jump_to_position(db, position, view=view) if position is not None else None
    return QueueJumpResponse(video_id=video.id if video else None)
