#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="/app/backend:${PYTHONPATH:-}"

APP_DATA_DIR="${APP_DATA_DIR:-/data}"
APP_DB_PATH="${APP_DB_PATH:-/data/review_queue.db}"

mkdir -p "$APP_DATA_DIR"
mkdir -p "$(dirname "$APP_DB_PATH")"

cd /app/backend
alembic upgrade head
exec uvicorn app.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8080}"