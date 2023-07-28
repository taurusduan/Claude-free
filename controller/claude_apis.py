from fastapi import APIRouter

from models import ClaudeRequest
from service.claude_service import send_message, receive_reply, check_channel_id, send_message_only, receive_reply_fast

router = APIRouter(
    prefix="/claude",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/send")
async def send(data: ClaudeRequest):
    data.channel_id = check_channel_id(data.channel_id)
    return send_message(data)


@router.post("/receive_reply")
async def receive(data: ClaudeRequest):
    data.channel_id = check_channel_id(data.channel_id)
    return receive_reply(data)


@router.post("/send_only")
async def send_only(data: ClaudeRequest):
    data.channel_id = check_channel_id(data.channel_id)
    return send_message_only(data)


@router.post("/receive_reply_fast")
async def receive_fast(data: ClaudeRequest):
    data.channel_id = check_channel_id(data.channel_id)
    return receive_reply_fast(data)
