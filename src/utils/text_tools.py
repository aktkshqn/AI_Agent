def trim_history(history: list[dict], max_history: int, keep_recent: int) -> list[dict]:
    if len(history) <= max_history:
        return history
    return history[-keep_recent:]
