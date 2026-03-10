from .gemini import generate_with_gemini
from .groq import generate_with_groq
from .openrouter import generate_with_openrouter


def generate_dialog_response(prompt: str) -> str:
    return generate_with_gemini(prompt)


def generate_summary_response(prompt: str) -> str:
    return generate_with_groq(prompt)
