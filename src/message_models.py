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

class InboundMessage(Message):
    direction = MessageDirection.INBOUND

class InboundSmsMessage(InboundMessage):
    type: MessageType = MessageType.SMS
    xillio_id: str

class InboundMmsMessage(InboundMessage):
    type: MessageType = MessageType.MMS
    xillio_id: str



