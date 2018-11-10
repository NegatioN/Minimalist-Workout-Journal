#!/usr/bin/env python3
# -*- coding: utf-8
import re
import data_def as datadef
from datetime import date, datetime

EXR_SET_REGEX = re.compile("[,]")
SET_REP_REGEX = re.compile("[*]")
WEIGHT_SET_REGEX = re.compile("(\+|-)")
SET_REGEX = re.compile("[']")
EXRS_REGEX = re.compile("[;]")
DATE_REGEX = re.compile('(.*)\[(.*)\]')


class Parser:
    def __init__(self, mappings):
        self.mappings = mappings

    def parse_user_input(self, text):
        exercise_list = []
        text, exr_date = self.grab_date(text)
        for exercises in self.split_exercises(text):
            ex_short, sets = self.split_exercise_and_set(exercises)
            exercise_id = self.get_mapping_id(ex_short)
            set_list = []
            for set in self.split_sets(sets):
                weight = self.grab_set_weight(set)
                remaining_set_text = self.split_weight_and_set(set)[0]
                set_num, reps = self.grab_set_and_reps(remaining_set_text)
                for i in range(set_num):
                    set_list.append(datadef.create_set_object(reps=reps, weight=weight))
            exercise_list.append(datadef.create_exercise(exercise_id, set_list))

        print(exercise_list)
        return datadef.create_workout(session_date=exr_date, exercises=exercise_list)

    def get_mapping_id(self, exercise_shortcut):
        return self.mappings[exercise_shortcut]["id"] if self.mappings[exercise_shortcut] else 1

    @staticmethod
    def split_exercises(full_text):
        return EXRS_REGEX.split(full_text)

    @staticmethod
    def split_sets(text):
        return SET_REGEX.split(text)

    @staticmethod
    def split_weight_and_set(one_set_text):
        return WEIGHT_SET_REGEX.split(one_set_text)

    def grab_set_weight(self, one_set_text):
        split_text = self.split_weight_and_set(one_set_text)
        if len(split_text) < 2:
            return 0
        else:
            modifier = 1 if split_text[1] == "+" else -1
            return modifier * float(split_text[len(split_text) - 1])

    @staticmethod
    def grab_set_and_reps(one_set_text):
        split_text = SET_REP_REGEX.split(one_set_text)
        if len(split_text) == 1:
            split_text = ["1"] + split_text
        return int(split_text[0]), int(split_text[1])

    @staticmethod
    def split_exercise_and_set(exercise_and_set_text):
        split_text = EXR_SET_REGEX.split(exercise_and_set_text)
        return split_text[0], split_text[1]    \

    @staticmethod
    def grab_date(full_text):
        out = DATE_REGEX.search(full_text)
        if out:
            return out.group(1), datetime.strptime(out.group(2), '%Y-%m-%d').date()
        else:
            return full_text, date.today()
