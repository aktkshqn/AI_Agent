import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

MEMORY_FILE = "memory.json"

# ---- メモリ読み込み ----
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ---- メモリ保存 ----
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # メモリに追加
    memory.append({"role": "user", "content": user_input})

    # GeminiはChat形式と少し違うのでまとめて渡す
    conversation_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in memory]
    )

    response = model.generate_content(conversation_text)
    reply = response.text

    print("AI:", reply)

    memory.append({"role": "assistant", "content": reply})

    save_memory(memory)