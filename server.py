#!/usr/bin/env python3
# -*- coding: utf-8
from aiohttp import web
import logging
from input_parser import Parser
from mappings import Mapping
import data_def
import json
import pandas as pd
import argparse
from auth import Authorization
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=8080)
parser.add_argument('-s', '--save', default='{}/my_workouts.csv'.format(dir_path))
parser.add_argument('-m', '--mapping', default='{}/mappings.json'.format(dir_path))
parser.add_argument('--secret', default='dummy')
parser.add_argument('--user', default='dummy')

options = parser.parse_args()

def load_data(path):
    if os.path.isfile(path):
        return pd.read_csv(options.save)
    else:
        return pd.DataFrame()

auth = Authorization(user=options.user, password=options.secret)
master_df = load_data(options.save)
logging.basicConfig(level=logging.INFO)

mapping = Mapping(mapping_dest_path=options.mapping).get_mappings()

input_parser = Parser(mappings=mapping)
rev_mapping = {k: v['id'] for k,v in mapping.items()}

async def display_mappings(request):
    await auth.authenticate(request)
    try:
        return web.Response(text=json.dumps(mapping))
    except Exception as e:
        logging.WARN("Couldn't find mappings")
        return web.Response(status=422)

async def json_workout(request):
    await auth.authenticate(request)
    workout = request.match_info.get('workout', "nothing")
    try:
        workout_data = input_parser.parse_user_input(workout)
        return web.Response(text=json.dumps(workout_data))
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

async def persist_workout(request):
    await auth.authenticate(request)
    workout = request.match_info.get('workout', "nothing")
    try:
        workout_data = input_parser.parse_user_input(workout)
        df = data_def.json_workout_to_df(workout_data)
        data_def.join_workout_dfs(master_df, df, options.save)
        return web.Response(text='Added workout')
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

async def last_of_exercise(request):
    await auth.authenticate(request)
    exr  = request.match_info.get('exercise', "nothing")
    try:
        exercise_num = rev_mapping[exr]
        x = master_df[master_df['exercise'] == exercise_num]
        t = x.sort_values(['date'], ascending=False)
        return web.Response(text=json.dumps({'Last known stats for {}'.format(exr):
                                                 [str(x) for x in t.values[0]]}))
    except:
        return web.Response(status=415)



app = web.Application()
app.router.add_get('/mappings', display_mappings)
app.router.add_get('/workout/{workout}', json_workout)
app.router.add_get('/workout/save/{workout}', persist_workout)
app.router.add_get('/get_last/{exercise}', last_of_exercise)

if __name__ == "__main__":
    web.run_app(app, port=options.port)
