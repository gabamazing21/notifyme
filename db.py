"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from base import Base
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Any

from models.user import User

# Define the database engine
DATABASE_URL = "sqlite:///notifications.db"
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_db():
    """ Initialize the database and create all tables."""

    Base.metadata.create_all(bind=engine)

def get_db():
    """ Provide a session for database intereactions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()