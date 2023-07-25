from typing import Optional
from pydantic import BaseModel


class ClaudeRequest(BaseModel):
    channel_id: Optional[str] = None
    conversation_key: Optional[str] = None
    message_key: Optional[str] = None
    message: Optional[str] = None
