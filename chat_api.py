# apis/v1/groq_chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from loguru import logger
import requests
import os

# Load from .env if needed
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/chat", tags=["groq-chat"])

# === Config ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")  # Default fallback
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# === Request Model ===
class QuestionRequest(BaseModel):
    question: str

# === POST /chat/ask ===
@router.post("/ask", summary="Ask a question to Groq LLM")
def ask_question(req: QuestionRequest):
    logger.info(f"📨 Received question: {req.question}")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req.question}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        logger.info("✅ Answer generated successfully.")
        return {"question": req.question, "answer": answer}

    except Exception as e:
        logger.error(f"❌ Error while contacting Groq API: {str(e)}")
        return {"error": str(e)}
