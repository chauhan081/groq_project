from pydantic import BaseModel

class TextRequest(BaseModel):
    user_id: str
    prompt: str
