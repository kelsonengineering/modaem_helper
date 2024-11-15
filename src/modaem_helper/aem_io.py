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

from typing import Any, Callable, Generator, Tuple

from shapefile import Reader

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
    if not isinstance(s, str):
        return s
    if not s:
        return default
    return eval(s, config)


def eval_float(s: Any,
               config: dict[str, Any] = None,
               default: Any = None) -> float | None:
    """
    Evaluate a string using the configuration given and return a float.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    ob = eval_object(s, config, default)
    if ob is None:
        return ob
    return float(ob)


def eval_int(s: Any,
             config: dict[str, Any] = None,
             default: Any = None) -> int | None:
    """
    Evaluate a string using the configuration given and return an int.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    ob = eval_object(s, config, default)
    if ob is None:
        return ob
    return int(ob)


def eval_bool(s: Any,
              config: dict[str, Any] = None,
              default: Any = None) -> bool | None:
    """
    Evaluate a string using the configuration given and return an int.

    :param s: The string to be evaluated
    :param config: The local environment as a dict
    :param default: The default value to be returned if no input is provided
    :return: A floating point value.
    """
    ob = eval_object(s, config, default)
    if ob is None:
        return ob
    return bool(ob)


Constraint = Callable[[Any], bool]


class ValidationError(Exception):
    ...


def validate(value: Any,
             test_function: Constraint = None,
             failure_message: str = "Constraint failed"):
    """
    Validates a value against one or more constraints, using functions or
    lambdas.

    :param value: A python object to validate
    :param test_function: A test_function to be used
    :param failure_message: The message to be reported on failure
    """
    if not test_function(value):
        raise ValidationError(f"Validation fails for value {value}: {failure_message}")


############
# Shapefile support via pyshp
############

SCALE_NONE = 1.0
SCALE_METERS_TO_FEET = 0.3048
SCALE_FEET_TO_METERS = 1.0 / 0.3048


ShapeXy = list[tuple[float, float]]
ShapeAttrs = dict[str, Any]
Shape = tuple[ShapeXy, ShapeAttrs]


def _read_points(rdr: Reader, i: int, scale: float = SCALE_NONE) -> ShapeXy:
    """
    Reads points from a shapefile and optionally scales them
    :param rdr: An open shapefile.Reader object
    :param i: The item to be read from the shapefile
    :param scale: The scaling factor for x and y data
    :return: A list of (x, y) tuples
    """
    return [(x * scale, y * scale) for x, y in rdr.shape(i).points]


def _read_attrs(rdr: Reader, i: int, field_names) -> ShapeAttrs:
    """
    Reads attributes from a shapefile. The pyshp shapefile reader returns records
    as tuples, and our preprocessing API uses dictionaries.
    :param rdr: A shapefile.Reader object
    :param i: The item to be read from the shapefile
    :param field_names: The field names of the shapefile
    :return: A dict of [str, attribute] data
    """
    return {name: value for name, value in zip(field_names, rdr.record(i))}


def shapefile_reader(file_name: str,
                     scale: float = SCALE_NONE
                     ) -> Generator[Shape, None, None]:
    with Reader(file_name) as rdr:
        # Find the explanation for the next line in the `pyshp` documentation ;-)
        field_names = [f[0] for f in rdr.fields[1:]]
        for i in range(rdr.numShapes):
            yield _read_points(rdr, i, scale), _read_attrs(rdr, i, field_names)


# Support for writing ModAEM input files
INDENT = "  "
