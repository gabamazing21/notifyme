from models.user import User
from db import SessionLocal
from functools import wraps
from flask import request, jsonify
"""
this module for authencation
"""

def api_key_required(f):
    """ Decorator to require API key for accessing endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = SessionLocal()
        try:
            # Get API key from the request headers
            api_key = request.headers.get("Authorization")
            if not api_key:
                return jsonify({"API key is missing"}), 401
            
            # Validate the API key
            user = db.query(User).filter(User.api_key == api_key).first()
            if not user:
                return jsonify({"error": "Invalid API key."}), 403
            
            # Pass the user to the route handler
            kwargs["current_user"] = user
            return f(*args, **kwargs)
        finally:
            db.close()
    return decorated_function
