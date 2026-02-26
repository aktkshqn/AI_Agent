from .gemini import generate_with_gemini
from .groq import generate_with_groq


def generate_dialog_response(prompt: str) -> str:
    return generate_with_gemini(prompt)


def generate_summary_response(prompt: str) -> str:
    return generate_with_groq(prompt)
