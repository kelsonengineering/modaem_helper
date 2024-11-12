"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

Tests for modaem_helper/io.py

"""

from modaem_helper import io


class TestEvalObject:
    def test_empty_string(self):
        assert io.eval_object("") is None

    def test_string_with_config(self):
        s = "LAYERS"
        config = {"K1": 100.0, "LAYERS": [1, 2, 3]}
        assert io.eval_object(s, config) == [1, 2, 3]

    def test_string_with_config_and_default(self):
        s = ""
        config = {"K1": 100.0, "LAYERS": [1, 2, 3]}
        assert io.eval_object(s, config, default=0) == 0

