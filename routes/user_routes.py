from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import User
from db import SessionLocal
import uuid

# Create a blueprint for user-related routes

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/api/register", methods=["POST"])
def register_user():
    """ Register a new user and generate an API key."""
    db = SessionLocal()

    try:
        data = request.get_json()

        # validate required fields
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required."}), 400
        
        # check if the user already exists
        if db.query(User).filter(User.email == data["email"]).first():
            return jsonify({"error": "Email already registered."}), 400
        
        # Generate hashed password and API key
        hashed_password = generate_password_hash(data["password"])
        api_key = str(uuid.uuid4())

        # create a new user
        user = User(email=data["email"], hashed_password=hashed_password, api_key=api_key)
        db.add(user)
        db.commit()

        return jsonify({
            "message": "User registered successfully. keep your api key safe to access the endpoint",
            "api_key": api_key
        }), 201
    finally:
        db.close()