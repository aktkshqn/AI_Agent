def new_session_payload(new_id: str) -> dict:
    return {
        "session_id": new_id,
        "history": [],
        "summary": "",
        "full_history": [],
        "analysis": {},
        "memories": {
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


def ensure_memory_shape(session_data: dict) -> dict:
    memories = session_data.setdefault("memories", {})

    essence = memories.setdefault("essence", {})
    essence.setdefault("summary", "")
    essence.setdefault("noise_removed_points", [])
    essence.setdefault("open_questions", [])

    strategy = memories.setdefault("strategy", {})
    strategy.setdefault("policy", "")
    strategy.setdefault("next_actions", [])

    session_data.setdefault("analysis", {})
    session_data.setdefault("history", [])
    session_data.setdefault("summary", "")
    session_data.setdefault("full_history", [])

    if not session_data["full_history"]:
        old_full = memories.get("full_history", [])
        if old_full:
            session_data["full_history"] = old_full

    return session_data
