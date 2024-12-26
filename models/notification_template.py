from  sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
import uuid

# Notification Templates
class NotificationTemplate(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    type = Column(Enum('email', 'sms', 'whatsapp', name='notification_type', nullable=False))
    name = Column(String(255), nullable=False)
    subject = Column(Text, nullable=True) # For email
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")

