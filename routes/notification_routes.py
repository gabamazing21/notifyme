from flask import Blueprint, request, jsonify
from models.user import User
from db import SessionLocal
from models.campaign_list import CampaignList
from models.notification_template import NotificationTemplate
from models.contact import Contact
from auth import api_key_required
from utils.file_utils import FileUtils
from services.contact_service import ContactService
from utils.notifications_utils import send_mail, send_sms, send_whatsapp

notification_routes = Blueprint("notification_routes", __name__)

@notification_routes.route("/api/campaigns/<campaign_id>/send", methods=["POST"])
@api_key_required
def send_notification(campaign_id, current_user):
    """Send notification to all or specific contacts in a campaign"""
    db = SessionLocal()
    try:
        data = request.get_json()

        # Validate request body
        mode = data.get("mode", "personalized") #Default to "personalized"

        if not data.get("template_id") or not data.get("method"):
            return jsonify({"error": "template_id and method are required."}), 400
        
        method = data["method"]
        if method not in ["email", "sms", "whatsapp"]:
            return jsonify({"error": "Invalid method. choose 'email', 'sms' or 'whatsapp'."}), 400
        
        # Check if the campaign belongs to the user
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id, CampaignList.user_id == current_user.id).first()
        
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        template = db.query(NotificationTemplate).filter(NotificationTemplate.id == data["template_id"], NotificationTemplate.user_id == current_user.id).first()
        
        if not template:
            return jsonify(
                {
                    "error": "Template not found or does not belong to you"
                }
            )
        
        # Get contacts
        contacts = db.query(Contact).filter(Contact.campaign_list_id == campaign_id).all()
        if not contacts:
            return jsonify({"error": "No contacts found to send notifications."}), 404
        
        # Send notifications
        if mode == "bulk":
            recipient_emails = [contact.email for contact in contacts]
            send_mail(recipient_emails, template.subject, template.content)
        elif mode == "personalized":
            results = {"success": [], "failed": []}
            for contact in contacts:
                try:
                    # Replace placeholders in the templates

                    content = template.content.format(
                        name=contact.first_name,
                        email=contact.email, 
                        phone=contact.phone_number)
                    subject = template.subject.format(
                        name=contact.first_name,
                        email=contact.email, 
                        phone=contact.phone_number)
                    
                    # Simulate sending based on method
                    if method == "email":
                        send_mail(contact.email, subject, content)
                    elif method == "sms":
                        send_sms(contact.phone_number, content)
                    elif method == "whatsapp":
                        send_whatsapp(contact.phone_number, content)
                    
                    results["success"].append({"contact_id": contact.id, "status": "sent"})
                except Exception as e:
                    results["failed"].append({"contact_id": contact.id, "status": str(e)})
            return jsonify(results), 200
    finally:
        db.close()