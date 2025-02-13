from fastapi.testclient import TestClient

from src.message_models import InboundMmsMessage, InboundSmsMessage
from src.message_api import app

client = TestClient(app)


def test_receive_sms():
    payload = {
        "from_address": "1234567890",
        "to_address": "0987654321",
        "body": "On my way with donuts!",
        "timestamp": "2021-01-01T00:00:00Z",
        "xillio_id": "1234"
    }
    response = client.post("/webhook/sms", json=payload)
    print(response)
    assert response.status_code == 200
    assert response.json() == {"response": "SMS Received"}

def test_receive_mms():
    payload = {
        "from_address": "1234567890",
        "to_address": "0987654321",
        "body": "On my way with donuts!",
        "timestamp": "2021-01-01T00:00:00Z",
        "xillio_id": "1234"
    }
    response = client.post("/webhook/mms", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "MMS Received"}

def test_receive_sms_invalid():
    payload = {
        "from_address": "1234567890",
        "to_address": "0987654321",
        "body": "On my way with donuts!",
        "timestamp": "2021-01-01T00:00:00Z"
    }
    response = client.post("/webhook/sms", json=payload)
    assert 400 <= response.status_code < 500

def test_receive_mms_invalid():
    payload = {
        "from_address": "1234567890",
        "to_address": "0987654321",
        "body": "On my way with donuts!",
        "timestamp": "2021-01-01T00:00:00Z"
    }
    response = client.post("/webhook/mms", json=payload)
    assert 400 <= response.status_code < 500

