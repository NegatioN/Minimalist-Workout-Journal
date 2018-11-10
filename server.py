#!/usr/bin/env python3
# -*- coding: utf-8
from aiohttp import web
import logging
from input_parser import Parser
from mappings import Mapping
import data_def
import json

PORT = 8080
SAVE_LOCATION = 'my_workouts.csv'

logging.basicConfig(level=logging.INFO)

mapping = Mapping(mapping_dest_path='mappings.json').get_mappings()

input_parser = Parser(mappings=mapping)

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
        data_def.join_workout_dfs(SAVE_LOCATION, df)
        return web.Response(text='Added workout')
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

app = web.Application()
app.router.add_get('/mappings', display_mappings)
app.router.add_get('/workout/{workout}', json_workout)
app.router.add_get('/workout/save/{workout}', persist_workout)

if __name__ == "__main__":
    web.run_app(app, port=PORT)
