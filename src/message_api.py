from fastapi import FastAPI, HTTPException

from src.message_models import InboundMmsMessage, InboundSmsMessage

app = FastAPI()

@app.post("/webhook/sms")
async def receive_sms(message: InboundSmsMessage):
    try:
        print(f"Received SMS from {message.from_address} to {message.to_address} at {message.timestamp}")
        return {"response": "SMS Received"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook/mms")
async def receive_mms(message: InboundMmsMessage):
    try:
        print(f"Received MMS from {message.from_address} to {message.to_address} at {message.timestamp}")
        return {"response": "MMS Received"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
