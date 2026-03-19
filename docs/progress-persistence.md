# How Progress Persistence Works

Progress is persisted in SQLite, not in browser storage.

## What is stored

For each video:

- `review_state` (`queued`, `watched`, `skipped`)
- `bookmarked`
- `playback_position_seconds`
- `last_interaction_at`
- `watch_completed_at`

For the app:

- `current_video_id`

## Continue behavior

The dashboard Continue button calls the queue endpoint.

1. If `current_video_id` still points to an unfinished, available item, that item is returned.
2. Otherwise the backend returns the oldest unfinished item.
