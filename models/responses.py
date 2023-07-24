from pydantic import BaseModel


class ClaudeResponse(BaseModel):
    conversation_key: str
    message_key: str
    message: str
