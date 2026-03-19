from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from app.auth import authenticate, create_access_token
from app.config import settings
from app.schemas import LoginRequest, LoginResponse, PublicConfigResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/public-config", response_model=PublicConfigResponse)
def public_config() -> PublicConfigResponse:
    return PublicConfigResponse(auth_enabled=settings.auth_enabled)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if not settings.auth_enabled:
        return LoginResponse(access_token="", auth_enabled=False)
    if not authenticate(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return LoginResponse(access_token=create_access_token(payload.username), auth_enabled=True)
