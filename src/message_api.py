from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from src.message_db import Base, Message, SessionLocal, engine
from src.message_service import MessageService
from src.message_models import (
    InboundEmailMessage, 
    InboundMmsMessage, 
    InboundSmsMessage, 
    OutboundMessage
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/debug/messages")
async def get_messages(db: Session = Depends(get_db)):
    try:
        messages = db.query(Message).all()
        return {
            "messages": [
                {
                    "id": m.id,
                    "body": m.body,
                    "from": m.from_address,
                    "to": m.to_address,
                    "timestamp": m.timestamp.isoformat() if m.timestamp else None
                } 
                for m in messages
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/webhook/sms")
async def receive_sms(
    message: InboundSmsMessage, 
    db: Session = Depends(get_db)
):
    logger.info(f"Received SMS  {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_inbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"response": "Inbound SMS Received"}

@app.post("/webhook/mms")
async def receive_mms(
    message: InboundMmsMessage, 
    db: Session = Depends(get_db)
):
    logger.info(f"Received MMS from {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_inbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"response": "Inbound MMS Received"}

@app.post("/webhook/email")
async def receive_email(
    message: InboundEmailMessage, 
    db: Session = Depends(get_db)
):
    logger.info(f"Received Email from {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_inbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"response": "Inbound Email Received"}


@app.post("/send")
async def send_message(
    message: OutboundMessage, 
    db: Session = Depends(get_db)
):
    logger.info(f"Sending message from {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_outbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"response": "Outbound Message Sent"}