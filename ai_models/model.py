from time import sleep
from typing import Tuple

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import INTERVAL
from utils import logger


class ClaudeSlack:
    client: WebClient
    claude_id: str

    def __init__(self, slack_token, claude_id):
        if slack_token is None or not slack_token:
            raise RuntimeError(f"Please configure the parameters: $SLACK_TOKEN in config.py")
        if claude_id is None or not claude_id:
            raise RuntimeError(f"Please configure the parameters: $CLAUDE_ID in config.py")
        # claude_id is member ID use to @Claude, allows Claude to answer your questions
        self.client = WebClient(token=slack_token)
        try:
            self.client.users_info(user=claude_id)
        except SlackApiError as e:
            print(e)
            logger.exception(e)
            raise RuntimeError(f"claude_id:{claude_id} this member does not exist!")
        self.claude_id = claude_id

    def send_message(self, channel_id, message: str, thread_ts=None) -> str:
        # thread_ts means to continue a conversation in the channel. if channel_id is a group, and you want to start a new conversation this value can not be passed
        response = self.client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts,
            text=f"<@{self.claude_id}> {message}"
        )
        # Returns the id of the current message, which can be used to get a reply. When thread_ts is None, it can be used as the thread_ts for the next session.
        return response["ts"]

    def get_reply(self, channel_id, oldest_ts, thread_ts=None) -> str:
        if thread_ts is None or len(thread_ts) == 0:
            thread_ts = None
        # channel_id id of a channel or id of a private conversation
        # oldest_ts is id of the message, which means to get the reply of this message, is actually to get all the messages after this message
        # thread_ts means a conversation id on a channel,if it's a private conversation, you can leave it alone
        try:
            while True:  # The loop waits for the reply to complete
                sleep(INTERVAL)
                response = self.client.conversations_replies(
                    channel=channel_id,
                    oldest=oldest_ts,
                    ts=thread_ts
                )
                message = list(response['messages'][1]["blocks"][0]["elements"][0]["elements"])
                if len(message) == 1 and "style" not in message[0]:
                    return message[0]["text"]
        except IndexError as e:
            print(e)
            logger.exception(e)
            raise RuntimeError("No reply for the time being!")

    def send_message_and_get_reply_on_channel(self, channel_id, message, thread_ts=None) -> Tuple[str, str, str]:
        # channel_id id of a channel or id of a private conversation
        # thread_ts means a conversation id on a channel,if it's None means a new conversation
        if thread_ts is None or len(thread_ts) == 0:
            thread_ts = None
        ts = self.send_message(channel_id, message, thread_ts)
        try:
            if thread_ts is None:  # a new conversation
                return ts, ts, self.get_reply(channel_id=channel_id, oldest_ts=ts, thread_ts=ts)
            else:  # old conversation
                return thread_ts, ts, self.get_reply(channel_id=channel_id, oldest_ts=ts, thread_ts=thread_ts)
        except SlackApiError:
            return thread_ts, ts, "Fail to get reply. Please retry again!"

    def send_message_and_get_reply_on_private_conversation(self, channel_id, message) -> str:
        ts = self.send_message(channel_id, message)
        return self.get_reply(channel_id=channel_id, oldest_ts=ts)

    def send_message_only(self, channel_id, message, thread_ts=None) -> Tuple[str, str]:
        # channel_id id of a channel or id of a private conversation
        # thread_ts means a conversation id on a channel,if it's None means a new conversation
        if thread_ts is None or len(thread_ts) == 0:
            thread_ts = None
        ts = self.send_message(channel_id, message, thread_ts)
        if thread_ts is None:  # a new conversation
            return ts, ts
        else:  # old conversation
            return thread_ts, ts

    def get_reply_fast(self, channel_id, oldest_ts, thread_ts=None) -> str:
        if thread_ts is None or len(thread_ts) == 0:
            thread_ts = None
        # channel_id id of a channel or id of a private conversation
        # oldest_ts is id of the message, which means to get the reply of this message, is actually to get all the messages after this message
        # thread_ts means a conversation id on a channel,if it's a private conversation, you can leave it alone
        try:
            response = self.client.conversations_replies(
                channel=channel_id,
                oldest=oldest_ts,
                ts=thread_ts
            )
            message = list(response['messages'][1]["blocks"][0]["elements"][0]["elements"])
            if len(message) == 1 and "style" not in message[0]:
                return message[0]["text"]
            else:
                return 'False'
        except IndexError as e:
            print(e)
            logger.exception(e)
            return 'False'
