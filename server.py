from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger
import uvicorn

# Import routers
from chat_api import router as chat_router
from chat_ws import register_websocket

# Load env
load_dotenv()
logger.add("logs/chat.log", rotation="500 KB")

# App config
app = FastAPI(
    title="Groq LLM API",
    description="FastAPI wrapper for Groq LLMs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router)
register_websocket(app)

@app.get("/")
def root():
    return {"message": "✅ Web & API Server is live!"}

# Run
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
