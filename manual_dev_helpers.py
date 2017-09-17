from wger_api import WgerAPI

def clean_workoutlog(token):
    api = WgerAPI(token)
    worklog_entries = api.get_workoutlog()
    for entry in worklog_entries:
        api.delete_workoutlog(entry["id"])

clean_workoutlog("")