"""Seed the persistent database once, then keep it across deploys.

On Railway the volume is mounted at /data and SQLITE_PATH=/data/db.sqlite3.
The first boot copies the bundled db2.sqlite3 (stages, questions, answers) there;
later boots leave it alone so users and reports survive redeploys.
"""
import os
import shutil
from pathlib import Path

base = Path(__file__).resolve().parent.parent
target = os.environ.get("SQLITE_PATH")
media = os.environ.get("MEDIA_ROOT")

if media:
    Path(media).mkdir(parents=True, exist_ok=True)

if target and not Path(target).exists():
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(base / "db2.sqlite3", target)
    print(f"Seeded {target} from db2.sqlite3")
else:
    print(f"Database at {target or 'bundled db2.sqlite3'} kept")
