#!/usr/bin/env python3
# -*- coding: utf-8
import pytest
from input_parser import Parser
from datetime import date


@pytest.fixture()
def stateful_parser():
    return Parser(mappings={"p": {"name": "pushup", "id": 1}, "s": {"name": "squat", "id": 2}})


class TestMWJ(object):
    @pytest.mark.parametrize("text", ["3*5+1"])
    def test_grab_set_weight_positive(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) > 0

    @pytest.mark.parametrize("text", ["3*5+1.5"])
    def test_grab_set_weight_floats(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) == 1.5

    @pytest.mark.parametrize("text", ["3*5-1"])
    def test_grab_set_weight_negative(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) < 0

    @pytest.mark.parametrize("text", ["3*5"])
    def test_grab_set_weight_noweight(self, text, stateful_parser):
        assert stateful_parser.grab_set_weight(text) == 0

    @pytest.mark.parametrize("text", ["1*3'3*7'24*1", "5", "1*5"])
    def test_split_sets(self, text):
        assert len(Parser.split_sets(text)) is text.count("'") + 1

    @pytest.mark.parametrize("text", ["{},1*1+1", "{},2*1-1", "{},5"])
    def test_split_exercise_and_set(self, text):
        ex = 's'
        complete_text = text.format(ex)
        assert Parser.split_exercise_and_set(complete_text)[0] == ex
        assert Parser.split_exercise_and_set(complete_text)[1] == "".join(complete_text[2:])

    @pytest.mark.parametrize("text", ["s,1*2;s,1*2;s,1*2",
                                      "s,1*2",
                                      "s,1",
                                      "s,1*2;p,188*29;lop,22*9"])
    def test_split_exercises(self, text):
        assert len(Parser.split_exercises(text)) is text.count(";") + 1

    def test_grab_date(self):
        t, d = Parser.grab_date('s,1+25')
        assert d == date.today()
        t, d = Parser.grab_date('s,1[2018-11-30]')
        assert d == date(2018, 11, 30)
        t, d = Parser.grab_date('bp,25+44[1990-2-3]')
        assert d == date(1990, 2, 3)


    @pytest.mark.parametrize("text", ["{}", "2*{}", "1*{}"])
    @pytest.mark.parametrize("reps", [5, 10, 100])
    def test_grab_set_and_reps(self, text, reps):
        complete_text = text.format(reps)
        answer = Parser.grab_set_and_reps(complete_text)
        sets = int(complete_text.split("*")[0]) if len(complete_text.split("*")) > 1 else 1
        assert answer[0] is sets and answer[1] is reps

    def test_parse_user_input(self, stateful_parser):
        expected_output = {'date': str(date.today()),
                           'comment': '',
                           'session_rating': '1',
                           'exercises': [{
                               'exercise_id': 2,
                               'sets': [{
                                   'reps': 5,
                                   'weight': 27.0,
                                   'weight_unit': 'kg'
                               },
                                   {
                                       'reps': 4,
                                       'weight': 0.0,
                                       'weight_unit': 'kg'
                                   }]
                           },
                               {
                                   'exercise_id': 1,
                                   'sets': [{
                                       'reps': 5,
                                       'weight': 0.0,
                                       'weight_unit': 'kg'
                                   }]
                               }]}
        assert stateful_parser.parse_user_input("s,1*5+27'1*4;p,1*5") == expected_output
