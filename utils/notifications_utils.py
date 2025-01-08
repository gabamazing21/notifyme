from flask_mail import Message
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
# twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
whatsapp_sandbox = os.getenv("TWILIO_WHATSAPP_SANDBOX")

def send_mail(to_email, subject, content):
    """Send an email using Flask-Mail."""
    try:
        msg = Message(
            subject=subject,
            recipients= [to_email] if isinstance(to_email, str) else to_email,
            body=content,
            sender="support@lokatalent.com"
        )
        from app import mail
        mail.send(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        raise

def send_sms(to_phone, content):
    """ Send SMS using Twilio. """
    try:
   
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=content,
            from_=twilio_phone,
            to=to_phone
        )

        print(f"SMS sent to {to_phone}: SID {message.sid}")
        return {"status": "sent", "sid": message.sid}
    except Exception as e:
        print(f"Failed to send SMS to {to_phone}: {str(e)}")
        raise

def send_whatsapp(to_phone, content):
    """ Send whatsapp message using Twilio. """
    try:

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=content,
            from_=f"whatsapp:{whatsapp_sandbox}",
            to=f"whatsapp:{to_phone}"
        )

        print(f"whatsapp message sent to {to_phone}: SID {message.sid}")
    except Exception as e:
        print(f"Failed to send whatsapp message to {to_phone}: {str(e)}")
        raise
