from __future__ import annotations

from fastapi import APIRouter, Depends
from app.auth import maybe_require_auth
from app.schemas import ScanStatusResponse
from app.services.scan_service import scan_manager

router = APIRouter(prefix="/api/scan", tags=["scan"], dependencies=[Depends(maybe_require_auth)])


@router.get("/status", response_model=ScanStatusResponse)
def status() -> ScanStatusResponse:
    return ScanStatusResponse(**scan_manager.latest_status())


@router.post("/start")
async def start_scan() -> dict:
    return await scan_manager.start_scan()
