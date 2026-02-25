import os
import json
from datetime import datetime

SAVE_FILE = "session.json"

def load_session():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "session_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
            "summary": "",
            "history": []
        }

def save_session(session_data: dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)