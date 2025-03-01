from datetime import datetime
from enum import Enum
from typing import ClassVar, List, Optional, Union
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    SMS = "sms"
    MMS = "mms"
    EMAIL = "email"

class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class Message(BaseModel):
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    body: str
    attachments: Optional[List[str]] = None
    timestamp: datetime

class InboundMessage(Message):
    direction: ClassVar[MessageDirection] = MessageDirection.INBOUND
    type: MessageType

class InboundSmsMessage(InboundMessage):
    type: MessageType = MessageType.SMS
    xillio_id: str

class InboundMmsMessage(InboundMessage):
    type: MessageType = MessageType.MMS
    xillio_id: str

class InboundEmailMessage(InboundMessage):
    type: MessageType = MessageType.EMAIL
    xillio_id: str

class OutboundMessage(Message):
    direction: ClassVar[MessageDirection] = MessageDirection.OUTBOUND
    type: MessageType
    xillio_id: str



