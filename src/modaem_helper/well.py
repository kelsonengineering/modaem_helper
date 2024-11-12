"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from dataclasses import dataclass
from typing import Any, Generator
import logging
import itertools

from .element import Element
from .io import eval_float, validate, package_header, package_end, ShapeScaling, shapefile_reader
from .model import Model


class Wl0Element(Element):
    """
    Contains a single well at a point provided. If more than one vertex is given, only
    the first one will be utilized (for now).

    FUTURE: Add support for partially-penetrating wells and other well options from modaem1.8
    """

    def __init__(self,
                 xy: list[tuple[float, float]],
                 attrs: dict[str, Any],
                 config=None):
        self.xy = self._validate_xy(xy)
        self.name = str(attrs.get("NAME", ""))
        self.qw = eval_float(attrs.get("QW"), config=config)
        self.rw = attrs.get("RW")
        validate(self.rw, lambda z: z > 0.0, "Attribute RW cannot be negative")

    @staticmethod
    def _validate_xy(xy: list[tuple[float, float]]) -> list[tuple[float, float]]:
        if len(xy) > 1:
            logging.info("Wl0Element can only have one vertex - using the first")
        return xy[0: 1]

    def to_modaem(self, element_id: int, indent: str = "  ") -> Generator[str]:
        """
        Yields up a sequence of text records for all the entries in the Element
        :param element_id: The integer ID number that ties the element to ModAEM output files
        :param indent: The indentation level
        :return:
        """
        x, y = self.xy[0]
        yield f"{indent}({x}, {y}) {self.qw} {self.rw} {element_id}"


class Wl0Collection:
    """
    Contains a collection of only the Wl0Elements extracted from a Model object
    """
    def __init__(self, model: Model):
        self.elements = [el for el in model.elements if isinstance(el, Wl0Element)]
        self.results = None

    def _body(self):
        for i, element in enumerate(self.elements):
            yield element.to_modaem(element_id=i)

    def to_modaem(self, indent: str = "  ") -> Generator[str]:
        """
        Returns the ModAEM input representation of the collection. If there are no wells, returns
        an empty string.
        :return: The ModAEM input for the collection.
        """
        logging.info("Writing ModAEM input for Wl0 package")
        for record in itertools.chain([package_header("wl0", len(self.elements)),
                                       self._body(),
                                       package_end(),
                                       ]):
            result = f"{indent}{record}"
            logging.info(f"{result}")
            yield result


@dataclass
class Wl1Element(Element):
    def __init__(self,
                 xy: list[tuple[float, float]],
                 attrs: dict[str, Any],
                 config=None):
        self.xy = self._validate_xy(xy)
        self.name = str(attrs.get("NAME", ""))
        self.specified_head = eval_float(attrs.get("HEAD"), config=config)
        self.rw = attrs.get("RW")
        validate(self.rw, lambda z: z > 0.0, "Attribute RW cannot be negative")

    @staticmethod
    def _validate_xy(xy: list[tuple[float, float]]) -> list[tuple[float, float]]:
        if len(xy) > 1:
            logging.info("Wl1Element can only have one vertex - using the first")
        return xy[0: 1]
