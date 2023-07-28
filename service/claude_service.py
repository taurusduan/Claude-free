from config import CHANNEL_ID
from models import ClaudeRequest, ClaudeResponse
from ai_models import claude_client as client


def send_message(data: ClaudeRequest) -> ClaudeResponse:
    conversation_key, message_key, message = client.send_message_and_get_reply_on_channel(channel_id=data.channel_id,
                                                                                          message=data.message,
                                                                                          thread_ts=data.conversation_key)
    return ClaudeResponse(conversation_key=conversation_key, message_key=message_key, message=message)


def receive_reply(data: ClaudeRequest) -> ClaudeResponse:
    message = client.get_reply(channel_id=data.channel_id, oldest_ts=data.message_key, thread_ts=data.conversation_key)
    return ClaudeResponse(conversation_key=data.conversation_key, message_key=data.message_key, message=message)


def check_channel_id(channel_id: str) -> str:
    if channel_id is None or len(channel_id) == 0:
        if CHANNEL_ID is None or len(CHANNEL_ID) == 0:
            raise RuntimeError(
                "Configure the CHANNEL_ID parameter in config.py, or pass the channel_id parameter in the request.")
        else:
            return CHANNEL_ID
    else:
        return channel_id


def send_message_only(data: ClaudeRequest) -> ClaudeResponse:
    conversation_key, message_key = client.send_message_only(channel_id=data.channel_id,
                                                             message=data.message,
                                                             thread_ts=data.conversation_key)
    return ClaudeResponse(conversation_key=conversation_key, message_key=message_key)


def receive_reply_fast(data: ClaudeRequest) -> ClaudeResponse:
    message = client.get_reply_fast(channel_id=data.channel_id, oldest_ts=data.message_key,
                                    thread_ts=data.conversation_key)
    return ClaudeResponse(conversation_key=data.conversation_key, message_key=data.message_key, message=message)
