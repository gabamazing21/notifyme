
from  sqlalchemy import Column, String, Text, Enum, JSON, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid
from base import Base



class User(Base):
    """
    User: Model for users and create table
    """
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True, nullable=True) # Added API key
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign_lists = relationship(
        "CampaignList", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="dynamic")
    
    notification_templates = relationship(
        "NotificationTemplate",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic")


