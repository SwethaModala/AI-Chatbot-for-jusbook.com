from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot import JusBookChatbot
from utils import setup_logging, save_conversation
import random
import uvicorn

logger = setup_logging()
app = FastAPI(title="JusBook Chatbot", description="AI Chatbot for jusbook.com")
templates = Jinja2Templates(directory="templates")
chatbot = JusBookChatbot()

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    user_text = (chat_message.message or "").strip()
    try:
        response = chatbot.get_response(user_text)
    except Exception:
        logger.exception("Error generating chatbot response")
        response = random.choice(chatbot.data.default_responses)
    try:
        save_conversation(user_text, response)
    except Exception:
        logger.exception("Failed to save conversation")
    return JSONResponse({"response": response})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.2", port=8000, reload=False)
