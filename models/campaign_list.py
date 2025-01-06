from  sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
import uuid


# Contact List
class CampaignList(Base):
    __tablename__ = 'campaign_lists'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="campaign_lists")
    contacts = relationship("Contact", back_populates="campaign_list", cascade="all, delete-orphan")
    scheduled = relationship("Scheduled", back_populates="campaign_lists")