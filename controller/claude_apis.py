from fastapi import APIRouter

from models import ClaudeRequest
from service.claude_service import send_message, receive_reply, check_channel_id

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
