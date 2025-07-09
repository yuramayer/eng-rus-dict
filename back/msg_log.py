"""Methods for the logging the bot's messages"""

from datetime import datetime, timezone
from dataclasses import dataclass, field


# pylint: disable=too-many-instance-attributes
@dataclass
class MessageLog:
    """
    Structured data object representing bot interaction event

    :param timestamp: ISO UTC timestamp of the message,
        default value - current timestamp
    :param chat_id: TG message chat id
    :param message_id: ID of the message in the Telegram
    :param direction: Direction of the message,
        should be 'inbound' (from user)
        or 'outbound' (from the bot)
    :param text: Content of the message
    :param router: Bot's router that handled the message
    :param method: Bot's method or handler name
    :param event_type: Type of the interaction:
        "message", "command", "error", etc
    """
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())
    chat_id: int
    message_id: int
    direction: str
    text: str
    router: str
    method: str
    event_type: str


def create_msg_log(
        log: MessageLog) -> dict:
    """
    Converts MessageLog object into dict for logging

    :param log: MessageLog dataclass instance with context
    :return: Dictionary for S3 Storage uploading
    """
    log_dict = {
        'timestamp': log.timestamp,
        'chat_id': log.chat_id,
        'message_id': log.message_id,
        'direction': log.direction,
        'text': log.text,
        'router': log.router,
        'method': log.method,
        'event_type': log.event_type
    }
    return log_dict
