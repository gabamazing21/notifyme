from flask import Blueprint, request, jsonify
from models.user import User
from db import SessionLocal
from models.campaign_list import CampaignList
from models.scheduled import Scheduled
from models.notification_template import NotificationTemplate
from models.contact import Contact
from auth import api_key_required
from utils.file_utils import FileUtils
from services.contact_service import ContactService
from utils.notifications_utils import send_mail, send_sms, send_whatsapp
from datetime import datetime
from tasks import schedule_task


scheduled_routes = Blueprint("scheduled_routes", __name__)

@scheduled_routes.route("/api/campaigns/<campaign_id>/schedule", methods=["POST"])
@api_key_required
def schedule_notification(campaign_id, current_user):
    """
    Schedule notification to all or specific contacts in a campaign
    at a particular period of time
    """
    db = SessionLocal()
    try:
        data = request.get_json()

        # Validate request body

        if not data.get("template_id") or not data.get("method") or not data.get("scheduled_time"):
            return jsonify({"error": "template_id, method and scheduled time are required."}), 400
        
        method = data["method"]
        if method not in ["email", "sms", "whatsapp"]:
            return jsonify({"error": "Invalid method. choose 'email', 'sms' or 'whatsapp'."}), 400
        
        # validate the scheduled time
        try:
            scheduled_time = datetime.strptime(data["scheduled_time"], "%Y-%m-%d %H:%M:%S")
            if scheduled_time <= datetime.now():
                return jsonify({
                    "error": "Scheduled time must be in the future."
                })
        except ValueError:
            return jsonify({
                "error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'. "
            }), 400

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
        
        # Create and store the schedule Notification

        scheduled = Scheduled(
            user_id = current_user.id,
            campaign_id = campaign_id,
            template_id = data["template_id"],
            method=method,
            scheduled_time=scheduled_time,
            status="pending"
        )
        db.add(scheduled)
        db.commit()

        # schedule the celery task to run at the specified time

        countdown = (scheduled_time - datetime.now()).total_seconds()

        print(f"Scheduling task for: {scheduled_time} (local time)")
        schedule_task.apply_async(
            args=[scheduled.id],
            countdown=countdown
        )
        
        print(f"Task scheduled for {scheduled_time}")
  
        return jsonify({
            "message": "Notification scheduled successfuly.", 
            "scheduled_id": scheduled.id
        }), 200
    finally:
        db.close()