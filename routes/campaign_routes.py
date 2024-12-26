from flask import Blueprint, request, jsonify
from models.user import User
from db import SessionLocal
from models.campaign_list import CampaignList
from auth import api_key_required
import uuid

campaign_routes = Blueprint("campaign_routes", __name__)

@campaign_routes.route("/api/campaigns", methods=["POST"])
@api_key_required
def create_campaign(current_user):
    """ Create a new campaign list for a user"""

    db = SessionLocal()
    try:
        data = request.get_json()
        
        # Validate required field
        if not data.get("name"):
            return jsonify({"error": "Campaign name is required"}), 400
        
        # Create the campaign List
        campaign = CampaignList(
            user_id = current_user.id,
            name=data["name"],
            description=data.get("description")
        )
        db.add(campaign)
        db.commit()

        return jsonify(
            {"message":"Campaign created successfully.",
             "campaign_id": campaign.id}), 201
    
    finally:
        db.close()