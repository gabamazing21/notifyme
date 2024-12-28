from models.contact import Contact
from sqlalchemy.orm import Session
import uuid

class ContactService:
    @staticmethod
    def validate_contact_data(contact_data):
        """Validate contact dataa."""
        if not contact_data.get("first_name") or not contact_data.get("email"):
            return False, "first_name and email are required."
        return True, None
    
    @staticmethod
    def process_single_contact(contact_data, campaign_id):
        """Process a single contact"""
        valid, error = ContactService.validate_contact_data(contact_data)
        if not valid:
            return None, error
        
        # add contact to the List
        contact = Contact(
            campaign_list_id = campaign_id,
            first_name = contact_data["first_name"],
            last_name = contact_data.get("last_namae"),
            email=contact_data["email"],
            phone_number=contact_data.get("phone_number"),
            whatsapp_number=contact_data.get("whatsapp_number"),
            address=contact_data.get("address"),
            custom_fields=contact_data.get("custom_fields", {})
        )

        return contact, None
    
    @staticmethod
    def process_bulk_contacts(contact_list, campaign_id):
        """Process bulk contacts."""
        contacts = []
        errors = []
        for idx, contact_data in enumerate(contact_list):
            contact, error = ContactService.process_single_contact(contact_data, campaign_id)
            if error:
                errors.append({"index": idx, "error": error})
            else:
                contacts.append(contact)
        return contacts, errors