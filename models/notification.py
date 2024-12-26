from  sqlalchemy import Column, String, Text, Enum, JSON, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid
from db import Base

# Notification


class Notification(Base):
    """
    models for notifications
    """
    __tablename__ = 'notifications'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    type = Column(Enum('email', 'sms', 'whatsapp', name='notification_type', nullable=False))
    message = Column(Text, nullable=False)
    receipient = Column(JSON, nullable=False) #list of recipinet id's or addresses
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")