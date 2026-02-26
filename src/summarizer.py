from llm_client import generate_response
import json

def summarize_and_extract(history: list) -> dict:
    # conversation text をつなげる
    text = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "AI"
        text += f"{role}: {msg['content']}\n"

    # LLM に雑談ノイズ除去 + 要約 + JSONタグ付けを指示
    prompt = f"""
次の会話履歴を分析してください。

1) 雑談・創作と無関係な雑談を削除
2) 重要と思われる内容を簡潔に要約
3) 以下の 3 つのカテゴリに分類して JSON で返答

- "summary": 重要情報の要約
- "tags": その要約に対するタグ配列 (FACT / USER_INTENT / AI_INFERENCE / CREATIVE_ASSUMPTION)
- "uncertain_points": あいまい・未確定な点の要約

出力は **この形式の JSON オブジェクトだけ** にしてください。

会話履歴:
{text}
"""

    # API 呼び出し
    raw_resp = generate_response(prompt)

    # 返り値を JSON として扱う
    try:
        structured = json.loads(raw_resp)
    except json.JSONDecodeError:
        # パースできない時は fallback
        structured = {
            "summary": raw_resp,
            "tags": [],
            "uncertain_points": []
        }

    return structured