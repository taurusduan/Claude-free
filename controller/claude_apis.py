from fastapi import APIRouter

from models import ClaudeRequest
from service.claude_service import send_message

router = APIRouter(
    prefix="/claude",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/send")
async def saving_data(data: ClaudeRequest):
    return send_message(data)
