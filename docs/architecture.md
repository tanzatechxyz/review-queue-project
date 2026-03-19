# Architecture Overview

## Product shape

This app is intentionally designed as a **review queue**, not as a media library.
The core experience is:

1. scan a folder of video files
2. derive a chronological order
3. resume exactly where the reviewer left off
4. advance quickly through the queue with large touch controls

## Backend

- **Framework:** FastAPI
- **Database:** SQLite via SQLAlchemy
- **Migrations:** Alembic
- **Background work:** in-process scan manager using asyncio tasks
- **Video streaming:** FastAPI `FileResponse` serving files directly from disk
- **Metadata extraction:** optional `ffprobe`
- **Thumbnail generation:** optional `ffmpeg`

### Main backend responsibilities

- recursive file discovery
- file identity / rename matching
- chronological date derivation
- progress persistence
- queue calculation
- scan status tracking
- optional local-only login

## Frontend

- **Framework:** React + TypeScript + Vite
- **Routing:** React Router
- **State/data:** light custom hooks using `fetch`
- **UI goal:** large, uncluttered tablet-first controls

### Main frontend screens

- dashboard
- player / review screen
- timeline / grid
- settings / admin
- optional login screen
