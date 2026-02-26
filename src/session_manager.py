import os
import json
from datetime import datetime

DATA_DIR = "data/sessions"
os.makedirs(DATA_DIR, exist_ok=True)


def get_session_file(session_id):
    return os.path.join(DATA_DIR, f"session_{session_id}.json")


def _new_session_payload(new_id: str) -> dict:
    return {
        "session_id": new_id,
        "summary": "",
        "history": [],
        "analysis": {},
        "memories": {
            "full_history": [],
            "conversation": {
                "recent_history": [],
                "past_summary": "",
            },
            "essence": {
                "summary": "",
                "noise_removed_points": [],
                "open_questions": [],
            },
            "strategy": {
                "policy": "",
                "next_actions": [],
            },
        },
    }


def _ensure_memory_shape(session_data: dict) -> dict:
    memories = session_data.setdefault("memories", {})

    memories.setdefault("full_history", [])

    conversation = memories.setdefault("conversation", {})
    conversation.setdefault("recent_history", [])
    conversation.setdefault("past_summary", session_data.get("summary", ""))

    essence = memories.setdefault("essence", {})
    essence.setdefault("summary", "")
    essence.setdefault("noise_removed_points", [])
    essence.setdefault("open_questions", [])

    strategy = memories.setdefault("strategy", {})
    strategy.setdefault("policy", "")
    strategy.setdefault("next_actions", [])

    # Backward compatibility for old keys
    session_data.setdefault("analysis", {})
    session_data.setdefault("history", [])
    session_data.setdefault("summary", "")

    return session_data


def load_session(session_id=None):
    if session_id:
        file_path = get_session_file(session_id)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return _ensure_memory_shape(json.load(f))

    files = sorted(os.listdir(DATA_DIR))
    if files:
        with open(os.path.join(DATA_DIR, files[-1]), "r", encoding="utf-8") as f:
            return _ensure_memory_shape(json.load(f))

    new_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    return _new_session_payload(new_id)


def save_session(session_data: dict):
    session_data = _ensure_memory_shape(session_data)
    file_path = get_session_file(session_data["session_id"])
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
