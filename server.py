#!/usr/bin/env python3
# -*- coding: utf-8
from aiohttp import web
import logging
from input_parser import Parser
from mappings import Mapping
import json
from datetime import date

PORT = 8080

logging.basicConfig(level=logging.INFO)

mapping = Mapping(mapping_dest_path='mappings.json').get_mappings()

input_parser = Parser(exercise_date=date.today(),
                      mappings=mapping,
                      workout_id=1)

#TODO collapse multiple inputs of the same exercise to ONE. ex: s,1x2;s,1x2;s,1x3

async def handle(request):
    workout = request.match_info.get('workout', "nothing")
    try:
        workout_data = input_parser.parse_user_input(workout)
        return web.Response(text=json.dumps(workout_data))
    except Exception as e:
        logging.WARN("Got unprocessable input: {}".format(workout))
        return web.Response(status=422)

app = web.Application()
app.router.add_get('/workout/{workout}', handle)

if __name__ == "__main__":
    web.run_app(app, port=PORT)
