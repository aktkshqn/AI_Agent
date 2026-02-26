def normalize_dialog_reply(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        return "うん。続けて。"
    # Keep the listening style compact.
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines[:3])
