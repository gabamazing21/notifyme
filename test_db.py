from models.campaign_list import CampaignList
from models.user import User
from models.contact import Contact
from db import initialize_db, SessionLocal

def test_database():
    # Initialize the database

    initialize_db()

    # create a database session
    db = SessionLocal()

    try:
        user = User(email="gabeamazing21@gmail.com", hashed_password="hashed_password", api_key="testapikey")
        db.add(user)
        db.commit()

        campaign = CampaignList(user_id=user.id, name="new year newsletter", description="a campaign for new year production")
        db.add(campaign)
        db.commit()

        Contact1 = Contact(
            campaign_list_id=campaign.id,
            first_name="Gabriel",
            last_name="Daramola",
            email="gabeamazing21@gmail.com",
            phone_number="07030842880",
        )
        Contact2 = Contact(
            campaign_list_id=campaign.id,
            first_name="Gabriel",
            last_name="Daramola",
            email="gabeamazing21@gmail.com",
            phone_number="07030842880",
        )
        
        db.add(Contact1)
        db.add(Contact2)
        db.commit()

        # query and pront data to verify relationships
        user_with_campaigns = db.query(User).filter(User.id == user.id).first()
        print(f"User: {user_with_campaigns.email}")
        for campaign in user_with_campaigns.campaign_lists:
            print(f" Campaign: {campaign.name} - {campaign.description}")
            for contact in campaign.contacts:
                print(f"  Contact: {contact.first_name}  {contact.last_name}  ({contact.email})")

    finally:
        db.close()

if __name__ == "__main__":
    test_database()