from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google_services.google_auth import get_credentials

MY_EMAIL = "swathikaranam246@gmail.com"

def send_email(to, subject, message_text):
    service = build("gmail", "v1", credentials=get_credentials())

    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={'raw': raw}
    ).execute()

    return "Email sent"


def save_note_to_gmail(content):
    return send_email(MY_EMAIL, "📝 Note", content)