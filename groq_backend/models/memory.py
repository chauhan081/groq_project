from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)  # "user" or "bot"
    content = Column(Text, nullable=False)
    msg_type = Column(String, default="text")
    timestamp = Column(DateTime, default=datetime.utcnow)

# Hybrid Memory Class
class Memory:
    def __init__(self):
        self.user_memory = {}

    def add_message(self, user_id: str, sender: str, message: str):
        if user_id not in self.user_memory:
            self.user_memory[user_id] = []
        self.user_memory[user_id].append({"sender": sender, "message": message})

    def get_full_context(self, user_id: str):
        if user_id not in self.user_memory:
            return ""
        return " ".join([msg["message"] for msg in self.user_memory[user_id]])

    def get_last_message(self, user_id: str):
        if user_id not in self.user_memory or not self.user_memory[user_id]:
            return None
        return self.user_memory[user_id][-1]["message"]
