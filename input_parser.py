#!/usr/bin/env python3
# -*- coding: utf-8
import re
from pprint import pprint

class Parser:
    def __init__(self, exercise_date, workout_id, mappings):
        self.exercise_date = exercise_date
        self.workout_id = workout_id
        self.mappings = mappings

    def parse_user_input(self, text):
        set_list = []
        for exercises in self.split_exercises(text):
            ex_short, sets = self.split_exercise_and_set(exercises)
            exercise_id = self.get_mapping_id(ex_short)
            for set in self.split_sets(sets):
                weight = self.grab_set_weight(set)
                remaining_set_text = self.split_weight_and_set(set)[0]
                set_num, reps = self.grab_set_and_reps(remaining_set_text)
                for i in range(set_num):
                    set_list.append(self.create_set_object(exercise_id=exercise_id,
                                                           weight=weight,
                                                           reps=reps,
                                                           date=self.exercise_date,
                                                           workout_id=self.workout_id))
        pprint(set_list)

    def get_mapping_id(self, exercise_shortcut):
        return self.mappings[exercise_shortcut]["id"] if self.mappings[exercise_shortcut] else 1

    @staticmethod
    def split_exercises(full_text):
        return re.compile("[;]").split(full_text)

    @staticmethod
    def split_sets(text):
        return re.compile("[']").split(text)

    @staticmethod
    def split_weight_and_set(one_set_text):
        return re.compile("(\+|-)").split(one_set_text)

    def grab_set_weight(self, one_set_text):
        split_text = self.split_weight_and_set(one_set_text)
        if len(split_text) < 2:
            return 0
        else:
            modifier = 1 if split_text[1] == "+" else -1
            return modifier * float(split_text[len(split_text) - 1])

    @staticmethod
    def grab_set_and_reps(one_set_text):
        split_text = re.compile("[x]").split(one_set_text)
        if len(split_text) == 1:
            split_text = ["1"] + split_text
        return int(split_text[0]), int(split_text[1])

    @staticmethod
    def split_exercise_and_set(exercise_and_set_text):
        split_text = re.compile("[,]").split(exercise_and_set_text)
        return split_text[0], split_text[1]

    @staticmethod
    def create_set_object(exercise_id, reps, weight, date, workout_id=121764):
        return {"reps": reps,
                "weight": weight,
                "exercise": exercise_id,
                "workout": workout_id,
                "repetition_unit": 1,
                "weight_unit": 1,
                "date": str(date)}
