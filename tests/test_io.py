"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

Tests for modaem_helper/io.py

"""

from modaem_helper import io


class TestEvalObject:
    config = {"K1": 100.0, "LAYERS": [1, 2, 3]}

    def test_empty_string(self):
        assert io.eval_object("") is None

    def test_string_with_config(self):
        s = "LAYERS"
        assert io.eval_object(s, self.config) == [1, 2, 3]

    def test_string_with_config_and_default(self):
        s = ""
        config = {"K1": 100.0, "LAYERS": [1, 2, 3]}
        assert io.eval_object(s, self.config, default=0) == 0


class TestEvalFloat:
    config = {"PI": 3.14}

    def test_empty_string(self):
        assert io.eval_float("") is None

    def test_empty_string_with_default(self):
        assert io.eval_int(s="", config=self.config, default=-20.0) == -20.0

    def test_float_string(self):
        assert io.eval_float("99.9") == 99.9

    def test_float_object(self):
        assert io.eval_float(-99.9) == -99.9

    def test_float_substitution(self):
        s = "2 * PI"
        assert io.eval_float(s, self.config, default=0.0) == 6.28


class TestEvalInt:
    config = {"N": 500}

    def test_empty_string(self):
        assert io.eval_int(s="") is None

    def test_empty_string_with_default(self):
        assert io.eval_int(s="", config=self.config, default=100) == 100

    def test_int_string(self):
        assert io.eval_int(s="99.9") == 99

    def test_int_object(self):
        assert io.eval_int(s=7) == 7

    def test_int_substitution(self):
        assert io.eval_int(s="N + 3", config=self.config, default=0) == 503


class TestEvalBool:
    config = {"TRUE": True}

    def test_empty_string(self):
        assert io.eval_bool(s="") is None

    def test_empty_string_with_default(self):
        assert io.eval_bool(s="", config=self.config, default=False) is False

    def test_bool_string(self):
        assert io.eval_bool(s="True") is True

    def test_bool_object(self):
        assert io.eval_bool(True or False) is True

    def test_bool_substitution(self):
        assert io.eval_bool(s="TRUE", config=self.config, default=0) is True



