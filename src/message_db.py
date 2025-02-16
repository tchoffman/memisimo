from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///./memisimo.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    type = Column(Enum("sms", "mms"), nullable=False)
    xillio_id = Column(String, nullable=False)
    body = Column(String, nullable=False)
    attachments = Column(String)
    timestamp = Column(DateTime, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    contact = relationship("Contact", back_populates="messages")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    connection = Column(String, nullable=False) # phone number or email
    type = Column(Enum("phone", "email"), nullable=False)
    messages = relationship("Message", back_populates="contact")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    messages = relationship("Message", back_populates="conversation")