from flask_mail import Message
from twilio.rest import Client

# twilio credentials
account_sid = "REMOVED"
auth_token = "REMOVED"
twilio_phone = "+12695337617"
whatsapp_sandbox = "+14155238886"

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
            to=twilio_phone
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
            from_=whatsapp_sandbox,
            to=f"whatsapp:{to_phone}"
        )

        print(f"whatsapp message sent to {to_phone}: SID {message.sid}")
    except Exception as e:
        print(f"Failed to send whatsapp message to {to_phone}: {str(e)}")
        raise