from googleapiclient.discovery import build
from google_services.google_auth import get_credentials
from datetime import datetime, timedelta

# ---------- 🎂 BIRTHDAY ----------
def add_birthday(name, date_str):
    service = build("calendar", "v3", credentials=get_credentials())

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        event = {
            'summary': f'🎂 Birthday: {name}',

            'start': {'date': formatted_date},
            'end': {'date': formatted_date},

            # 🔁 Repeat yearly
            'recurrence': ['RRULE:FREQ=YEARLY'],

            # 🔔 Reminder
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 1440},  # 1 day before
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return f"🎂 Birthday for {name} added (yearly)"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------- 📅 MEETING ----------
def create_meeting(email, subject, description, date_str, time_str):
    service = build("calendar", "v3", credentials=get_credentials())

    try:
        start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end = start + timedelta(hours=1)

        event = {
            'summary': subject,
            'description': description,

            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },

            # 📧 Invite
            'attendees': [{'email': email}],

            # 🎥 Meet link
            'conferenceData': {
                'createRequest': {
                    'requestId': 'meet123',
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            },

            # 🔔 Reminder
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        meet_link = event.get("hangoutLink", "No link")

        return f"📅 Meeting scheduled!\n🔗 {meet_link}"

    except Exception as e:
        return f"❌ Error: {str(e)}"