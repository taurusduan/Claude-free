from typing import Optional
from pydantic import BaseModel


class ClaudeRequest(BaseModel):
    channel_id: str
    conversation_key: Optional[str] = None
    message: str
