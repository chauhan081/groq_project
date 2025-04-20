from fastapi import APIRouter, Request, Depends
from utils.groq_llm import query_groq
from utils.translator import detect_and_translate
from utils.memory import save_message, get_conversation_context
from utils.db import get_db, SessionLocal
from models.schemas import TextRequest

router = APIRouter()

# Define generate_response_from_groq
def generate_response_from_groq(context):
    # Example: Call your Groq-based function here (query_groq)
    response = query_groq(context)
    return response

@router.post("/text")
async def handle_text_input(request: TextRequest, db: SessionLocal = Depends(get_db)):
    # 1. Save user message
    save_message(request.user_id, "user", request.prompt)

    # 2. Get full conversation context
    context = get_conversation_context(request.user_id)

    # 3. Generate Groq response using full context
    groq_response = generate_response_from_groq(context)  # this should include full convo
    
    # 4. Save bot response
    save_message(request.user_id, "bot", groq_response)

    return {"response": groq_response}
