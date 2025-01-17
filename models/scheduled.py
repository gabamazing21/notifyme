
from  sqlalchemy import Column, String, Text, Enum, JSON, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid
from base import Base

class Scheduled(Base):
    __tablename__ = "scheduled"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    campaign_id = Column(String(36), ForeignKey('campaign_lists.id'), nullable=False)
    template_id = Column(String(36), ForeignKey('notification_templates.id'), nullable=False)
    method = Column(Enum("sms", "whatsapp", "email", name="method_enum"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum("pending", "sent", name="status_enum"), default="pending")

    # relationship
    user = relationship("User", back_populates="scheduled")
    campaign_lists = relationship("CampaignList", back_populates="scheduled")
    notification_templates = relationship("NotificationTemplate", back_populates="scheduled")