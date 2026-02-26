from llm import generate_dialog_response, generate_summary_response


def generate_response(prompt: str) -> str:
    # Backward compatible default path.
    return generate_dialog_response(prompt)


__all__ = ["generate_response", "generate_dialog_response", "generate_summary_response"]
