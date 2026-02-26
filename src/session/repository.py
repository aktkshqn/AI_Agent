from datetime import datetime

from .paths import find_latest_session_id, session_paths
from .schema import ensure_memory_shape, new_session_payload
from .storage import load_json, save_json


def _new_session_id() -> str:
    # Second-level ID with collision-safe suffix.
    base = datetime.now().strftime("%Y%m%d-%H%M%S")
    paths = session_paths(base)
    if not load_json(paths["state"], {}):
        return base

    idx = 1
    while True:
        candidate = f"{base}-{idx:02d}"
        if not load_json(session_paths(candidate)["state"], {}):
            return candidate
        idx += 1


def load_session(session_id=None, create_new=False):
    if create_new:
        new_id = _new_session_id()
        state = new_session_payload(new_id)
        paths = session_paths(new_id)

        summary_index = load_json(paths["summary_index"], {})
        legacy_summary = load_json(paths["legacy_summary"], {"summary": ""})
        all_summary_text = summary_index.get("global_summary", legacy_summary.get("summary", ""))
        all_full = load_json(paths["global_full"], {"messages": []})
        all_essence = load_json(
            paths["global_essence"],
            load_json(
                paths["legacy_essence"],
                {"essence": {"summary": "", "noise_removed_points": [], "open_questions": []}},
            ),
        )

        state["summary"] = all_summary_text
        state["full_history"] = all_full.get("messages", [])
        state["essence"] = all_essence.get("essence", state.get("essence", {}))
        return ensure_memory_shape(state)

    target_id = session_id or find_latest_session_id()
    if target_id:
        paths = session_paths(target_id)
        state = load_json(paths["state"], new_session_payload(target_id))
        summary_index = load_json(paths["summary_index"], {})
        legacy_summary = load_json(paths["legacy_summary"], {"summary": state.get("summary", "")})
        all_summary_text = summary_index.get("global_summary", legacy_summary.get("summary", state.get("summary", "")))
        all_full = load_json(paths["global_full"], {"messages": state.get("full_history", [])})
        all_essence = load_json(
            paths["global_essence"],
            load_json(
                paths["legacy_essence"],
                {"essence": state.get("essence", {"summary": "", "noise_removed_points": [], "open_questions": []})},
            ),
        )

        state["summary"] = all_summary_text
        state["full_history"] = all_full.get("messages", state.get("full_history", []))
        state["essence"] = all_essence.get("essence", state.get("essence", {}))
        return ensure_memory_shape(state)

    new_id = _new_session_id()
    return new_session_payload(new_id)


def save_session(session_data: dict):
    session_data = ensure_memory_shape(session_data)
    session_id = session_data["session_id"]
    paths = session_paths(session_id)
    updated_at = datetime.now().isoformat(timespec="seconds")

    state_doc = {
        "session_id": session_id,
        "history": session_data["history"],
        "updated_at": updated_at,
    }

    summary_index = load_json(paths["summary_index"], {"global_summary": "", "topics": []})
    summary_index["global_summary"] = session_data["summary"]
    summary_index["updated_at"] = updated_at
    full_doc = {
        "scope": "all",
        "messages": session_data["full_history"],
        "updated_at": updated_at,
    }
    essence_doc = {
        "scope": "all",
        "essence": session_data["essence"],
        "updated_at": updated_at,
    }

    save_json(paths["state"], state_doc)
    save_json(paths["summary_index"], summary_index)
    save_json(paths["global_full"], full_doc)
    save_json(paths["global_essence"], essence_doc)
