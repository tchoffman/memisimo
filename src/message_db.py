from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    type = Column(Enum("sms", "mms"), nullable=False)
    xillio_id = Column(String, nullable=False)
    body = Column(String, nullable=False)
    attachments = Column(String)
    timestamp = Column(DateTime, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    connection = Column(String, nullable=False) # phone number or email
    type = Column(Enum("phone", "email"), nullable=False)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
