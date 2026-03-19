# Database Schema

## videos

| column | type | notes |
|---|---|---|
| id | string PK | stable internal ID |
| rel_path | string unique | path relative to configured root |
| abs_path | string | absolute path on disk |
| filename | string | basename |
| extension | string | lowercase extension |
| size_bytes | integer | file size |
| mtime_ns | integer | last modification time |
| birth_time | datetime nullable | filesystem birth time if available |
| modified_time | datetime | filesystem modified time |
| discovered_at | datetime | first seen |
| last_seen_at | datetime | last seen during scan |
| content_fingerprint | string nullable index | rename matching |
| path_fingerprint | string | fallback identity |
| duration_seconds | float nullable | from ffprobe when available |
| thumbnail_path | string nullable | local thumbnail cache |
| filename_date | datetime nullable | parsed from filename |
| metadata_date | datetime nullable | embedded media creation time |
| filesystem_date | datetime nullable | filesystem fallback date |
| derived_sort_date | datetime nullable | selected sort date |
| derived_sort_source | string nullable | filename / metadata / filesystem |
| review_state | string | queued / watched / skipped |
| bookmarked | boolean | bookmark flag |
| playback_position_seconds | float | last known playback position |
| last_interaction_at | datetime nullable | last user interaction |
| watch_completed_at | datetime nullable | when marked watched |
| error_message | text nullable | latest file/probe error |
| is_missing | boolean | set true when file disappears |
| missing_since | datetime nullable | when disappearance was detected |
