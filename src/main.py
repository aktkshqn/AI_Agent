from Curator import curate_memory
from Dialog import generate_dialog_reply
from session_manager import load_session, save_session

MAX_HISTORY = 12
KEEP_RECENT = 8


def trim_history(history: list[dict]) -> list[dict]:
    if len(history) <= MAX_HISTORY:
        return history
    return history[-KEEP_RECENT:]


def main() -> None:
    session_data = load_session(create_new=True)
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

        user_msg = {"role": "user", "content": user_input}
        session_data["history"].append(user_msg)
        session_data["full_history"].append(user_msg)

        try:
            ai_reply = generate_dialog_reply(
                user_input=user_input,
                history=session_data["history"][:-1],
                summary=session_data.get("summary", ""),
            )
        except Exception as exc:
            print(f"AI: [error] failed to call model: {exc}")
            continue

        print(f"AI: {ai_reply}")
        ai_msg = {"role": "assistant", "content": ai_reply}
        session_data["history"].append(ai_msg)
        session_data["full_history"].append(ai_msg)

        try:
            curated = curate_memory(
                recent_history=session_data["history"],
                current_summary=session_data.get("summary", ""),
            )
            session_data["summary"] = curated.get("summary", session_data.get("summary", ""))
            session_data["essence"] = curated.get("essence", session_data.get("essence", {}))
        except Exception as exc:
            print(f"[warn] curator failed: {exc}")

        session_data["history"] = trim_history(session_data["history"])
        save_session(session_data)

    save_session(session_data)


if __name__ == "__main__":
    main()
