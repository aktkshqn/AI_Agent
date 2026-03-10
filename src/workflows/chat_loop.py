from Curator import curate_memory
from Dialog import generate_dialog_reply
import os
from session import load_session, save_session
from utils.text_tools import trim_history

MAX_HISTORY = 12
KEEP_RECENT = 8
SUMMARY_INTERVAL_RALLIES = 6


def _should_run_curator(full_history: list[dict]) -> bool:
    # 1 rally = user + assistant (2 messages)
    rally_count = len(full_history) // 2
    return rally_count > 0 and rally_count % SUMMARY_INTERVAL_RALLIES == 0


def run_chat_loop() -> None:
    session_data = load_session(create_new=True)
    print("CUI chat started. Type 'exit' to finish.")
    if not os.getenv("GROQ_API_KEY"):
        print("[warn] GROQ_API_KEY is not set. Curator summary updates may fail.")
    if not os.getenv("GOOGLE_API_KEY"):
        print("[warn] GOOGLE_API_KEY is not set. Dialog replies may fail.")

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

        if _should_run_curator(session_data["full_history"]):
            try:
                curated = curate_memory(
                    recent_history=session_data["history"],
                    current_summary=session_data.get("summary", ""),
                )
                session_data["summary"] = curated.get("summary", session_data.get("summary", ""))
                session_data["essence"] = curated.get("essence", session_data.get("essence", {}))
            except Exception as exc:
                print(f"[warn] curator failed: {exc}")

        session_data["history"] = trim_history(session_data["history"], MAX_HISTORY, KEEP_RECENT)
        save_session(session_data)

    save_session(session_data)
