# chat_ws.py
from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger
import requests, os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

def register_websocket(app):
    @app.websocket("/ws")
    async def websocket_ai_chat(websocket: WebSocket):
        await websocket.accept()
        logger.info("🔌 WebSocket connection opened.")
        conversation = []

        try:
            while True:
                user_message = await websocket.receive_text()
                logger.info(f"🧑 User: {user_message}")
                conversation.append({"role": "user", "content": user_message})

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
                    logger.info(f"🤖 Bot: {ai_reply}")
                    await websocket.send_text(ai_reply)
                else:
                    logger.error(response.text)
                    await websocket.send_text("⚠️ AI error occurred.")

        except WebSocketDisconnect:
            logger.warning("❌ WebSocket disconnected.")
