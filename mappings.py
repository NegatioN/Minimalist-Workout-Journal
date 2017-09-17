#!/usr/bin/env python3
# -*- coding: utf-8
import logging
import json
import os


def make_shortcut(exercise_name, limit):
    words = exercise_name.split(" ")
    return "".join([w[0:limit+1] for w in words]).lower()


def find_appropriate_shortcut(exercise, name, mappings, cur_ex_names):
    for i in range(len(name)):
        proposed_binding = make_shortcut(name, i)
        if proposed_binding not in mappings and name not in cur_ex_names:
            return proposed_binding, {"name": name, "id": exercise["id"]}

class Mapping:
    def __init__(self, api, mapping_dest_path):
        self.api = api
        self.mapping_dest_path = mapping_dest_path

    @staticmethod
    def generate_mappings(exercises):
        mapping = {}
        for ex in exercises:
            name = ex["name"]
            if name:
                existing_exercise_names = [v["name"] for k, v in mapping.items()]
                shortcut, nameId = find_appropriate_shortcut(ex, name, mapping, existing_exercise_names)
                mapping[shortcut] = nameId
        return mapping

    @staticmethod
    def save_mappings(mappings, dest):
        with open(dest, "w+") as save_file:
            json.dump(mappings, save_file)
        logging.info("Saved new mapping-file.")

    def get_mappings(self):
        if not os.path.isfile(self.mapping_dest_path):
            logging.info("Found no prior mapping-file at {}".format(self.mapping_dest_path))
            exercises = self.api.get_exercises()
            mappings = self.generate_mappings(exercises)
            self.save_mappings(mappings, self.mapping_dest_path)
        else:
            with open(self.mapping_dest_path, "r") as map_file:
                mappings = json.load(map_file)
            logging.info("Loaded mapping-file from disk.")
        return mappings