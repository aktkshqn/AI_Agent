import json
from llm_client import generate_response


def _extract_json_object(raw_text: str) -> dict | None:
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    try:
        return json.loads(raw_text[start : end + 1])
    except json.JSONDecodeError:
        return None


def derive_essence_and_strategy(summary: str, recent_history: list[dict]) -> dict:
    history_text = ""
    for msg in recent_history:
        role = "User" if msg.get("role") == "user" else "AI"
        history_text += f"{role}: {msg.get('content', '')}\n"

    prompt = f"""
あなたはTRPG創作支援のディレクターです。
次の情報から、今後の計画に必要な内容だけを抽出し、JSONのみで返してください。

要件:
- JSON以外の文字を含めない
- 日本語で出力
- ノイズ（雑談・感情的反復・重複）を除く
- next_actions は最大3件

出力形式:
{{
  "essence": {{
    "summary": "...",
    "noise_removed_points": ["..."],
    "open_questions": ["..."]
  }},
  "strategy": {{
    "policy": "...",
    "next_actions": ["..."]
  }}
}}

過去要約:
{summary}

直近会話:
{history_text}
"""

    raw = generate_response(prompt)
    parsed = _extract_json_object(raw)
    if not parsed:
        return {
            "essence": {
                "summary": "",
                "noise_removed_points": [],
                "open_questions": [],
            },
            "strategy": {
                "policy": "",
                "next_actions": [],
            },
        }

    return {
        "essence": {
            "summary": parsed.get("essence", {}).get("summary", ""),
            "noise_removed_points": parsed.get("essence", {}).get("noise_removed_points", []),
            "open_questions": parsed.get("essence", {}).get("open_questions", []),
        },
        "strategy": {
            "policy": parsed.get("strategy", {}).get("policy", ""),
            "next_actions": parsed.get("strategy", {}).get("next_actions", []),
        },
    }


def analyze_conversation(summary: str, recent_history: list[dict]) -> str:
    """Backward-compatible wrapper."""
    return json.dumps(
        derive_essence_and_strategy(summary, recent_history),
        ensure_ascii=False,
    )
