# NotifyMe API: Comprehensive Guide

NotifyMe is a custom notification service that allows developers and businesses to send notifications via **email**, **SMS**, and **WhatsApp**. It provides robust APIs for managing campaigns, contacts, and templates, and supports scheduling notifications.

## Features

- **User Authentication**: API key-based authentication.
- **Campaign Management**: Create and manage campaigns for your notification needs.
- **Contact Management**: Add contacts individually, in bulk, or via CSV upload.
- **Templates**: Create reusable templates for notifications.
- **Notifications**: Send notifications via email, SMS, or WhatsApp, either immediately or scheduled.
- **Scheduling**: Schedule notifications for a specific date and time.

---

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
2. [API Overview](#api-overview)
   - [Authentication](#authentication)
   - [Endpoints](#endpoints)
3. [Detailed Usage](#detailed-usage)
   - [Register](#register)
   - [Manage Campaigns](#manage-campaigns)
   - [Manage Contacts](#manage-contacts)
   - [Manage Templates](#manage-templates)
   - [Send Notifications](#send-notifications)
   - [Schedule Notifications](#schedule-notifications)
4. [Contributing](#contributing)
5. [License](#license)

---

## Getting Started

### Prerequisites

1. Python 3.9+
2. PostgreSQL database
3. Redis for Celery task queue
4. Access to Twilio (for SMS/WhatsApp) and an email service (e.g., SendGrid).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/notifyme.git
   cd notifyme
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables in a `.env` file:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=production
   DATABASE_URL="your_postgres_database_url"
   REDIS_URL="your_redis_url"
   TWILIO_ACCOUNT_SID="your_twilio_account_sid"
   TWILIO_AUTH_TOKEN="your_twilio_auth_token"
   SENDGRID_API_KEY="your_sendgrid_api_key"
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Start the application:
   ```bash
   flask run
   ```

7. Start the Celery worker:
   ```bash
   celery -A celery_instance.celery worker --loglevel=info
   ```

8. Start the Celery beat scheduler:
   ```bash
   celery -A celery_instance.celery beat --loglevel=info
   ```

---

## API Overview

### Authentication
All requests require an API key provided during registration. Include the API key in the `Authorization` header of your requests.

Example:
```bash
-H "Authorization: your_api_key"
```

### Endpoints

#### Users
- `POST /api/register`: Register a new user.

#### Campaigns
- `POST /api/campaigns`: Create a campaign.
- `GET /api/campaigns`: List all campaigns.
- `PUT /api/campaigns/<campaign_id>`: Update a campaign.
- `DELETE /api/campaigns/<campaign_id>`: Delete a campaign.

#### Contacts
- `POST /api/campaigns/<campaign_id>/contacts`: Add contacts to a campaign (single, bulk, or via CSV).
- `GET /api/campaigns/<campaign_id>/contacts`: List all contacts in a campaign.
- `PUT /api/campaigns/<campaign_id>/contacts/<contact_id>`: Update a contact.
- `DELETE /api/campaigns/<campaign_id>/contacts/<contact_id>`: Delete a contact.

#### Templates
- `POST /api/templates`: Create a notification template.
- `GET /api/templates`: List all templates.
- `PUT /api/templates/<template_id>`: Update a template.
- `DELETE /api/templates/<template_id>`: Delete a template.

#### Notifications
- `POST /api/campaigns/<campaign_id>/send`: Send notifications.

#### Scheduling
- `POST /api/campaigns/<campaign_id>/schedule`: Schedule notifications.

---

## Detailed Usage

### Register
#### Endpoint: `POST /api/register`
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "message": "Account created successfully.",
  "api_key": "generated_api_key"
}
```

---

### Manage Campaigns
#### Create Campaign
**Endpoint:** `POST /api/campaigns`
**Request:**
```json
{
  "name": "New Year Campaign",
  "description": "Campaign for New Year promotions."
}
```
**Response:**
```json
{
  "message": "Campaign created successfully.",
  "campaign_id": "generated_campaign_id"
}
```

#### Get All Campaigns
**Endpoint:** `GET /api/campaigns`
**Response:**
```json
[
  {
    "id": "campaign-uuid",
    "name": "New Year Campaign",
    "description": "Campaign for New Year promotions.",
    "created_at": "2024-12-30T10:00:00.000Z"
  }
]
```

#### Update Campaign
**Endpoint:** `PUT /api/campaigns/<campaign_id>`
**Request:**
```json
{
  "name": "Updated Campaign Name",
  "description": "Updated campaign description."
}
```
**Response:**
```json
{
  "message": "Campaign updated successfully."
}
```

#### Delete Campaign
**Endpoint:** `DELETE /api/campaigns/<campaign_id>`
**Response:**
```json
{
  "message": "Campaign deleted successfully."
}
```

---

### Manage Contacts
#### Add Contact (Single)
**Endpoint:** `POST /api/campaigns/<campaign_id>/contacts`
**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone_number": "+2347012345678",
  "whatsapp_number": "+2347012345678",
  "address": "123 Main Street",
  "custom_fields": {"company": "TechCorp"}
}
```
**Response:**
```json
{
  "message": "Contact added successfully."
}
```

#### Get Contacts in a Campaign
**Endpoint:** `GET /api/campaigns/<campaign_id>/contacts`
**Response:**
```json
[
  {
    "id": "contact-uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+2347012345678",
    "whatsapp_number": "+2347012345678",
    "address": "123 Main Street",
    "custom_fields": {"company": "TechCorp"}
  }
]
```

#### Update Contact
**Endpoint:** `PUT /api/campaigns/<campaign_id>/contacts/<contact_id>`
**Request:**
```json
{
  "first_name": "Updated Name",
  "email": "updated.email@example.com"
}
```
**Response:**
```json
{
  "message": "Contact updated successfully."
}
```

#### Delete Contact
**Endpoint:** `DELETE /api/campaigns/<campaign_id>/contacts/<contact_id>`
**Response:**
```json
{
  "message": "Contact deleted successfully."
}
```

---

### Manage Templates
#### Create Template
**Endpoint:** `POST /api/templates`
**Request:**
```json
{
  "name": "Welcome Template",
  "type": "email",
  "subject": "Welcome!",
  "content": "Hello {{name}}, welcome to NotifyMe!"
}
```
**Response:**
```json
{
  "message": "Template created successfully."
}
```

### Schedule Notification

**Endpoint**: `POST /api/campaigns/<campaign_id>/schedule`

**Description**: Schedule a notification (SMS, Email, or WhatsApp) for a specific campaign at a specified date and time.

**Request Headers**:
- `Authorization`: API key
- `Content-Type`: `application/json`

**Request Body**:
```json
{
  "template_id": "<template_id>",
  "method": "<method>",
  "scheduled_time": "<YYYY-MM-DD HH:MM:SS>"
}
```

**Parameters**:
- `campaign_id`: The unique ID of the campaign (provided in the URL).
- `template_id`: The unique ID of the notification template.
- `method`: The method of notification (`sms`, `email`, or `whatsapp`).
- `scheduled_time`: The time when the notification should be sent (in `YYYY-MM-DD HH:MM:SS` format).

**Sample cURL Request**:
```bash
curl -X POST "http://127.0.0.1:5000/api/campaigns/<campaign_id>/schedule" \
-H "Authorization: <your_api_key>" \
-H "Content-Type: application/json" \
-d '{
    "template_id": "40825129-95b8-4499-86d4-c05ed7965bc4",
    "method": "email",
    "scheduled_time": "2025-01-06 15:30:00"
}'
```

**Responses**:
- **200 OK**:
```json
{
  "message": "Notification scheduled successfully.",
  "scheduled_id": "<scheduled_id>"
}
```
- **400 Bad Request**:
```json
{
  "error": "Invalid method. Choose 'email', 'sms', or 'whatsapp'."
}
```

---

### Send Notification

**Endpoint**: `POST /api/campaigns/<campaign_id>/send`

**Description**: Send a notification (SMS, Email, or WhatsApp) to contacts in a specific campaign. Supports both personalized and bulk modes.

**Request Headers**:
- `Authorization`: API key
- `Content-Type`: `application/json`

**Request Body**:
```json
{
  "template_id": "<template_id>",
  "method": "<method>",
  "mode": "<mode>"
}
```

**Parameters**:
- `campaign_id`: The unique ID of the campaign (provided in the URL).
- `template_id`: The unique ID of the notification template.
- `method`: The method of notification (`sms`, `email`, or `whatsapp`).
- `mode`: The mode of sending (`personalized` for individual customization or `bulk` for general messages).

**Sample cURL Request**:
```bash
curl -X POST "http://127.0.0.1:5000/api/campaigns/<campaign_id>/send" \
-H "Authorization: <your_api_key>" \
-H "Content-Type: application/json" \
-d '{
    "template_id": "40825129-95b8-4499-86d4-c05ed7965bc4",
    "method": "email",
    "mode": "personalized"
}'
```

**Responses**:
- **200 OK**:
```json
{
  "success": [
    {"contact_id": "<contact_id>", "status": "sent"}
  ],
  "failed": [
    {"contact_id": "<contact_id>", "status": "<error_message>"}
  ]
}
```
- **400 Bad Request**:
```json
{
  "error": "Invalid method. Choose 'email', 'sms', or 'whatsapp'."
}
```
- **404 Not Found**:
```json
{
  "error": "Campaign not found or does not belong to you."
}


