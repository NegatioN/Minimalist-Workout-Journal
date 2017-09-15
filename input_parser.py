#!/usr/bin/env python3
# -*- coding: utf-8
import re

def output_to_tuple(value, expected_tuple_num=2):
    output = ()
    try:
        for i in range(expected_tuple_num):
            output += (value[i],)
    except:
        pass
    return output

def split_get_parts(text, sep, exp_parts=2):
    return output_to_tuple(re.compile(sep).split(text), expected_tuple_num=exp_parts)


def split_sets(text):
    return re.compile("[;]").split(text)

def grab_set_weight(text):
    split_text = re.compile("(\+|-)").split(text)
    if len(split_text) < 2:
        return 0
    else:
        modifier = 1 if split_text[1] == "+" else -1
        return modifier * int(split_text[len(split_text)-1])


def parse_user_input(text):
    exercise_shortcut, rest = split_get_parts(text, sep=",")
    sets, rest = split_get_parts(rest, sep=";")
    for set in sets:
        print(set)
        set_split = re.compile("x+-").split(text)
        set_num = set_split[0]
        rep_num = set_split[1]
        weight_num = set_split[2] if set_split[2] else 0
        #set_num, rep_num, weight_num = split_get_parts(set, "x+-", exp_parts=3)
        print(set_num, rep_num, weight_num)
    print(exercise_shortcut)
    print(sets)
    print(rest)