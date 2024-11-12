"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

Module modaem_helper/io

This module implements a simple mechanism for reading geospatial data. For now,
modaem_helper is limited to the ESRI Shapefile format for geospatial data sets.
This results from the fact that v0.1 of modaem_helper is derived from the
timml_helper scripts that I've developed for my Groundwater Flow Modeling class,
and I'm in a hurry to get a ModAEM toolchain in place.

TODO: Move geospatial I/O to geopandas.

"""

from typing import Any, Callable

import shapefile as shp

Evaluator = Callable[[Any, dict[str, Any], Any], Any]


def eval_object(s: Any,
                config: dict[str, Any] = None,
                default=None) -> Any:
    """
    Evaluate a string using the configuration given and return the object 
    represented there. If the string is empty, return `default`. 
    
    modaem_helper expects that all the values read as attributes from geospatial
    data sets will be strings. However, some users might wish to work with 
    native data types. As a result, if the argument `s` is not a string, it
    will be returned unchanged.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A Python object.
    """
    if isinstance(s, str) and not s:
        return default
    return eval(s, config)


def eval_float(s: str,
               config: dict[str, Any] = None,
               default: Any = None) -> float:
    """
    Evaluate a string using the configuration given and return a float.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    return float(eval_object(s, config, default))


def eval_int(s: str,
             config: dict[str, Any] = None,
             default: Any = None) -> int:
    """
    Evaluate a string using the configuration given and return an int.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    return int(eval_object(s, config, default))


def eval_bool(s: str,
              config: dict[str, Any] = None,
              default: Any = None) -> bool:
    """
    Evaluate a string using the configuration given and return an int.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    return bool(eval_object(s, config, default))


Constraint = Callable[[Any], bool]


class ValidationError(Exception):
    ...


def validate(value: Any,
             constraints: list[tuple[Constraint, str]]) -> bool:
    """
    Validates a value against one or more constraints, using functions or
    lambdas.

    :param value: A python object to validate
    :param constraints: A list of (test_function, failure_message) pairs
    :return: True if all validations succeeded else False
    """
    for test_function, failure_message in constraints:
        if not test_function(value):
            raise ValidationError(f"Validation fails for value {value}: {failure_message}")

    return True
