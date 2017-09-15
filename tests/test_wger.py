#!/usr/bin/env python3
# -*- coding: utf-8
import pytest
import input_parser


class TestWger(object):
    @pytest.mark.parametrize("text", ["3x5+1"])
    def test_grab_set_weight_positive(self, text):
        assert input_parser.grab_set_weight(text) > 0

    @pytest.mark.parametrize("text", ["3x5-1"])
    def test_grab_set_weight_negative(self, text):
        assert input_parser.grab_set_weight(text) < 0

    @pytest.mark.parametrize("text", ["3x5"])
    def test_grab_set_weight_noweight(self, text):
        assert input_parser.grab_set_weight(text) == 0

    @pytest.mark.parametrize("text", ["1x3'3x7'24x1", "5", "1x5"])
    def test_split_sets(self, text):
        assert len(input_parser.split_sets(text)) is text.count("'") + 1

    @pytest.mark.parametrize("text", ["{},1x1+1", "{},2x1-1", "{},5"])
    def test_split_exercise_and_set(self, text):
        ex = 's'
        complete_text = text.format(ex)
        assert input_parser.split_exercise_and_set(complete_text)[0] == ex
        assert input_parser.split_exercise_and_set(complete_text)[1] == "".join(complete_text[2:])

    @pytest.mark.parametrize("text", ["s,1x2;s,1x2;s,1x2",
                                      "s,1x2",
                                      "s,1",
                                      "s,1x2;p,188x29;lop,22x9"])
    def test_split_exercises(self, text):
        assert len(input_parser.split_exercises(text)) is text.count(";") + 1
