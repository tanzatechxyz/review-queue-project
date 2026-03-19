#!/usr/bin/env bash
set -euo pipefail
cd /app/backend
alembic upgrade head
exec uvicorn app.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8080}"
