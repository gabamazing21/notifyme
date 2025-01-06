from tasks import schedule_task
from celery_instance import celery_app
from flask import Flask, jsonify
from db import initialize_db
from routes.user_routes import user_routes
from routes.campaign_routes import campaign_routes
from routes.contact_routes import contact_routes
from routes.template_routes import template_routes
from routes.notification_routes import notification_routes
from routes.scheduled_routes import scheduled_routes
from models.contact import Contact
from models.user import User
from models.notification_template import NotificationTemplate
from models.campaign_list import CampaignList
from flask_mail import Mail
import os
from dotenv import load_dotenv




app = Flask(__name__)
load_dotenv()


# Flask-Mail configuration
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "apikey"
app.config["MAIL_PASSWORD"] = os.getenv("SENDGRID_API_KEY")
app.config["MAIL_DEFAULT_SENDER"] = "support@lokatalent.com"
app.config["MAIL_DEBUG"] = True
app.config["MAIL_MAX_EMAILS"] = 1000
app.config["DEBUG"] = True
mail = Mail(app)

# Initialze the database
initialize_db()

# Register Blueprints
app.register_blueprint(user_routes)
app.register_blueprint(campaign_routes)
app.register_blueprint(contact_routes)
app.register_blueprint(template_routes)
app.register_blueprint(notification_routes)
app.register_blueprint(scheduled_routes)

if __name__ == "__main__":
    app.run(debug=True)