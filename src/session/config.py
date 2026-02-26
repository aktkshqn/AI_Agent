import json
import os

BASE_DATA_DIR = "data"
SESSIONS_DIR = os.path.join(BASE_DATA_DIR, "sessions")
SUMMARY_DIR = os.path.join(BASE_DATA_DIR, "summary")
SUMMARY_TOPICS_DIR = os.path.join(SUMMARY_DIR, "topics")
CURATOR_DIR = os.path.join(BASE_DATA_DIR, "curator")
CURATOR_TOPIC_ESSENCE_DIR = os.path.join(CURATOR_DIR, "topic_essence")
STRATEGY_DIR = os.path.join(BASE_DATA_DIR, "strategy")
STRATEGY_TOPIC_DIR = os.path.join(STRATEGY_DIR, "topic_strategy")
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
    SUMMARY_TOPICS_DIR,
    CURATOR_DIR,
    CURATOR_TOPIC_ESSENCE_DIR,
    STRATEGY_DIR,
    STRATEGY_TOPIC_DIR,
    META_DIR,
):
    _ensure_dir(_path)

_ensure_json(os.path.join(SUMMARY_DIR, "active_topic.json"), {"active_topic_id": None})
_ensure_json(os.path.join(SUMMARY_DIR, "summary_index.json"), {"global_summary": "", "topics": []})
_ensure_json(os.path.join(CURATOR_DIR, "essence_all.json"), {"scope": "all", "essence": {}})
_ensure_json(os.path.join(STRATEGY_DIR, "strategy_all.json"), {"scope": "all", "strategy": {}})
_ensure_json(os.path.join(META_DIR, "schema_version.json"), {"version": "0.1.0"})
