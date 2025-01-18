NotifyMe API: Comprehensive Guide

NotifyMe is a custom notification service that allows developers and businesses to send notifications via email, SMS, and WhatsApp. It provides robust APIs for managing campaigns, contacts, and templates, and supports scheduling notifications.

Features

User Authentication: API key-based authentication.

Campaign Management: Create and manage campaigns for your notification needs.

Contact Management: Add contacts individually, in bulk, or via CSV upload.

Templates: Create reusable templates for notifications.

Notifications: Send notifications via email, SMS, or WhatsApp, either immediately or scheduled.

Scheduling: Schedule notifications for a specific date and time.

Table of Contents

Getting Started

Prerequisites

Installation

API Overview

Authentication

Endpoints

Detailed Usage

Register

Manage Campaigns

Manage Contacts

Manage Templates

Send Notifications

Schedule Notifications

Contributing

License

Getting Started

Prerequisites

Python 3.9+

PostgreSQL database

Redis for Celery task queue

Access to Twilio (for SMS/WhatsApp) and an email service (e.g., SendGrid).

Installation

Clone the repository:

git clone https://github.com/yourusername/notifyme.git
cd notifyme

Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure your environment variables in a .env file:

FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL="your_postgres_database_url"
REDIS_URL="your_redis_url"
TWILIO_ACCOUNT_SID="your_twilio_account_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
SENDGRID_API_KEY="your_sendgrid_api_key"

Initialize the database:

flask db upgrade

Start the application:

flask run

Start the Celery worker:

celery -A celery_instance.celery worker --loglevel=info

Start the Celery beat scheduler:

celery -A celery_instance.celery beat --loglevel=info

API Overview

Authentication

All requests require an API key provided during registration. Include the API key in the Authorization header of your requests.

Example:

-H "Authorization: your_api_key"

Endpoints

Users

POST /api/register: Register a new user.

Campaigns

POST /api/campaigns: Create a campaign.

GET /api/campaigns: List all campaigns.

PUT /api/campaigns/<campaign_id>: Update a campaign.

DELETE /api/campaigns/<campaign_id>: Delete a campaign.

Contacts

POST /api/campaigns/<campaign_id>/contacts: Add contacts to a campaign (single, bulk, or via CSV).

GET /api/campaigns/<campaign_id>/contacts: List all contacts in a campaign.

PUT /api/campaigns/<campaign_id>/contacts/<contact_id>: Update a contact.

DELETE /api/campaigns/<campaign_id>/contacts/<contact_id>: Delete a contact.

Templates

POST /api/templates: Create a notification template.

GET /api/templates: List all templates.

PUT /api/templates/<template_id>: Update a template.

DELETE /api/templates/<template_id>: Delete a template.

Notifications

POST /api/campaigns/<campaign_id>/send: Send notifications.

Scheduling

POST /api/campaigns/<campaign_id>/schedule: Schedule notifications.

Detailed Usage

Register

Endpoint: POST /api/register

Request:

{
  "email": "user@example.com",
  "password": "password123"
}

Response:

{
  "message": "Account created successfully.",
  "api_key": "generated_api_key"
}

Manage Campaigns

Create Campaign

Endpoint: POST /api/campaigns
Request:

{
  "name": "New Year Campaign",
  "description": "Campaign for New Year promotions."
}

Response:

{
  "message": "Campaign created successfully.",
  "campaign_id": "generated_campaign_id"
}

... (add similar sections for each endpoint) ...

Contributing

We welcome contributions to NotifyMe! To contribute:

Fork the repository.

Create a feature branch: git checkout -b feature-name.

Commit your changes: git commit -m "Add feature".

Push to your branch: git push origin feature-name.

Create a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

