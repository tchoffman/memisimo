from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel


class MessageType(str, Enum):
    SMS = "sms"
    MMS = "mms"

class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class Message(BaseModel):
    from_address: str
    to_address: str
    body: str
    attachments: Optional[List[str]] = None
    timestamp: datetime

class InboundSmsMessage(Message):
    type: MessageType = MessageType.SMS
    direction: MessageDirection = MessageDirection.INBOUND
    xillio_id: str

class InboundMmsMessage(Message):
    type: MessageType = MessageType.MMS
    direction: MessageDirection = MessageDirection.INBOUND
    xillio_id: str



