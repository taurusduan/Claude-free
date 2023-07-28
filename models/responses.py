from typing import Optional

from pydantic import BaseModel


class ClaudeResponse(BaseModel):
    conversation_key: str
    message_key: str
    message: Optional[str] = None
