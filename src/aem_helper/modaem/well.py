"""
aem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from dataclasses import dataclass
from typing import Any, Generator
import logging

from aem_helper.aem_element import BaseElement, BaseElementCollection
from aem_helper.aem_io import eval_float, validate, ShapeXy


class Wl0Element(BaseElement):
    """
    Contains a single well at a point provided. If more than one vertex is given, only
    the first one will be utilized (for now).

    FUTURE: Add support for partially-penetrating wells and other well options from modaem1.8
    """

    def __init__(self,
                 xy: ShapeXy,
                 attrs: dict[str, Any],
                 config=None):
        super().__init__()
        self.xy = self.validate_xy(xy)
        self.name = str(attrs.get("NAME", ""))
        self.qw = eval_float(attrs.get("QW"), config=config)
        self.rw = attrs.get("RW")
        validate(self.rw, lambda z: z > 0.0, "Attribute RW cannot be negative")

    @staticmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        if len(xy) > 1:
            logging.info("Wl0Element can only have one vertex - using the first")
        return xy[0: 1]

    def header(self):
        yield ""

    def body(self, element_id) -> Generator[str, None, None]:
        x, y = self.xy[0]
        yield f"{INDENT}({x}, {y}) {self.qw} {self.rw} {element_id}"

    def footer(self):
        yield ""


class Wl0Collection(BaseElementCollection):
    """
    Contains a collection of only the Wl0Elements extracted from a Model object
    """
    def __init__(self, model: Model) -> None:
        super().__init__(model, Wl0Element)

    def header(self) -> Generator[str, None, None]:
        """
        Yields a text string for the head of the collection
        :yield: The text "wl0 <number-of-wells>?
        """
        yield f"{INDENT}wl0 {len(self.elements)}"

    def body(self) -> Generator[str, None, None]:
        for i, element in enumerate(self.elements):
            yield element.build(element_id=i)

    def footer(self) -> Generator[str, None, None]:
        yield "end"


@dataclass
class Wl1Element(BaseElement):
    def __init__(self,
                 xy: list[tuple[float, float]],
                 attrs: dict[str, Any],
                 config=None):
        self.xy = self.validate_xy(xy)
        self.name = str(attrs.get("NAME", ""))
        self.specified_head = eval_float(attrs.get("HEAD"), config=config)
        self.rw = attrs.get("RW")
        validate(self.rw, lambda z: z > 0.0, "Attribute RW cannot be negative")

    @staticmethod
    def validate_xy(xy: list[tuple[float, float]]) -> list[tuple[float, float]]:
        if len(xy) > 1:
            logging.info("Wl1Element can only have one vertex - using the first")
        return xy[0: 1]
