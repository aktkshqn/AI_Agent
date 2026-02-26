def empty_essence() -> dict:
    return {
        "summary": "",
        "noise_removed_points": [],
        "open_questions": [],
    }


def normalize_curator_output(parsed: dict, current_summary: str) -> dict:
    essence = parsed.get("essence", {}) if isinstance(parsed, dict) else {}
    return {
        "summary": (parsed.get("summary", current_summary) if isinstance(parsed, dict) else current_summary),
        "essence": {
            "summary": essence.get("summary", ""),
            "noise_removed_points": essence.get("noise_removed_points", []),
            "open_questions": essence.get("open_questions", []),
        },
    }
