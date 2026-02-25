from session_manager import load_session, save_session
from llm_client import generate_response
from summarizer import summarize_history
from director import analyze_conversation
import json

MAX_HISTORY = 10
KEEP_RECENT = 6

def build_prompt(session_data):
    conversation_text = ""

    if session_data.get("summary"):
        conversation_text += f"これまでの要約:\n{session_data['summary']}\n\n"

    for msg in session_data["history"]:
        role = "User" if msg["role"] == "user" else "AI"
        conversation_text += f"{role}: {msg['content']}\n"

    return conversation_text


def maybe_summarize(session_data):
    if len(session_data["history"]) > MAX_HISTORY:
        old_part = session_data["history"][:-KEEP_RECENT]
        recent_part = session_data["history"][-KEEP_RECENT:]

        new_summary = summarize_history(old_part)

        if session_data.get("summary"):
            combined = session_data["summary"] + "\n" + new_summary
            session_data["summary"] = summarize_history(
                [{"role": "user", "content": combined}]
            )
        else:
            session_data["summary"] = new_summary

        session_data["history"] = recent_part


def main():
    session_data = load_session()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        session_data["history"].append({
            "role": "user",
            "content": user_input
        })

        prompt = build_prompt(session_data)
        ai_reply = generate_response(prompt)
        print("AI:", ai_reply)

        session_data["history"].append({
            "role": "assistant",
            "content": ai_reply
        })
        
        maybe_summarize(session_data)
        
        # …inside loop after maybe_summarize…
        director_output = analyze_conversation(
            session_data.get("summary", ""),
            session_data["history"]
        )

        # JSON部分だけ抽出
        start = director_output.find("{")
        end = director_output.rfind("}") + 1
        
        try:
            parsed = json.loads(director_output[start:end])
            session_data["analysis"] = parsed["analysis"]
            session_data["summary"] = parsed["summary"]
        except Exception as e:
            print("Director解析に失敗:", e)
    
        save_session(session_data)


if __name__ == "__main__":
    main()