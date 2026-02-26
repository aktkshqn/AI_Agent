from .policy import DIALOG_POLICY


def build_dialog_prompt(user_input: str, history: list[dict], summary: str) -> str:
    prompt = DIALOG_POLICY.strip() + "\n\n"
    if summary:
        prompt += f"Context summary:\n{summary}\n\n"

    for msg in history:
        role = "User" if msg.get("role") == "user" else "AI"
        prompt += f"{role}: {msg.get('content', '')}\n"

    prompt += f"User: {user_input}\nAI:"
    return prompt
