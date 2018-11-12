#!/usr/bin/env python3
# -*- coding: utf-8
from aiohttp import web
import logging
from input_parser import Parser
from mappings import Mapping
import data_def
import json
import pandas as pd

PORT = 8080
SAVE_LOCATION = 'my_workouts.csv'
master_df = pd.read_csv(SAVE_LOCATION)


logging.basicConfig(level=logging.INFO)

mapping = Mapping(mapping_dest_path='mappings.json').get_mappings()

input_parser = Parser(mappings=mapping)
rev_mapping = {k: v['id'] for k,v in mapping.items()}

async def display_mappings(request):
    try:
        return web.Response(text=json.dumps(mapping))
    except Exception as e:
        logging.WARN("Couldn't find mappings")
        return web.Response(status=422)

async def json_workout(request):
    workout = request.match_info.get('workout', "nothing")
    try:
        workout_data = input_parser.parse_user_input(workout)
        return web.Response(text=json.dumps(workout_data))
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

def concat_content(workout, prev_workouts):
    if len(prev_workouts) > 0:
        prev_workouts.append(workout)
    else:
        return [workout]

async def persist_workout(request):
    workout = request.match_info.get('workout', "nothing")
    try:
        workout_data = input_parser.parse_user_input(workout)
        df = data_def.json_workout_to_df(workout_data)
        data_def.join_workout_dfs(master_df, df, SAVE_LOCATION)
        return web.Response(text='Added workout')
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

async def last_of_exercise(request):
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
    web.run_app(app, port=PORT)
