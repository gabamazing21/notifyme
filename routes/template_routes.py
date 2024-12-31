from flask import Blueprint, request, jsonify
from models.user import User
from db import SessionLocal
from models.campaign_list import CampaignList
from models.notification_template import NotificationTemplate
from auth import api_key_required
from utils.file_utils import FileUtils
from services.contact_service import ContactService

template_routes = Blueprint("template_routes", __name__)

@template_routes.route("/api/templates/", methods=["POST"])
@api_key_required
def create_templates(current_user):
    """Create a new notification template."""
    db = SessionLocal()
    try:
        data = request.get_json()

        # validate require fields
        if not data.get("name") or not data.get("type") or not data.get("content"):
            return jsonify({"error": "name, type, and body are required."}), 400
        
        # create template
        template = NotificationTemplate(
            user_id=current_user.id,
            name=data["name"],
            type=data["type"],
            content=data["content"],
            subject=data.get("subject")
        )
        db.add(template)
        db.commit()

        return jsonify({
            "message": "Template created successfully",
            "template_id": template.id
        }), 201
    finally:
        db.close()

@template_routes.route("/api/templates/", methods=["GET"])
@api_key_required
def get_templates(current_user):
    """CGet all nnotification templates for the user."""
    db = SessionLocal()
    try:
        templates = db.query(NotificationTemplate).filter(NotificationTemplate.user_id == current_user.id).all()

        

        return jsonify([{
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "content": template.content,
            "created_at": template.created_at,
            "subject": template.subject
        } for template in templates]), 201
    finally:
        db.close()

@template_routes.route("/api/templates/<template_id>", methods=["GET"])
@api_key_required
def get_template(template_id, current_user):
    """ Get details of a specific template."""
    db = SessionLocal()
    try:
        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id,
            NotificationTemplate.user_id == current_user.id).first()
        
        if not template:
            return jsonify({
                "error":"Template not found or does not belong to you."
            }), 404
        return jsonify({
            "id": template.id,
            "name": template.name,
            "type": template.type,
            "content": template.content,
            "created_at": template.created_at,
            "subject": template.subject 
        }), 201
    finally:
        db.close()


@template_routes.route("/api/templates/<template_id>", methods=["PUT"])
@api_key_required
def update_template(template_id, current_user):
    """ update a notification template."""
    db = SessionLocal()
    try:
        data = request.get_json()

        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id,
            NotificationTemplate.user_id == current_user.id).first()
        
        if not template:
            return jsonify({
                "error":"Template not found or does not belong to you."
            }), 404
        
        # Update fields
        if "name" in data:
            template.name = data["name"]
        if "type" in data:
            template.type = data["type"]
        if "content" in data:
            template.content = data["content"]
        if "subject" in data:
            template.subject = data["subject"]

        db.commit()
        return jsonify({
            "message": " Template updated successfully."
        }), 201
    finally:
        db.close()


@template_routes.route("/api/templates/<template_id>", methods=["DELETE"])
@api_key_required
def del_template(template_id, current_user):
    """ update a notification template."""
    db = SessionLocal()
    try:
        template = db.query(NotificationTemplate).filter(
            NotificationTemplate.id == template_id,
            NotificationTemplate.user_id == current_user.id).first()
        
        if not template:
            return jsonify({
                "error":"Template not found or does not belong to you."
            }), 404
        
        db.delete(template)
        db.commit()
        return jsonify({
            "message": " Template deleted successfully."
        }), 201
    finally:
        db.close()