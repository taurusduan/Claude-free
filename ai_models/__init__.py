from config import SLACK_TOKEN, CLAUDE_ID
from .model import *

claude_client = ClaudeSlack(slack_token=SLACK_TOKEN, claude_id=CLAUDE_ID)
