from .db import SessionLocal
from models.memory import ChatMessage, Memory

# Initialize memory object (used like cache)
memory = Memory()

def save_message(user_id, sender, content, msg_type="text"):
    db = SessionLocal()
    message = ChatMessage(user_id=user_id, sender=sender, content=content, msg_type=msg_type)
    db.add(message)
    db.commit()
    db.close()

    # Also store in memory (cache)
    memory.add_message(user_id, sender, content)

def get_user_history(user_id):
    db = SessionLocal()
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.timestamp).all()
    db.close()
    return messages

def get_conversation_context(user_id):
    return memory.get_full_context(user_id)

def get_last_message(user_id):
    return memory.get_last_message(user_id)

def get_conversation_context(user_id):
    messages = get_user_history(user_id)
    return "\n".join([f"{msg.sender}: {msg.content}" for msg in messages])
