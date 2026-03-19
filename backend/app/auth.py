from __future__ import annotations

from typing import Annotated
from fastapi import Header, HTTPException, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from app.config import settings

TOKEN_SALT = "review-queue-auth"


def serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.secret_key, salt=TOKEN_SALT)


def create_access_token(username: str) -> str:
    return serializer().dumps({"username": username})


def verify_access_token(token: str) -> dict:
    try:
        return serializer().loads(token, max_age=60 * 60 * 24 * 30)
    except SignatureExpired as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except BadSignature as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def authenticate(username: str, password: str) -> bool:
    return username == settings.username and password == settings.password


def maybe_require_auth(authorization: Annotated[str | None, Header()] = None) -> None:
    if not settings.auth_enabled:
        return
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    verify_access_token(authorization.split(" ", 1)[1])
