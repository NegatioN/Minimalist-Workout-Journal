#!/usr/bin/env python3
# -*- coding: utf-8
import json
import argparse
import os
from datetime import date
from input_parser import Parser
from wger_api import WgerAPI
import logging


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--mapping_dest', default="mappings.json", dest="mapping_dest",
                        help='Path to save mapping-file to.')
arg_parser.add_argument('--token', dest="token", help='Auth token for your account.', required=True)
arg_parser.add_argument('--input', dest="inp", help='input to parse', required=True)
arg_parser.add_argument('--loglevel', dest="loglevel", help='Which level to log', default=logging.INFO,
                        choices=[logging.INFO, logging.WARN, logging.DEBUG])
arg_parser.add_argument('--date', dest="exr_date", default=date.today(), help='Date to add the given exercise to.')
arg_parser.add_argument('--workout', dest="workout", default=121764,
                        help='Workout-id for the workout-program you want to assign the workouts to.')
config = arg_parser.parse_args()

logging.basicConfig(level=config.loglevel)


def generate_mappings(exercises):
    mapping = {}
    for ex in exercises:
        name = ex["name"]
        if name:
            name_l = list(name)
            for i in range(len(name_l)):
                proposed_binding = "".join(name_l[:i + 1]).lower()
                cur_ex_names = [v["name"] for k, v in mapping.items()]
                if proposed_binding not in mapping and name not in cur_ex_names:
                    nameId = {"name": name, "id": ex["id"]}
                    mapping[proposed_binding] = nameId
                    break
    return mapping


def save_mappings(mappings, dest):
    with open(dest, "w+") as save_file:
        json.dump(mappings, save_file)
    logging.info("Saved new mapping-file.")


def get_mappings(api, mapping_dest_path):
    if not os.path.isfile(mapping_dest_path):
        logging.info("Found no prior mapping-file at {}".format(mapping_dest_path))
        exercises = api.get_exercises()
        mappings = generate_mappings(exercises)
        save_mappings(mappings, mapping_dest_path)
    else:
        with open(mapping_dest_path, "r") as map_file:
            mappings = json.load(map_file)
        logging.info("Loaded mapping-file from disk.")
    return mappings


#TODO add a way to say something about how the workout went to graph form better later.
def create_workout_session(session_date, workout_id):
    return {
        "date": str(session_date),
        "notes": "",
        "impression": "1",
        "time_start": None,
        "time_end": None,
        "workout": workout_id
    }


def main():
    api = WgerAPI(config.token)
    mappings = get_mappings(api, config.mapping_dest)
    input_parser = Parser(exercise_date=config.exr_date,
                          mappings=mappings,
                          workout_id=config.workout)
    sets_to_post = input_parser.parse_user_input(config.inp)

    workout_days = [x["date"] for x in api.get_workoutsessions()]
    if not str(config.exr_date) in workout_days:
        session_data = create_workout_session(config.exr_date, config.workout)
        api.post_workoutsession(session_data)
        logging.info("Created a new workout-session for {}".format(str(config.exr_date)))

    for set_data in sets_to_post:
        api.post_workoutlog(set_data)

    logging.info("Posted {} sets of your workout to wger.de!".format(len(sets_to_post)))


if __name__ == "__main__":
    main()
