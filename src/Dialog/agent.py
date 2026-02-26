from llm import generate_dialog_response

from .prompt_builder import build_dialog_prompt
from .validator import normalize_dialog_reply


def generate_dialog_reply(user_input: str, history: list[dict], summary: str) -> str:
    prompt = build_dialog_prompt(user_input=user_input, history=history, summary=summary)
    return normalize_dialog_reply(generate_dialog_response(prompt))
