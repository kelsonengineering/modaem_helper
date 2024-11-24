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

    def trailer(self):
        yield ""


class Wl0Collection(BaseElementCollection):
    """
    Contains a collection of only the Wl0Elements extracted from a Model object
    """
    element_type = Wl0Element

    def __init__(self, model: Model) -> None:
        super().__init__(model)

    def header(self) -> Generator[str, None, None]:
        """
        Yields a text string for the head of the collection
        :yield: The text "wl0 <number-of-wells>?
        """
        if len(self.elements) > 0:
            yield f"wl0 {len(self.elements)}"

    def body(self) -> Generator[str, None, None]:
        if len(self.elements) > 0:
            for i, element in enumerate(self.elements):
                yield from element.build()

    def trailer(self) -> Generator[str, None, None]:
        if len(self.elements) > 0:
            yield f"end"
