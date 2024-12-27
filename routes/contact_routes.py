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
def add_contact(campaign_id, current_user):
    """
    Add single, bulk, or upload contacts via csv to a campaign.
    """

    db = SessionLocal()
    try:
        
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id).first()
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
            
            contacts, errors = ContactService.process_bulk_contacts(rows, campaign_id)
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
            contact, error = ContactService.process_single_contact(data, campaign_id)
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
            contact, error = ContactService.process_bulk_contacts(data, campaign_id)
            db.bulk_save_objects(contacts)
            db.commit()

            return jsonify({
                "message": "Contacts uploaded successfully via file.",
                "success_count": len(contacts),
                "errors": errors
            }), 201
        
        else:
            return jsonify({
                "error": "Invalid data format. Provide a JSON object, array, or csv file."
            }), 400
    
    finally:
        db.close()

@contact_routes.route("/api/<campaigns_id>/contacts", methods=["GET"])
@api_key_required
def add_contact(campaign_id, current_user):
    """ endpoint to Add a single contact to a campaign"""

    db = SessionLocal()
    try:
        data = request.get_json()
        
        # Validate required field
        if not data.get("name") or not data.get["email"]:
            return jsonify({"error": "first_name and email are required"}), 400
        
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id).first()
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Create the campaign List
        contact = Contact(
            campaign_list_id = campaign_id,
            first_name = data["first_name"],
            last_name = data.get["last_namae"],
            email=data["email"],
            phone_number=data.get("phone_number"),
            whatsapp_number=data.get("whatsapp_number"),
            address=data.get("address")
            custom_fields=data.get("custom_fields", {})
        )
        db.add(contact)
        db.commit()

        return jsonify(
            {"message":"Contact addedd  successfully.",
             "contact_id": contact.id}), 201
    
    finally:
        db.close()