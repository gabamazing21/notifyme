from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy import Column, String, Text, Enum, JSON, ForeignKey, DateTime
from datetime import datetime
import uuid
from secrets import token_urlsafe



class User(db.Model):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    api_key = name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Contact List Model
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    email = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    whatsapp_number = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    custom_fields = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Contact List
class ContactList(db.Model):
    __tablename__ = 'contact_lists'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Contact-List Relationships
class ContactListRelationship(db.Model):
    __tablename__ = 'contacts_list_relationships'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    list_id = Column(String(36), ForeignKey('contact_lists.id'), nullable=False)
    contact_id = Column(String(36), ForeignKey('contacts.id'), nullable=False)


# Notification Templates
class NotificationTemplate(db.MOdel):
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    type = Column(Enum('email', 'sms', 'whatsapp', name='notification_type', nullable=False))
    name = Column(String(255), nullable=False)
    subject = Column(Text, nullable=True) # For email
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

#Notification
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    type = Column(Enum('email', 'sms', 'whatsapp', name='notification_type', nullable=False))
    message = Column(Text, nullable=False)
    receipient = Column(JSON, nullable=False) #list of recipinet id's or addresses
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)