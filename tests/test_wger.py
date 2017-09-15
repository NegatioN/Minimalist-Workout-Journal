#!/usr/bin/env python3
# -*- coding: utf-8
import pytest
from input_parser import Parser
from datetime import date


@pytest.fixture()
def stateful_parser():
    return Parser(exercise_date=date.today(), workout_id=5, mappings={"p": {"name": "pushup", "id": 1},
                                                                      "s": {"name": "squat", "id": 2}})


class TestWger(object):
    @pytest.mark.parametrize("text", ["3x5+1"])
    def test_grab_set_weight_positive(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) > 0

    @pytest.mark.parametrize("text", ["3x5+1.5"])
    def test_grab_set_weight_floats(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) == 1.5

    @pytest.mark.parametrize("text", ["3x5-1"])
    def test_grab_set_weight_negative(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) < 0

    @pytest.mark.parametrize("text", ["3x5"])
    def test_grab_set_weight_noweight(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) == 0

    @pytest.mark.parametrize("text", ["1x3'3x7'24x1", "5", "1x5"])
    def test_split_sets(self, text):
        assert len(Parser.split_sets(text)) is text.count("'") + 1

    @pytest.mark.parametrize("text", ["{},1x1+1", "{},2x1-1", "{},5"])
    def test_split_exercise_and_set(self, text):
        ex = 's'
        complete_text = text.format(ex)
        assert Parser.split_exercise_and_set(complete_text)[0] == ex
        assert Parser.split_exercise_and_set(complete_text)[1] == "".join(complete_text[2:])

    @pytest.mark.parametrize("text", ["s,1x2;s,1x2;s,1x2",
                                      "s,1x2",
                                      "s,1",
                                      "s,1x2;p,188x29;lop,22x9"])
    def test_split_exercises(self, text):
        assert len(Parser.split_exercises(text)) is text.count(";") + 1

    @pytest.mark.parametrize("text", ["{}", "2x{}", "1x{}"])
    @pytest.mark.parametrize("reps", [5, 10, 100])
    def test_grab_set_and_reps(self, text, reps):
        complete_text = text.format(reps)
        answer = Parser.grab_set_and_reps(complete_text)
        sets = int(complete_text.split("x")[0]) if len(complete_text.split("x")) > 1 else 1
        assert answer[0] is sets and answer[1] is reps

    def test_parse_user_input(self, stateful_parser):
        expected_output = [{'date': str(date.today()),
                            'exercise': 2,
                            'repetition_unit': 1,
                            'reps': 5,
                            'weight': 27.0,
                            'weight_unit': 1,
                            'workout': 5}]
        assert stateful_parser.parse_user_input("s,1x5+27") == expected_output
