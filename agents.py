from db import SessionLocal
from models import Task, Note, Birthday, Meeting
from google_services.google_tasks import add_task_to_google
from google_services.gmail_service import save_note_to_gmail
from google_services.google_calendar import add_birthday as add_birthday_google, create_meeting

class Agent:

    def add_task(self, title, time, user_id):
        db = SessionLocal()
        task = Task(title=title, user_id=user_id)
        db.add(task)
        db.commit()
        db.close()

        try:
            add_task_to_google(title)
        except:
            pass

        return f"✅ Task '{title}' added"

    def delete_task(self, task_id):
        db = SessionLocal()
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
        db.close()

    def get_tasks(self, user_id):
        db = SessionLocal()
        data = db.query(Task).filter(Task.user_id == user_id).all()
        db.close()
        return data

    def add_note(self, content, user_id):
        db = SessionLocal()
        note = Note(content=content, user_id=user_id)
        db.add(note)
        db.commit()
        db.close()

        try:
            save_note_to_gmail(content)
        except:
            pass

        return "📝 Note saved"

    def get_notes(self, user_id):
        db = SessionLocal()
        return db.query(Note).filter(Note.user_id == user_id).all()

    def add_birthday(self, name, email, date, user_id):
        db = SessionLocal()
        db.add(Birthday(name=name, email=email, date=date, user_id=user_id))
        db.commit()
        db.close()

        try:
            add_birthday_google(name, date)
        except:
            pass

        return "🎂 Birthday added"

    def get_birthdays(self, user_id):
        db = SessionLocal()
        return db.query(Birthday).filter(Birthday.user_id == user_id).all()

    def add_meeting(self, email, subject, description, date, time, user_id):
        db = SessionLocal()
        db.add(Meeting(email=email, subject=subject, description=description,
                       date=date, time=time, user_id=user_id))
        db.commit()
        db.close()

        try:
            create_meeting(email, subject, description, date, time)
        except:
            pass

        return "📅 Meeting created"

    def get_meetings(self, user_id):
        db = SessionLocal()
        return db.query(Meeting).filter(Meeting.user_id == user_id).all()