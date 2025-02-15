from src.message_db import Contact, Conversation, Message
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
            # Determine "Contact"
            contact_type = "phone" if message.type in ["sms", "mms"] else "email" # TODO: Should rely on an Enum/Map of message type to contact type.
            contact = self._get_or_create_contact(message.from_address, contact_type)

            # Determine "Conversation"
            conversation = self._get_or_create_conversation(contact.id)

            # Persist Message / Conversation to Database
            # TODO: Naming of Pydantic and SQLAlchemy models confusing/clashing
            message = Message(
                from_address=message.from_address,
                to_address=message.to_address,
                type=message.type,
                xillio_id=message.xillio_id,
                body=message.body,
                timestamp=message.timestamp,
                conversation_id=conversation.id
            )
            self.db.add(message)
            self.db.commit()
            return message
        
        except Exception as e:
            logger.error(f"Error processing inbound message: {str(e)}")

    def process_outbound_message(self, message: OutboundMessage):
        #TODO: Determine "Contact" - Get OR Create Contact
        #TODO: Determine "Conversation" - Get OR Create Conversation
        #TODO: Persist Message / Conversation to Database
        pass

        