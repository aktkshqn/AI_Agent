from llm_client import generate_response

def summarize_history(history: list) -> str:
    text = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "AI"
        text += f"{role}: {msg['content']}\n"

    summary_prompt = f"""
以下の会話を簡潔に要約してください。
重要な決定事項・方向性・前提条件を残してください。

{text}
"""

    return generate_response(summary_prompt)