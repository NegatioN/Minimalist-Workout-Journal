from requests import auth, get, post
import json
import argparse
import os

#TODO get exercises, confirm mappings
#TODO make mappings-file
#TODO make parser of format p,2x5+3.3kg;1x3

parser = argparse.ArgumentParser()
parser.add_argument('--mapping_dest', default="mappings.json", dest="mapping_dest", help='Path to save mapping-file to.', required=True)
parser.add_argument('--token', dest="token", help='Auth token for your account.', required=True)
config = parser.parse_args()

API_URL = "https://wger.de/api/v2"


class MyAuth(auth.AuthBase):
    def __call__(self, r):
        r.headers['Authorization'] = "Token {}".format(config.token)
        return r

def get_api(endpoint, action, options=""):
    call_url = "{}/{}".format(API_URL, endpoint)
    if action and action != "":
        call_url = "{}/{}".format(call_url, action)
    if options and options != "":
        call_url = "{}{}".format(call_url, options)
    res = get(call_url, auth=MyAuth())

    if res.status_code == 200:
        return json.loads(res.content)
    else:
        return {}


def get_exercises():
    return get_api(endpoint="exercise", options="?limit=1000&language=2")["results"]


def get_workout(workout_id):
    return get_api(endpoint="set", action=workout_id, options="/add")


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


