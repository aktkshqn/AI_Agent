from llm_client import generate_response

from .prompt_builder import build_dialog_prompt


def generate_dialog_reply(user_input: str, history: list[dict], summary: str) -> str:
    prompt = build_dialog_prompt(user_input=user_input, history=history, summary=summary)
    return generate_response(prompt)
