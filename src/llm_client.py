import re
import time

from llm import generate_with_gemini, generate_with_groq, generate_with_openrouter

_cooldown_until = {
    "dialog_gemini": 0.0,
    "dialog_groq": 0.0,
    "dialog_openrouter": 0.0,
    "summary_groq": 0.0,
    "summary_openrouter": 0.0,
}


def _parse_retry_seconds(text: str) -> int:
    m = re.search(r"retry[^0-9]*([0-9]+(?:\.[0-9]+)?)\s*s", text, flags=re.IGNORECASE)
    if m:
        return max(1, int(float(m.group(1))))
    return 30


def _guard_rate_limit(channel: str) -> None:
    now = time.time()
    if now < _cooldown_until[channel]:
        wait = int(_cooldown_until[channel] - now) + 1
        raise RuntimeError(f"{channel} is cooling down ({wait}s).")


def _call_with_cooldown(channel: str, fn, prompt: str) -> str:
    _guard_rate_limit(channel)
    try:
        return fn(prompt)
    except Exception as exc:
        text = str(exc)
        if "429" in text or "RESOURCE_EXHAUSTED" in text or "rate" in text.lower():
            retry = _parse_retry_seconds(text)
            _cooldown_until[channel] = time.time() + retry
            raise RuntimeError(f"{channel} rate-limited. retry in {retry}s.") from exc
        raise


def generate_dialog_response(prompt: str) -> str:
    try:
        # メイン: Groq (高速ダイアローグ用) を優先してみる
        return _call_with_cooldown("dialog_groq", generate_with_groq, prompt)
    except Exception:
        try:
            # 代役1: 本家Gemini API
            return _call_with_cooldown("dialog_gemini", generate_with_gemini, prompt)
        except Exception:
            try:
                # 代役2: OpenRouter の無料枠モデル
                return _call_with_cooldown("dialog_openrouter", generate_with_openrouter, prompt)
            except RuntimeError as exc:
                msg = str(exc)
                if "cooling down" in msg or "rate-limited" in msg:
                    return "Okay. Please continue."
                raise

def generate_summary_response(prompt: str) -> str:
    try:
        # メイン: 本家Gemini 或いは Groq
        return _call_with_cooldown("summary_groq", generate_with_groq, prompt)
    except Exception:
        # 代役: OpenRouter
        return _call_with_cooldown("summary_openrouter", generate_with_openrouter, prompt)


def generate_response(prompt: str) -> str:
    return generate_dialog_response(prompt)


__all__ = ["generate_response", "generate_dialog_response", "generate_summary_response"]
