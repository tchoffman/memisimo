from fastapi import FastAPI, HTTPException
import logging

from message_db import SessionLocal
from message_service import MessageService
from src.message_models import InboundMmsMessage, InboundSmsMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook/sms")
async def receive_sms(message: InboundSmsMessage, db = next(get_db())):
    logger.log(f"Received SMS  {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_inbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook/mms")
async def receive_mms(message: InboundMmsMessage, db = next(get_db())):
    # TODO: Refactor: Extract Method for SMS and MMS
    logger.log(f"Received MMS from {message.from_address} to {message.to_address} at {message.timestamp}")
    service = MessageService(db)
    try:
        service.process_inbound_message(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
