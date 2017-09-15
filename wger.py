#!/usr/bin/env python3
# -*- coding: utf-8
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