from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import Config
from db import initialize_db
from routes import register_blueprints

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Initialize database
    initialize_db(app)

    # Register blueprints
    register_blueprints(app)


if __name__ == "__main__":
    app.run(debug=True)