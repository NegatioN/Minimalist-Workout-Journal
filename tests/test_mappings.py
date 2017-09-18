#!/usr/bin/env python3
# -*- coding: utf-8
import pytest
import mappings
from collections import Counter


class TestMappings(object):
    @pytest.mark.parametrize("first_word", ["Squat", "Split", "10", "Check"])
    @pytest.mark.parametrize("second_word", ["Squat", "Split", "10", "Check"])
    def test_make_shortcut(self, first_word, second_word):
        exp_answer = first_word[0] + second_word[0]
        exercise_name = " ".join([first_word, second_word])
        assert mappings.make_shortcut(exercise_name, 0) == exp_answer.lower()

    @pytest.mark.parametrize("exercises", [["Squat", "Split"],
                                           ["Front Squat", "Front split"],
                                           ["Bentover Dumbbell Rows", "Bend", "Bent High Pulls", "Benchpress Dumbbells"]])
    def test_find_appropriate_shortcut(self, exercises):
        alternatives = []
        for ex in exercises:
            for i in range(len(exercises)):
                alternatives.append(mappings.make_shortcut(ex, i))
        seen = []
        for ex in exercises:
            shortcut, nameId = mappings.find_appropriate_shortcut(1, ex, [])
            seen.append(ex)
            assert shortcut in alternatives
        assert [item for item, count in Counter(seen).items() if count > 1] == []
