from session_manager import load_session, save_session
from llm_client import generate_response
from summarizer import summarize_and_extract

MAX_HISTORY = 12
KEEP_RECENT = 8


def build_prompt(session_data: dict) -> str:
    conversation_text = (
        "You are a supportive creative partner for TRPG campaign planning.\n"
        "Keep responses practical and concise.\n\n"
    )

    if session_data.get("summary"):
        conversation_text += f"Session summary so far:\n{session_data['summary']}\n\n"

    for msg in session_data["history"]:
        role = "User" if msg["role"] == "user" else "AI"
        conversation_text += f"{role}: {msg['content']}\n"

    conversation_text += "AI:"
    return conversation_text


def maybe_summarize(session_data: dict) -> None:
    if len(session_data["history"]) <= MAX_HISTORY:
        return

    old_part = session_data["history"][:-KEEP_RECENT]
    recent_part = session_data["history"][-KEEP_RECENT:]

    try:
        extracted = summarize_and_extract(old_part)
        new_summary = extracted.get("summary", "").strip()
        if new_summary:
            if session_data.get("summary"):
                session_data["summary"] += "\n" + new_summary
            else:
                session_data["summary"] = new_summary
        session_data["analysis"] = {
            "tags": extracted.get("tags", []),
            "uncertain_points": extracted.get("uncertain_points", []),
        }
    except Exception as exc:
        print(f"[warn] summarize failed: {exc}")

    session_data["history"] = recent_part


def main() -> None:
    session_data = load_session()
    print("CUI chat started. Type 'exit' to finish.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        session_data["history"].append({"role": "user", "content": user_input})

        try:
            ai_reply = generate_response(build_prompt(session_data))
        except Exception as exc:
            print(f"AI: [error] failed to call model: {exc}")
            continue

        print(f"AI: {ai_reply}")
        session_data["history"].append({"role": "assistant", "content": ai_reply})

        maybe_summarize(session_data)
        save_session(session_data)

    save_session(session_data)


if __name__ == "__main__":
    main()
