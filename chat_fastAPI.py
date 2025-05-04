from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
# run_server.py
import uvicorn


load_dotenv()

app = FastAPI()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  # Or "mixtral-8x7b-32768", etc.

class QuestionRequest(BaseModel):
    question: str

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running. Use POST /ask to ask a question."}


@app.post("/ask")
def ask_question(req: QuestionRequest):
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

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return {"question": req.question, "answer": answer}


# if __name__ == "__main__":
#     uvicorn.run("chat_fastAPI:app", host="127.0.0.1", port=8000, reload=True)