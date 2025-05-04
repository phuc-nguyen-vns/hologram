from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests
import os
from dotenv import load_dotenv


app = FastAPI()

# Load your GROQ or OpenAI-compatible key
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(GROQ_API_KEY)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  # or another model

@app.websocket("/ws")
async def websocket_ai_chat(websocket: WebSocket):
    await websocket.accept()
    conversation = []

    try:
        while True:
            user_message = await websocket.receive_text()
            conversation.append({"role": "user", "content": user_message})

            # Send to Groq / OpenAI
            payload = {
                "model": GROQ_MODEL,
                "messages": [{"role": "system", "content": "You are a helpful assistant."}] + conversation
            }

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(GROQ_URL, headers=headers, json=payload)
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                conversation.append({"role": "assistant", "content": ai_reply})
                await websocket.send_text(ai_reply)
            else:
                await websocket.send_text("⚠️ AI error: " + response.text)

    except WebSocketDisconnect:
        print("🔌 Client disconnected")
