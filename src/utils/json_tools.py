import json


def dumps_pretty(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
