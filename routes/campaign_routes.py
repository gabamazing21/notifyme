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

@campaign_routes.route("/api/campaigns", methods=["GET"])
@api_key_required
def get_campaigns(current_user):
    """ get all campaign list for a user"""

    db = SessionLocal()
    try:
        campaigns = db.query(CampaignList).filter(CampaignList.user_id == current_user.id).all()
        
        
        # Create the campaign List
        return jsonify([{
            "id": campaign.id,
            "name": campaign.name,
            "descriptions": campaign.description,
            "created_at": campaign.created_at
        } for campaign in campaigns
        ])
    finally:
        db.close()

@campaign_routes.route("/api/campaigns/<campaign_id>", methods=["GET"])
@api_key_required
def get_campaign(campaign_id, current_user):
    """ Get details of a single campaign."""

    db = SessionLocal()
    try:
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id, CampaignList.user_id == current_user.id).first()
        
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Create the campaign List
        return jsonify({
            "id": campaign.id,
            "name": campaign.name,
            "descriptions": campaign.description,
            "created_at": campaign.created_at
        })
    finally:
        db.close()


@campaign_routes.route("/api/campaigns/<campaign_id>", methods=["PUT"])
@api_key_required
def update_campaign(campaign_id, current_user):
    """ update a single campaign."""

    db = SessionLocal()
    try:
        data = request.get_json()
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id, CampaignList.user_id == current_user.id).first()
        
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Update fields
        if "name" in data:
            campaign.name = data["name"]
        if "description" in data:
            campaign.description = data["description"]
        
        db.commit()
        
        # Create the campaign List
        return jsonify({
            "message": "Campaign updated successfully",
        })
    finally:
        db.close()


@campaign_routes.route("/api/campaigns/<campaign_id>", methods=["DELETE"])
@api_key_required
def delete_campaign(campaign_id, current_user):
    """ Delete a campaign list."""

    db = SessionLocal()
    try:
        # Find the campaign
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id, CampaignList.user_id == current_user.id).first()
        
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        db.delete(campaign)
        db.commit()
        
        # Create the campaign List
        return jsonify({
            "message": "Campaign deleted successfully",
        })
    finally:
        db.close()


@campaign_routes.route("/api/campaigns/<campaign_id>", methods=["PUT"])
@api_key_required
def update_campaign(campaign_id, current_user):
    """ update a single campaign."""

    db = SessionLocal()
    try:
        data = request.get_json()
        campaign = db.query(CampaignList).filter(CampaignList.id == campaign_id, CampaignList.user_id == current_user.id).first()
        
        if not campaign:
            return jsonify(
                {
                    "error": "Campaign not found or does not belong to you"
                }
            )
        
        # Update fields
        if "name" in data:
            campaign.name = data["name"]
        if "description" in data:
            campaign.description = data["description"]
        
        db.commit()
        
        # Create the campaign List
        return jsonify({
            "message": "Campaign updated successfully",
        })
    finally:
        db.close()