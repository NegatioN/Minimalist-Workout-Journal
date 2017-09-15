#!/usr/bin/env python3
# -*- coding: utf-8
import pytest
import input_parser


class TestMain(object):
    #@pytest.mark.parametrize("text_answer", {"3x5+39": 39, "3x5-39": -39})
    @pytest.mark.parametrize("text", ["3x5+1"])
    def test_grab_set_weight_positive(self, text):
        assert input_parser.grab_set_weight(text) > 0

    @pytest.mark.parametrize("text", ["3x5-1"])
    def test_grab_set_weight_negative(self, text):
        assert input_parser.grab_set_weight(text) < 0

    @pytest.mark.parametrize("text", ["3x5"])
    def test_grab_set_weight_noweight(self, text):
        assert input_parser.grab_set_weight(text) == 0

