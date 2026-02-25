from google import genai
import os
import json
from datetime import datetime

# ===== 初期設定 =====
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SAVE_FILE = "session.json"

# ===== セッション読み込み =====
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        session_data = json.load(f)
else:
    session_data = {
        "session_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "history": []
    }

# ===== メインループ =====
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # 履歴に追加
    session_data["history"].append({
        "role": "user",
        "content": user_input
    })

    # モデルに渡す用テキストを構築
    conversation_text = ""
    for msg in session_data["history"]:
        role = "User" if msg["role"] == "user" else "AI"
        conversation_text += f"{role}: {msg['content']}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_text,
    )

    ai_reply = response.text
    print("AI:", ai_reply)

    # AI返答を履歴に追加
    session_data["history"].append({
        "role": "assistant",
        "content": ai_reply
    })

    # JSON保存
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)