from requests import auth, get, post, delete
import json
import functools
from collections import defaultdict

API_URL = "https://wger.de/api/v2"


def make_call_url(api_url, action, endpoint, options):
    call_url = "{}/{}".format(api_url, endpoint)
    if action and action != "":
        call_url = "{}/{}".format(call_url, action)
    if options and options != "":
        call_url = "{}{}".format(call_url, options)
    return call_url


class VerySimpleAuth(auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = "Token {}".format(self.token)
        return r


class WgerAPI:
    def __init__(self, token, api_url=API_URL):
        self.auth = VerySimpleAuth(token=token)
        self.make_my_call_url = functools.partial(make_call_url, api_url)

    def get_api(self, endpoint, action="", options=""):
        call_url = self.make_my_call_url(action, endpoint, options)
        res = get(call_url, auth=self.auth)
        return json.loads(res.content) if res.status_code == 200 else defaultdict(list)

    def post_api(self, endpoint, data, action="", options=""):
        # needs trailing /, base redirects, and gives us a get-call instead.
        call_url = self.make_my_call_url(action, endpoint, options)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        post(call_url, json=data, auth=self.auth, headers=headers)

    def get_exercises(self):
        return self.get_api(endpoint="exercise", options="?limit=1000&language=2")["results"]

    def post_workoutlog(self, workoutlog_set_data):
        self.post_api(endpoint="workoutlog/", data=workoutlog_set_data)

    def get_workoutlog(self):
        return self.get_api(endpoint="workoutlog/")["results"]

    def delete_workoutlog(self, id, action="", options=""):
        endpoint="workoutlog/{}".format(id)
        delete(self.make_my_call_url(action, endpoint, options), auth=self.auth)

    def get_workoutsessions(self):
        return self.get_api("workoutsession", options="?limit=9999")["results"]

    def post_workoutsession(self, session_data):
        self.post_api(endpoint="workoutsession/", data=session_data)