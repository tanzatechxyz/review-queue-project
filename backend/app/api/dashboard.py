from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import maybe_require_auth
from app.db import get_db
from app.schemas import DashboardStatsResponse
from app.services.queue_service import dashboard_stats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"], dependencies=[Depends(maybe_require_auth)])


@router.get("/stats", response_model=DashboardStatsResponse)
def stats(db: Session = Depends(get_db)) -> DashboardStatsResponse:
    return DashboardStatsResponse(**dashboard_stats(db))
