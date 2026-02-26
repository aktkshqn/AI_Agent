import json
import os

BASE_DATA_DIR = "data"
SESSIONS_DIR = os.path.join(BASE_DATA_DIR, "sessions")
SUMMARY_DIR = os.path.join(BASE_DATA_DIR, "summary")
CURATOR_DIR = os.path.join(BASE_DATA_DIR, "curator")
STRATEGY_DIR = os.path.join(BASE_DATA_DIR, "strategy")
META_DIR = os.path.join(BASE_DATA_DIR, "meta")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _ensure_json(path: str, payload: dict) -> None:
    if os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


for _path in (
    BASE_DATA_DIR,
    SESSIONS_DIR,
    SUMMARY_DIR,
    CURATOR_DIR,
    STRATEGY_DIR,
    META_DIR,
):
    _ensure_dir(_path)

_ensure_json(os.path.join(SUMMARY_DIR, "active_topic.json"), {"active_topic_id": None})
_ensure_json(os.path.join(SUMMARY_DIR, "summary_index.json"), {"global_summary": "", "topics": []})
_ensure_json(os.path.join(CURATOR_DIR, "essence_all.json"), {"scope": "all", "essence": {}})
_ensure_json(os.path.join(STRATEGY_DIR, "strategy_all.json"), {"scope": "all", "strategy": {}})
_ensure_json(os.path.join(META_DIR, "schema_version.json"), {"version": "0.1.0"})
