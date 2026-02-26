import os
from datetime import datetime

from .config import DATA_DIR


def date_from_session_id(session_id: str) -> str:
    if len(session_id) >= 8 and session_id[:8].isdigit():
        return f"{session_id[:4]}-{session_id[4:6]}-{session_id[6:8]}"
    return datetime.now().strftime("%Y-%m-%d")


def session_dir_from_date(date_key: str) -> str:
    date_dir = os.path.join(DATA_DIR, date_key)
    os.makedirs(date_dir, exist_ok=True)
    return date_dir


def session_paths(session_id: str) -> dict:
    date_key = date_from_session_id(session_id)
    base = session_dir_from_date(date_key)
    return {
        "state": os.path.join(base, f"session_{session_id}.json"),
        "global_summary": os.path.join(DATA_DIR, "summary_all.json"),
        "global_full": os.path.join(DATA_DIR, "full_all.json"),
        "global_essence": os.path.join(DATA_DIR, "essence_all.json"),
    }


def find_latest_session_id() -> str | None:
    latest = None
    for _, _, files in os.walk(DATA_DIR):
        for file_name in files:
            if not (file_name.startswith("session_") and file_name.endswith(".json")):
                continue
            session_id = file_name[len("session_") : -len(".json")]
            if latest is None or session_id > latest:
                latest = session_id
    return latest
