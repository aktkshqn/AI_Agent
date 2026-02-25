from llm_client import generate_response


def analyze_conversation(summary: str, recent_history: list[dict]) -> str:
    """
    要約 + 直近履歴を解析して、
    以下の構造の JSON を返す:

    {
      "summary": "...自然文...",
      "analysis": {
        "fact": [],
        "user_intent": [],
        "ai_inference": [],
        "open_questions": []
      }
    }
    """
    history_text = ""
    for msg in recent_history:
        role = "User" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""
以下の会話要約と直近の会話を読み込み、
JSONで必ず次の形のオブジェクトを返してください:

{{
  "summary": "...自然文...",
  "analysis": {{
    "fact": [...],
    "user_intent": [...],
    "ai_inference": [...],
    "open_questions": [...]
  }}
}}

会話要約:
{summary}

直近の会話:
{history_text}
"""

    return generate_response(prompt)