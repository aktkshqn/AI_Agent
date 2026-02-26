def new_session_payload(new_id: str) -> dict:
    return {
        "session_id": new_id,
        "history": [],
        "summary": "",
        "full_history": [],
        "essence": {
            "summary": "",
            "noise_removed_points": [],
            "open_questions": [],
        },
    }


def ensure_memory_shape(session_data: dict) -> dict:
    essence = session_data.setdefault("essence", {})
    essence.setdefault("summary", "")
    essence.setdefault("noise_removed_points", [])
    essence.setdefault("open_questions", [])

    session_data.setdefault("history", [])
    session_data.setdefault("summary", "")
    session_data.setdefault("full_history", [])

    return session_data
