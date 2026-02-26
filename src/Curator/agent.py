from llm import generate_summary_response

from .merge import merge_summary
from .parser import extract_json_object
from .prompt_builder import build_curator_prompt
from .schema import empty_essence, normalize_curator_output


def curate_memory(recent_history: list[dict], current_summary: str) -> dict:
    prompt = build_curator_prompt(recent_history=recent_history, current_summary=current_summary)
    raw = generate_summary_response(prompt)
    parsed = extract_json_object(raw)
    if not parsed:
        return {
            "summary": current_summary,
            "essence": empty_essence(),
        }

    normalized = normalize_curator_output(parsed, current_summary)
    normalized["summary"] = merge_summary(current_summary, normalized["summary"])
    return normalized
