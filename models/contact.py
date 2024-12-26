from  sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
import uuid


# Contact List Model
class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_list_id = Column(String(36), ForeignKey('campaign_lists.id'), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    email = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    whatsapp_number = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    custom_fields = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    campaign_list = relationship("CampaignList", back_populates="contacts")