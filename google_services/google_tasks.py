from googleapiclient.discovery import build
from google_services.google_auth import get_credentials

def add_task_to_google(task_title):
    creds = get_credentials()
    service = build("tasks", "v1", credentials=creds)

    # Get default task list
    tasklists = service.tasklists().list().execute()
    tasklist_id = tasklists["items"][0]["id"]

    task = {
        "title": task_title
    }

    service.tasks().insert(
        tasklist=tasklist_id,
        body=task
    ).execute()

    return "✅ Task added to Google Tasks"