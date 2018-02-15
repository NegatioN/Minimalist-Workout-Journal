#!/usr/bin/env python3
# -*- coding: utf-8
from aiohttp import web
import logging
from input_parser import Parser
from mappings import Mapping
import json
from datetime import date

PORT = 8080
SAVE_LOCATION = 'my_workouts.json'

logging.basicConfig(level=logging.INFO)

mapping = Mapping(mapping_dest_path='mappings.json').get_mappings()

input_parser = Parser(exercise_date=date.today(),
                      mappings=mapping,
                      workout_id=1)

#TODO collapse multiple inputs of the same exercise to ONE. ex: s,1x2;s,1x2;s,1x3

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
        print(workout_data)
        with open(SAVE_LOCATION, 'w+') as f:
            if f.read() == '':
                prev_content = []
            else:
                prev_content = json.loads(f)
            prev_content.append(workout_data)
            json.dump(prev_content, f)
        return web.Response(text='Added workout')
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

app = web.Application()
app.router.add_get('/workout/{workout}', json_workout)
app.router.add_get('/workout/save/{workout}', persist_workout)

if __name__ == "__main__":
    web.run_app(app, port=PORT)
