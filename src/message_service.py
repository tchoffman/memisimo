from src.message_db import Contact, Conversation, Message
from src.message_models import InboundMessage, MessageType, OutboundMessage
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
            contact_type = "phone" if message.type in ["sms", "mms"] else "email" # TODO: Feels sketchy
            contact = self._get_or_create_contact(message.from_address, contact_type)

            # Determine "Conversation"
            conversation = self._get_or_create_conversation(contact.id)

            # Persist Message / Conversation to Database
            message = Message(
                conversation_id=conversation.id,
                contact_id=contact.id,
                from_address=message.from_address,
                to_address=message.to_address,
                type=message.type,
                xillio_id=message.xillio_id,
                body=message.body,
                attachments=str(message.attachments),
                timestamp=message.timestamp
            )
            self.db.add(message)
            self.db.commit()
            return message
        
        except Exception as e:
            logger.error(f"Error processing inbound message: {str(e)}")
            self.db.rollback()
            raise e

    def process_outbound_message(self, message: OutboundMessage):
        try:
            contact = self._get_or_create_contact(message.to_address, "phone")
            conversation = self._get_or_create_conversation(contact.id)
            message = Message(
                conversation_id=conversation.id,
                contact_id=contact.id,
                from_address=message.from_address,
                to_address=message.to_address,
                type=message.type,
                xillio_id=message.xillio_id,
                body=message.body,
                attachments=str(message.attachments),
                timestamp=message.timestamp
            )
            self.db.add(message)
            self.db.commit()
            logger.info(f"Persisted Outbound Message: {message}")
        except Exception as e:
            logger.error(f"Error processing outbound message: {str(e)}")
            self.db.rollback()
            raise e

        try:
            if message.type in [MessageType.SMS, MessageType.MMS]:
                # TODO: Implement Send SMS/MMS
                logger.info(f"POSTING SMS to  www.provider.app/api/messages")
            elif message.type == MessageType.EMAIL:
                logger.info(f"POSTING EMAIL to  www.mailplus.app/api/email")
            else:
                raise ValueError(f"Invalid message type: {message.type}")
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise e

        return message


        