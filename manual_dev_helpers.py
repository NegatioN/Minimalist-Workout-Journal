#!/usr/bin/env python3
# -*- coding: utf-8
from wger_api import WgerAPI
import mappings

def clean_workoutlog(token):
    api = WgerAPI(token)
    worklog_entries = api.get_workoutlog()
    for entry in worklog_entries:
        api.delete_workoutlog(entry["id"])



clean_workoutlog("")
#mappings.Mapping("", "mappings.json").edit_mapping("squats", "s")