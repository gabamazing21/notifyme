from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import User
from db import SessionLocal
import uuid

campaign_routes = Blueprint("campaign_routes", __name__)

