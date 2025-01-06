import time
from flask import jsonify
from celery_instance import celery_app
from utils.notifications_utils import send_mail, send_sms, send_whatsapp
from db import SessionLocal
from models.scheduled import Scheduled
from models.contact import Contact
from models.notification_template import NotificationTemplate
from models.campaign_list import CampaignList

@celery_app.task(name="schedule_task")
def schedule_task(scheduled_id):
    """
    celery task to send schedule notifications.

    Args:
        scheduled_id(str): The ID of the scheduled notification.
    """
    db = SessionLocal()
    try:
        # Retrieve the scheduled notifications from the database
        scheduled = db.query(Scheduled).filter(Scheduled.id == scheduled_id).first()
        if not scheduled or scheduled.status != "pending":
            return
        
        # Retrieve contracts for the campaign

        # Get contacts
        contacts = db.query(Contact).filter(Contact.campaign_list_id == scheduled.campaign_id).all()
        if not contacts:
            return jsonify({"error": "No contacts found to send notifications."}), 404
        
        # Retrieve the notification template
        template = scheduled.template

        # Sed notification based on the method
        if scheduled.method == "email":
            for contact in contacts:
                send_mail(contact.email, template.subject, template.content)
        elif scheduled.method == "sms":
            for contact in contacts:
                send_sms(contact.phone_number, template.content)
        elif scheduled.method == "whatsapp":
            for contact in contacts:
                send_whatsapp(contact.whatsapp_number, template.content)
        
        # Update the scheduled notification status to "sent"
        scheduled.status = "sent"
        db.commit()
    except Exception as e:
        print(f"Error sending scheduled notification: {e}")
    finally:
        db.close()