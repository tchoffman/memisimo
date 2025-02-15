from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.message_api import app, get_db
from src.message_db import Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite://"  # In-memory database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

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
    assert response.json() == {"response": "Inbound SMS Received"}

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
    assert response.json() == {"response": "Inbound MMS Received"}

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

