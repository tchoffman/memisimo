from datetime import datetime, timezone
import pytest
from src.message_models import Message, MessageType, MessageDirection, InboundSmsMessage, InboundMmsMessage

@pytest.fixture(scope="module")
def get_text_message():
    return {
        "from_address": "1234567890",
        "to_address": "0987654321",
        "body": "Bring Donuts!",
        "timestamp": "2021-01-01T00:00:00Z"
    }

def test_message_model():
    message = Message(
        from_address="1234567890",
        to_address="0987654321",
        body="Bring Donuts!",
        timestamp="2021-01-01T00:00:00Z"
    )

    assert message.from_address == "1234567890"
    assert message.to_address == "0987654321"
    assert message.body == "Bring Donuts!"
    assert message.timestamp == datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc)

def test_inbound_sms_message():
    message = InboundSmsMessage(
        from_address="1234567890",
        to_address="0987654321",
        body="Bring Donuts!",
        timestamp="2021-01-01T00:00:00Z",
        xillio_id="1234"
    )

    assert message.from_address == "1234567890"
    assert message.to_address == "0987654321"
    assert message.body == "Bring Donuts!"
    assert message.timestamp == datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert message.xillio_id == "1234"
    assert message.type == MessageType.SMS
    assert message.direction == MessageDirection.INBOUND

def test_inbound_mms_message():
    message = InboundMmsMessage(
        from_address="1234567890",
        to_address="0987654321",
        body="Bring Donuts!",
        timestamp="2021-01-01T00:00:00Z",
        xillio_id="1234"
    )

    assert message.from_address == "1234567890"
    assert message.to_address == "0987654321"
    assert message.body == "Bring Donuts!"
    assert message.timestamp == datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert message.xillio_id == "1234"
    assert message.type == MessageType.MMS
    assert message.direction == MessageDirection.INBOUND

def test_from_address_required():
    with pytest.raises(ValueError) as e:
        message = Message(
            to_address="0987654321",
            body="Bring Donuts!",
            timestamp="2021-01-01T00:00:00Z"
        )
    assert str(e.value) == "1 validation error for Message\nfrom_address\n  field required (type=value_error.missing)"

def test_to_address_required():
    with pytest.raises(ValueError) as e:
        message = Message(
            from_address="1234567890",
            body="Bring Donuts!",
            timestamp="2021-01-01T00:00:00Z"
        )
    assert str(e.value) == "1 validation error for Message\nto_address\n  field required (type=value_error.missing)"

def test_body_required():
    with pytest.raises(ValueError) as e:
        message = Message(
            from_address="1234567890",
            to_address="0987654321",
            timestamp="2021-01-01T00:00:00Z"
        )
    assert str(e.value) == "1 validation error for Message\nbody\n  field required (type=value_error.missing)"
    
def test_timestamp_required():
    with pytest.raises(ValueError) as e:
        message = Message(
            from_address="1234567890",
            to_address="0987654321",
            body="Bring Donuts!"
        )
    assert str(e.value) == "1 validation error for Message\ntimestamp\n  field required (type=value_error.missing)"
