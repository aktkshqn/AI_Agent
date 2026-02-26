def merge_summary(current_summary: str, new_summary: str) -> str:
    new_summary = (new_summary or "").strip()
    if not new_summary:
        return current_summary
    return new_summary
