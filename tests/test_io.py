"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

Tests for modaem_helper/aem_io.py

"""

import pathlib

import pytest
import shapefile
import tempfile

from modaem_helper import aem_io


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
        assert io.eval_float(s="", config=self.config, default=-20.0) == -20.0

    def test_float_string(self):
        assert aem_io.eval_float("99.9") == 99.9

    def test_float_object(self):
        assert io.eval_float(-99.9) == -99.9

    def test_float_substitution(self):
        s = "2 * PI"
        assert aem_io.eval_float(s, self.config, default=0.0) == 6.28


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
        assert aem_io.eval_bool(s="") is None

    def test_empty_string_with_default(self):
        assert io.eval_bool(s="", config=self.config, default=False) is False

    def test_bool_string(self):
        assert io.eval_bool(s="True") is True

    def test_bool_object(self):
        assert aem_io.eval_bool(True or False) is True

    def test_bool_substitution(self):
        assert io.eval_bool(s="TRUE", config=self.config, default=0) is True


# Test ths shapefile support

@pytest.fixture()
def shapefile_config() -> str:
    """
    Prepares a shapefile with two items in it.
    :return: None
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        shape_path = pathlib.Path(tmpdirname) / "temp_shape"
        w = shapefile.Writer(shape_path, shapeType=shapefile.POINT)
        w.field("NAME", "C", 32)
        w.field("QW", "C", 32)
        w.field("RW", "C", 32)
        w.point(100.0, 100.0)
        w.record("TEST", "10000.0", "0.5")
        w.close()
        yield shape_path


def test_read_shapefile(shapefile_config) -> None:
    """
    Test input from a shapefile.
    :param shapefile_config: A shapefile path provided by a fixture
    """
    rdr = io.shapefile_reader(shapefile_config, scale=io.SCALE_NONE)
    xy, attrs = next(rdr)
    assert attrs["NAME"] == "TEST"
    assert attrs["QW"] == "10000.0"
    assert attrs["RW"] == "0.5"
    assert len(xy) == 1
    assert xy[0] == (100.0, 100.0)
