from models import ClaudeRequest, ClaudeResponse
from ai_models import claude_client as client


def send_message(data: ClaudeRequest) -> ClaudeResponse:
    conversation_key, message_key, message = client.send_message_and_get_reply_on_channel(channel_id=data.channel_id,
                                                                                          message=data.message,
                                                                                          thread_ts=data.conversation_key)
    return ClaudeResponse(conversation_key=conversation_key, message_key=message_key, message=message)
