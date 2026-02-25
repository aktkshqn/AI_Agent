from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
    )

    print("AI:", response.text)