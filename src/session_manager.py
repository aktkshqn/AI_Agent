import os
import json
from datetime import datetime

DATA_DIR = "data/sessions"
os.makedirs(DATA_DIR, exist_ok=True)

def get_session_file(session_id):
    return os.path.join(DATA_DIR, f"session_{session_id}.json")

def load_session(session_id=None):
    if session_id:
        file_path = get_session_file(session_id)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    files = sorted(os.listdir(DATA_DIR))
    if files:
        with open(os.path.join(DATA_DIR, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
    new_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    return {
        "session_id": new_id,
        "summary": "",
        "history": [],
        "director_memory": {},
        "presenter_memory": {}
    }

def save_session(session_data: dict):
    file_path = get_session_file(session_data["session_id"])
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)