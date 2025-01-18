from flask import Blueprint, request, jsonify
from models.user import User
from db import SessionLocal
from models.campaign_list import CampaignList
from models.contact import Contact
from auth import api_key_required
from utils.file_utils import FileUtils
from services.contact_service import ContactService

contact_routes = Blueprint("contact_routes", __name__)

@contact_routes.route("/api/campaigns/<campaigns_id>/contacts", methods=["POST"])
@api_key_required
def add_contact(current_user, campaigns_id):
    """
    Add single, bulk, or upload contacts via csv to a campaign.
    """

    db = SessionLocal()
    try:
        
        campaign = db.query(CampaignList).filter(CampaignList.id == campaigns_id, CampaignList.user_id == current_user.id).first()
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Handle file upload
        if "file" in request.files:
            file = request.files["file"]
            if not file.filename.endswith(".csv"):
                return jsonify({
                    "error": "Invalid file type. Only CSV files are supported."
                }), 400
            rows, error = FileUtils.parse_csv(file)
            if error:
                return jsonify({"error": error}), 400
            
            contacts, errors = ContactService.process_bulk_contacts(rows, campaigns_id)
            db.bulk_save_objects(contacts)
            db.commit()

            return jsonify({
                "message": "Contacts uploaded successfully via file.",
                "success_count": len(contacts),
                "errors": errors
            }), 201
        
        data = request.get_json()
        if isinstance(data, dict):
            """if it's single contact"""
            contact, error = ContactService.process_single_contact(data, campaigns_id)
            if error:
                return jsonify({
                    "error": error
                }), 400
            db.add(contact)
            db.commit()

            return jsonify({
                "message": "Contacts added successfully.",
                "contact_id": contact.id,
            }), 201
        
        elif isinstance(data, list):
            """ if it's bulk json contact"""
            contact, error = ContactService.process_bulk_contacts(data, campaigns_id)
            db.bulk_save_objects(contact)
            db.commit()

            return jsonify({
                "message": "Contacts uploaded successfully via json.",
                "success_count": len(contact),
                "errors": error
            }), 201
        
        else:
            return jsonify({
                "error": "Invalid data format. Provide a JSON object, array, or csv file."
            }), 400
    
    finally:
        db.close()


@contact_routes.route("/api/campaigns/<campaigns_id>/contacts", methods=["GET"])
@api_key_required
def get_contact(current_user, campaigns_id):
    """
    get all contact in a campaign list.
    """

    db = SessionLocal()
    try:
    
        campaign = db.query(Contact).filter(CampaignList.id == campaigns_id, CampaignList.user_id == current_user.id).first()
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Retrieve contacts for the campaign
        contacts = db.query(Contact).filter(Contact.campaign_list_id == campaigns_id).all()

        # Serialiize contacts into a list of dictionaries
        if not contacts:
            return jsonify({
                "error": "contacts not found in the campaign"
            })

        contact_list = [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "phone_number": contact.phone_number,
                "whatsapp_number": contact.whatsapp_number,
                "address": contact.address,
                "custom_fields": contact.custom_fields,
                "created_at": contact.created_at
            }
            for contact in contacts
        ]

        return jsonify(contact_list), 200
    
    finally:
        db.close()

@contact_routes.route("/api/campaigns/<campaigns_id>/contacts/<contact_id>", methods=["PUT"])
@api_key_required
def update_contact(current_user, campaigns_id, contact_id):
    """
    update a contact in a campaign
    """

    db = SessionLocal()
    try:        
        campaign = db.query(Contact).filter(CampaignList.id == campaigns_id, CampaignList.user_id == current_user.id).first()
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Retrieve contacts for the campaign
        contact = db.query(Contact).filter(Contact.campaign_list_id == campaigns_id, Contact.id == contact_id).first()

        if not contact:
            return jsonify({
                "error": "contacts not found in the campaign"
            })

        # Get the updated data from the request
        data = request.get_json()
        contact.first_name = data.get("first_name", contact.first_name)
        contact.last_name = data.get("last_name", contact.last_name)
        contact.email = data.get("email", contact.email)
        contact.phone_number = data.get("phone_number", contact.phone_number)
        contact.whatsapp_number = data.get("whatsapp_number", contact.whatsapp_number)
        contact.address = data.get("address", contact.address)
        contact.custom_fields = data.get("custom_fields", contact.custom_fields)
        db.commit()
        return jsonify({
            "message": "Contact updated successfuly",
            "contact_id": contact.id
        }), 200
    
    finally:
        db.close()

@contact_routes.route("/api/campaigns/<campaigns_id>/contacts/<contact_id>", methods=["DELETE"])
@api_key_required
def delete_contact(current_user, campaigns_id, contact_id):
    """
    delete a contact in a campaign
    """

    db = SessionLocal()
    try:        
        campaign = db.query(Contact).filter(CampaignList.id == campaigns_id, CampaignList.user_id == current_user.id).first()
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Retrieve contacts for the campaign
        contact = db.query(Contact).filter(Contact.campaign_list_id == campaigns_id, Contact.id == contact_id).first()

        if not contact:
            return jsonify({
                "error": "contacts not found in the campaign"
            })

        # Get the updated data from the request
        db.delete(contact)
        db.commit()
        return jsonify({
            "message": "Contact deleted successfuly",
            "contact_id": contact.id
        }), 200
    
    finally:
        db.close()