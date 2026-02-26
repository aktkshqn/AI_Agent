from session_manager import load_session, save_session
from llm_client import generate_response
from summarizer import summarize_and_extract
from director import derive_essence_and_strategy

MAX_HISTORY = 12
KEEP_RECENT = 8


def update_director_memories(session_data: dict) -> None:
    memories = session_data.setdefault("memories", {})
    try:
        result = derive_essence_and_strategy(
            session_data.get("summary", ""),
            session_data.get("history", []),
        )
    except Exception as exc:
        print(f"[warn] director update failed: {exc}")
        return

    memories["essence"] = result.get("essence", memories.get("essence", {}))
    memories["strategy"] = result.get("strategy", memories.get("strategy", {}))


def build_prompt(session_data: dict) -> str:
    memories = session_data.get("memories", {})
    essence = memories.get("essence", {})
    strategy = memories.get("strategy", {})

    prompt = (
        "You are a supportive creative partner for TRPG campaign planning.\n"
        "Keep responses practical and concise.\n\n"
    )

    if session_data.get("summary"):
        prompt += f"Past summary:\n{session_data['summary']}\n\n"

    points = essence.get("noise_removed_points", [])
    if points:
        prompt += "Planning essence:\n"
        prompt += "\n".join(f"- {p}" for p in points) + "\n\n"

    if strategy.get("policy"):
        prompt += f"Current policy:\n{strategy['policy']}\n\n"

    for msg in session_data.get("history", []):
        role = "User" if msg["role"] == "user" else "AI"
        prompt += f"{role}: {msg['content']}\n"

    prompt += "AI:"
    return prompt


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
    session_data = load_session(create_new=True)  # New chat state, shared daily summary/full
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
            ai_reply = generate_response(build_prompt(session_data))
        except Exception as exc:
            print(f"AI: [error] failed to call model: {exc}")
            continue

        print(f"AI: {ai_reply}")

        ai_msg = {"role": "assistant", "content": ai_reply}
        session_data["history"].append(ai_msg)
        session_data["full_history"].append(ai_msg)

        maybe_summarize(session_data)
        update_director_memories(session_data)
        save_session(session_data)

    save_session(session_data)


if __name__ == "__main__":
    main()

