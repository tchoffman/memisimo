from message_db import Contact, Conversation
from src.message_models import InboundMessage, OutboundMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, db_session):
        self.db = db_session

    def _get_or_create_contact(self, connection, type):
        contact = self.db.query(Contact).filter_by(connection=connection).first()
        if not contact:
            contact = Contact(connection=connection, type=type)
            self.db.add(contact)
            self.db.commit()
        return contact

    def _get_or_create_conversation(self, contact_id):
        conversation = self.db.query(Conversation).filter_by(contact_id=contact_id).first()
        if not conversation:
            conversation = Conversation(contact_id=contact_id)
            self.db.add(conversation)
            self.db.commit()
        return conversation

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

        