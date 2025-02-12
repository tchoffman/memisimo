from fastapi.testclient import TestClient

from src.message_api import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_put_root():
    payload = {
        "message": "Goodnight Moon"
    }

    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"body": "Processed payload {'message': 'Goodnight Moon'}"}

