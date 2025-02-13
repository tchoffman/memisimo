from src.message_models import InboundMessage, OutboundMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, db_session):
        self.db_session = db_session

    def _get_or_create_contact(self):
        pass

    def _get_or_create_conversation(self):
        pass

    def process_inbound_message(self, message: InboundMessage):
        try:
            # TODO: Determine "Contact" - Get OR Create Contact
            # TODO: Determine "Conversation" - Get OR Create Conversation
            # TODO: Persist Message / Conversation to Database
            print(f"Received message from {message.from_address} to {message.to_address} at {message.timestamp}")
            return {"response": "Message Processed"}
        except Exception as e:
            logger.error(f"Error processing inbound message: {str(e)}")

    def process_outbound_message(self, message: OutboundMessage):
        #TODO: Determine "Contact" - Get OR Create Contact
        #TODO: Determine "Conversation" - Get OR Create Conversation
        #TODO: Persist Message / Conversation to Database
        pass

        