#!/usr/bin/env python3
# -*- coding: utf-8

from requests import auth, get, post
import json
import argparse
import os
from datetime import date
import input_parser

from pprint import pprint

#TODO make parser of format p,2x5+3.3kg;1x3

parser = argparse.ArgumentParser()
parser.add_argument('--mapping_dest', default="mappings.json", dest="mapping_dest", help='Path to save mapping-file to.')
parser.add_argument('--token', dest="token", help='Auth token for your account.')#, required=True)
parser.add_argument('--workout', dest="workout", help='Workout-id for the workout-program you want to assign the workouts to.')
config = parser.parse_args()

API_URL = "https://wger.de/api/v2"


class MyAuth(auth.AuthBase):
    def __call__(self, r):
        r.headers['Authorization'] = "Token {}".format(config.token)
        return r



def define_call_url(action, endpoint, options):
    call_url = "{}/{}".format(API_URL, endpoint)
    if action and action != "":
        call_url = "{}/{}".format(call_url, action)
    if options and options != "":
        call_url = "{}{}".format(call_url, options)
    return call_url


def get_api(endpoint, action="", options=""):
    call_url = define_call_url(action, endpoint, options)
    res = get(call_url, auth=MyAuth())

    if res.status_code == 200:
        return json.loads(res.content)
    else:
        return {}


def post_api(endpoint, data, action="", options=""):
    call_url = define_call_url(action, endpoint, options)
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    print(data)
    res = post(call_url, json=data, auth=MyAuth(), headers=headers)
    print(res.status_code)


def get_exercises():
    return get_api(endpoint="exercise", options="?limit=1000&language=2")["results"]


def get_workout(workout_id):
    return get_api(endpoint="set", action=workout_id, options="/add")

def post_workoutlog(reps, weight, exercise, workout_id, wrk_date=date.today()):
    post_data = {
        "reps": reps,
        "weight": float(weight),
        "date": str(wrk_date),
        "exercise": exercise,
        "workout": workout_id,
        "repetition_unit": 1,
        "weight_unit": 1
    }
    post_api(endpoint="workoutlog/", data=post_data, options="", action="") # needs trailing /, base redirects.


def generate_mappings(exercises):
    mapping = {}
    for ex in exercises:
        name = ex["name"]
        if name:
            name_l = list(name)
            for i in range(len(name_l)):
                proposed_binding = "".join(name_l[:i+1]).lower()
                cur_ex_names = [v["name"] for k, v in mapping.items()]
                if proposed_binding not in mapping and name not in cur_ex_names:
                    nameId = {"name": name, "id": ex["id"]}
                    mapping[proposed_binding] = nameId
                    break
    return mapping


def save_mappings(mappings, dest):
    with open(dest, "w+") as save_file:
        json.dump(mappings, save_file)


if not os.path.isfile(config.mapping_dest):
    exercises = get_exercises()
    save_mappings(generate_mappings(exercises), config.mapping_dest)

#exercises = get_exercises()
#print(exercises)
#post_workoutlog(reps=5, weight=122.0, workout_id=121764, exercise=192)
pprint(input_parser.parse_user_input("s,1x5+27;p,17;c,2x5'1x8"))