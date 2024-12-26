from flask import Flask
from db import initialize_db
from routes.user_routes import user_routes
from routes.campaign_routes import campaign_routes
from models.contact import Contact
from models.user import User
from models.campaign_list import CampaignList


app = Flask(__name__)

# Initialze the database
initialize_db()

# Register Blueprints
app.register_blueprint(user_routes)
app.register_blueprint(campaign_routes)


if __name__ == "__main__":
    app.run(debug=True)