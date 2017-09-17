#!/usr/bin/env python3
# -*- coding: utf-8
import argparse
from datetime import date
from input_parser import Parser
from wger_api import WgerAPI
import logging
import wger_data_defs as wdata
from mappings import Mapping


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--mapping_dest', default="mappings.json", dest="mapping_dest",
                        help='Path to save mapping-file to.')
arg_parser.add_argument('--token', dest="token", help='Auth token for your account.', required=True)
arg_parser.add_argument('--input', dest="inp", help='input to parse', required=True)
arg_parser.add_argument('--loglevel', dest="loglevel", help='Which level to log', default=logging.INFO,
                        choices=[logging.INFO, logging.WARN, logging.DEBUG])
arg_parser.add_argument('--date', dest="exr_date", default=date.today(), help='Date to add the given exercise to.')
config = arg_parser.parse_args()

logging.basicConfig(level=config.loglevel)


def get_workout_id(api, exercise_date):
    workouts = api.get_workouts()
    if not str(exercise_date) in [x["creation_date"] for x in workouts]:
        workout_id = api.post_workout()["id"]
        session_data = wdata.create_workout_session(exercise_date, workout_id)
        api.post_workoutsession(session_data)
        logging.info("Created a new workout-session for {}".format(str(config.exr_date)))
        return workout_id
    else:
        for entry in workouts:
            if entry["creation_date"] == str(exercise_date):
                return entry["id"]


def main():
    api = WgerAPI(config.token)
    mappings = Mapping(api=api, mapping_dest_path=config.mapping_dest).get_mappings()

    workout_id = get_workout_id(api, config.exr_date)
    logging.debug("Workout id:{}".format(workout_id))

    input_parser = Parser(exercise_date=config.exr_date,
                          mappings=mappings,
                          workout_id=workout_id)
    sets_to_post = input_parser.parse_user_input(config.inp)

    for set_data in sets_to_post:
        api.post_workoutlog(set_data)

    logging.info("Posted {} sets of your workout to wger.de!".format(len(sets_to_post)))


if __name__ == "__main__":
    main()
