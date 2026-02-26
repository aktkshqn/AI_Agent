from llm_client import generate_response

from .parser import extract_json_object
from .prompt_builder import build_curator_prompt


def curate_memory(recent_history: list[dict], current_summary: str) -> dict:
    prompt = build_curator_prompt(recent_history=recent_history, current_summary=current_summary)
    raw = generate_response(prompt)
    parsed = extract_json_object(raw)
    if not parsed:
        return {
            "summary": current_summary,
            "essence": {
                "summary": "",
                "noise_removed_points": [],
                "open_questions": [],
            },
        }

    essence = parsed.get("essence", {})
    return {
        "summary": parsed.get("summary", current_summary),
        "essence": {
            "summary": essence.get("summary", ""),
            "noise_removed_points": essence.get("noise_removed_points", []),
            "open_questions": essence.get("open_questions", []),
        },
    }
