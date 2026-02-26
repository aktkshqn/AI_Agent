from datetime import datetime

from .paths import find_latest_session_id, session_paths
from .schema import ensure_memory_shape, new_session_payload
from .storage import load_json, save_json


def load_session(session_id=None, create_new=False):
    if create_new:
        new_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        state = new_session_payload(new_id)
        paths = session_paths(new_id)

        all_summary = load_json(paths["global_summary"], {"summary": ""})
        all_full = load_json(paths["global_full"], {"messages": []})

        state["summary"] = all_summary.get("summary", "")
        state["full_history"] = all_full.get("messages", [])
        return ensure_memory_shape(state)

    target_id = session_id or find_latest_session_id()
    if target_id:
        paths = session_paths(target_id)
        state = load_json(paths["state"], new_session_payload(target_id))
        all_summary = load_json(paths["global_summary"], {"summary": state.get("summary", "")})
        all_full = load_json(paths["global_full"], {"messages": state.get("full_history", [])})

        state["summary"] = all_summary.get("summary", state.get("summary", ""))
        state["full_history"] = all_full.get("messages", state.get("full_history", []))
        return ensure_memory_shape(state)

    new_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    return new_session_payload(new_id)


def save_session(session_data: dict):
    session_data = ensure_memory_shape(session_data)
    session_id = session_data["session_id"]
    paths = session_paths(session_id)
    updated_at = datetime.now().isoformat(timespec="seconds")

    state_doc = {
        "session_id": session_id,
        "history": session_data["history"],
        "analysis": session_data["analysis"],
        "memories": session_data["memories"],
        "updated_at": updated_at,
    }

    summary_doc = {
        "scope": "all",
        "summary": session_data["summary"],
        "updated_at": updated_at,
    }
    full_doc = {
        "scope": "all",
        "messages": session_data["full_history"],
        "updated_at": updated_at,
    }

    save_json(paths["state"], state_doc)
    save_json(paths["global_summary"], summary_doc)
    save_json(paths["global_full"], full_doc)
