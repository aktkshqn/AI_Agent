def build_curator_prompt(recent_history: list[dict], current_summary: str) -> str:
    history_text = ""
    for msg in recent_history:
        role = "User" if msg.get("role") == "user" else "AI"
        history_text += f"{role}: {msg.get('content', '')}\n"

    return f"""
あなたはTRPG創作対話の記録整理担当です。
以下の会話から、全体要約の更新案とノイズ除去済み要点をJSONのみで返してください。

要件:
- JSON以外を出力しない
- 日本語で出力
- 過剰に長くしない

出力形式:
{{
  "summary": "更新後の要約",
  "essence": {{
    "summary": "要点の短い要約",
    "noise_removed_points": ["..."],
    "open_questions": ["..."]
  }}
}}

現在の要約:
{current_summary}

直近会話:
{history_text}
"""
