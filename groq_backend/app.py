from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes.text_handler import router as text_router
from routes.image_handler import router as image_router
from routes.audio_handler import router as audio_router
from models.memory import Base, ChatMessage
from utils.db import engine
from utils.memory import save_message, get_conversation_context, get_last_message, get_user_history

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Table creation
Base.metadata.create_all(bind=engine)

# Message Model for hybrid save endpoint
class Message(BaseModel):
    user_id: str
    sender: str
    content: str
    msg_type: str = "text"

@app.post("/send_message")
def send_message_endpoint(msg: Message):
    try:
        save_message(msg.user_id, msg.sender, msg.content, msg.msg_type)
        context = get_conversation_context(msg.user_id)
        return {"status": "Message saved", "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/get_last_message/{user_id}")
def get_last_message_endpoint(user_id: str):
    try:
        last_message = get_last_message(user_id)
        return {"last_message": last_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/get_user_history/{user_id}")
def get_user_history_endpoint(user_id: str):
    try:
        messages = get_user_history(user_id)
        return {"messages": [msg.content for msg in messages]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Groq Assistant API is running 🚀"}

# Routers
app.include_router(text_router, prefix="/api")
app.include_router(image_router, prefix="/api")
app.include_router(audio_router, prefix="/api")
