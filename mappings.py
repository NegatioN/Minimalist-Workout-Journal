#!/usr/bin/env python3
# -*- coding: utf-8
import logging
import json
import os


def make_shortcut(exercise_name, limit):
    words = exercise_name.split(" ")
    return "".join([w[0:limit+1] for w in words]).lower()


def find_appropriate_shortcut(id, name, mappings):
    for i in range(len(name)):
        proposed_binding = make_shortcut(name, i)
        if proposed_binding not in mappings:
            return proposed_binding, {"name": name, "id": id}

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
                print(name)
                existing_exercise_names = [v["name"] for k, v in mapping.items()]
                if name not in existing_exercise_names:
                    shortcut, nameId = find_appropriate_shortcut(ex["id"], name, mapping)
                    mapping[shortcut] = nameId
        return mapping

    @staticmethod
    def save_mappings(mappings, dest):
        with open(dest, "w+") as save_file:
            json.dump(mappings, save_file, indent=4, sort_keys=True)
        logging.info("Saved new mapping-file.")

    def get_mappings(self):
        if not os.path.isfile(self.mapping_dest_path):
            logging.info("Found no prior mapping-file at {}".format(self.mapping_dest_path))
            exercises = self.api.get_exercises()
            mappings = self.generate_mappings(exercises)
            self.save_mappings(mappings, self.mapping_dest_path)
        else:
            mappings = self.get_saved_mappings()
        return mappings

    def get_saved_mappings(self):
        with open(self.mapping_dest_path, "r") as map_file:
            mappings = json.load(map_file)
            logging.info("Loaded mapping-file from disk.")
        return mappings

    def show_mappings_if_exists(self):
        mappings = self.get_saved_mappings()
        for mapping, entry in mappings.items():
            print("Shortcut: {} - Name: {}".format(mapping, entry["name"]))

    def edit_mapping(self, name, shortcut):
        mappings = self.get_saved_mappings()
        found_some = False
        for mapping in mappings:
            entry = mappings[mapping]
            if entry["name"].lower() == name:
                if shortcut in mappings:
                    cur_name = mappings[shortcut]["name"]
                    id = mappings[shortcut]["id"]
                    new_shortcut, info = find_appropriate_shortcut(id, cur_name, mappings)
                    mappings[new_shortcut] = info
                    print("Moved {} to new shortcut: {}".format(cur_name, new_shortcut))
                mappings[shortcut] = entry
                found_some = True
                mappings.pop(mapping, None)
                break
        if found_some:
            print("Moved {} to new shortcut: {}".format(name, shortcut))
            self.save_mappings(mappings, self.mapping_dest_path)
        else:
            print("Didn't find {}".format(name))


