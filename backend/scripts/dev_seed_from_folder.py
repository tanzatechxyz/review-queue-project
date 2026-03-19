from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from app.db import SessionLocal
from app.services.scan_service import scan_manager
from app.services.settings_service import get_or_create_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Point the app at a local folder and trigger a scan.")
    parser.add_argument("folder", help="Path to a folder containing local test videos")
    args = parser.parse_args()
    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")
    db = SessionLocal()
    try:
        settings = get_or_create_settings(db)
        settings.root_folder = str(folder)
        db.add(settings)
        db.commit()
    finally:
        db.close()
    asyncio.run(scan_manager.start_scan())
    print(f"Scan started for {folder}")


if __name__ == "__main__":
    main()
