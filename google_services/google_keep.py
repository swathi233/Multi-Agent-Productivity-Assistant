import gkeepapi
from datetime import datetime


class GoogleKeepService:
    def __init__(self):
        self.keep = gkeepapi.Keep()
        self.login()

    def login(self):
        email = "codetesting020@gmail.com"
        app_password = "nutzovyozoxjqwxb"  # 16-char Google App Password (no spaces)
        
        try:
            # NEW METHOD (fixes deprecation warning)
            success = self.keep.authenticate(email, app_password)

            if not success:
                raise Exception("Authentication failed")

        except Exception as e:
            print("Keep Init Error:", e)
            raise Exception("❌ Google Keep authentication failed")

    def create_note_with_reminder(self, title, content, reminder_time_str=None):
        note = self.keep.createNote(title, content)

        if reminder_time_str:
            try:
                reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
                note.remind(reminder_time)
            except Exception as e:
                print("Reminder error:", e)

        self.keep.sync()
        return note.id